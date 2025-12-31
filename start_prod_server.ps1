# ==============================================================================
# Production Server Startup Script
# ==============================================================================
# Purpose: Start production server with proper logging and error handling
# File: start_prod_server.ps1 | Repository: X-Filamenta-Python
# Created: 2025-12-30
# ==============================================================================

param(
    [switch]$Clean = $false
)

# Set location
Set-Location -Path "D:\xarema\X-Filamenta-Python"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Production Server Startup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Stop existing Python processes if Clean flag is set
if ($Clean) {
    Write-Host "[1/4] Stopping existing Python processes..." -ForegroundColor Yellow
    Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "      Done." -ForegroundColor Green
} else {
    Write-Host "[1/4] Skipping process cleanup (use -Clean to force)" -ForegroundColor Gray
}

# Check Python environment
Write-Host "[2/4] Checking Python environment..." -ForegroundColor Yellow
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "      ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "      Please run: python -m venv .venv" -ForegroundColor Red
    exit 1
}
$pythonVersion = & ".\.venv\Scripts\python.exe" --version
Write-Host "      $pythonVersion" -ForegroundColor Green

# Check if app can be imported
Write-Host "[3/4] Testing Flask app import..." -ForegroundColor Yellow
$testImport = & ".\.venv\Scripts\python.exe" -c "from backend.src.app import create_app; print('OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Cannot import Flask app!" -ForegroundColor Red
    Write-Host "      $testImport" -ForegroundColor Red
    exit 1
}
Write-Host "      Import successful" -ForegroundColor Green

# Start server
Write-Host "[4/4] Starting production server..." -ForegroundColor Yellow
Write-Host "`n----------------------------------------" -ForegroundColor Cyan
Write-Host "  Server logs below:" -ForegroundColor Cyan
Write-Host "----------------------------------------`n" -ForegroundColor Cyan

# Run the server (blocking - will show all output)
& ".\.venv\Scripts\python.exe" run_prod.py

# If we reach here, server was stopped
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Server stopped" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

