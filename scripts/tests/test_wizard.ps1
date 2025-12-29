# Script de test rapide du wizard
# Usage: .\test_wizard.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        TEST WIZARD D'INSTALLATION - GUIDE RAPIDE          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Vérifier qu'on est dans le bon dossier
if (-not (Test-Path "run.py")) {
    Write-Host "❌ ERREUR: Vous devez executer ce script depuis D:\xarema\X-Filamenta-Python\" -ForegroundColor Red
    exit 1
}

# 2. Vérifier que l'environnement virtuel existe
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "❌ ERREUR: Environnement virtuel non trouve" -ForegroundColor Red
    Write-Host "   Creez-le avec: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "1. Preparation du test..." -ForegroundColor Yellow
Write-Host ""

# 3. Supprimer le flag d'installation
if (Test-Path "instance\installed.flag") {
    Remove-Item "instance\installed.flag" -Force
    Write-Host "   ✓ Flag d'installation supprime" -ForegroundColor Green
} else {
    Write-Host "   ✓ Pas de flag existant" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. Lancement du test automatise..." -ForegroundColor Yellow
Write-Host ""

# 4. Lancer le test automatisé
.\.venv\Scripts\python.exe scripts\tests\test_wizard_manual.py
$testResult = $LASTEXITCODE

Write-Host ""

if ($testResult -eq 0) {
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              ✅ TEST AUTOMATISE REUSSI ✅                 ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Le wizard fonctionne correctement en mode automatise!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🧪 POUR TESTER DANS LE NAVIGATEUR:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Supprimez le flag:" -ForegroundColor White
    Write-Host "     Remove-Item instance\installed.flag" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  2. Lancez l'application:" -ForegroundColor White
    Write-Host "     python run.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  3. Ouvrez dans votre navigateur:" -ForegroundColor White
    Write-Host "     http://localhost:5000/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  4. Suivez les etapes:" -ForegroundColor White
    Write-Host "     - Cliquez sur 'Continuer en francais'" -ForegroundColor Cyan
    Write-Host "     - Cliquez sur 'Commencer'" -ForegroundColor Cyan
    Write-Host "     - Configurez la base de donnees (SQLite par defaut)" -ForegroundColor Cyan
    Write-Host "     - Creez le compte administrateur" -ForegroundColor Cyan
    Write-Host "     - Finalisez l'installation" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║                ❌ TEST ECHOUE ❌                          ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Consultez les logs ci-dessus pour plus de details" -ForegroundColor Yellow
}

Write-Host ""

