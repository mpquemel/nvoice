# 🎙️ NVoice
### Assistente de Voz Inteligente para NVDA

O **NVoice** é um add-on para o leitor de telas NVDA que transforma a interação com Inteligências Artificiais em uma experiência natural, fluida e acessível. Em vez de digitar prompts complexos, o usuário interage via voz em tempo real, recebendo respostas via áudio neural.

---

## 🎯 O Problema
Para pessoas com deficiência visual, a interação com LLMs (como GPT, Gemini e Llama) via teclado pode ser lenta e exaustiva. Embora existam assistentes de voz, a maioria não é integrada ao fluxo de trabalho do NVDA, exigindo a troca de contextos ou o uso de ferramentas externas que não respeitam a dinâmica de navegação de quem utiliza leitores de tela.

## 💡 A Solução
O NVoice resolve isso integrando um pipeline de **SST $\rightarrow$ LLM $\rightarrow$ TTS** diretamente no NVDA. Com um único atalho (`NVDA+Z`), o usuário ativa a escuta, faz sua pergunta e recebe a resposta instantaneamente, sem sair do seu ambiente de trabalho.

### ✨ Funcionalidades Principais
- **Multiprovedores de IA:** Suporte nativo a Ollama (Local), Groq, Google Gemini, OpenAI e OpenRouter.
- **STT de Alta Precisão:** Integração com Groq Whisper e Faster-Whisper local para transcrições precisas.
- **Vozes Neurais Humanizadas:** Utiliza o Microsoft Edge TTS para respostas com entonação natural (ex: `pt-BR-AntonioNeural`).
- **Totalmente Acessível:** Interface de configuração via wxPython desenhada para ser 100% navegável via NVDA.
- **Privacidade Total:** Opção de rodar tudo localmente via Ollama, garantindo que os dados nunca saiam da máquina.

---

## 🛠️ Guia de Instalação

### Usuários (Instalação Rápida)
1. Baixe o arquivo `nvoice-1.0.0.nvda-addon`.
2. No NVDA, vá em `Ferramentas` $\rightarrow$ `Gerenciar complementos` $\rightarrow$ `Instalar`.
3. Selecione o arquivo e confirme a instalação.
4. Reinicie o NVDA.

### Desenvolvedores (Build do Código)
```bash
# Clone o repositório
git clone https://github.com/mpquemel/nvoice.git
cd nvoice-addon

# Instale as dependências
pip install -r requirements.txt

# Gere o pacote do add-on
scons
```

---

## ⌨️ Comandos e Atalhos

| Atalho | Ação |
|--------|-------|
| **NVDA + Z** | Ativar/Desativar escuta (Push-to-Talk) |
| **NVDA + Shift + Z** | Abrir Painel de Configurações |

---

## ⚙️ Arquitetura do Fluxo
`[Voz do Usuário]` $\rightarrow$ `[Groq/Whisper (STT)]` $\rightarrow$ `[LLM (Gemini/Llama/GPT)]` $\rightarrow$ `[Edge TTS]` $\rightarrow$ `[Saída de Áudio NVDA]`

---

## 📜 Licença e Créditos
Este projeto está licenciado sob a **GPL v2+**.
Desenvolvido por **Melhym Pereira Quemel**.

Feito com 💙 para derrubar as barreiras entre a voz e a inteligência artificial.
