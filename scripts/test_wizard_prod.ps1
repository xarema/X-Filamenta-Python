#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de test du wizard d'installation comme en production
.DESCRIPTION
    Prepare et teste le wizard d'installation X-Filamenta-Python
    Simule une installation fraiche en production
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  WIZARD TEST - MODE PRODUCTION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ProjectRoot = "D:\xarema\X-Filamenta-Python"
$InstancePath = "$ProjectRoot\instance"
$BackendInstancePath = "$ProjectRoot\backend\instance"

# Etape 1: Nettoyage complet
Write-Host "[1/5] Nettoyage de l'environnement..." -ForegroundColor Yellow
Write-Host "  - Suppression du flag d'installation" -ForegroundColor Gray

if (Test-Path "$InstancePath\installed.flag") {
    Remove-Item "$InstancePath\installed.flag" -Force
    Write-Host "    OK installed.flag supprime" -ForegroundColor Green
}

if (Test-Path "$BackendInstancePath\installed.flag") {
    Remove-Item "$BackendInstancePath\installed.flag" -Force
    Write-Host "    OK backend/instance/installed.flag supprime" -ForegroundColor Green
}

Write-Host "  - Suppression des bases de donnees de test" -ForegroundColor Gray

$testDatabases = @(
    "$InstancePath\*.db",
    "$BackendInstancePath\*.db"
)

foreach ($pattern in $testDatabases) {
    Get-ChildItem $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Host "    OK $($_.Name) supprime" -ForegroundColor Green
    }
}

Write-Host ""

# Etape 2: Verification de l'environnement
Write-Host "[2/5] Verification de l'environnement..." -ForegroundColor Yellow

if (-not (Test-Path "$ProjectRoot\.venv")) {
    Write-Host "  ERREUR Environnement virtuel Python non trouve!" -ForegroundColor Red
    Write-Host "    Creez-le avec: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "  OK Environnement virtuel Python detecte" -ForegroundColor Green

# Activer l'environnement virtuel
$ActivateScript = "$ProjectRoot\.venv\Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    & $ActivateScript
    Write-Host "  OK Environnement virtuel active" -ForegroundColor Green
} else {
    Write-Host "  ERREUR Script d'activation non trouve!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Etape 3: Verification des dependances
Write-Host "[3/5] Verification des dependances Python..." -ForegroundColor Yellow

$RequiredPackages = @("flask", "sqlalchemy", "werkzeug")
$MissingPackages = @()

foreach ($package in $RequiredPackages) {
    $installed = python -c "import $package; print('OK')" 2>&1
    if ($installed -like "*OK*") {
        Write-Host "  OK $package installe" -ForegroundColor Green
    } else {
        Write-Host "  ERREUR $package manquant" -ForegroundColor Red
        $MissingPackages += $package
    }
}

if ($MissingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "  Installation des dependances manquantes..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    Write-Host "  OK Dependances installees" -ForegroundColor Green
}

Write-Host ""

# Etape 4: Verification de la structure du projet
Write-Host "[4/5] Verification de la structure du projet..." -ForegroundColor Yellow

$RequiredDirs = @(
    "backend\src",
    "frontend\static",
    "frontend\templates",
    "instance"
)

foreach ($dir in $RequiredDirs) {
    $path = "$ProjectRoot\$dir"
    if (Test-Path $path) {
        Write-Host "  OK $dir" -ForegroundColor Green
    } else {
        Write-Host "  ERREUR $dir manquant!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Etape 5: Instructions de test
Write-Host "[5/5] Preparation terminee!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PRET POUR LE TEST DU WIZARD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Demarrage du serveur Flask..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Commande: " -NoNewline -ForegroundColor Gray
Write-Host "python run.py" -ForegroundColor White
Write-Host ""

Write-Host "Une fois le serveur demarre:" -ForegroundColor Cyan
Write-Host "  1. Ouvrez votre navigateur" -ForegroundColor White
Write-Host "  2. Accedez a: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000/" -ForegroundColor Yellow
Write-Host "  3. Suivez les etapes du wizard:" -ForegroundColor White
Write-Host ""
Write-Host "     -> Choisir la langue (FR ou EN)" -ForegroundColor Gray
Write-Host "     -> Bienvenue" -ForegroundColor Gray
Write-Host "     -> Verification des prerequis" -ForegroundColor Gray
Write-Host "     -> Configuration de la base de donnees" -ForegroundColor Gray
Write-Host "       • SQLite (recommande pour test)" -ForegroundColor DarkGray
Write-Host "       • MySQL ou PostgreSQL" -ForegroundColor DarkGray
Write-Host "     -> Creation du compte administrateur" -ForegroundColor Gray
Write-Host "     -> Resume et finalisation" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  POINTS A VERIFIER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "OK Fil d'Ariane (Breadcrumb):" -ForegroundColor Yellow
Write-Host "  - Les etapes terminees affichent un OK" -ForegroundColor White
Write-Host "  - Les etapes terminees sont cliquables" -ForegroundColor White
Write-Host "  - L'etape active est en bleu" -ForegroundColor White
Write-Host "  - Les etapes futures sont grisees" -ForegroundColor White
Write-Host ""

Write-Host "OK Base de donnees SQLite:" -ForegroundColor Yellow
Write-Host "  - Test de connexion cree les tables" -ForegroundColor White
Write-Host "  - Fichier cree dans: instance/x-filamenta_python.db" -ForegroundColor White
Write-Host ""

Write-Host "OK Compte administrateur:" -ForegroundColor Yellow
Write-Host "  - Validation du mot de passe" -ForegroundColor White
Write-Host "  - Messages d'erreur en francais si langue FR" -ForegroundColor White
Write-Host ""

Write-Host "OK Finalisation:" -ForegroundColor Yellow
Write-Host "  - Creation de l'admin reussie" -ForegroundColor White
Write-Host "  - Redirection vers la page de login" -ForegroundColor White
Write-Host "  - Login fonctionne avec les credentials" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Pause avant de demarrer
Write-Host "Appuyez sur ENTREE pour demarrer le serveur Flask..." -ForegroundColor Yellow
$null = Read-Host

# Demarrer le serveur
Write-Host ""
Write-Host "Demarrage du serveur en cours..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $ProjectRoot
python run.py

