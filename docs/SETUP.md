---
Purpose: Developer setup guide for X-Filamenta-Python
Description: Step-by-step instructions to set up a development environment

File: docs/SETUP.md | Repository: X-Filamenta-Python
Created: 2025-12-29T16:15:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public

---

# Development Setup Guide

Complete instructions for setting up X-Filamenta-Python for development.

## Prerequisites

- **Windows 11** (or Linux/macOS)
- **Python 3.12+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)
- **IDE:** IntelliJ IDEA or VS Code

## Quick Start (5 minutes)

### 1. Clone Repository

```powershell
git clone https://github.com/XAREMA/X-Filamenta-Python.git
cd X-Filamenta-Python
```

### 2. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
# Backend dependencies
pip install -r requirements-dev.txt

# Frontend dependencies
npm install
```

### 4. Configure Environment

```powershell
Copy-Item ".env.example" ".env"
# Edit .env with your local settings
```

### 5. Run Development Server

```powershell
# Terminal 1: Backend (Flask dev server)
.\.venv\Scripts\python.exe backend\src\app.py

# Terminal 2: Frontend (if needed)
npm run dev
```

Visit http://localhost:5000

---

## Detailed Setup

### 1. Clone & Initial Setup

```powershell
# Clone the repository
git clone https://github.com/XAREMA/X-Filamenta-Python.git
cd X-Filamenta-Python

# Verify Python version
python --version  # Should be 3.12+

# Create and activate virtual environment (if not already done)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Python Dependencies

```powershell
# Upgrade pip
.\.venv\Scripts\python.exe -m pip install --upgrade pip

# Install development dependencies
pip install -r requirements-dev.txt

# Verify installation
pip list | Select-String "flask|pytest|ruff|mypy"
```

### 3. Database Setup

```powershell
# Initialize database
.\.venv\Scripts\python.exe -m alembic upgrade head

# Create initial tables (optional, wizard will do this)
# .\.venv\Scripts\python.exe backend\src\utils\init_db.py
```

### 4. Environment Configuration

```powershell
# Copy example environment file
Copy-Item ".env.example" ".env"
```

Edit `.env` and set:
```env
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
MAIL_SERVER=smtp.mailtrap.io
# ... etc
```

### 5. Frontend Setup

```powershell
# Install Node dependencies
npm install

# Build frontend assets (if needed)
npm run build
```

### 6. Verify Installation

```powershell
# Run a quick test
.\.venv\Scripts\pytest.exe -v

# Check code style
.\.venv\Scripts\ruff.exe check .
```

---

## Running the Application

### Development Mode (Debug)

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run Flask dev server (auto-reload on changes)
.\.venv\Scripts\python.exe backend\src\app.py
```

**Features:**
- Auto-reload on file changes
- Detailed error pages
- Debugger enabled

### Production Mode (Testing)

```powershell
# Run Waitress WSGI server
.\.venv\Scripts\python.exe run_prod.py
```

**For realistic testing of prod behavior**

---

## Common Workflows

### Running Tests

```powershell
# Run all tests
.\.venv\Scripts\pytest.exe -v

# Run specific test file
.\.venv\Scripts\pytest.exe backend/tests/unit/test_auth.py -v

# Run with coverage
.\.venv\Scripts\pytest.exe --cov=backend/src --cov-report=html

# View coverage report
start htmlcov\index.html
```

### Code Formatting

```powershell
# Format Python code
.\.venv\Scripts\ruff.exe format .

# Format Frontend code
npm run fmt
```

### Linting

```powershell
# Lint Python
.\.venv\Scripts\ruff.exe check .

# Type checking
.\.venv\Scripts\mypy.exe backend/src

# Lint Frontend
npm run lint
```

### Database Migrations

```powershell
# Create a new migration
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "describe change"

# Apply migrations
.\.venv\Scripts\python.exe -m alembic upgrade head

# Rollback last migration
.\.venv\Scripts\python.exe -m alembic downgrade -1
```

---

## Troubleshooting

### "python" command not found

**Problem:** PowerShell doesn't recognize `python` command.

**Solution:** Always use the full venv path:
```powershell
# Instead of: python script.py
.\.venv\Scripts\python.exe script.py
```

### Virtual Environment Issues

```powershell
# Deactivate current venv
deactivate

# Remove and recreate venv
Remove-Item ".venv" -Recurse -Force
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### Port Already in Use

```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000

# Kill the process
Stop-Process -Id <PID> -Force
```

### Database Lock

```powershell
# Delete database file to start fresh
Remove-Item "instance/*.db" -Force

# Recreate with wizard
.\.venv\Scripts\python.exe run_prod.py
```

### Import Errors

```powershell
# Reinstall dependencies
pip install -r requirements-dev.txt --force-reinstall

# Clear Python cache
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
```

---

## IDE Setup

### IntelliJ IDEA (Recommended)

1. **Open Project:**
   - File → Open → select project folder
   - Trust project when prompted

2. **Configure Python Interpreter:**
   - File → Settings → Project → Python Interpreter
   - Add Interpreter → Add Local Interpreter → Existing Environment
   - Select `.\.venv\Scripts\python.exe`

3. **Configure Run Configurations:**
   - Run → Edit Configurations
   - Create "Flask" run configuration
   - Set Script path: `backend\src\app.py`
   - Working directory: project root
   - Python interpreter: .venv

4. **Enable Code Quality Tools:**
   - Install plugins: Ruff, MyPy
   - Settings → Tools → Python Integrated Tools
   - Default test runner: pytest

### VS Code

1. **Install Extensions:**
   - Python
   - Pylance
   - Flask
   - Prettier
   - ESLint

2. **Create `.vscode/settings.json`:**
   ```json
   {
     "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
     "python.linting.ruffEnabled": true,
     "python.linting.enabled": true,
     "python.testing.pytestEnabled": true,
     "[python]": {
       "editor.formatOnSave": true,
       "editor.defaultFormatter": "charliermarsh.ruff"
     },
     "[html]": {
       "editor.formatOnSave": true,
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     }
   }
   ```

---

## Git Workflow

### First Time Setup

```powershell
# Configure Git (if not done globally)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Creating a Feature Branch

```powershell
# Update main branch
git fetch upstream
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit
git add .
git commit -m "feat: add my feature"

# Push to your fork
git push origin feature/my-feature

# Create PR on GitHub
```

### Keep Branch Updated

```powershell
# Update from upstream
git fetch upstream
git rebase upstream/main

# If conflicts occur
git rebase --continue
# or
git rebase --abort
```

---

## Next Steps

After setup, check out:
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Contribution guidelines
- [../docs/ARCHITECTURE.md](ARCHITECTURE.md) — System design
- [../README.md](../README.md) — Project overview

---

**Happy coding! 🚀**

For issues or questions, see [CONTRIBUTING.md](../CONTRIBUTING.md#questions--support)

