# ------------------------------------------------------------------------------
# Purpose: Production server runner for Windows
# Description: Powershell script to run the production server using the venv.
#
# File: run_prod.ps1 | Repository: X-Filamenta-Python
# Created: 2025-12-28T14:24:00+01:00
# Last modified (Git): TBD | Commit: TBD
#
# Distributed by: XAREMA | Coder: AleGabMar
# App version: 0.0.1-Alpha | File version: 0.0.1-Alpha
#
# License: AGPL-3.0-or-later
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (c) 2025 XAREMA. All rights reserved.
#
# Metadata:
# - Status: Stable
# - Classification: Public
# ------------------------------------------------------------------------------

if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "Starting X-Filamenta in Production mode..." -ForegroundColor Cyan
    .\.venv\Scripts\python.exe run_prod.py
} else {
    Write-Host "Error: Virtual environment not found at .\.venv" -ForegroundColor Red
    Write-Host "Please run 'python -m venv .venv' and install requirements first." -ForegroundColor Yellow
    exit 1
}
