# Test Wizard Installation - PowerShell Script (Debug Mode)
#
# Purpose: Automated test script for wizard installation
# Usage: .\scripts\tests\test_wizard_debug.ps1
#
# File: scripts/tests/test_wizard_debug.ps1
# Created: 2025-12-28
# License: AGPL-3.0-or-later

Write-Host "======================================================================"
Write-Host "WIZARD INSTALLATION - TEST DEBUG MODE"
Write-Host "======================================================================"
Write-Host ""

# Step 1: Clean database
Write-Host "[STEP 1] Cleaning database..."
if (Test-Path "instance\*.db") {
    Remove-Item "instance\*.db" -Force
    Write-Host "[OK] Database cleaned"
} else {
    Write-Host "[INFO] No database files to clean"
}
Write-Host ""

# Step 2: Remove installation marker
Write-Host "[STEP 2] Removing installation marker..."
if (Test-Path ".installed") {
    Remove-Item ".installed" -Force
    Write-Host "[OK] Installation marker removed"
} else {
    Write-Host "[INFO] No installation marker found"
}
Write-Host ""

# Step 3: Activate venv and run
Write-Host "[STEP 3] Starting server in DEBUG mode..."
Write-Host ""
Write-Host "Server will start at: http://127.0.0.1:5000/"
Write-Host "Wizard redirect to: http://127.0.0.1:5000/install/"
Write-Host ""
Write-Host "Press Ctrl+C to stop server"
Write-Host ""
Write-Host "======================================================================"
Write-Host ""

# Activate venv and run
.\.venv\Scripts\activate.ps1
python run_prod.py

