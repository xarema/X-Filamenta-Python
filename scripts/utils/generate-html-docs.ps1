<#
Purpose: Generate complete HTML documentation from Markdown files
Description: Converts all project documentation to navigable HTML

File: scripts/utils/generate-html-docs.ps1 | Repository: X-Filamenta-Python
Created: 2025-12-28T21:45:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
#>

# Configuration
$ProjectRoot = "D:\xarema\X-Filamenta-Python"
$DocsRoot = Join-Path $ProjectRoot "docs"
$HtmlOutput = Join-Path $DocsRoot "HTML"
$StyleFile = Join-Path $HtmlOutput "style.css"

Write-Host "=== Generating HTML Documentation ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot" -ForegroundColor Gray
Write-Host "Output: $HtmlOutput" -ForegroundColor Gray
Write-Host ""

# Create output directory if not exists
if (-not (Test-Path $HtmlOutput)) {
    New-Item -ItemType Directory -Path $HtmlOutput -Force | Out-Null
}

# Function to convert markdown title to HTML-safe filename
function Get-HtmlFileName {
    param([string]$MdPath)

    $relativePath = $MdPath.Replace($DocsRoot, "").TrimStart("\")
    $htmlPath = $relativePath -replace "\.md$", ".html"
    $htmlPath = $htmlPath -replace "\\", "-"
    $htmlPath = $htmlPath -replace "^-", ""

    return $htmlPath
}

# Function to extract title from markdown
function Get-MarkdownTitle {
    param([string]$FilePath)

    $content = Get-Content $FilePath -Raw

    # Try to find first # heading
    if ($content -match "(?m)^#\s+(.+)$") {
        return $matches[1].Trim()
    }

    # Fallback to filename
    return [System.IO.Path]::GetFileNameWithoutExtension($FilePath)
}

# Function to convert markdown to HTML
function ConvertTo-Html {
    param(
        [string]$MdPath,
        [string]$Title,
        [string]$RelativeStylePath = "style.css"
    )

    $content = Get-Content $MdPath -Raw -Encoding UTF8

    # Simple markdown conversion (basic support)
    # Headers
    $content = $content -replace "(?m)^### (.+)$", "<h3>`$1</h3>"
    $content = $content -replace "(?m)^## (.+)$", "<h2>`$1</h2>"
    $content = $content -replace "(?m)^# (.+)$", "<h1>`$1</h1>"

    # Code blocks with language
    $content = $content -replace "(?s)```powershell\s*\n(.*?)\n```", '<pre><code class="language-powershell">$1</code></pre>'
    $content = $content -replace "(?s)```python\s*\n(.*?)\n```", '<pre><code class="language-python">$1</code></pre>'
    $content = $content -replace "(?s)```bash\s*\n(.*?)\n```", '<pre><code class="language-bash">$1</code></pre>'
    $content = $content -replace "(?s)```json\s*\n(.*?)\n```", '<pre><code class="language-json">$1</code></pre>'
    $content = $content -replace "(?s)```\s*\n(.*?)\n```", '<pre><code>$1</code></pre>'

    # Inline code
    $content = $content -replace "``([^`]+)``", "<code>`$1</code>"
    $content = $content -replace "`([^`]+)`", "<code>`$1</code>"

    # Bold and italic
    $content = $content -replace "\*\*(.+?)\*\*", "<strong>`$1</strong>"
    $content = $content -replace "\*(.+?)\*", "<em>`$1</em>"

    # Links
    $content = $content -replace "\[(.+?)\]\((.+?)\)", '<a href="$2">$1</a>'

    # Lists
    $content = $content -replace "(?m)^- (.+)$", "<li>`$1</li>"
    $content = $content -replace "(?m)^(\d+)\. (.+)$", "<li>`$2</li>"

    # Blockquotes
    $content = $content -replace "(?m)^> (.+)$", "<blockquote>`$1</blockquote>"

    # Paragraphs (simple line breaks)
    $content = $content -replace "(?m)^([^<\n].*)$", "<p>`$1</p>"

    # Clean up multiple paragraph tags
    $content = $content -replace "</p>\s*<p>", "</p>`n<p>"

    # HTML template
    $html = @"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$Title - X-Filamenta Documentation</title>
    <link rel="stylesheet" href="$RelativeStylePath">
</head>
<body>
    <header>
        <h1>📚 X-Filamenta Documentation</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="all-pages.html">All Pages</a>
            <a href="analysis-reports.html">Analysis Reports</a>
        </nav>
    </header>

    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-section">
                <div class="sidebar-title">Quick Access</div>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="guides-quickstart.html">Quick Start</a></li>
                    <li><a href="deployment-DEPLOYMENT.html">Deployment</a></li>
                    <li><a href="features-README.html">Features</a></li>
                    <li><a href="security-README.html">Security</a></li>
                    <li><a href="troubleshooting-README.html">Troubleshooting</a></li>
                </ul>
            </div>
        </aside>

        <main class="main">
            $content

            <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e0e0e0;">
                <p style="color: #666; font-size: 0.9rem;">
                    © 2025 XAREMA. Licensed under AGPL-3.0-or-later.
                    <a href="https://github.com/XAREMA" target="_blank">View source</a>
                </p>
            </footer>
        </main>
    </div>
</body>
</html>
"@

    return $html
}

# Get all markdown files
Write-Host "Scanning for markdown files..." -ForegroundColor Yellow
$mdFiles = Get-ChildItem -Path $DocsRoot -Filter "*.md" -Recurse | Where-Object {
    $_.FullName -notlike "*\node_modules\*" -and
    $_.FullName -notlike "*\.git\*" -and
    $_.FullName -notlike "*\HTML\*"
}

Write-Host "Found $($mdFiles.Count) markdown files" -ForegroundColor Green
Write-Host ""

# Convert each file
$convertedCount = 0
foreach ($mdFile in $mdFiles) {
    $title = Get-MarkdownTitle -FilePath $mdFile.FullName
    $htmlFileName = Get-HtmlFileName -MdPath $mdFile.FullName
    $htmlPath = Join-Path $HtmlOutput $htmlFileName

    Write-Host "Converting: $($mdFile.Name) -> $htmlFileName" -ForegroundColor Cyan

    try {
        $htmlContent = ConvertTo-Html -MdPath $mdFile.FullName -Title $title
        $htmlContent | Out-File -FilePath $htmlPath -Encoding UTF8 -Force
        $convertedCount++
    }
    catch {
        Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Conversion Complete ===" -ForegroundColor Green
Write-Host "Converted: $convertedCount files" -ForegroundColor Green
Write-Host "Output directory: $HtmlOutput" -ForegroundColor Gray
Write-Host ""
Write-Host "Open index.html in browser:" -ForegroundColor Yellow
Write-Host "  Start-Process '$HtmlOutput\index.html'" -ForegroundColor White

