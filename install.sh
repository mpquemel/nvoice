#!/bin/bash
# NVoice - Script de Instalação Rápida
# Uso: ./install.sh

echo "🔧 Instalando NVoice Add-on para NVDA..."

# Verifica dependências
echo "📦 Verificando dependências..."
python3 -c "import pyaudio" 2>/dev/null || pip3 install pyaudio
python3 -c "import requests" 2>/dev/null || pip3 install requests
python3 -c "import edge_tts" 2>/dev/null || pip3 install edge-tts
python3 -c "import configobj" 2>/dev/null || pip3 install configobj

# Opcional: faster-whisper para STT local
echo "🎤 Instalar faster-whisper para STT local? (opcional, ~2GB)"
read -p "Instalar? (s/N): " install_whisper
if [ "$install_whisper" == "s" ] || [ "$install_whisper" == "S" ]; then
    pip3 install faster-whisper
    echo "✅ faster-whisper instalado"
fi

# Build do add-on
echo "🏗️  Build do add-on..."
if command -v scons &> /dev/null; then
    scons
    echo "✅ Build concluído: nvoice-1.0.0.nvda-addon"
else
    echo "⚠️  SCons não encontrado. Instalando..."
    pip3 install scons
    scons
    echo "✅ Build concluído: nvoice-1.0.0.nvda-addon"
fi

# Copia para pasta do NVDA (Linux/WSL)
NVDA_ADDON_DIR="$HOME/.nvda/addons/nvoice"
echo "📁 Copiando para $NVDA_ADDON_DIR..."
mkdir -p "$NVDA_ADDON_DIR"
cp -r addon/* "$NVDA_ADDON_DIR/"

echo "✅ NVoice instalado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "1. Reinicie o NVDA"
echo "2. NVDA → Preferências → NVoice (para configurar)"
echo "3. Pressione NVDA+Z para testar"
echo ""
echo "📚 Documentação: README.md"
