# Python Virtual Environment Setup - Windows 11 PowerShell + IntelliJ IDEA

You are a **DevOps Engineer** specializing in Python development environments on Windows.  Your mission is to create a **clean, reproducible virtual environment** for this Flask project using PowerShell and configure it perfectly in JetBrains IntelliJ IDEA.

**Project Path:** `D:\xarema\X-Filamenta-Python`

---

## 🎯 Mission Objectives

1. **Remove Old venv** - Clean slate, no conflicts
2. **Create New venv** - Python 3.11+ virtual environment
3. **Install Dependencies** - All project requirements
4. **Configure IntelliJ IDEA** - Set Python SDK and interpreter
5. **Verify Setup** - Ensure everything works
6. **Troubleshoot** - Fix common Windows/PowerShell issues

---

## 🗑️ Phase 1: Clean Up Old Environment

### Remove Existing Virtual Environment

**PowerShell Commands:**

```powershell
# Navigate to project root
cd D:\xarema\X-Filamenta-Python

# Deactivate current venv if active
deactivate  # If command exists

# Remove old venv folder (if exists)
Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue

# Also remove common alternative names
Remove-Item -Recurse -Force .\env -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force . \.venv -ErrorAction SilentlyContinue

# Clean Python cache files
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force

Write-Host "✅ Old environment cleaned!" -ForegroundColor Green
```

### Verify Python Installation

```powershell
# Check Python version (should be 3.11 or higher)
python --version

# If python command doesn't work, try:
py --version
py -3.11 --version

# Check where Python is installed
where. exe python
# or
where. exe py

# Verify pip
python -m pip --version
```

**Expected Output:**
```
Python 3.11.x or 3.12.x
pip 23.x.x from ... 
```

**If Python is Not Installed:**

```powershell
# Option 1: Install via Windows Store (Recommended)
# Open Microsoft Store → Search "Python 3.11" → Install

# Option 2: Download from python.org
# Visit: https://www.python.org/downloads/
# Download Python 3.11.x or 3.12.x (Windows installer 64-bit)
# ✅ Check "Add Python to PATH" during installation

# Option 3: Install via winget
winget install Python. Python. 3.11

# After installation, restart PowerShell
```

---

## 🏗️ Phase 2: Create New Virtual Environment

### Enable PowerShell Script Execution (If Needed)

```powershell
# Check current execution policy
Get-ExecutionPolicy

# If it's "Restricted", you need to change it
# Run PowerShell as Administrator: 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Confirm the change
Get-ExecutionPolicy
# Should show: RemoteSigned
```

### Create Virtual Environment

```powershell
# Navigate to project root
cd D:\xarema\X-Filamenta-Python

# Create virtual environment (Python 3.11+)
python -m venv venv

# If 'python' doesn't work, try:
py -3.11 -m venv venv

# Verify venv was created
Test-Path .\venv\Scripts\Activate.ps1
# Should return:  True

Write-Host "✅ Virtual environment created!" -ForegroundColor Green
```

### Activate Virtual Environment

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Your prompt should change to show (venv) prefix: 
# (venv) PS D:\xarema\X-Filamenta-Python>

# Verify activation
Write-Host $env:VIRTUAL_ENV
# Should show: D:\xarema\X-Filamenta-Python\venv

# Check Python location (should be inside venv)
Get-Command python | Select-Object Source
# Should show: D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe
```

**Common Activation Issues:**

```powershell
# Issue:  "Activate.ps1 cannot be loaded because running scripts is disabled"
# Solution: Set execution policy (see above)

# Issue: "Activate. ps1 is not recognized"
# Solution: Check if venv was created correctly
Test-Path .\venv\Scripts\Activate.ps1

# Issue: Multiple Python versions
# Solution:  Specify exact Python version
py -3.11 -m venv venv
```

---

## 📦 Phase 3: Install Dependencies

### Upgrade pip and Essential Tools

```powershell
# Ensure venv is activated (you should see (venv) in prompt)

# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install wheel and setuptools
python -m pip install --upgrade setuptools wheel

Write-Host "✅ pip upgraded!" -ForegroundColor Green
```

### Install Project Dependencies

```powershell
# Install from requirements.txt
pip install -r requirements.txt

# If you have multiple requirement files:
pip install -r requirements.txt
pip install -r requirements-dev. txt  # Development dependencies (if exists)

# Verify installations
pip list

# Check for specific packages
pip show Flask
pip show pytest
```

### Install Additional Development Tools

```powershell
# Install code quality tools
pip install black isort ruff mypy

# Install testing tools
pip install pytest pytest-cov pytest-flask

# Install security tools (optional for dev)
pip install bandit pip-audit

Write-Host "✅ All dependencies installed!" -ForegroundColor Green
```

### Create requirements.txt (If Missing)

```powershell
# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Or create manually with essential packages:
@"
# Flask Core
Flask==3.0.0
Werkzeug==3.0.1

# Configuration
python-dotenv==1.0.0

# Database
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5

# Forms & Security
Flask-WTF==1.2.1
WTForms==3.1.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1

# Development
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
ruff==0.1.8
mypy==1.7.1
"@ | Out-File -FilePath requirements.txt -Encoding UTF8
```

---

## 🔧 Phase 4: Configure IntelliJ IDEA

### Method 1: Automatic Configuration (Recommended)

**Steps in IntelliJ IDEA:**

1. **Open Project**
   - `File` → `Open` → Navigate to `D:\xarema\X-Filamenta-Python`
   - Click `OK`

2. **Configure Python SDK**
   - `File` → `Project Structure` (Ctrl + Alt + Shift + S)
   - Click `Project` in left sidebar
   - Click `Add SDK` → `Python SDK`
   - Select `Virtualenv Environment`
   - Choose `Existing environment`
   - Click `...` (folder icon)
   - Navigate to:  `D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe`
   - Click `OK`
   - Click `Apply` and `OK`

3. **Verify Configuration**
   - `File` → `Settings` (Ctrl + Alt + S)
   - Navigate to: `Project:  X-Filamenta-Python` → `Python Interpreter`
   - Should show: `Python 3.11 (venv)` with path to your venv
   - Package list should show all installed packages (Flask, pytest, etc.)

### Method 2: PowerShell Command to Get Python Path

```powershell
# Ensure venv is activated first
.\venv\Scripts\Activate.ps1

# Get exact path to venv Python interpreter
$pythonPath = (Get-Command python).Source
Write-Host "Python Path: $pythonPath" -ForegroundColor Cyan
Write-Host "Copy this path and paste it in IntelliJ IDEA" -ForegroundColor Yellow

# Expected output:  D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe

# Copy to clipboard automatically
$pythonPath | Set-Clipboard
Write-Host "✅ Path copied to clipboard!" -ForegroundColor Green
```

### Configure IntelliJ IDEA Settings

**File → Settings (Ctrl + Alt + S)**

#### 1. Python Interpreter

```
Settings → Project:  X-Filamenta-Python → Python Interpreter
- Select: Python 3.11 (venv)
- Location: D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe
```

#### 2. Flask Configuration

```
Settings → Languages & Frameworks → Flask
- ✅ Enable Flask support
- Flask project root: D:\xarema\X-Filamenta-Python
- FLASK_APP: app.py (or your main file)
- FLASK_ENV: development
```

#### 3. Run Configuration

```
Run → Edit Configurations → + → Flask Server
- Name: Flask Dev Server
- Target type: Script path
- Script path: D:\xarema\X-Filamenta-Python\app.py
- Python interpreter: Python 3.11 (venv)
- Working directory: D:\xarema\X-Filamenta-Python
- Environment variables: 
    FLASK_APP=app
    FLASK_ENV=development
    FLASK_DEBUG=1
```

#### 4. Python Tools

```
Settings → Tools → Python Integrated Tools
- Default test runner: pytest
- Docstring format: Google
- Package requirements file: requirements.txt
```

#### 5. Code Style

```
Settings → Editor → Code Style → Python
- Scheme: Black (if available)
- ✅ Use tab character:  No
- Tab size: 4
- Indent:  4
- Continuation indent: 8
- Maximum line length: 100
```

#### 6. External Tools (Black, Ruff)

**Black Formatter:**
```
Settings → Tools → External Tools → +
- Name: Black
- Program: D:\xarema\X-Filamenta-Python\venv\Scripts\black.exe
- Arguments: $FilePath$
- Working directory: $ProjectFileDir$
- ✅ Synchronize files after execution
- ✅ Open console for tool output
```

**Ruff Linter:**
```
Settings → Tools → External Tools → +
- Name:  Ruff Check
- Program: D:\xarema\X-Filamenta-Python\venv\Scripts\ruff.exe
- Arguments: check $FilePath$ --fix
- Working directory: $ProjectFileDir$
- ✅ Synchronize files after execution
```

#### 7. File Watchers (Optional - Auto-format on Save)

```
Settings → Tools → File Watchers → +
- Name: Black
- File type: Python
- Scope: Project Files
- Program: D:\xarema\X-Filamenta-Python\venv\Scripts\black.exe
- Arguments: $FilePath$
- Working directory:  $ProjectFileDir$
- ✅ Auto-save edited files to trigger the watcher
- ✅ Trigger the watcher on external changes
```

---

## ✅ Phase 5: Verify Setup

### Verification Script

```powershell
# Navigate to project
cd D:\xarema\X-Filamenta-Python

# Create verification script
@"
# verify_setup.ps1
Write-Host "`n🔍 Verifying Python Environment Setup" -ForegroundColor Cyan
Write-Host "Project: X-Filamenta-Python"
Write-Host ("=" * 60)

# Check if venv is activated
if (`$env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment is activated" -ForegroundColor Green
    Write-Host "   Location: `$env:VIRTUAL_ENV`n"
} else {
    Write-Host "❌ Virtual environment is NOT activated" -ForegroundColor Red
    Write-Host "   Run: .\venv\Scripts\Activate.ps1`n"
    exit 1
}

# Verify correct venv path
if (`$env:VIRTUAL_ENV -eq "D:\xarema\X-Filamenta-Python\venv") {
    Write-Host "✅ Correct venv path" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: venv path mismatch" -ForegroundColor Yellow
    Write-Host "   Expected: D:\xarema\X-Filamenta-Python\venv"
    Write-Host "   Current: `$env:VIRTUAL_ENV"
}

# Check Python version
`$pythonVersion = python --version
Write-Host "`nPython Version: `$pythonVersion"

# Check pip version
`$pipVersion = python -m pip --version
Write-Host "Pip Version: `$pipVersion`n"

# Check critical packages
Write-Host "Checking critical packages..."
`$packages = @("Flask", "pytest", "black", "ruff", "mypy")

foreach (`$pkg in `$packages) {
    `$installed = pip show `$pkg 2>`$null
    if (`$installed) {
        `$version = (`$installed | Select-String "Version:").ToString().Split(": ")[1].Trim()
        Write-Host "  ✅ `$pkg (`$version)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ `$pkg (not installed)" -ForegroundColor Red
    }
}

# Test Flask import
Write-Host "`nTesting Flask import..."
python -c "import flask; print(f'  ✅ Flask {flask.__version__} works!')"

# Check project structure
Write-Host "`nChecking project structure..."
`$requiredDirs = @("app", "tests")
foreach (`$dir in `$requiredDirs) {
    if (Test-Path `$dir) {
        Write-Host "  ✅ `$dir/ exists" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ `$dir/ missing" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ Verification complete!" -ForegroundColor Green
Write-Host ("=" * 60)
"@ | Out-File -FilePath verify_setup.ps1 -Encoding UTF8

# Run verification
.\verify_setup.ps1
```

### Quick Test Commands

```powershell
# Ensure you're in project directory
cd D:\xarema\X-Filamenta-Python

# Activate venv
.\venv\Scripts\Activate.ps1

# Test Flask
python -c "import flask; print('Flask version:', flask.__version__)"

# Test project app (if app/__init__.py exists)
python -c "from app import create_app; app = create_app(); print('✅ App created successfully!')"

# Run Flask server (quick test)
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run
# Should start on http://127.0.0.1:5000
# Press Ctrl+C to stop

# Run tests
pytest tests/ -v

# Run linter
ruff check app/

# Format code
black app/ --check
```

---

## 🐛 Phase 6: Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Cannot activate venv - scripts disabled"

```powershell
# Solution: Change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify
Get-ExecutionPolicy
# Should show: RemoteSigned
```

#### Issue 2: "Python not recognized"

```powershell
# Check if Python is in PATH
$env:PATH -split ';' | Select-String -Pattern "Python"

# If not found, add Python to PATH: 
# Manual:  System Properties → Environment Variables → Path → Edit → Add: 
#   C:\Users\YourUser\AppData\Local\Programs\Python\Python311
#   C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Scripts

# Or use py launcher instead: 
py -3.11 -m venv venv
```

#### Issue 3: "pip install fails with SSL error"

```powershell
# Upgrade pip with trusted host
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Or use pip with --trusted-host flag
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

#### Issue 4: "Module not found in IntelliJ but works in PowerShell"

```powershell
# Solution:  Invalidate caches
# In IntelliJ: File → Invalidate Caches → Invalidate and Restart

# Also check interpreter: 
# File → Settings → Project → Python Interpreter
# Ensure it points to:  D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe
```

#### Issue 5: "Permission denied when creating venv"

```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → Run as Administrator

# Or change folder permissions:
icacls "D:\xarema\X-Filamenta-Python" /grant:r "$env:USERNAME:(OI)(CI)F" /T
```

#### Issue 6: "Long path error on Windows"

```powershell
# Enable long paths in Windows (Run as Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Restart computer after this change
```

#### Issue 7: "IntelliJ doesn't recognize Flask routes"

```
# Solution: Configure Flask support
File → Settings → Languages & Frameworks → Flask
- ✅ Enable Flask support
- Set templates folder: app/templates
- Set static folder: app/static
```

---

## 📝 Quick Reference Scripts

### Create Handy PowerShell Functions

```powershell
# Add to your PowerShell profile
# Edit profile: notepad $PROFILE

# Quick navigate to project
function Go-Filamenta {
    cd D:\xarema\X-Filamenta-Python
    Write-Host "📁 Navigated to X-Filamenta-Python" -ForegroundColor Cyan
}
Set-Alias filamenta Go-Filamenta

# Activate venv quickly
function Activate-Venv {
    cd D:\xarema\X-Filamenta-Python
    if (Test-Path .\venv\Scripts\Activate.ps1) {
        .\venv\Scripts\Activate.ps1
        Write-Host "✅ venv activated for X-Filamenta-Python" -ForegroundColor Green
    } else {
        Write-Host "❌ venv not found" -ForegroundColor Red
    }
}
Set-Alias venv Activate-Venv

# Quick Flask run
function Start-Flask {
    cd D:\xarema\X-Filamenta-Python
    .\venv\Scripts\Activate.ps1
    $env:FLASK_APP = "app"
    $env: FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    flask run
}
Set-Alias flaskrun Start-Flask

# Quick test
function Run-Tests {
    cd D:\xarema\X-Filamenta-Python
    .\venv\Scripts\Activate. ps1
    pytest tests/ -v --cov=app
}
Set-Alias test Run-Tests

# Format code
function Format-Code {
    cd D:\xarema\X-Filamenta-Python
    .\venv\Scripts\Activate.ps1
    black app/ tests/
    isort app/ tests/
    Write-Host "✅ Code formatted" -ForegroundColor Green
}
Set-Alias fmt Format-Code
```

### Reload profile: 
```powershell
. $PROFILE
```

### Usage:
```powershell
# Now you can use shortcuts: 
filamenta   # Navigate to project
venv        # Activate venv
flaskrun    # Run Flask
test        # Run tests
fmt         # Format code
```

---

## 📋 Complete Setup Checklist

### Initial Setup
- [ ] Python 3.11+ installed
- [ ] PowerShell execution policy set to RemoteSigned
- [ ] Navigated to `D:\xarema\X-Filamenta-Python`
- [ ] Old venv removed
- [ ] New venv created at `D:\xarema\X-Filamenta-Python\venv`
- [ ] Venv activated (prompt shows `(venv)`)
- [ ] pip upgraded to latest version
- [ ] requirements.txt exists
- [ ] All dependencies installed from requirements.txt
- [ ] Development tools installed (black, ruff, mypy, pytest)

### IntelliJ IDEA Configuration
- [ ] Project opened:  `D:\xarema\X-Filamenta-Python`
- [ ] Python SDK configured:  `D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe`
- [ ] Python Interpreter shows all installed packages
- [ ] Flask support enabled
- [ ] Flask run configuration created
- [ ] pytest configured as test runner
- [ ] Black configured as external tool
- [ ] Ruff configured as external tool
- [ ] File watchers set (optional)

### Verification
- [ ] `python --version` shows Python 3.11+
- [ ] `pip list` shows Flask, pytest, black, ruff, mypy
- [ ] `python -c "import flask"` works without error
- [ ] `flask run` starts development server
- [ ] `pytest tests/` runs (even if no tests yet)
- [ ] IntelliJ recognizes Python interpreter
- [ ] IntelliJ shows no import errors

---

## 🚀 One-Command Complete Setup

```powershell
# Complete automated setup script
# Save as: setup_venv. ps1

cd D:\xarema\X-Filamenta-Python

Write-Host "`n🚀 X-Filamenta-Python Environment Setup" -ForegroundColor Cyan
Write-Host ("=" * 60)

# Step 1: Clean old environment
Write-Host "`n📍 Step 1: Cleaning old environment..." -ForegroundColor Yellow
Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Write-Host "✅ Cleaned" -ForegroundColor Green

# Step 2: Create new venv
Write-Host "`n📍 Step 2: Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if (Test-Path .\venv\Scripts\Activate.ps1) {
    Write-Host "✅ venv created" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create venv" -ForegroundColor Red
    exit 1
}

# Step 3: Activate venv
Write-Host "`n📍 Step 3: Activating venv..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "✅ venv activated" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host "`n📍 Step 4: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel --quiet
Write-Host "✅ pip upgraded" -ForegroundColor Green

# Step 5: Install dependencies
Write-Host "`n📍 Step 5: Installing dependencies..." -ForegroundColor Yellow
if (Test-Path requirements.txt) {
    pip install -r requirements.txt --quiet
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠ requirements.txt not found" -ForegroundColor Yellow
}

# Step 6: Install dev tools
Write-Host "`n📍 Step 6: Installing dev tools..." -ForegroundColor Yellow
pip install black isort ruff mypy pytest pytest-cov --quiet
Write-Host "✅ Dev tools installed" -ForegroundColor Green

# Step 7: Verification
Write-Host "`n📍 Step 7: Verifying setup..." -ForegroundColor Yellow
$pythonPath = (Get-Command python).Source
Write-Host "Python:  $pythonPath"
python --version
pip list | Select-String -Pattern "Flask|pytest|black|ruff"

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 60)
Write-Host "`nNext steps:"
Write-Host "1. Configure IntelliJ IDEA:"
Write-Host "   File → Project Structure → SDK → $pythonPath"
Write-Host "2. Run Flask:  flask run"
Write-Host "3. Run tests: pytest tests/"
```

### Run the setup script:
```powershell
cd D:\xarema\X-Filamenta-Python
.\setup_venv.ps1
```

---

## 🎓 Summary

**Your project is now configured at:**
- **Path:** `D:\xarema\X-Filamenta-Python`
- **venv:** `D:\xarema\X-Filamenta-Python\venv`
- **Python:** `D:\xarema\X-Filamenta-Python\venv\Scripts\python.exe`

**To start working:**
```powershell
cd D:\xarema\X-Filamenta-Python
.\venv\Scripts\Activate. ps1
flask run
```

**Your environment is ready to code!  🎉**

---