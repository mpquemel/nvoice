# coding: utf-8
import os
import configobj
import globalVars
from typing import Dict, Any

class NVoiceConfig:
    """Gerenciador central de configurações do NVoice (Padrão Singleton)."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NVoiceConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self) -> None:
        if self._initialized:
            return
            
        self.DEFAULT_CONFIG: Dict[str, Any] = {
            'general': {
                'provider': 'groq',
                'stt_engine': 'groq',
                'save_history': 'False',
                'history_file': ''
            },
            'groq': {'api_key': '', 'model': 'llama-3.3-70b-versatile'},
            'openai': {'api_key': '', 'model': 'gpt-4o'},
            'gemini': {'api_key': '', 'model': 'gemini-flash-latest'},
            'openrouter': {'api_key': '', 'model': 'meta-llama/llama-3.1-70b-instruct'},
            'ollama': {'endpoint': 'http://localhost:11434', 'model': 'qwen2.5:0.5b'},
            'whisper_local': {'model': 'base'} # NOVO: Tamanho do modelo Whisper CLI
        }
        
        self.config_path: str = os.path.join(globalVars.appArgs.configPath, 'nvoice_config.ini')
        self._config: configobj.ConfigObj = self._load()
        self._initialized = True
    
    def _load(self) -> configobj.ConfigObj:
        conf = configobj.ConfigObj(self.config_path, encoding='UTF-8') if os.path.exists(self.config_path) else configobj.ConfigObj(encoding='UTF-8')
        for section, values in self.DEFAULT_CONFIG.items():
            if section not in conf:
                conf[section] = {}
            for key, val in values.items():
                if key not in conf[section]:
                    conf[section][key] = val
        return conf
    
    def save(self) -> None:
        self._config.filename = self.config_path
        self._config.write()
    
    def get(self, section: str, key: str) -> str:
        return self._config.get(section, {}).get(key, '')
        
    def get_bool(self, section: str, key: str) -> bool:
        return str(self.get(section, key)).lower() == 'true'
        
    def set(self, section: str, key: str, value: str) -> None:
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self.save()