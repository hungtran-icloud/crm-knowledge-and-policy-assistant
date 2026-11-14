# dev.ps1 — Thay thế Makefile trên Windows
# Dùng: .\dev.ps1 <target>
param([string]$Target = "help")

$Root = $PSScriptRoot

function Invoke-DevDB {
    Write-Host "Starting dev databases (PostgreSQL+pgvector, Redis)..." -ForegroundColor Cyan
    Write-Host "  Note: MinIO (storage) is a separate profile. Run '.\dev.ps1 dev-storage' when needed." -ForegroundColor DarkGray
    docker compose up -d db redis
}

function Invoke-DevStorage {
    Write-Host "Starting object storage (MinIO)..." -ForegroundColor Cyan
    Write-Host "  Requires Docker Hub access. If blocked, skip for Phase 1-2." -ForegroundColor Yellow
    docker compose --profile storage up -d storage
}

function Invoke-Up {
    Write-Host "Starting all services..." -ForegroundColor Cyan
    docker compose up -d
}

function Invoke-Down {
    Write-Host "Stopping all services..." -ForegroundColor Cyan
    docker compose down
}

function Invoke-Logs {
    docker compose logs -f
}

function Invoke-Lint {
    Write-Host "Running backend lint..." -ForegroundColor Cyan
    Set-Location "$Root\backend"
    python -m ruff check .
    Set-Location $Root
}

function Invoke-Test {
    Write-Host "Running backend tests..." -ForegroundColor Cyan
    Set-Location "$Root\backend"
    python -m pytest -q
    Set-Location $Root
}

function Invoke-Migrate {
    Write-Host "Running Alembic migrations..." -ForegroundColor Cyan
    Set-Location "$Root\backend"
    python -m alembic upgrade head
    Set-Location $Root
}

function Invoke-Dev {
    Write-Host "Starting FastAPI dev server on http://localhost:8000..." -ForegroundColor Cyan
    Set-Location "$Root\backend"
    python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    Set-Location $Root
}

function Invoke-Help {
    Write-Host ""
    Write-Host "Usage: .\dev.ps1 <target>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Targets:"
    Write-Host "  dev-db      Start PostgreSQL+pgvector, Redis"
    Write-Host "  dev         Start FastAPI backend dev server (uvicorn --reload)"
    Write-Host "  dev-storage Start MinIO storage (Phase 3+)"
    Write-Host "  up          Start all containerized services"
    Write-Host "  down        Stop all services"
    Write-Host "  logs        Tail logs"
    Write-Host "  lint        Run ruff lint"
    Write-Host "  test        Run pytest"
    Write-Host "  migrate     Run alembic upgrade head"
    Write-Host ""
}

switch ($Target) {
    "dev-db"      { Invoke-DevDB }
    "dev-storage" { Invoke-DevStorage }
    "dev"         { Invoke-Dev }
    "start"       { Invoke-Dev }
    "up"          { Invoke-Up }
    "down"        { Invoke-Down }
    "logs"        { Invoke-Logs }
    "lint"        { Invoke-Lint }
    "test"        { Invoke-Test }
    "migrate"     { Invoke-Migrate }
    default       { Invoke-Help }
}

