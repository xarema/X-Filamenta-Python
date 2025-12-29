# Script de demarrage serveur production
# Simplifie - Version finale

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "DEMARRAGE SERVEUR PRODUCTION" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Arret serveurs
Write-Host "[1/3] Arret des serveurs..." -ForegroundColor Yellow
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Nettoyage
Write-Host "[2/3] Nettoyage base de donnees..." -ForegroundColor Yellow
Remove-Item "instance\app.db", "instance\installed.flag" -Force -ErrorAction SilentlyContinue

# Demarrage
Write-Host "[3/3] Demarrage serveur..." -ForegroundColor Yellow
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "URL: http://127.0.0.1:5000/install/" -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

& .\.venv\Scripts\python.exe run_prod.py

