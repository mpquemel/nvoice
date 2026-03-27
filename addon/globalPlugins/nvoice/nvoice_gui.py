# coding: utf-8
import wx
import gui
import threading
import json
import urllib.request
import addonHandler
from gui.settingsDialogs import SettingsPanel
from .nvoice_config import NVoiceConfig
import logHandler

addonHandler.initTranslation()


class NVoiceSettingsPanel(SettingsPanel):
	title = "NVoice"

	def makeSettings(self, settingsSizer: wx.Sizer) -> None:
		self.config = NVoiceConfig()

		# Main LLM Provider
		prov_sizer = wx.BoxSizer(wx.HORIZONTAL)
		prov_sizer.Add(wx.StaticText(self, label=_("LLM Provider:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		self.provider_cb = wx.ComboBox(self, choices=["groq", "openai", "gemini", "openrouter", "ollama"], style=wx.CB_READONLY)
		self.provider_cb.SetValue(self.config.get('general', 'provider'))
		prov_sizer.Add(self.provider_cb, 1, wx.ALL, 5)
		settingsSizer.Add(prov_sizer, 0, wx.EXPAND)

		# Voice Recognition Engine (STT)
		stt_box = wx.StaticBox(self, label=_("Voice Recognition (STT)"))
		stt_box_sizer = wx.StaticBoxSizer(stt_box, wx.VERTICAL)

		stt_sizer = wx.BoxSizer(wx.HORIZONTAL)
		stt_sizer.Add(wx.StaticText(stt_box, label=_("Engine:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		self.stt_cb = wx.ComboBox(stt_box, choices=[_("groq (Fast Cloud)"), _("local (Whisper CLI Offline)")], style=wx.CB_READONLY)
		stt_val = "local (Whisper CLI Offline)" if self.config.get('general', 'stt_engine') == 'local' else "groq (Fast Cloud)"
		self.stt_cb.SetValue(stt_val)
		stt_sizer.Add(self.stt_cb, 1, wx.ALL, 5)
		stt_box_sizer.Add(stt_sizer, 0, wx.EXPAND)

		# Local Whisper Model
		wh_sizer = wx.BoxSizer(wx.HORIZONTAL)
		wh_sizer.Add(wx.StaticText(stt_box, label=_("Local Model (CLI):")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		self.wh_model_cb = wx.ComboBox(stt_box, choices=["tiny", "base", "small", "medium", "large"], style=wx.CB_READONLY)
		self.wh_model_cb.SetValue(self.config.get('whisper_local', 'model') or 'base')
		wh_sizer.Add(self.wh_model_cb, 1, wx.ALL, 5)
		stt_box_sizer.Add(wh_sizer, 0, wx.EXPAND)

		settingsSizer.Add(stt_box_sizer, 0, wx.EXPAND | wx.ALL, 5)

		# API Keys
		self.api_keys = {}
		for prov in ["groq", "openai", "gemini", "openrouter"]:
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(wx.StaticText(self, label=_("API Key {provider}:").format(provider=prov.capitalize())), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
			ctrl = wx.TextCtrl(self, style=wx.TE_PASSWORD)
			ctrl.SetValue(self.config.get(prov, 'api_key'))
			sizer.Add(ctrl, 1, wx.ALL, 5)
			settingsSizer.Add(sizer, 0, wx.EXPAND)
			self.api_keys[prov] = ctrl

		# Ollama Endpoint
		ollama_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ollama_sizer.Add(wx.StaticText(self, label=_("Ollama Endpoint:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
		self.ollama_ctrl = wx.TextCtrl(self)
		self.ollama_ctrl.SetValue(self.config.get('ollama', 'endpoint'))
		ollama_sizer.Add(self.ollama_ctrl, 1, wx.ALL, 5)
		settingsSizer.Add(ollama_sizer, 0, wx.EXPAND)

		# History Export
		hist_box = wx.StaticBox(self, label=_("Conversation History Export"))
		hist_sizer = wx.StaticBoxSizer(hist_box, wx.VERTICAL)

		self.save_hist_cb = wx.CheckBox(hist_box, label=_("Automatically save conversations to text file (.txt)"))
		self.save_hist_cb.SetValue(self.config.get_bool('general', 'save_history'))
		self.save_hist_cb.Bind(wx.EVT_CHECKBOX, self.onSaveHistToggle)
		hist_sizer.Add(self.save_hist_cb, 0, wx.ALL, 5)

		path_sizer = wx.BoxSizer(wx.HORIZONTAL)
		path_sizer.Add(wx.StaticText(hist_box, label=_("File Location:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.hist_path_ctrl = wx.TextCtrl(hist_box)
		self.hist_path_ctrl.SetValue(self.config.get('general', 'history_file'))
		path_sizer.Add(self.hist_path_ctrl, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.btn_browse = wx.Button(hist_box, label=_("Browse..."))
		self.btn_browse.Bind(wx.EVT_BUTTON, self.onBrowseHist)
		path_sizer.Add(self.btn_browse, 0, wx.ALL, 5)
		hist_sizer.Add(path_sizer, 0, wx.EXPAND)

		settingsSizer.Add(hist_sizer, 0, wx.EXPAND | wx.ALL, 5)
		self._toggle_hist_controls(self.save_hist_cb.GetValue())

		# Dynamic Model Management
		model_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btn_fetch = wx.Button(self, label=_("Fetch Models from Current Provider"))
		self.btn_fetch.Bind(wx.EVT_BUTTON, self.onFetchModels)
		model_sizer.Add(self.btn_fetch, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.model_cb = wx.ComboBox(self, style=wx.CB_READONLY)
		curr_prov = self.provider_cb.GetValue()
		self.model_cb.SetValue(self.config.get(curr_prov, 'model'))
		model_sizer.Add(self.model_cb, 1, wx.ALL, 5)
		settingsSizer.Add(model_sizer, 0, wx.EXPAND)

	def onSaveHistToggle(self, evt) -> None:
		self._toggle_hist_controls(self.save_hist_cb.GetValue())

	def _toggle_hist_controls(self, enabled: bool) -> None:
		self.hist_path_ctrl.Enable(enabled)
		self.btn_browse.Enable(enabled)

	def onBrowseHist(self, evt) -> None:
		with wx.FileDialog(self, _("Select or create history file"), wildcard=_("Text files (*.txt)|*.txt"), style=wx.FD_SAVE) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			self.hist_path_ctrl.SetValue(pathname)

	def onFetchModels(self, evt) -> None:
		prov = self.provider_cb.GetValue()
		api_key = self.api_keys.get(prov, self.ollama_ctrl).GetValue()
		self.btn_fetch.Disable()
		threading.Thread(target=self._fetch_models_thread, args=(prov, api_key), daemon=True).start()

	def _fetch_models_thread(self, prov: str, api_key: str) -> None:
		models = []
		headers = {'User-Agent': 'NVoice/2.0 (NVDA Addon)'}
		try:
			if prov == "groq":
				headers['Authorization'] = f'Bearer {api_key}'
				req = urllib.request.Request("https://api.groq.com/openai/v1/models", headers=headers)
				with urllib.request.urlopen(req, timeout=10) as res:
					models = [m['id'] for m in json.loads(res.read())['data']]
			elif prov == "openai":
				headers['Authorization'] = f'Bearer {api_key}'
				req = urllib.request.Request("https://api.openai.com/v1/models", headers=headers)
				with urllib.request.urlopen(req, timeout=10) as res:
					models = [m['id'] for m in json.loads(res.read())['data'] if "gpt" in m['id']]
			elif prov == "openrouter":
				headers['Authorization'] = f'Bearer {api_key}'
				req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers=headers)
				with urllib.request.urlopen(req, timeout=10) as res:
					models = [m['id'] for m in json.loads(res.read())['data']]
			elif prov == "gemini":
				req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", headers=headers)
				with urllib.request.urlopen(req, timeout=10) as res:
					models = [m['name'].replace('models/', '') for m in json.loads(res.read())['models']]
			elif prov == "ollama":
				endpoint = api_key
				req = urllib.request.Request(f"{endpoint}/api/tags", headers=headers)
				with urllib.request.urlopen(req, timeout=5) as res:
					models = [m['name'] for m in json.loads(res.read()).get('models', [])]
		except Exception as e:
			logHandler.log.error(_("Error fetching models: {error}").format(error=e))
			models = [_("Error fetching")]

		def update_ui():
			self.model_cb.Clear()
			if models:
				self.model_cb.AppendItems(models)
				self.model_cb.SetValue(models[0])
			self.btn_fetch.Enable()
		wx.CallAfter(update_ui)

	def onSave(self) -> None:
		prov = self.provider_cb.GetValue()
		self.config.set('general', 'provider', prov)
		self.config.set('general', 'stt_engine', 'local' if 'local' in self.stt_cb.GetValue() else 'groq')

		self.config.set('whisper_local', 'model', self.wh_model_cb.GetValue())

		self.config.set('general', 'save_history', str(self.save_hist_cb.GetValue()))
		self.config.set('general', 'history_file', self.hist_path_ctrl.GetValue().strip())

		for p, ctrl in self.api_keys.items():
			self.config.set(p, 'api_key', ctrl.GetValue().strip())

		self.config.set('ollama', 'endpoint', self.ollama_ctrl.GetValue().strip())
		if self.model_cb.GetValue():
			self.config.set(prov, 'model', self.model_cb.GetValue())
		self.config.save()
