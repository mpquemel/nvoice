# coding: utf-8
import globalPluginHandler
import scriptHandler
import ui
import addonHandler
from gui.settingsDialogs import NVDASettingsDialog

from .nvoice_config import NVoiceConfig
from .nvoice_core import NVoiceCore
from .nvoice_gui import NVoiceSettingsPanel


def getAddonMetadata():
	try:
		addon = globalPluginHandler.getCodeManager().getAddonByName("nvoice")
		return addon
	except Exception:
		return None


addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "NVoice"

	def __init__(self) -> None:
		super().__init__()
		NVDASettingsDialog.categoryClasses.append(NVoiceSettingsPanel)

		self.config = NVoiceConfig()
		self.core = NVoiceCore(self.config)

	def terminate(self) -> None:
		if NVoiceSettingsPanel in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.remove(NVoiceSettingsPanel)
		super().terminate()

	@scriptHandler.script(
		description=_("Activates/Deactivates NVoice (Free Conversation)"),
		gesture="kb:nvda+z"
	)
	def script_toggle_nvoice(self, gesture) -> None:
		self.core.toggle_recording(use_context=False)

	@scriptHandler.script(
		description=_("Activates/Deactivates NVoice (Sending current screen/focus context)"),
		gesture="kb:nvda+shift+z"
	)
	def script_toggle_nvoice_context(self, gesture) -> None:
		self.core.toggle_recording(use_context=True)

	@scriptHandler.script(
		description=_("Clears NVoice conversation history"),
		gesture="kb:nvda+alt+z"
	)
	def script_clear_history(self, gesture) -> None:
		self.core.clear_history()
