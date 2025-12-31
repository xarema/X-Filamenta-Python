# PowerShell Rules — Windows 11

**Purpose:** PowerShell and Windows-specific command rules (auto-loaded + reference)  
**File:** `.github/powershell.instructions.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder: AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 

**Metadata:**
- Status: Stable
- Classification: Internal
- Auto-loaded: Context-dependent

---

## 1) Mandatory Environment

- **Shell:** PowerShell (Windows 11)
- **Path separator:** `\` (Windows paths)
- **Chain commands with:** `;` or new lines (**NOT** `&&`)
- **Use PowerShell pipeline** objects and cmdlets

---

## 2) Absolute Prohibitions (Linux-Only Commands)

**NEVER suggest or use:**
- `head`, `tail`, `grep`, `sed`, `awk`, `cut`, `tr`, `xargs`
- `ls`, `cat`, `rm`, `cp`, `mv`, `touch` (use PowerShell equivalents)
- `find` (use `Get-ChildItem -Recurse`)
- `export`, `which`, `chmod`, `chown`
- `curl | bash` style commands

**If user pastes such commands, convert them to PowerShell equivalents.**

---

## 3) Standard Equivalents

### 3.1 Files / Folders

| Linux Command | PowerShell Equivalent |
|---------------|----------------------|
| `ls` | `Get-ChildItem` (alias: `gci`, `ls`) |
| `pwd` | `Get-Location` (alias: `pwd`) |
| `cd <path>` | `Set-Location <path>` (alias: `cd`) |
| `mkdir <dir>` | `New-Item -ItemType Directory -Path <dir>` |
| `touch <file>` | `New-Item -ItemType File -Path <file>` |
| `cp <src> <dst>` | `Copy-Item <src> <dst> -Recurse -Force` |
| `mv <src> <dst>` | `Move-Item <src> <dst> -Force` |
| `rm <path>` | `Remove-Item <path> -Recurse -Force` |
| `test -e <path>` | `Test-Path <path>` |

**Examples:**

```powershell
# List files
Get-ChildItem

# List files recursively
Get-ChildItem -Recurse

# Create directory
New-Item -ItemType Directory -Path "backend\src\services"

# Create file
New-Item -ItemType File -Path "README.md"

# Copy folder
Copy-Item "old_folder" "new_folder" -Recurse -Force

# Delete file
Remove-Item "temp. txt" -Force

# Check if file exists
Test-Path "config.json"
```

### 3.2 Text Output / Filtering

| Linux Command | PowerShell Equivalent |
|---------------|----------------------|
| `cat <file>` | `Get-Content <file>` |
| `head -n 20 <file>` | `Get-Content <file> | Select-Object -First 20` |
| `tail -n 40 <file>` | `Get-Content <file> | Select-Object -Last 40` |
| `tail -f <file>` | `Get-Content <file> -Tail 40 -Wait` |
| `grep "pattern" <file>` | `Select-String -Pattern "pattern" <file>` |
| `grep -E "A|B"` | `Select-String -Pattern "A|B"` |

**Examples:**

```powershell
# Read file
Get-Content "README.md"

# First 20 lines (head)
Get-Content "app.log" | Select-Object -First 20

# Last 40 lines (tail)
Get-Content "app.log" | Select-Object -Last 40

# Follow file (tail -f)
Get-Content "app.log" -Tail 40 -Wait

# Search text (grep)
Select-String -Pattern "ERROR" "app.log"

# Search from pipeline
Get-Process 2>&1 | Select-String -Pattern "python"

# Multiple patterns (grep -E)
Get-Content "app.log" | Select-String -Pattern "ERROR|WARN|CRITICAL"

# Print only matched lines
Get-Content "app. log" | Select-String -Pattern "ERROR" | ForEach-Object { $_.Line }
```

### 3.3 Processes

| Linux Command | PowerShell Equivalent |
|---------------|----------------------|
| `ps aux` | `Get-Process` |
| `ps aux | grep python` | `Get-Process | Where-Object {$_.Name -like "*python*"}` |
| `kill <pid>` | `Stop-Process -Id <pid> -Force` |
| `killall python` | `Get-Process python* | Stop-Process -Force` |

**Examples:**

```powershell
# List all processes
Get-Process

# Find Python processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Kill process by ID
Stop-Process -Id 1234 -Force

# Kill all Python processes
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 3.4 Networking

| Linux Command | PowerShell Equivalent |
|---------------|----------------------|
| `wget <url>` | `Invoke-WebRequest <url> -OutFile <file>` |
| `curl <url>` | `Invoke-RestMethod <url>` |
| `netstat -an` | `Get-NetTCPConnection` |

**Examples:**

```powershell
# Download file
Invoke-WebRequest "https://example.com/file.zip" -OutFile "file.zip"

# GET JSON API
$response = Invoke-RestMethod "https://api.example.com/users"

# Check port usage
Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 5000}
```

### 3.5 Archives

| Linux Command | PowerShell Equivalent |
|---------------|----------------------|
| `zip -r archive.zip folder/` | `Compress-Archive -Path folder -DestinationPath archive.zip -Force` |
| `unzip archive.zip` | `Expand-Archive -Path archive.zip -DestinationPath folder -Force` |

**Examples:**

```powershell
# Create ZIP
Compress-Archive -Path "backend" -DestinationPath "backup.zip" -Force

# Extract ZIP
Expand-Archive -Path "backup.zip" -DestinationPath "restore" -Force
```

### 3.6 JSON / Objects

```powershell
# Parse JSON file
$data = Get-Content "config.json" | ConvertFrom-Json

# Access property
$data.version

# Convert object to JSON
$obj = @{ name = "Test"; version = "1.0.0" }
$obj | ConvertTo-Json -Depth 10

# Save to file
$obj | ConvertTo-Json -Depth 10 | Set-Content "output.json"
```

---

## 4) PowerShell-Specific Rules

### 4.1 Environment Variables

```powershell
# Set for current session
$env:VAR_NAME = "value"

# Get variable
$env:VAR_NAME

# List all
Get-ChildItem Env: 
```

### 4.2 Output

- Use `Write-Host` **only** for UX messages
- Prefer returning objects/strings for pipeline

```powershell
# ❌ BAD: Write-Host breaks pipeline
function Get-User {
  Write-Host "User: John"
}

# ✅ GOOD: Return object
function Get-User {
  return @{ Name = "John"; Email = "john@example.com" }
}
```

### 4.3 Error Handling

**Capture errors with `2>&1` and pipe to `Select-String`:**

```powershell
# Capture all output (stdout + stderr)
.\. venv\Scripts\python.exe app.py 2>&1 | Select-String -Pattern "ERROR|WARN"
```

### 4.4 String Quotes

- **Double quotes (`"`):** For interpolation
- **Single quotes (`'`):** For literals

```powershell
$name = "World"
Write-Host "Hello, $name"   # Output: Hello, World
Write-Host 'Hello, $name'   # Output: Hello, $name
```

### 4.5 Line Continuation

**Avoid backtick (`` ` ``) unless necessary; prefer parentheses:**

```powershell
# ❌ AVOID: Backtick continuation
Get-ChildItem -Path "C:\Projects" `
  -Filter "*.py" `
  -Recurse

# ✅ BETTER: Natural break in pipeline
Get-ChildItem -Path "C:\Projects" -Filter "*.py" -Recurse |
  Where-Object { $_.Length -gt 1KB }
```

---

## 5) Python Execution (Windows venv-friendly)

### 5.1 Always Use `.venv` Interpreter

**NEVER use `python` directly (not on PATH in Windows by default).**

**Correct commands:**

```powershell
# Run script
. \.venv\Scripts\python. exe backend\src\app.py

# Run module
.\.venv\Scripts\python.exe -m pytest

# Install dependencies
.\.venv\Scripts\pip.exe install -r requirements.txt

# Ruff (linter)
.\.venv\Scripts\ruff. exe check . 

# Mypy (type checker)
.\.venv\Scripts\mypy.exe backend/src
```

### 5.2 Activate venv (Optional)

**If you prefer, activate venv first:**

```powershell
# Activate
.\.venv\Scripts\Activate.ps1

# Now you can use python/pip directly
python --version
pip list
pytest

# Deactivate
deactivate
```

---

## 6) Server Kill Commands (Critical)

### 6.1 Kill All Python Processes

```powershell
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 6.2 Kill Any Python Variant

```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 6.3 Kill by Port

```powershell
# Find process using port 5000
$processId = (Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue).OwningProcess

# Kill it
if ($processId) {
  Stop-Process -Id $processId -Force
}
```

### 6.4 One-Liner (All Servers)

```powershell
Get-Process python. exe, waitress -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue ; Write-Host "All servers killed"
```

### 6.5 Verification

```powershell
# Check no Python processes running
Get-Process python.exe -ErrorAction SilentlyContinue | Measure-Object

# Check port 5000 is free
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
# If nothing displayed = port free
```

---

## 7) Command Formatting Guidelines

### 7.1 For Copilot Output

- Provide commands as **PowerShell** blocks, one per line, or chained with `;`
- Always use Windows paths (e.g., `D:\xarema\... `) and quote paths with spaces
- If admin required, explicitly say so and provide: 
  ```powershell
  Start-Process PowerShell -Verb RunAs
  ```

### 7.2 Example Conversions

**Linux:**
```bash
python test.py 2>&1 | head -20
```

**PowerShell:**
```powershell
. \.venv\Scripts\python. exe test.py 2>&1 | Select-Object -First 20
```

---

**Linux:**
```bash
cat app.log | tail -40
```

**PowerShell:**
```powershell
Get-Content app.log | Select-Object -Last 40
```

---

**Linux:**
```bash
ps aux | grep -E "python|waitress" | awk '{print $2}' | xargs kill -9
```

**PowerShell:**
```powershell
Get-Process python*, waitress -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## 8) Common Workflows

### 8.1 Clean Start (Development)

```powershell
# 1. Kill all servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Clean database (if needed)
Remove-Item "instance\*. db" -Force -ErrorAction SilentlyContinue

# 3. Activate venv (optional)
.\.venv\Scripts\Activate.ps1

# 4. Run migrations (if needed)
.\.venv\Scripts\flask.exe db upgrade

# 5. Start dev server
.\.venv\Scripts\python.exe backend\src\app.py
```

### 8.2 Testing Workflow

```powershell
# 1. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Run linters
.\.venv\Scripts\ruff.exe check . 
.\.venv\Scripts\ruff.exe format --check . 
.\.venv\Scripts\mypy.exe backend/src

# 3. Run tests
.\.venv\Scripts\pytest.exe -v

# 4. Check logs for errors
Get-Content "logs\app.log" | Select-String -Pattern "ERROR|CRITICAL"
```

### 8.3 Production Launch

```powershell
# 1. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Verify port free
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue

# 3. Start production server
.\.venv\Scripts\python.exe run_prod.py

# 4. Monitor logs (separate terminal)
Get-Content "logs\app.log" -Tail 40 -Wait
```

---

## 9) Troubleshooting

### 9.1 Port Already in Use

```powershell
# Find what's using port 5000
Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess, State

# Kill that process
Stop-Process -Id <PID> -Force
```

### 9.2 Process Won't Die

```powershell
# More aggressive kill
Get-Process python.exe | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Get-Process python.exe -ErrorAction SilentlyContinue
```

### 9.3 venv Not Recognized

```powershell
# Full path to Python
& "D:\xarema\X-Filamenta-Python\. venv\Scripts\python.exe" --version

# Recreate venv if corrupted
Remove-Item ". venv" -Recurse -Force
py -m venv .venv
. \. venv\Scripts\pip.exe install -r requirements.txt
```

---

## 10) Quick Reference Table

| Task | Command |
|------|---------|
| **Kill all Python** | `Get-Process python.exe | Stop-Process -Force` |
| **Check port 5000** | `Get-NetTCPConnection -LocalPort 5000` |
| **Kill by PID** | `Stop-Process -Id <PID> -Force` |
| **Run dev server** | `.\.venv\Scripts\python.exe backend\src\app.py` |
| **Run tests** | `.\.venv\Scripts\pytest.exe` |
| **Lint** | `.\.venv\Scripts\ruff.exe check .` |
| **Format check** | `.\.venv\Scripts\ruff.exe format --check .` |
| **Type check** | `.\.venv\Scripts\mypy.exe backend/src` |
| **Tail logs** | `Get-Content "app.log" -Tail 40 -Wait` |
| **Search logs for errors** | `Get-Content "app.log" | Select-String "ERROR"` |

---

## 11) PowerShell Profile (Optional)

**Add to `$PROFILE` for quick access:**

```powershell
# Create/edit profile
notepad $PROFILE

# Add functions: 
function Kill-Servers {
    Get-Process python.exe, waitress -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "All servers killed" -ForegroundColor Green
}

function Start-DevServer {
    Kill-Servers
    .\.venv\Scripts\python.exe backend\src\app.py
}

function Start-ProdServer {
    Kill-Servers
    .\.venv\Scripts\python.exe run_prod.py
}

# Usage:
# Kill-Servers
# Start-DevServer
# Start-ProdServer
```

---

## 12) Don'ts

- ❌ Use `&&` for chaining (use `;` or `if ($?)`)
- ❌ Use Linux commands (`grep`, `tail`, etc.)
- ❌ Use `python` directly (use `.\. venv\Scripts\python.exe`)
- ❌ Forget `-ErrorAction SilentlyContinue` when expecting failures
- ❌ Use backticks for line continuation (prefer natural breaks)

---

**See Also:**
- `.github/copilot-instructions.md` — General project rules
- `.github/python.instructions.md` — Python/Flask rules
- `.github/workflow-rules.md` — Workflow process