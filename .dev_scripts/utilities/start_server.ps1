# Start Server Script
# Starts the production server and displays logs in real-time

param(
    [switch]$NoOpen = $false
)

Write-Host "Starting production server..." -ForegroundColor Cyan

# Check that venv exists
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found at .\.venv" -ForegroundColor Red
    exit 1
}

# Kill previous processes on port 5000
Write-Host "Cleaning port 5000..."
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port5000) {
    Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue |
        ForEach-Object {
            Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
        }
}

# Start the server
Write-Host "Launching server on http://localhost:5000" -ForegroundColor Green
.\.venv\Scripts\python.exe run_prod.py

Write-Host "Server stopped." -ForegroundColor Yellow

