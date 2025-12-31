# Clean Server Script
# Kills processes, removes temporary files, prepares clean environment

param(
    [switch]$Full = $false
)

Write-Host "Cleaning production server..." -ForegroundColor Cyan

# 1. Kill processes using port 5000
Write-Host "Step 1: Freeing port 5000..."
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port5000) {
    Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue |
        ForEach-Object {
            Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    Write-Host "Port 5000 freed" -ForegroundColor Green
}

# 2. Clean temporary files
Write-Host "Step 2: Cleaning temporary files..."
@(
    "instance\dev.db",
    "instance\x-filamenta_python.db",
    "instance\app.db",
    ".env",
    ".env.local"
) | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item $_ -Force -ErrorAction SilentlyContinue
        Write-Host "Removed: $_" -ForegroundColor Yellow
    }
}

# 3. Clean Python caches if --full
if ($Full) {
    Write-Host "Step 3: Cleaning Python caches..."
    Get-ChildItem -Path . -Include "__pycache__" -Recurse -Force |
        ForEach-Object { Remove-Item $_.FullName -Recurse -Force }
    Write-Host "Python caches cleaned" -ForegroundColor Green
}

Write-Host "Cleanup completed!" -ForegroundColor Green
Write-Host "Server ready for clean startup." -ForegroundColor Cyan

