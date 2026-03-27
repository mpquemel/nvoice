# NVoice - Windows PowerShell Install Script
# Uso: .\install.ps1

Write-Host "🔧 Instalando NVoice Add-on para NVDA..." -ForegroundColor Cyan

# Verifica dependências
Write-Host "📦 Verificando dependências..." -ForegroundColor Yellow

$deps = @("pyaudio", "requests", "edge-tts", "configobj")
foreach ($dep in $deps) {
    try {
        python -c "import $dep" 2>$null
        Write-Host "  ✅ $dep já instalado" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Instalando $dep..." -ForegroundColor Yellow
        pip install $dep
    }
}

# Opcional: faster-whisper
Write-Host ""
Write-Host "🎤 Instalar faster-whisper para STT local? (opcional, ~2GB)" -ForegroundColor Yellow
$install_whisper = Read-Host "Instalar? (s/N)"
if ($install_whisper -eq "s" -or $install_whisper -eq "S") {
    Write-Host "  Instalando faster-whisper..." -ForegroundColor Cyan
    pip install faster-whisper
    Write-Host "  ✅ faster-whisper instalado" -ForegroundColor Green
}

# Build do add-on
Write-Host ""
Write-Host "🏗️  Build do add-on..." -ForegroundColor Cyan

if (Get-Command scons -ErrorAction SilentlyContinue) {
    scons
    Write-Host "✅ Build concluído: nvoice-1.0.0.nvda-addon" -ForegroundColor Green
} else {
    Write-Host "⚠️  SCons não encontrado. Instalando..." -ForegroundColor Yellow
    pip install scons
    scons
    Write-Host "✅ Build concluído: nvoice-1.0.0.nvda-addon" -ForegroundColor Green
}

# Copia para pasta do NVDA (Windows)
$NVDA_ADDON_DIR = "$env:APPDATA\nvda\addons\nvoice"
Write-Host ""
Write-Host "📁 Copiando para $NVDA_ADDON_DIR..." -ForegroundColor Cyan

if (!(Test-Path $NVDA_ADDON_DIR)) {
    New-Item -ItemType Directory -Force -Path $NVDA_ADDON_DIR | Out-Null
}

Copy-Item -Recurse -Force "addon\*" $NVDA_ADDON_DIR

Write-Host ""
Write-Host "✅ NVoice instalado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Reinicie o NVDA"
Write-Host "2. NVDA → Preferências → NVoice (para configurar)"
Write-Host "3. Pressione NVDA+Z para testar"
Write-Host ""
Write-Host "📚 Documentação: README.md" -ForegroundColor Gray
