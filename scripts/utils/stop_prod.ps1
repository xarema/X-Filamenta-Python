# Script d'arret du serveur de production
# File: .dev_scripts/utilities/stop_prod.ps1

Write-Host "============================================" -ForegroundColor Red
Write-Host "     ARRET SERVEUR PRODUCTION (Waitress)    " -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host ""

# Arrêter tous les processus Python
$PythonProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*"}

if ($PythonProcesses) {
    Write-Host "Processus Python trouves:" -ForegroundColor Yellow
    $PythonProcesses | ForEach-Object {
        Write-Host "  - PID: $($_.Id) | $($_.ProcessName)" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "Arret en cours..." -ForegroundColor Yellow

    $PythonProcesses | Stop-Process -Force 2>$null

    Start-Sleep -Seconds 1

    Write-Host "[OK] Tous les processus Python ont ete arretes" -ForegroundColor Green
} else {
    Write-Host "[INFO] Aucun processus Python en cours d'execution" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Verification du port 5000..." -ForegroundColor Gray
$Port5000 = netstat -ano | Select-String "5000"

if ($Port5000) {
    Write-Host "[ATTENTION] Le port 5000 est encore utilise:" -ForegroundColor Yellow
    Write-Host $Port5000
} else {
    Write-Host "[OK] Le port 5000 est libre" -ForegroundColor Green
}

