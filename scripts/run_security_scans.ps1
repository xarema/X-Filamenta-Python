# Security Scanners Execution Script
# Runs all security checks and generates a report
# Version: 1.0.0
# Date: 2025-12-30

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$reportFile = "Analysis_reports\2025-12-30_$timestamp`_security-scan-results.md"

# Banner
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " X-Filamenta-Python - Security Scan Suite" -ForegroundColor Cyan
Write-Host " Running: Bandit, Safety, pip-audit" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project root
Set-Location "D:\xarema\X-Filamenta-Python"

# Results storage
$results = @{
    Bandit = @{ Status = ""; Output = ""; Issues = 0 }
    Safety = @{ Status = ""; Output = ""; Issues = 0 }
    PipAudit = @{ Status = ""; Output = ""; Issues = 0 }
}

# Scan 1: Bandit
Write-Host "🔍 Running Bandit (Python Security Linter)..." -ForegroundColor Cyan

try {
    $banditOutput = & .\.venv\Scripts\bandit.exe -r backend\src -ll -f text 2>&1
    $results.Bandit.Output = $banditOutput -join "`n"

    if ($LASTEXITCODE -eq 0) {
        $results.Bandit.Status = "✅ PASS"
        $results.Bandit.Issues = 0
        Write-Host "   ✅ Bandit: No high/medium severity issues found" -ForegroundColor Green
    } else {
        $results.Bandit.Status = "⚠️ ISSUES FOUND"
        # Count issues from output
        $issueCount = ($banditOutput | Select-String "Issue:").Count
        $results.Bandit.Issues = $issueCount
        Write-Host "   ⚠️ Bandit: $issueCount issue(s) found" -ForegroundColor Yellow
    }
}
catch {
    $results.Bandit.Status = "❌ ERROR"
    $results.Bandit.Output = "Error running Bandit: $_"
    Write-Host "   ❌ Bandit: Error occurred" -ForegroundColor Red
}

Write-Host ""

# Scan 2: Safety
Write-Host "🔍 Running Safety (Dependency Vulnerability Check)..." -ForegroundColor Cyan

try {
    $safetyOutput = & .\.venv\Scripts\safety.exe check --json 2>&1 | Out-String
    $results.Safety.Output = $safetyOutput

    # Try to parse JSON
    try {
        $safetyJson = $safetyOutput | ConvertFrom-Json
        $vulnCount = $safetyJson.vulnerabilities.Count

        if ($vulnCount -eq 0) {
            $results.Safety.Status = "✅ PASS"
            $results.Safety.Issues = 0
            Write-Host "   ✅ Safety: No vulnerabilities found" -ForegroundColor Green
        } else {
            $results.Safety.Status = "⚠️ VULNERABILITIES"
            $results.Safety.Issues = $vulnCount
            Write-Host "   ⚠️ Safety: $vulnCount vulnerabilities found" -ForegroundColor Yellow
        }
    }
    catch {
        # JSON parsing failed, check text output
        if ($safetyOutput -like "*0 vulnerabilities found*") {
            $results.Safety.Status = "✅ PASS"
            $results.Safety.Issues = 0
            Write-Host "   ✅ Safety: No vulnerabilities found" -ForegroundColor Green
        } else {
            $results.Safety.Status = "⚠️ CHECK OUTPUT"
            Write-Host "   ⚠️ Safety: Check output for details" -ForegroundColor Yellow
        }
    }
}
catch {
    $results.Safety.Status = "❌ ERROR"
    $results.Safety.Output = "Error running Safety: $_"
    Write-Host "   ❌ Safety: Error occurred" -ForegroundColor Red
}

Write-Host ""

# Scan 3: pip-audit
Write-Host "🔍 Running pip-audit (CVE Scanner)..." -ForegroundColor Cyan

try {
    $pipAuditOutput = & .\.venv\Scripts\pip-audit.exe 2>&1 | Out-String
    $results.PipAudit.Output = $pipAuditOutput

    if ($LASTEXITCODE -eq 0 -or $pipAuditOutput -like "*No known vulnerabilities found*") {
        $results.PipAudit.Status = "✅ PASS"
        $results.PipAudit.Issues = 0
        Write-Host "   ✅ pip-audit: No known vulnerabilities found" -ForegroundColor Green
    } else {
        # Count vulnerabilities
        $vulnCount = ($pipAuditOutput | Select-String "Found \d+ known").Matches.Groups[1].Value
        if ($vulnCount) {
            $results.PipAudit.Issues = [int]$vulnCount
        }
        $results.PipAudit.Status = "⚠️ VULNERABILITIES"
        Write-Host "   ⚠️ pip-audit: Vulnerabilities found" -ForegroundColor Yellow
    }
}
catch {
    $results.PipAudit.Status = "❌ ERROR"
    $results.PipAudit.Output = "Error running pip-audit: $_"
    Write-Host "   ❌ pip-audit: Error occurred" -ForegroundColor Red
}

Write-Host ""

# Summary
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " Security Scan Summary" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bandit:    $($results.Bandit.Status) ($($results.Bandit.Issues) issues)" -ForegroundColor $(if ($results.Bandit.Issues -eq 0) { "Green" } else { "Yellow" })
Write-Host "Safety:    $($results.Safety.Status) ($($results.Safety.Issues) issues)" -ForegroundColor $(if ($results.Safety.Issues -eq 0) { "Green" } else { "Yellow" })
Write-Host "pip-audit: $($results.PipAudit.Status) ($($results.PipAudit.Issues) issues)" -ForegroundColor $(if ($results.PipAudit.Issues -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

$totalIssues = $results.Bandit.Issues + $results.Safety.Issues + $results.PipAudit.Issues

if ($totalIssues -eq 0) {
    Write-Host "✅ ALL SECURITY SCANS PASSED - No critical issues found" -ForegroundColor Green
    $overallStatus = "✅ PASS"
} elseif ($totalIssues -le 5) {
    Write-Host "⚠️ MINOR ISSUES FOUND - Review recommended ($totalIssues total)" -ForegroundColor Yellow
    $overallStatus = "⚠️ REVIEW NEEDED"
} else {
    Write-Host "⚠️ MULTIPLE ISSUES FOUND - Action required ($totalIssues total)" -ForegroundColor Red
    $overallStatus = "⚠️ ACTION REQUIRED"
}

Write-Host ""

# Generate Markdown Report
$reportContent = @"
# Security Scan Results

**Date:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Project:** X-Filamenta-Python
**Version:** 0.1.0-Beta
**Overall Status:** $overallStatus

---

## Summary

| Scanner | Status | Issues Found |
|---------|--------|--------------|
| Bandit | $($results.Bandit.Status) | $($results.Bandit.Issues) |
| Safety | $($results.Safety.Status) | $($results.Safety.Issues) |
| pip-audit | $($results.PipAudit.Status) | $($results.PipAudit.Issues) |
| **TOTAL** | **$overallStatus** | **$totalIssues** |

---

## Detailed Results

### 1. Bandit (Python Security Linter)

**Status:** $($results.Bandit.Status)
**Issues Found:** $($results.Bandit.Issues)

``````
$($results.Bandit.Output)
``````

---

### 2. Safety (Dependency Vulnerability Check)

**Status:** $($results.Safety.Status)
**Issues Found:** $($results.Safety.Issues)

``````
$($results.Safety.Output)
``````

---

### 3. pip-audit (CVE Scanner)

**Status:** $($results.PipAudit.Status)
**Issues Found:** $($results.PipAudit.Issues)

``````
$($results.PipAudit.Output)
``````

---

## Recommendations

$(if ($totalIssues -eq 0) {
@"
✅ **All security scans passed successfully!**

The codebase has no known security vulnerabilities at this time. Continue to:
- Run security scans regularly (weekly/monthly)
- Keep dependencies up to date
- Review security best practices
"@
} elseif ($totalIssues -le 5) {
@"
⚠️ **Minor issues detected - review recommended**

While the issues found are not critical, they should be reviewed and addressed:
1. Review each issue in detail above
2. Determine if fixes are needed before production
3. Document accepted risks if issues are known/acceptable
4. Plan remediation for next release if not urgent
"@
} else {
@"
⚠️ **Multiple issues detected - action required**

Several security issues have been identified:
1. **Review all issues immediately**
2. **Prioritize fixes** based on severity
3. **Update vulnerable dependencies** where possible
4. **Document workarounds** for known issues
5. **Re-run scans** after fixes to verify
6. **Consider delaying deployment** until critical issues are resolved
"@
})

---

**Report Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Scan Duration:** ~1 minute
**Next Scan:** Schedule monthly security audits
"@

# Save report
$reportContent | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "📄 Report saved: $reportFile" -ForegroundColor Cyan
Write-Host ""

# Return status
if ($totalIssues -eq 0) {
    exit 0
} else {
    exit 1
}

