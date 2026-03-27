# NVoice - Guia de Primeiros Passos

## 🎯 Objetivo
Configurar e testar o NVoice em 5 minutos.

---

## Passo 1: Instalar Dependências

### Windows (PowerShell)
```powershell
# Abra PowerShell como usuário normal
cd ~/.openclaw/workspace/nvoice-addon
.\install.ps1
```

### Linux/WSL (Bash)
```bash
cd ~/.openclaw/workspace/nvoice-addon
chmod +x install.sh
./install.sh
```

---

## Passo 2: Escolher Provider

### Opção A: Ollama Local (Recomendado para teste)
**Vantagens:** Sem API key, offline, privacidade total

```bash
# 1. Instalar Ollama (se não tiver)
# Windows: https://ollama.com/download
# Linux/WSL:
curl -fsSL https://ollama.com/install.sh | sh

# 2. Baixar modelo leve (3-7GB)
ollama pull llama3.2:3b
# ou
ollama pull qwen2.5:7b

# 3. Verificar se está rodando
ollama list
# Deve mostrar o modelo instalado

# 4. Testar endpoint
curl http://localhost:11434/api/tags
# Deve retornar JSON com modelos
```

### Opção B: Groq Cloud (Free Tier)
**Vantagens:** Muito rápido, créditos free generosos

1. Acesse: https://console.groq.com/keys
2. Crie conta (Google/GitHub)
3. Gere API Key
4. Anote a key (começa com `gsk_...`)

**Limites Free:**
- STT (Whisper): ~15 horas/mês
- Chat (Llama-3.3-70b): ~15k requests/dia

### Opção C: Google Gemini
**Vantagens:** Multimodal (aceita imagens)

1. Acesse: https://makersuite.google.com/app/apikey
2. Crie conta Google
3. Gere API Key
4. Anote a key

---

## Passo 3: Instalar Add-on no NVDA

### Método 1: Script Automático
Já rodou o `install.ps1` ou `install.sh` acima? Então já está instalado!

### Método 2: Manual
1. No NVDA: `Ferramentas → Gerenciar complementos`
2. Clique em `Instalar...`
3. Navegue até: `~/.openclaw/workspace/nvoice-addon/`
4. Selecione a pasta `addon` (ou o arquivo `.nvda-addon` se fez build)
5. Confirme e reinicie o NVDA

---

## Passo 4: Configurar NVoice

1. **Abra NVDA** (reiniciado)
2. Pressione **NVDA+Shift+Z** (ou vá em `Preferências → NVoice`)
3. Preencha:

### Para Ollama:
```
Provider: Ollama (Local)
Endpoint: http://localhost:11434 (já vem preenchido)
API Key: (deixe em branco)
```
4. Clique em **"Buscar Modelos"**
5. Selecione o modelo (ex: `llama3.2:3b`)
6. Voz TTS: `pt-BR-AntonioNeural`
7. Rate: `+40%` (ou ajuste)
8. **Salvar**

### Para Groq:
```
Provider: Groq (Cloud)
API Key: cole sua key (gsk_...)
```
4. Clique em **"Testar"** (deve dizer "API válida")
5. Clique em **"Buscar Modelos"**
6. Selecione: `llama-3.3-70b-versatile` (ou outro)
7. **Salvar**

---

## Passo 5: Testar!

1. **Pressione NVDA+Z**
   - Deve ouvir um bip (440Hz, 100ms)
   - NVDA diz: "NVoice: Ouvindo..."

2. **Fale claramente:**
   - "Qual é a capital do Brasil?"
   - "Que horas são?"
   - "Me conte uma piada"

3. **Pressione NVDA+Z novamente**
   - Bip mais agudo (880Hz, 100ms)
   - NVDA diz: "NVoice: Processando..."

4. **Aguarde a resposta**
   - STT transcreve (2-5s)
   - IA processa (1-10s)
   - TTS fala (Antonio Neural)

---

## 🐛 Problemas Comuns

### "NVoice: Configure primeiro em Preferências > NVoice"
**Causa:** Provider não configurado  
**Solução:** NVDA+Shift+Z, selecione provider, salve

### "Erro ao conectar no Ollama"
**Causa:** Ollama não está rodando  
**Solução:**
```bash
# Verifique se está rodando
ollama list

# Se não estiver, inicie:
ollama serve
```

### "API Groq inválida"
**Causa:** API key errada ou expirada  
**Solução:** Gere nova key em https://console.groq.com/keys

### "NVoice não responde ao NVDA+Z"
**Causa:** Atalho em conflito  
**Solução:**
1. NVDA → `Preferências → Gestos de entrada`
2. Busque por "NVoice"
3. Verifique se NVDA+Z está atribuído
4. Se não, atribua manualmente

### TTS não fala
**Causa:** edge-tts não instalado  
**Solução:**
```bash
pip install edge-tts

# Teste:
edge-tts --text "teste" --voice pt-BR-AntonioNeural --write-media teste.mp3
```

---

## ✅ Checklist de Sucesso

- [ ] Dependências instaladas (`pip list | grep -E "pyaudio|requests|edge-tts"`)
- [ ] Provider configurado (Ollama/Groq/etc.)
- [ ] Modelo selecionado
- [ ] API key testada (se cloud)
- [ ] NVDA reiniciado após instalar add-on
- [ ] NVDA+Z aciona "Ouvindo..."
- [ ] Resposta por voz funciona

---

## 📞 Precisa de Ajuda?

1. **Logs do NVDA:**
   - Windows: `%APPDATA%\nvda\nvda.log`
   - Linux: `~/.nvda/nvda.log`
   - Busque por "NVoice" no log

2. **Teste providers individualmente:**
   ```bash
   # Ollama
   curl http://localhost:11434/api/generate -d '{"model":"llama3.2:3b","prompt":"oi"}'
   
   # Groq
   curl https://api.groq.com/openai/v1/chat/completions \
     -H "Authorization: Bearer SUA_KEY" \
     -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"oi"}]}'
   ```

3. **Reporte bugs:**
   - GitHub: https://github.com/mpquemel/nvoice-addon/issues
   - Email: melhym@quemel.adv.br

---

**Pronto!** Agora é só usar. 🎉

**NVoice 1.0.0** — Março 2026
