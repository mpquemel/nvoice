# coding: utf-8
import globalPluginHandler
import scriptHandler
import ui
from gui.settingsDialogs import NVDASettingsDialog

from .nvoice_config import NVoiceConfig
from .nvoice_core import NVoiceCore
from .nvoice_gui import NVoiceSettingsPanel

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
        description="Ativa/Desativa NVoice (Conversa Livre)",
        gesture="kb:nvda+z"
    )
    def script_toggle_nvoice(self, gesture) -> None:
        self.core.toggle_recording(use_context=False)

    @scriptHandler.script(
        description="Ativa/Desativa NVoice (Enviando o contexto atual da tela/foco)",
        gesture="kb:nvda+shift+z"
    )
    def script_toggle_nvoice_context(self, gesture) -> None:
        self.core.toggle_recording(use_context=True)

    @scriptHandler.script(
        description="Limpa o histórico de conversa do NVoice",
        gesture="kb:nvda+alt+z"
    )
    def script_clear_history(self, gesture) -> None:
        self.core.clear_history()