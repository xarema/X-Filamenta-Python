<#
.SYNOPSIS
    Check AI Compliance — Vérifie que l'IA a suivi les règles du projet

.DESCRIPTION
    Script de vérification pour détecter les violations des règles AI :
    - Fichiers créés à la racine (au lieu de scripts/)
    - Commandes Linux dans les scripts PowerShell
    - Fichiers sans headers obligatoires
    - Texte hardcodé dans les templates (TODO)

.NOTES
    Purpose: Validation automatique de la conformité AI
    File: scripts/utils/check_ai_compliance.ps1 | Repository: X-Filamenta-Python
    Created: 2025-12-31T00:00:00+00:00
    Last modified (Git): TBD | Commit: TBD

    Distributed by: XAREMA | Coder: AleGabMar
    App version:  0.0.1-Alpha | File version: 1.0.0

    License: AGPL-3.0-or-later
    SPDX-License-Identifier: AGPL-3.0-or-later

    Copyright (c) 2025 XAREMA. All rights reserved.

    Metadata:
    - Status: Stable
    - Classification:  Internal

. EXAMPLE
    .\scripts\utils\check_ai_compliance.ps1

. EXAMPLE
    .\scripts\utils\check_ai_compliance.ps1 -Verbose
#>

[CmdletBinding()]
param()

Write-Host ""
Write-Host "🔍 Vérification de conformité AI..." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# ────────────────────────────────────────────────────────────────────────────
# 1. Vérifier fichiers de test à la racine
# ────────────────────────────────────────────────────────────────────────────

Write-Host "[1/5] Vérification des fichiers de test..." -ForegroundColor Yellow

$rootTestFiles = Get-ChildItem -Path "." -Filter "test_*.py" -File -ErrorAction SilentlyContinue
if ($rootTestFiles) {
  $errors += "Fichiers de test trouvés à la racine (doivent être dans scripts/tests/)"
  Write-Host "  ❌ Fichiers de test à la racine :" -ForegroundColor Red
  $rootTestFiles | ForEach-Object {
    Write-Host "     - $($_.Name)" -ForegroundColor Red
  }
} else {
  Write-Host "  ✅ Aucun fichier de test à la racine" -ForegroundColor Green
}

# ────────────────────────────────────────────────────────────────────────────
# 2. Vérifier fichiers debug à la racine
# ────────────────────────────────────────────────────────────────────────────

Write-Host "[2/5] Vérification des fichiers debug..." -ForegroundColor Yellow

$rootDebugFiles = Get-ChildItem -Path "." -Filter "*debug*.py" -File -ErrorAction SilentlyContinue
if ($rootDebugFiles) {
  $errors += "Fichiers debug trouvés à la racine (doivent être dans scripts/debug/)"
  Write-Host "  ❌ Fichiers debug à la racine :" -ForegroundColor Red
  $rootDebugFiles | ForEach-Object {
    Write-Host "     - $($_.Name)" -ForegroundColor Red
  }
} else {
  Write-Host "  ✅ Aucun fichier debug à la racine" -ForegroundColor Green
}

# ────────────────────────────────────────────────────────────────────────────
# 3. Vérifier commandes Linux dans scripts PowerShell
# ────────────────────────────────────────────────────────────────────────────

Write-Host "[3/5] Vérification des commandes Linux dans PowerShell..." -ForegroundColor Yellow

$linuxCommands = @("grep", "tail", "head", "cat", "\bls\b", "\brm\b", "\bcp\b", "\bmv\b", "touch", "chmod", "chown", "export", "which")
$scriptFiles = Get-ChildItem -Path "scripts" -Filter "*.ps1" -Recurse -File -ErrorAction SilentlyContinue

$linuxViolations = @()

foreach ($file in $scriptFiles) {
  $content = Get-Content $file.FullName -Raw
  foreach ($cmd in $linuxCommands) {
    # Utiliser regex pour éviter faux positifs
    if ($content -match "\b$cmd\b") {
      $linuxViolations += "  - $($file.Name): commande '$cmd'"
    }
  }
}

if ($linuxViolations. Count -gt 0) {
  $errors += "Commandes Linux trouvées dans scripts PowerShell"
  Write-Host "  ❌ Commandes Linux détectées :" -ForegroundColor Red
  $linuxViolations | ForEach-Object { Write-Host $_ -ForegroundColor Red }
} else {
  Write-Host "  ✅ Aucune commande Linux détectée" -ForegroundColor Green
}

# ────────────────────────────────────────────────────────────────────────────
# 4. Vérifier headers dans fichiers Python (scripts/)
# ────────────────────────────────────────────────────────────────────────────

Write-Host "[4/5] Vérification des headers dans fichiers Python..." -ForegroundColor Yellow

$pythonFiles = Get-ChildItem -Path "scripts" -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue
$missingHeaders = @()

foreach ($file in $pythonFiles) {
  $content = Get-Content $file.FullName -Raw

  # Vérifier présence du header minimal
  if ($content -notmatch "Purpose:" -or
    $content -notmatch "Repository:  X-Filamenta-Python" -or
    $content -notmatch "License: AGPL-3.0-or-later") {
    $missingHeaders += "  - $($file. FullName)"
  }
}

if ($missingHeaders.Count -gt 0) {
  $warnings += "Fichiers Python sans header complet détectés"
  Write-Host "  ⚠️  Fichiers sans header complet :" -ForegroundColor DarkYellow
  $missingHeaders | ForEach-Object { Write-Host $_ -ForegroundColor DarkYellow }
} else {
  Write-Host "  ✅ Tous les fichiers Python ont des headers" -ForegroundColor Green
}

# ────────────────────────────────────────────────────────────────────────────
# 5. Vérifier utilisation de `python` au lieu de `.venv\Scripts\python.exe`
# ────────────────────────────────────────────────────────────────────────────

Write-Host "[5/5] Vérification utilisation directe de 'python'..." -ForegroundColor Yellow

$pythonViolations = @()

foreach ($file in $scriptFiles) {
  $content = Get-Content $file.FullName -Raw

  # Chercher "python " sans ". venv"
  if ($content -match "\bpython\s+" -and $content -notmatch "\.venv\\Scripts\\python\.exe") {
    $pythonViolations += "  - $($file.Name): utilise 'python' directement"
  }
}

if ($pythonViolations. Count -gt 0) {
  $errors += "Utilisation directe de 'python' détectée (utiliser .venv\Scripts\python.exe)"
  Write-Host "  ❌ Utilisation directe de 'python' :" -ForegroundColor Red
  $pythonViolations | ForEach-Object { Write-Host $_ -ForegroundColor Red }
} else {
  Write-Host "  ✅ Utilisation correcte de Python (venv)" -ForegroundColor Green
}

# ────────────────────────────────────────────────────────────────────────────
# Résumé final
# ────────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "RÉSUMÉ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
  Write-Host "✅ Aucune violation détectée !" -ForegroundColor Green
  Write-Host "   L'IA a correctement suivi les règles du projet." -ForegroundColor Green
  exit 0
} else {
  if ($errors.Count -gt 0) {
    Write-Host "❌ ERREURS CRITIQUES ($($errors.Count)) :" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    Write-Host ""
  }

  if ($warnings.Count -gt 0) {
    Write-Host "⚠️  AVERTISSEMENTS ($($warnings.Count)) :" -ForegroundColor DarkYellow
    $warnings | ForEach-Object { Write-Host "   - $_" -ForegroundColor DarkYellow }
    Write-Host ""
  }

  Write-Host "Voir les règles dans :" -ForegroundColor Cyan
  Write-Host "  - . github/AI_REMINDER.md" -ForegroundColor Cyan
  Write-Host "  - . github/powershell.instructions.md" -ForegroundColor Cyan
  Write-Host "  - . github/copilot-instructions.md" -ForegroundColor Cyan
  Write-Host ""

  exit 1
}
