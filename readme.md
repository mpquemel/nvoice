# NVoice - AI Voice Assistant for NVDA

[[!meta title="NVoice - AI Voice Assistant for NVDA"]]

NVoice transforms NVDA into a **low-latency conversational AI assistant**.
With NVoice, you can dialog with the world's most advanced AI models using just your voice.

## Features

- **Voice-activated AI conversations** - Talk naturally with AI models
- **Multi-provider support** - Groq, Gemini, OpenAI, OpenRouter, Ollama
- **Dual STT engines** - Fast cloud (Groq Whisper) or local (Whisper CLI)
- **Context injection** - Send current screen/focus content to AI
- **Conversation history** - Automatic save to text file
- **Streaming synthesis** - Real-time voice response with natural pauses
- **7 languages** - Full internationalization support
- **No dependencies** - Pure Python, works with any NVDA installation

## Installation

1. Download the latest `.nvda-addon` file from the releases
2. Press `NVDA+q` to open the Add-ons Manager
3. Install the addon from file
4. Restart NVDA

## Configuration

Press `NVDA+q` and navigate to NVoice settings to configure:

- **LLM Provider** - Choose your AI provider (Groq, OpenAI, Gemini, OpenRouter, Ollama)
- **STT Engine** - Cloud (Groq Whisper) or Local (Whisper CLI)
- **API Keys** - Enter your credentials for each provider
- **History** - Enable automatic conversation logging

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `NVDA+Z` | Start/stop free conversation |
| `NVDA+Shift+Z` | Start/stop with screen context |
| `NVDA+Alt+Z` | Clear conversation history |

## Requirements

- NVDA 2024.1 or later
- Windows 10/11
- Internet connection (for cloud providers)

## Supported AI Providers

- **Groq** (recommended) - Fast inference, free tier available
- **OpenAI** - GPT-4o and more
- **Google Gemini** - Google's AI models
- **OpenRouter** - Unified access to multiple models
- **Ollama** - Local AI models (no internet required)

## License

This add-on is distributed under the **GNU General Public License v2**.

## Author

Melhym Quemel - [mpquemel@gmail.com](mailto:mpquemel@gmail.com)

## Support and Feedback

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/mpquemel/nvoice).

---

*NVoice: Empowering blind and low-vision users with conversational AI.*
