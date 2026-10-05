#!/usr/bin/env pwsh
# setup.ps1 -- Setup inicial do ambiente DAVID Pastoral (Fase 0)
# Uso: .\setup.ps1

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DAVID Pastoral -- Setup da Fase 0"             -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# [1] Docker
Write-Host "[1/6] Verificando Docker..." -ForegroundColor Yellow
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "  ERRO: Docker nao encontrado." -ForegroundColor Red
    Write-Host "  Instale o Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
}
Write-Host "  OK: $(docker --version)" -ForegroundColor Green

# [2] Python
Write-Host "[2/6] Verificando Python 3.10+..." -ForegroundColor Yellow
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "  ERRO: Python nao encontrado." -ForegroundColor Red
    exit 1
}
Write-Host "  OK: $(python --version)" -ForegroundColor Green

# [3] Git
Write-Host "[3/6] Verificando Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  ERRO: Git nao encontrado. Instale em https://git-scm.com/" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: $(git --version)" -ForegroundColor Green

# [4] Ambiente virtual Python
Write-Host "[4/6] Criando ambiente virtual Python..." -ForegroundColor Yellow
Set-Location $projectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "  OK: .venv criado" -ForegroundColor Green
} else {
    Write-Host "  OK: .venv ja existe" -ForegroundColor Green
}

Write-Host "  Instalando dependencias (pode demorar na primeira vez)..."
& "$projectRoot\.venv\Scripts\pip.exe" install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "  AVISO: alguns pacotes podem ter falhado -- verifique manualmente" -ForegroundColor Yellow
}

# [5] Arquivo .env
Write-Host "[5/6] Configurando .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  OK: .env criado a partir do .env.example" -ForegroundColor Green
    Write-Host "  ATENCAO: Edite o .env e defina POSTGRES_PASSWORD" -ForegroundColor Yellow
} else {
    Write-Host "  OK: .env ja existe" -ForegroundColor Green
}

# [6] Clonar BibleMarkdown
Write-Host "[6/6] Verificando corpus biblico (BibleMarkdown)..." -ForegroundColor Yellow
$bibleDir = Join-Path $projectRoot "rag\biblia\sources\BibleMarkdown"

if (-not (Test-Path $bibleDir)) {
    Write-Host "  Clonando BibleMarkdown (ACF 2007)..."
    git clone https://github.com/ameisehaufen/BibleMarkdown.git $bibleDir --depth 1 --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: BibleMarkdown clonado" -ForegroundColor Green
    } else {
        Write-Host "  ERRO ao clonar BibleMarkdown" -ForegroundColor Red
    }
} else {
    Write-Host "  OK: BibleMarkdown ja existe em $bibleDir" -ForegroundColor Green
}

# Resumo
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Setup concluido! Proximos passos:" -ForegroundColor Green
Write-Host ""
Write-Host "  1. Subir os servicos Docker:"
Write-Host "     docker-compose up -d" -ForegroundColor White
Write-Host ""
Write-Host "  2. Baixar o modelo Ollama (gemma2:9b -- ~5.5GB, faz uma vez so):"
Write-Host "     docker exec -it david_ollama ollama pull gemma2:9b" -ForegroundColor White
Write-Host ""
Write-Host "  3. Testar indexacao da Biblia (dry-run):"
Write-Host "     .venv\Scripts\python.exe rag\biblia\load_biblia.py --source rag\biblia\sources\BibleMarkdown --dry-run" -ForegroundColor White
Write-Host ""
Write-Host "  4. Indexar a Biblia no RAG (com benchmark):"
Write-Host "     .venv\Scripts\python.exe rag\biblia\load_biblia.py --source rag\biblia\sources\BibleMarkdown --benchmark" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
