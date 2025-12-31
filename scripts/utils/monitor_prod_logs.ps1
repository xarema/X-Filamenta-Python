# Script de monitoring des logs du serveur de production
# File: .dev_scripts/utilities/monitor_prod_logs.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "     MONITORING LOGS SERVEUR PRODUCTION     " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = "D:\xarema\X-Filamenta-Python"
Set-Location $ProjectRoot

# Trouver le dernier fichier de log
$LatestLog = Get-ChildItem logs\*.err -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($LatestLog) {
    Write-Host "Fichier monitore: $($LatestLog.Name)" -ForegroundColor Yellow
    Write-Host "Appuyez sur Ctrl+C pour arreter" -ForegroundColor Gray
    Write-Host ""
    Write-Host "--- DEBUT DES LOGS ---" -ForegroundColor Cyan
    Write-Host ""

    # Afficher les logs en temps réel
    Get-Content $LatestLog.FullName -Wait -Tail 50
} else {
    Write-Host "[ERREUR] Aucun fichier de log trouve dans le dossier 'logs'" -ForegroundColor Red
    Write-Host "Avez-vous demarre le serveur avec start_prod_with_logs.ps1 ?" -ForegroundColor Yellow
}

