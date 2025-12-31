<#
.SYNOPSIS
    Pre-commit Hook for Code Quality (PowerShell Version)

.DESCRIPTION
    Enforce code quality standards before commit. 
    Runs linting, formatting, type checking, i18n validation, and tests. 
    
    Purpose: Automated code quality checks
    File: scripts/hooks/pre-commit.ps1 | Repository: X-Filamenta-Python
    
    Created: 2025-12-30
    Last modified (Git): TBD | Commit: TBD
    
    Distributed by: XAREMA | Coder: AleGabMar
    App version: 0.0.1-Alpha | File version: 1.0.0
    
    License: AGPL-3.0-or-later
    SPDX-License-Identifier: AGPL-3.0-or-later
    
    Copyright (c) 2025 XAREMA.  All rights reserved.
    
    Metadata:
    - Status:  Stable
    - Classification: Internal

. NOTES
    Installation (NOT RECOMMENDED - use pre-commit package instead):
        Copy-Item scripts\hooks\pre-commit.ps1 . git\hooks\pre-commit
    
    Better option (cross-platform):
        pip install pre-commit
        pre-commit install
    
    Manual test:
        .\scripts\hooks\pre-commit.ps1

.EXAMPLE
    # Run manually
    .\scripts\hooks\pre-commit.ps1
#>

#Requires -Version 5.1

# Stop on errors
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "🔍 Running pre-commit checks..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# ---- Check if venv exists ----
if (-not (Test-Path ". venv")) {
    Write-Host "❌ Virtual environment not found (.venv/)" -ForegroundColor Red
    Write-Host "   Create it with:  python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# ---- Python Linting (Ruff) ----
Write-Host "📝 Checking code with Ruff..." -ForegroundColor Yellow
try {
    & .\. venv\Scripts\ruff. exe check . 
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Ruff linting passed" -ForegroundColor Green
    } else {
        throw "Ruff linting failed"
    }
} catch {
    Write-Host "   ❌ Ruff linting failed" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# ---- Python Formatting (Ruff) ----
Write-Host "🎨 Checking code formatting with Ruff..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\ruff.exe format --check . 
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Code formatting passed" -ForegroundColor Green
    } else {
        throw "Code formatting issues found"
    }
} catch {
    Write-Host "   ❌ Code formatting issues found" -ForegroundColor Red
    Write-Host "      Fix with: . \.venv\Scripts\ruff.exe format ." -ForegroundColor Yellow
    $ErrorCount++
}
Write-Host ""

# ---- Type Checking (Mypy) ----
Write-Host "🔍 Running type checker (Mypy)..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\mypy. exe backend/src
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Type checking passed" -ForegroundColor Green
    } else {
        throw "Type checking failed"
    }
} catch {
    Write-Host "   ❌ Type checking failed" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# ---- i18n Translation Check ----
Write-Host "🌐 Checking i18n translations..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\python. exe scripts\utils\check_i18n.py --strict
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ i18n validation passed" -ForegroundColor Green
    } else {
        throw "i18n validation failed"
    }
} catch {
    Write-Host "   ❌ i18n validation failed" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# ---- Tests (Pytest) ----
Write-Host "🧪 Running tests (pytest)..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\pytest.exe --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ All tests passed" -ForegroundColor Green
    } else {
        throw "Tests failed"
    }
} catch {
    Write-Host "   ❌ Tests failed" -ForegroundColor Red
    $ErrorCount++
}
Write-Host ""

# ---- Summary ----
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "✅ All pre-commit checks passed!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "❌ $ErrorCount check(s) failed" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Fix the issues above before committing." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  To bypass this hook (NOT RECOMMENDED):" -ForegroundColor Yellow
    Write-Host "   git commit --no-verify -m `"message`"" -ForegroundColor Yellow
    exit 1
}