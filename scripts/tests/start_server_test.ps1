# Test Server Start

Write-Host "============================================"
Write-Host "TEST DEMARRAGE SERVEUR"
Write-Host "============================================"
Write-Host ""

cd D:\xarema\X-Filamenta-Python

Write-Host "[INFO] Cleaning old DB..."
if (Test-Path "instance\*.db") {
    Remove-Item "instance\*.db" -Force
    Write-Host "[OK] DB cleaned"
}

if (Test-Path ".installed") {
    Remove-Item ".installed" -Force
    Write-Host "[OK] Marker removed"
}

Write-Host ""
Write-Host "[INFO] Starting server..."
Write-Host "[URL] http://127.0.0.1:5000/"
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host ""

.\.venv\Scripts\python.exe run_prod.py

