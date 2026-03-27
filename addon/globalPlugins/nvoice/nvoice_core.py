# coding: utf-8
import os
import tempfile
import ctypes
import json
import urllib.request
import urllib.error
import uuid
import threading
import datetime
import re
import subprocess
from typing import Optional, List, Dict
import addonHandler

import api
import textInfos
import speech
from speech.commands import PitchCommand
import ui
import queueHandler
import logHandler

addonHandler.initTranslation()


class AudioRecorder:
	def __init__(self) -> None:
		self.winmm = ctypes.windll.winmm
		self.filepath: str = os.path.join(tempfile.gettempdir(), "nvoice_capture.wav")

	def start(self) -> None:
		self.winmm.mciSendStringW("close nvoice_rec", None, 0, None)
		self.winmm.mciSendStringW("open new type waveaudio alias nvoice_rec", None, 0, None)
		self.winmm.mciSendStringW("record nvoice_rec", None, 0, None)

	def stop(self) -> str:
		self.winmm.mciSendStringW(f'save nvoice_rec "{self.filepath}"', None, 0, None)
		self.winmm.mciSendStringW("close nvoice_rec", None, 0, None)
		return self.filepath


class NVoiceCore:
	def __init__(self, config) -> None:
		self.config = config
		self.recorder = AudioRecorder()
		self.is_recording = False
		self.history: List[Dict[str, str]] = []

	def clear_history(self) -> None:
		self.history.clear()
		ui.message(_("History cleared. Memory reset."))

	def get_screen_context(self) -> str:
		obj = api.getFocusObject()
		if not obj:
			return ""
		try:
			info = obj.makeTextInfo(textInfos.POSITION_ALL)
			return info.text
		except Exception:
			return obj.name or ""

	def toggle_recording(self, use_context: bool = False) -> None:
		if not self.is_recording:
			self.is_recording = True
			msg = _("Listening with context...") if use_context else _("Listening...")
			ui.message(msg)

			context_text = self.get_screen_context() if use_context else ""

			self.current_context = context_text

			self.recorder.start()
		else:
			self.is_recording = False
			ui.message(_("Processing..."))
			audio_file = self.recorder.stop()
			threading.Thread(target=self._process_pipeline, args=(audio_file, self.current_context), daemon=True).start()

	def _process_pipeline(self, audio_file: str, context_text: str) -> None:
		try:
			stt_engine = self.config.get('general', 'stt_engine')
			text = ""

			if stt_engine == 'local':
				text = self._transcribe_local(audio_file)
			else:
				text = self._transcribe_groq(audio_file)

			if not text:
				return

			final_prompt = text
			if context_text:
				final_prompt = _("User has focus on this text on screen:\n'''{context}'''\n\nUser question: {question}").format(context=context_text, question=text)

			self.history.append({"role": "user", "content": final_prompt})
			if len(self.history) > 6:
				self.history = self.history[-6:]

			self._route_provider_streaming()

		except Exception as e:
			logHandler.log.error(f"Pipeline Error: {e}")
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Internal processing error."))
		finally:
			if os.path.exists(audio_file):
				os.remove(audio_file)

	def _transcribe_local(self, audio_path: str) -> str:
		"""Transcribes using Whisper CLI installed globally on the user's Windows."""
		model = self.config.get('whisper_local', 'model')
		if not model:
			model = 'base'

		output_dir = os.path.dirname(audio_path)

		# Command: whisper nvoice_capture.wav --model base --language pt --output_format txt --output_dir %TEMP%
		command = [
			"whisper",
			audio_path,
			"--model", model,
			"--language", "pt",
			"--output_format", "txt",
			"--output_dir", output_dir
		]

		# 0x08000000 is CREATE_NO_WINDOW on Windows.
		# Prevents the black DOS screen from flashing and stealing NVDA focus!
		CREATE_NO_WINDOW = 0x08000000

		try:
			# Run command invisibly
			result = subprocess.run(command, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)

			if result.returncode != 0:
				logHandler.log.error(f"Whisper CLI Error: {result.stderr}")
				queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Local Whisper error."))
				return ""

			# Whisper generates a txt file with the same name as the original wav
			base_name = os.path.splitext(os.path.basename(audio_path))[0]
			txt_file = os.path.join(output_dir, f"{base_name}.txt")

			if os.path.exists(txt_file):
				with open(txt_file, "r", encoding="utf-8") as f:
					text = f.read().strip()
				os.remove(txt_file)  # Cleanup!
				return text
			return ""

		except FileNotFoundError:
			# Falls here if Windows says: "The 'whisper' command does not exist"
			msg = _("Warning: Whisper command is not installed on your computer. Change STT to Groq or install Whisper.")
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, msg)
			return ""

	def _transcribe_groq(self, audio_path: str) -> str:
		api_key = self.config.get('groq', 'api_key').strip()
		if not api_key:
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Groq API Key is missing for STT."))
			return ""

		boundary = uuid.uuid4().hex
		headers = {
			'Authorization': f'Bearer {api_key}',
			'Content-Type': f'multipart/form-data; boundary={boundary}',
			'User-Agent': 'NVoice/2.0 (NVDA Addon)'
		}

		with open(audio_path, 'rb') as f:
			audio_data = f.read()

		body = bytearray()
		body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode('utf-8'))
		body.extend(audio_data)
		body.extend(f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-large-v3-turbo\r\n--{boundary}--\r\n'.encode('utf-8'))

		req = urllib.request.Request('https://api.groq.com/openai/v1/audio/transcriptions', data=body, headers=headers, method='POST')
		try:
			with urllib.request.urlopen(req, timeout=10) as res:
				return json.loads(res.read()).get('text', '')
		except Exception as e:
			logHandler.log.error(f"STT Error: {e}")
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Groq STT error."))
			return ""

	def _route_provider_streaming(self) -> None:
		prov = self.config.get('general', 'provider')
		if prov == 'gemini':
			self._stream_gemini()
		else:
			self._stream_openai_compatible(prov)

	def _stream_openai_compatible(self, prov: str) -> None:
		api_key = self.config.get(prov, 'api_key').strip()
		model = self.config.get(prov, 'model')

		url = "https://api.groq.com/openai/v1/chat/completions"
		headers = {'Content-Type': 'application/json', 'User-Agent': 'NVoice/2.0 (NVDA Addon)'}

		if prov == 'openai':
			url = "https://api.openai.com/v1/chat/completions"
		elif prov == 'openrouter':
			url = "https://openrouter.ai/api/v1/chat/completions"
			headers['HTTP-Referer'] = 'https://github.com/mpquemel/nvoice-addon'
			headers['X-Title'] = 'NVoice NVDA Add-on'
		elif prov == 'ollama':
			url = f"{self.config.get('ollama', 'endpoint')}/v1/chat/completions"

		if prov != 'ollama':
			headers['Authorization'] = f'Bearer {api_key}'

		payload = {'model': model, 'messages': self.history, 'stream': True}
		req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

		self._read_sse_stream(req, is_gemini=False)

	def _stream_gemini(self) -> None:
		api_key = self.config.get('gemini', 'api_key').strip()
		model = self.config.get('gemini', 'model')
		url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key}"

		gemini_history = []
		for msg in self.history:
			role = "model" if msg["role"] == "assistant" else "user"
			gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

		headers = {'Content-Type': 'application/json', 'User-Agent': 'NVoice/2.0 (NVDA Addon)'}
		payload = {'contents': gemini_history}
		req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
		self._read_sse_stream(req, is_gemini=True)

	def _strip_markdown(self, text: str) -> str:
		text = re.sub(r'[*_]{1,3}', '', text)
		text = re.sub(r'`{1,3}', '', text)
		text = re.sub(r'#+\s*', '', text)
		return text

	def _read_sse_stream(self, req: urllib.request.Request, is_gemini: bool) -> None:
		buffer, full_response = "", ""
		try:
			with urllib.request.urlopen(req, timeout=15) as res:
				for line in res:
					line_str = line.decode('utf-8').strip()
					if line_str.startswith('data: ') and line_str != 'data: [DONE]':
						chunk = ""
						data_json_str = line_str[6:]

						try:
							data = json.loads(data_json_str)
						except json.JSONDecodeError:
							continue

						if is_gemini:
							if "candidates" in data and data["candidates"]:
								parts = data["candidates"][0].get("content", {}).get("parts", [])
								if parts:
									chunk = parts[0].get("text", "")
						else:
							choices = data.get("choices", [])
							if choices:
								chunk = choices[0].get("delta", {}).get("content", "")

						if chunk:
							buffer += chunk
							full_response += chunk
							if any(p in buffer for p in ['.', '!', '?', '\n']):
								self._speak_chunk(buffer)
								buffer = ""

				if buffer.strip():
					self._speak_chunk(buffer)

			if full_response.strip():
				self.history.append({"role": "assistant", "content": full_response})
				self._save_to_text_file(full_response)

		except Exception as e:
			logHandler.log.error(f"Streaming Error: {e}")
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Communication error in streaming."))

	def _save_to_text_file(self, response: str) -> None:
		save_hist = self.config.get_bool('general', 'save_history')
		hist_file = self.config.get('general', 'history_file')

		if save_hist and hist_file:
			try:
				prompt = self.history[-2]["content"] if len(self.history) >= 2 else "Transcription unavailable"
				now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

				stt_engine = self.config.get('general', 'stt_engine')
				if stt_engine == 'local':
					stt_name = _("Whisper Local CLI (Model: {model})").format(model=self.config.get('whisper_local', 'model'))
				else:
					stt_name = _("Groq Whisper (Fast Cloud)")

				prov = self.config.get('general', 'provider')
				model = self.config.get(prov, 'model')

				clean_response = self._strip_markdown(response)

				with open(hist_file, 'a', encoding='utf-8') as f:
					f.write(f"\n{'='*60}\n")
					f.write(f"Date/Time: {now}\n")
					f.write(f"STT Engine: {stt_name}\n")
					f.write(f"AI Provider: {prov.upper()} | Model: {model}\n")
					f.write(f"{'-'*60}\n")
					f.write(f"Your Question / Context: \n{prompt}\n")
					f.write(f"{'-'*60}\n")
					f.write(f"AI Response: \n{clean_response}\n")
			except Exception as e:
				logHandler.log.error(f"Error writing to history file: {e}")

	def _speak_chunk(self, text: str) -> None:
		clean_text = self._strip_markdown(text.strip())
		if clean_text:
			queueHandler.queueFunction(
				queueHandler.eventQueue,
				speech.speak,
				[PitchCommand(multiplier=1.3), clean_text, PitchCommand(multiplier=1.0)]
			)
