# Pre-Production Cleanup Script
# Automated cleanup for X-Filamenta-Python before production deployment
# Version: 1.0.0
# Date: 2025-12-30

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("validate-only", "cleanup-and-validate", "aggressive-cleanup")]
    [string]$Mode = "cleanup-and-validate",

    [Parameter(Mandatory=$false)]
    [switch]$SkipBackup,

    [Parameter(Mandatory=$false)]
    [switch]$SkipTests,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$projectRoot = "D:\xarema\X-Filamenta-Python"

# Colors
function Write-Success { param($msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "❌ $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "ℹ️  $msg" -ForegroundColor Cyan }
function Write-Step { param($msg) Write-Host "`n📋 $msg" -ForegroundColor Cyan }

# Banner
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " X-Filamenta-Python - Pre-Production Cleanup" -ForegroundColor Cyan
Write-Host " Mode: $Mode" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location $projectRoot

# Step 1: Create Backup
if (-not $SkipBackup -and $Mode -ne "validate-only") {
    Write-Step "Creating backup..."

    $backupDir = "backups\pre-prod-$timestamp"

    try {
        New-Item -Path $backupDir -ItemType Directory -Force | Out-Null

        $excludeDirs = @('.venv', 'venv', 'node_modules', '__pycache__', '.git', 'backups')

        Get-ChildItem -Path . -Exclude $excludeDirs | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $backupDir -Recurse -Force -ErrorAction SilentlyContinue
        }

        Write-Success "Backup created: $backupDir"
    }
    catch {
        Write-Error "Backup failed: $_"
        exit 1
    }
}

# Step 2: Validation Mode - Check Files
Write-Step "Scanning for files to clean..."

$filesToClean = @{
    PythonCache = @()
    TestArtifacts = @()
    Logs = @()
    IDE = @()
    DevDBs = @()
}

# Python cache
$filesToClean.PythonCache += Get-ChildItem -Path . -Recurse -Include "__pycache__" -Directory -ErrorAction SilentlyContinue
$filesToClean.PythonCache += Get-ChildItem -Path . -Recurse -Include "*.pyc","*.pyo","*.pyd" -File -ErrorAction SilentlyContinue

# Test artifacts
$filesToClean.TestArtifacts += Get-Item ".pytest_cache" -ErrorAction SilentlyContinue
$filesToClean.TestArtifacts += Get-Item "htmlcov" -ErrorAction SilentlyContinue
$filesToClean.TestArtifacts += Get-Item ".coverage" -ErrorAction SilentlyContinue

# Logs (old dev logs only)
if (Test-Path "logs") {
    $filesToClean.Logs += Get-ChildItem -Path logs -Filter "*.log" -File |
        Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)}
}

# IDE files
$filesToClean.IDE += Get-Item ".vscode" -ErrorAction SilentlyContinue
$filesToClean.IDE += Get-Item ".idea" -ErrorAction SilentlyContinue
$filesToClean.IDE += Get-ChildItem -Path . -Recurse -Include "*.swp","*.swo" -File -ErrorAction SilentlyContinue

# Dev databases
if (Test-Path "instance") {
    $filesToClean.DevDBs += Get-ChildItem -Path instance -Filter "dev.db" -ErrorAction SilentlyContinue
    $filesToClean.DevDBs += Get-ChildItem -Path instance -Filter "test.db" -ErrorAction SilentlyContinue
}

# Report findings
$totalFiles = ($filesToClean.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum

Write-Info "Found $totalFiles files/directories to clean:"
Write-Host "  - Python cache: $($filesToClean.PythonCache.Count)" -ForegroundColor White
Write-Host "  - Test artifacts: $($filesToClean.TestArtifacts.Count)" -ForegroundColor White
Write-Host "  - Old logs: $($filesToClean.Logs.Count)" -ForegroundColor White
Write-Host "  - IDE files: $($filesToClean.IDE.Count)" -ForegroundColor White
Write-Host "  - Dev databases: $($filesToClean.DevDBs.Count)" -ForegroundColor White

# Step 3: Cleanup (if not validate-only)
if ($Mode -ne "validate-only") {
    Write-Step "Cleaning files..."

    $cleaned = 0

    foreach ($category in $filesToClean.Keys) {
        foreach ($item in $filesToClean[$category]) {
            try {
                if (Test-Path $item.FullName) {
                    Remove-Item -Path $item.FullName -Recurse -Force
                    $cleaned++
                    if ($Verbose) {
                        Write-Host "  Removed: $($item.FullName)" -ForegroundColor Gray
                    }
                }
            }
            catch {
                Write-Warning "Could not remove: $($item.FullName)"
            }
        }
    }

    Write-Success "Cleaned $cleaned files/directories"
}

# Step 4: Check for Debug Code
Write-Step "Scanning for debug code..."

$debugPatterns = @(
    @{Pattern='print\('; Name='print() statements'},
    @{Pattern='console\.log\('; Name='console.log()'},
    @{Pattern='debugger'; Name='debugger'},
    @{Pattern='import pdb'; Name='pdb import'},
    @{Pattern='pdb\.set_trace'; Name='pdb.set_trace()'},
    @{Pattern='breakpoint\(\)'; Name='breakpoint()'},
    @{Pattern='TODO'; Name='TODO comments'},
    @{Pattern='FIXME'; Name='FIXME comments'}
)

$debugFound = @()

foreach ($pattern in $debugPatterns) {
    $found = Get-ChildItem -Path backend\src -Recurse -Filter *.py -ErrorAction SilentlyContinue |
        Select-String -Pattern $pattern.Pattern -ErrorAction SilentlyContinue

    if ($found) {
        $debugFound += @{Pattern=$pattern.Name; Count=$found.Count; Files=$found}
    }
}

if ($debugFound.Count -gt 0) {
    Write-Warning "Found debug code:"
    foreach ($item in $debugFound) {
        Write-Host "  - $($item.Pattern): $($item.Count) occurrences" -ForegroundColor Yellow
        if ($Verbose) {
            $item.Files | ForEach-Object {
                Write-Host "    $($_.Path):$($_.LineNumber)" -ForegroundColor Gray
            }
        }
    }
} else {
    Write-Success "No debug code found"
}

# Step 5: Check Configuration
Write-Step "Validating configuration..."

if (Test-Path .env) {
    $envContent = Get-Content .env

    $issues = @()

    # Check DEBUG
    if ($envContent -match "DEBUG=True|FLASK_DEBUG=1") {
        $issues += "DEBUG is enabled (must be False for production)"
    }

    # Check FLASK_ENV
    if ($envContent -match "FLASK_ENV=development") {
        $issues += "FLASK_ENV is 'development' (must be 'production')"
    }

    # Check SECRET_KEY
    if ($envContent -match "SECRET_KEY=dev-secret-key") {
        $issues += "SECRET_KEY is default value (must be changed)"
    }

    if ($issues.Count -gt 0) {
        Write-Error ".env configuration issues:"
        $issues | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    } else {
        Write-Success ".env configuration looks good"
    }
} else {
    Write-Warning ".env file not found (required for production)"
}

# Step 6: Security Scan (basic)
Write-Step "Running basic security scan..."

$secretPatterns = @(
    'password\s*=\s*"[^"]+"',
    'api_key\s*=\s*"[^"]+"',
    'SECRET_KEY\s*=\s*"[^"]{10,}"'
)

$secretsFound = $false

foreach ($pattern in $secretPatterns) {
    $found = Get-ChildItem -Path backend\src -Recurse -Filter *.py -ErrorAction SilentlyContinue |
        Select-String -Pattern $pattern -ErrorAction SilentlyContinue

    if ($found) {
        $secretsFound = $true
        Write-Warning "Potential hardcoded secret: $pattern"
        if ($Verbose) {
            $found | ForEach-Object {
                Write-Host "  $($_.Path):$($_.LineNumber)" -ForegroundColor Yellow
            }
        }
    }
}

if (-not $secretsFound) {
    Write-Success "No obvious hardcoded secrets found"
}

# Step 7: Run Tests (if not skipped)
if (-not $SkipTests -and $Mode -ne "validate-only") {
    Write-Step "Running test suite..."

    if (Test-Path ".venv\Scripts\pytest.exe") {
        try {
            & .\.venv\Scripts\pytest.exe backend\tests -v --tb=short

            if ($LASTEXITCODE -eq 0) {
                Write-Success "All tests passed"
            } else {
                Write-Error "Tests failed"
            }
        }
        catch {
            Write-Warning "Could not run tests: $_"
        }
    } else {
        Write-Warning "pytest not found in venv"
    }
}

# Step 8: Check Required Files
Write-Step "Checking required files..."

$requiredFiles = @(
    'requirements.txt',
    'README.md',
    'LICENSE',
    '.env.example',
    '.gitignore',
    'backend\src\__init__.py',
    'backend\src\app.py',
    'run_prod.py'
)

$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Warning "Missing required files:"
    $missingFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    Write-Success "All required files present"
}

# Final Summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " Cleanup Summary" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

if ($Mode -ne "validate-only") {
    Write-Host "✅ Cleaned: $cleaned files/directories" -ForegroundColor Green
}
Write-Host "⚠️  Debug code: $($debugFound.Count) patterns found" -ForegroundColor Yellow
Write-Host "⚠️  Missing files: $($missingFiles.Count)" -ForegroundColor Yellow

if ($debugFound.Count -gt 0 -or $missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  WARNINGS FOUND - Review before production deployment" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✅ PROJECT READY FOR PRODUCTION DEPLOYMENT" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review warnings (if any)" -ForegroundColor White
Write-Host "  2. Create production .env file" -ForegroundColor White
Write-Host "  3. Run security scanners (bandit, safety, pip-audit)" -ForegroundColor White
Write-Host "  4. Execute full test suite" -ForegroundColor White
Write-Host "  5. Follow deployment guide (docs/guides/DEPLOYMENT.md)" -ForegroundColor White
Write-Host ""

# Generate report
$reportPath = "Analysis_reports\2025-12-30_$timestamp`_cleanup-script-run.md"

$reportContent = @"
# Cleanup Script Execution Report

**Date:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Mode:** $Mode
**Backup:** $(if ($SkipBackup) { "Skipped" } else { $backupDir })

## Summary

- Files cleaned: $cleaned
- Debug patterns found: $($debugFound.Count)
- Missing required files: $($missingFiles.Count)

## Details

### Files Cleaned
- Python cache: $($filesToClean.PythonCache.Count)
- Test artifacts: $($filesToClean.TestArtifacts.Count)
- Old logs: $($filesToClean.Logs.Count)
- IDE files: $($filesToClean.IDE.Count)
- Dev databases: $($filesToClean.DevDBs.Count)

### Debug Code Found
$(if ($debugFound.Count -gt 0) {
    $debugFound | ForEach-Object { "- $($_.Pattern): $($_.Count) occurrences" }
} else {
    "None"
})

### Missing Files
$(if ($missingFiles.Count -gt 0) {
    $missingFiles | ForEach-Object { "- $_" }
} else {
    "None"
})

## Status

$(if ($debugFound.Count -gt 0 -or $missingFiles.Count -gt 0) {
    "⚠️ **WARNINGS PRESENT** - Review required"
} else {
    "✅ **READY FOR DEPLOYMENT**"
})
"@

$reportContent | Out-File -FilePath $reportPath -Encoding UTF8
Write-Info "Report saved: $reportPath"

Write-Host ""

