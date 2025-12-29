#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de verification post-installation du wizard
.DESCRIPTION
    Verifie que le wizard a correctement installe l'application
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICATION POST-INSTALLATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = "D:\xarema\X-Filamenta-Python"
$InstancePath = "$ProjectRoot\instance"

$AllOK = $true

# 1. Verifier le flag d'installation
Write-Host "[1/5] Verification du flag d'installation..." -ForegroundColor Yellow

if (Test-Path "$InstancePath\installed.flag") {
    Write-Host "  OK Flag d'installation present" -ForegroundColor Green
} else {
    Write-Host "  ERREUR Flag d'installation manquant!" -ForegroundColor Red
    $AllOK = $false
}

Write-Host ""

# 2. Verifier la base de donnees
Write-Host "[2/5] Verification de la base de donnees..." -ForegroundColor Yellow

$DBFile = "$InstancePath\x-filamenta_python.db"

if (Test-Path $DBFile) {
    Write-Host "  OK Base de donnees creee: $((Get-Item $DBFile).Name)" -ForegroundColor Green

    $DBSize = (Get-Item $DBFile).Length
    Write-Host "    Taille: $([math]::Round($DBSize / 1KB, 2)) KB" -ForegroundColor Gray

    # Verifier les tables avec sqlite3 (si disponible)
    $sqlite3 = Get-Command sqlite3 -ErrorAction SilentlyContinue
    if ($sqlite3) {
        Write-Host "  - Verification des tables..." -ForegroundColor Gray
        $tables = sqlite3 $DBFile ".tables"
        if ($tables) {
            Write-Host "    Tables trouvees: $($tables -split '\s+' | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Green
            Write-Host "    $tables" -ForegroundColor DarkGray
        } else {
            Write-Host "    ERREUR Aucune table trouvee!" -ForegroundColor Red
            $AllOK = $false
        }
    } else {
        Write-Host "    (sqlite3 non disponible pour verifier les tables)" -ForegroundColor DarkGray
    }
} else {
    Write-Host "  ERREUR Base de donnees non creee!" -ForegroundColor Red
    $AllOK = $false
}

Write-Host ""

# 3. Verifier l'utilisateur admin via Python
Write-Host "[3/5] Verification de l'utilisateur administrateur..." -ForegroundColor Yellow

$CheckAdmin = @"
import sys
sys.path.insert(0, '.')
try:
    from backend.src.app import create_app
    from backend.src.models.user import User
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('OK')
            print(f'Username: {admin.username}')
            print(f'Email: {admin.email}')
            print(f'Is Admin: {admin.is_admin}')
            print(f'Is Active: {admin.is_active}')
        else:
            print('NOTFOUND')
except Exception as e:
    print(f'ERROR: {e}')
"@

Set-Location $ProjectRoot
& .\.venv\Scripts\python.exe -c $CheckAdmin | Out-File -FilePath temp_check.txt -Encoding UTF8

$result = Get-Content temp_check.txt
Remove-Item temp_check.txt -Force

if ($result -match "OK") {
    Write-Host "  OK Utilisateur admin cree" -ForegroundColor Green
    $result | Where-Object { $_ -match "Username|Email|Is Admin|Is Active" } | ForEach-Object {
        Write-Host "    $_" -ForegroundColor Gray
    }
} elseif ($result -match "NOTFOUND") {
    Write-Host "  ERREUR Utilisateur admin non trouve!" -ForegroundColor Red
    $AllOK = $false
} else {
    Write-Host "  ERREUR lors de la verification:" -ForegroundColor Red
    Write-Host "    $result" -ForegroundColor DarkRed
    $AllOK = $false
}

Write-Host ""

# 4. Test de connexion
Write-Host "[4/5] Test de connexion a l'application..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/" -Method GET -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop

    if ($response.StatusCode -eq 200) {
        Write-Host "  OK Application accessible (HTTP 200)" -ForegroundColor Green

        if ($response.Content -match "login" -or $response.Content -match "connexion") {
            Write-Host "  OK Redirection vers login detectee" -ForegroundColor Green
        } else {
            Write-Host "  ? Contenu inattendu" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ? Status code: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ATTENTION Serveur non accessible (normal si arrete)" -ForegroundColor Yellow
    Write-Host "    Demarrez le serveur avec: python run.py" -ForegroundColor Gray
}

Write-Host ""

# 5. Verification des fichiers statiques
Write-Host "[5/5] Verification des fichiers statiques..." -ForegroundColor Yellow

$StaticFiles = @(
    "frontend\static\css\main.css",
    "frontend\static\js\plugins"
)

foreach ($file in $StaticFiles) {
    $path = "$ProjectRoot\$file"
    if (Test-Path $path) {
        Write-Host "  OK $file" -ForegroundColor Green
    } else {
        Write-Host "  ERREUR $file manquant" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($AllOK) {
    Write-Host "  OK INSTALLATION REUSSIE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "L'application est prete a etre utilisee!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour tester le login:" -ForegroundColor Cyan
    Write-Host "  1. Demarrez le serveur: python run.py" -ForegroundColor White
    Write-Host "  2. Ouvrez: http://localhost:5000/auth/login" -ForegroundColor White
    Write-Host "  3. Connectez-vous avec:" -ForegroundColor White
    Write-Host "     Username: admin" -ForegroundColor Yellow
    Write-Host "     Password: [celui cree dans le wizard]" -ForegroundColor Yellow
} else {
    Write-Host "  ERREUR PROBLEMES DETECTES" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Veuillez relancer le wizard d'installation." -ForegroundColor Yellow
}

Write-Host ""

