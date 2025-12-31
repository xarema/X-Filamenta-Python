# Backup Database Script
# Creates a tar.gz backup of the SQLite database

param(
    [string]$DatabasePath = "instance/dev.db",
    [string]$BackupDir = ".dev_scripts/backups",
    [string]$OutputName = $null
)

# Check if database exists
if (-not (Test-Path $DatabasePath)) {
    Write-Host "ERROR: Database not found at $DatabasePath" -ForegroundColor Red
    exit 1
}

# Create backup filename with timestamp if not provided
if (-not $OutputName) {
    $timestamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss")
    $OutputName = "x-filamenta_backup_$timestamp.tar.gz"
}

$BackupPath = Join-Path $BackupDir $OutputName

# Create backups directory if it doesn't exist
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Created backup directory: $BackupDir" -ForegroundColor Green
}

# Create tar.gz backup
try {
    Write-Host "Creating backup: $BackupPath" -ForegroundColor Cyan

    # Use native tar command (Windows 11+)
    $dbDir = Split-Path $DatabasePath
    $dbFile = Split-Path $DatabasePath -Leaf

    tar.exe -czf $BackupPath -C $dbDir $dbFile

    if ($LASTEXITCODE -eq 0) {
        $FileSize = (Get-Item $BackupPath).Length / 1MB
        Write-Host "Backup created successfully: $BackupPath" -ForegroundColor Green
        Write-Host "Size: $([math]::Round($FileSize, 2)) MB" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Backup creation failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    exit 1
}

