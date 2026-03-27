# NVoice - Assistente de Voz com IA para NVDA

[![NVDA 2025.3.3+](https://img.shields.io/badge/NVDA-2025.3.3%2B-blue)](https://www.nvaccess.org/download)
[![License: GPL v2+](https://img.shields.io/badge/License-GPL%20v2%2B-green)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

**NVoice** é um add-on para NVDA que permite conversar com IAs usando sua voz. Pressione **NVDA+Z**, fale, e receba respostas por áudio.

## 🚀 Recursos Principais

### Providers Suportados
| Provider | Tipo | API Key | Destaque |
|----------|------|---------|----------|
| **Ollama** | Local | ❌ Não | Privacidade total, offline |
| **Groq** | Cloud | ✅ Free tier | Whisper STT + LLM rápido |
| **Google Gemini** | Cloud | ✅ | Multimodal (visão) |
| **OpenAI GPT-4** | Cloud | ✅ | Modelo mais capaz |
| **OpenRouter** | Cloud | ✅ | 100+ modelos |

### STT (Speech-to-Text)
- **Groq Whisper-large-v3-turbo** - Cloud, free, ~15h/mês grátis
- **Faster-Whisper local** - Offline, requer instalação

### TTS (Text-to-Speech)
- Microsoft Edge TTS (vozes neurais)
- pt-BR-AntonioNeural (padrão)
- pt-BR-FranciscaNeural
- pt-BR-ThalitaMultilingualNeural
- Rate, volume, pitch ajustáveis

## 📦 Instalação

### Pré-requisitos
- NVDA 2025.3.3 ou superior
- Python 3.11+ (já vem com NVDA 2026+)

### Opção 1: Instalar do arquivo (.nvda-addon)
1. Baixe `nvoice-1.0.0.nvda-addon`
2. No NVDA: `Ferramentas → Gerenciar complementos → Instalar`
3. Selecione o arquivo e confirme
4. Reinicie o NVDA

### Opção 2: Desenvolvimento (local)
```bash
# Clone ou acesse a pasta
cd ~/.openclaw/workspace/nvoice-addon

# Instale dependências
pip install -r requirements.txt

# Build
scons

# O arquivo nvoice-1.0.0.nvda-addon será criado
```

### Opção 3: Instalação direta (dev)
```bash
# Copia para pasta de addons do NVDA
cp -r addon/* "$APPDATA/nvda/addons/nvoice/"

# Reinicie NVDA
```

## 🎯 Uso

### Ativar NVoice
1. Pressione **NVDA+Z**
2. Fale seu comando/pergunta
3. Pressione **NVDA+Z** novamente para parar
4. Aguarde a resposta por áudio

### Configurar
1. **NVDA → Preferências → NVoice**
2. Selecione provider (Ollama, Groq, etc.)
3. Para cloud: insira API key e clique em **"Testar"**
4. Clique em **"Buscar Modelos"** para listar disponíveis
5. Selecione modelo desejado
6. Configure voz TTS (Antonio, Francisca, etc.)
7. Ajuste rate (+40% padrão) e volume
8. **Salvar**

## ⚙️ Configuração de Providers

### Ollama (Local - Recomendado para privacidade)
```
Endpoint: http://localhost:11434
API Key: (não precisa)
Modelos: lista automática
```

**Instalar Ollama:**
```bash
# Windows: baixar em https://ollama.com
# Ou WSL/Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo:
ollama pull llama3.2:3b
# ou
ollama pull qwen2.5:7b
```

### Groq (Free Tier Generoso)
```
API Key: https://console.groq.com/keys
STT: whisper-large-v3-turbo (free)
Chat: llama-3.3-70b-versatile (free ~15k req/dia)
```

### Google Gemini
```
API Key: https://makersuite.google.com/app/apikey
Modelos: gemini-2.0-flash, gemini-pro-vision
```

### OpenAI
```
API Key: https://platform.openai.com/api-keys
Modelos: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
```

### OpenRouter
```
API Key: https://openrouter.ai/keys
Modelos: 100+ (Llama, Mistral, Claude, etc.)
```

## ⌨️ Atalhos

| Atalho | Ação |
|--------|------|
| **NVDA+Z** | Ativar/desativar escuta |
| **NVDA+Shift+Z** | Abrir configurações |

## 🏗️ Arquitetura

```
[NVDA+Z] → Microfone → [STT: Groq/Whisper] → Texto
                                              ↓
                                        [Provider IA]
                                              ↓
                                        [TTS: Edge]
                                              ↓
                                          Áudio → NVDA
```

## 📁 Estrutura

```
nvoice-addon/
├── addon/
│   ├── globalPlugins/nvoice/
│   │   ├── __init__.py        # Entry point, script NVDA+Z
│   │   ├── nvoice_config.py   # Config manager (JSON/INI)
│   │   ├── nvoice_core.py     # STT → IA → TTS pipeline
│   │   └── nvoice_gui.py      # Settings dialog (wxPython)
│   ├── doc/PT/readme.html
│   └── manifest.ini
├── requirements.txt
├── buildVars.py
└── SConstruct
```

## 🛠️ Desenvolvimento

### Dependências
```bash
pip install pyaudio faster-whisper requests edge-tts configobj
```

### Build
```bash
scons
# Gera: nvoice-1.0.0.nvda-addon
```

### Testar
1. Instale o `.nvda-addon` no NVDA
2. Configure provider (Ollama local é mais fácil pra testar)
3. Pressione NVDA+Z e fale
4. Verifique logs em `%APPDATA%\nvda\nvda.log`

## 🐛 Troubleshooting

### NVoice não responde
- Verifique se NVDA+Z não está em conflito (Preferências → Gestos)
- Confira se provider está configurado

### Ollama não conecta
- Teste: `curl http://localhost:11434/api/tags`
- Verifique se Ollama está rodando: `ollama list`

### Groq API inválida
- Gere key em: https://console.groq.com/keys
- Free tier: ~15h de áudio/mês, ~15k requests/dia

### TTS não fala
- Verifique se `edge-tts` está instalado: `pip show edge-tts`
- Teste voz: `edge-tts --text "teste" --voice pt-BR-AntonioNeural --write-media teste.mp3`

## 📋 Roadmap

### v1.0 (Atual)
- ✅ STT (Groq + Whisper local)
- ✅ IA (5 providers)
- ✅ TTS (Edge)
- ✅ Config GUI completa

### v1.1 (Próximo)
- [ ] Histórico de conversas (JSON)
- [ ] Compartilhamento de contexto da tela
- [ ] Comandos de voz ("repetir", "parar")

### v2.0
- [ ] Wake word ("Hey NVoice")
- [ ] Suporte a imagens (Gemini/GPT-4 Vision)
- [ ] Profiles por aplicativo
- [ ] Internacionalização (i18n)

## 📄 Licença

GPL v2+

## 👤 Autor

**Melhym Quemel** - [GitHub](https://github.com/mpquemel)

---

**NVoice 1.0.0** — Março 2026
