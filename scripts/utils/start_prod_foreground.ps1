# Script de demarrage simple du serveur (mode foreground pour debug)
# File: .dev_scripts/utilities/start_prod_foreground.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SERVEUR PRODUCTION (Mode Foreground)  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Nettoyer processus existants
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force 2>$null
Write-Host "[OK] Processus nettoyes" -ForegroundColor Green

# Aller dans le dossier projet
Set-Location D:\xarema\X-Filamenta-Python

Write-Host ""
Write-Host "Demarrage du serveur..." -ForegroundColor Yellow
Write-Host "URL: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Gray
Write-Host ""

# Lancer en mode foreground (bloquant)
.\.venv\Scripts\python.exe run_prod.py

