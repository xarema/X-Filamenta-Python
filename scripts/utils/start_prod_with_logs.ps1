# Script de demarrage du serveur de production avec logs
# File: .dev_scripts/utilities/start_prod_with_logs.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Demarrage serveur PRODUCTION (Waitress)  " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Nettoyer les processus existants
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force 2>$null
Write-Host "[OK] Processus nettoyes" -ForegroundColor Green

# Se placer dans le répertoire du projet
$ProjectRoot = "D:\xarema\X-Filamenta-Python"
Set-Location $ProjectRoot

# Créer le dossier logs si inexistant
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
}

$LogFile = "logs\prod_server_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Lancer le serveur dans une nouvelle fenêtre
Write-Host ""
Write-Host "Lancement du serveur..." -ForegroundColor Yellow
Write-Host "Logs: $LogFile" -ForegroundColor Gray
Write-Host ""

Start-Process -FilePath "$ProjectRoot\.venv\Scripts\python.exe" `
    -ArgumentList "run_prod.py" `
    -WorkingDirectory $ProjectRoot `
    -RedirectStandardOutput $LogFile `
    -RedirectStandardError "$LogFile.err" `
    -WindowStyle Normal

Start-Sleep -Seconds 2
Write-Host "[OK] Serveur demarre en arriere-plan" -ForegroundColor Green
Write-Host ""
Write-Host "URL: http://127.0.0.1:5000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ouverture du navigateur..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process msedge "http://localhost:5000"

