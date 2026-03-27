#!/usr/bin/env python3
# NVoice - Test Script
# coding: utf-8
# Uso: python3 test_nvoice.py

import sys
import os

print("🧪 NVoice - Script de Testes")
print("=" * 50)

# Teste 1: Dependências
print("\n1️⃣  Verificando dependências...")
deps = {
    'pyaudio': 'Áudio (microfone)',
    'requests': 'HTTP (APIs)',
    'edge_tts': 'TTS (voz)',
    'configobj': 'Configurações',
    'faster_whisper': 'STT local (opcional)'
}

missing = []
for dep, desc in deps.items():
    try:
        __import__(dep.replace('-', '_'))
        print(f"  ✅ {dep:20} - {desc}")
    except ImportError:
        if dep == 'faster_whisper':
            print(f"  ⚠️  {dep:20} - {desc} (OPCIONAL)")
        else:
            print(f"  ❌ {dep:20} - {desc}")
            missing.append(dep)

if missing:
    print(f"\n⚠️  Faltam dependências: {', '.join(missing)}")
    print(f"Instale: pip install {' '.join(missing)}")
    sys.exit(1)

# Teste 2: Configuração
print("\n2️⃣  Verificando configuração...")
config_path = os.path.expanduser("~/.nvda/nvoice_config.ini")
if os.path.exists(config_path):
    print(f"  ✅ Config encontrada: {config_path}")
else:
    print(f"  ⚠️  Config não existe (será criada na primeira execução)")

# Teste 3: Ollama (se disponível)
print("\n3️⃣  Testando Ollama (local)...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=3)
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"  ✅ Ollama conectado: {len(models)} modelo(s)")
        for model in models:
            print(f"     - {model['name']}")
    else:
        print(f"  ❌ Ollama retornou erro {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"  ❌ Ollama não está rodando (http://localhost:11434)")
except Exception as e:
    print(f"  ❌ Erro: {e}")

# Teste 4: Groq (se API key configurada)
print("\n4️⃣  Testando Groq API...")
import configobj
try:
    config = configobj.ConfigObj(config_path, encoding='UTF-8')
    groq_key = config.get('groq', {}).get('api_key', '')
    
    if groq_key:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {groq_key}"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print(f"  ✅ Groq API válida: {len(models)} modelo(s) disponível(eis)")
        else:
            print(f"  ❌ Groq API inválida (erro {response.status_code})")
    else:
        print(f"  ⚠️  Groq API key não configurada")
except Exception as e:
    print(f"  ❌ Erro ao testar Groq: {e}")

# Teste 5: Google Gemini (se API key configurada)
print("\n5️⃣  Testando Google Gemini API...")
try:
    config = configobj.ConfigObj(config_path, encoding='UTF-8')
    google_key = config.get('google', {}).get('api_key', '')
    
    if google_key:
        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={google_key}",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"  ✅ Gemini API válida: {len(models)} modelo(s)")
        else:
            print(f"  ❌ Gemini API inválida (erro {response.status_code})")
    else:
        print(f"  ⚠️  Google API key não configurada")
except Exception as e:
    print(f"  ❌ Erro ao testar Gemini: {e}")

# Teste 6: TTS (Edge TTS)
print("\n6️⃣  Testando Edge TTS...")
try:
    import asyncio
    import edge_tts
    
    async def test_tts():
        communicate = edge_tts.Communicate(
            "NVoice testando",
            "pt-BR-AntonioNeural",
            rate="+40%"
        )
        await communicate.save("/tmp/nvoice_test.mp3")
        return True
    
    asyncio.run(test_tts())
    print(f"  ✅ Edge TTS funciona (arquivo: /tmp/nvoice_test.mp3)")
except Exception as e:
    print(f"  ❌ Edge TTS falhou: {e}")

# Teste 7: Áudio (PyAudio)
print("\n7️⃣  Testando PyAudio (microfone)...")
try:
    import pyaudio
    audio = pyaudio.PyAudio()
    
    devices = []
    for i in range(audio.get_device_count()):
        dev = audio.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            devices.append(dev['name'])
    
    print(f"  ✅ PyAudio OK: {len(devices)} dispositivo(s) de entrada")
    for dev in devices[:3]:  # Mostra só os 3 primeiros
        print(f"     - {dev[:50]}")
    
    audio.terminate()
except Exception as e:
    print(f"  ❌ PyAudio falhou: {e}")

print("\n" + "=" * 50)
print("✅ Testes concluídos!")
print("\n📝 Próximo passo:")
print("   1. Instale o add-on no NVDA")
print("   2. NVDA → Preferências → NVoice")
print("   3. Configure provider e modelo")
print("   4. Pressione NVDA+Z e teste!")
