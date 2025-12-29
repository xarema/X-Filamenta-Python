# Script de test serveur production
# Date: 2025-12-28

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEMARRAGE SERVEUR PRODUCTION (TEST)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Nettoyage
Write-Host "[1/4] Arret des serveurs..." -ForegroundColor Yellow
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "[2/4] Nettoyage base de donnees..." -ForegroundColor Yellow
Remove-Item "instance\app.db", "instance\installed.flag" -Force -ErrorAction SilentlyContinue

Write-Host "[3/4] Verification port 5000..." -ForegroundColor Yellow
$port5000 = netstat -ano | findstr :5000
if ($port5000) {
    Write-Host "ATTENTION: Port 5000 occupe!" -ForegroundColor Red
    Write-Host $port5000
} else {
    Write-Host "Port 5000 libre" -ForegroundColor Green
}

Write-Host "[4/4] Demarrage serveur production..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Serveur pret sur http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Démarrage
& .\.venv\Scripts\python.exe run_prod.py

