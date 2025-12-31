# Setup Scripts

**Purpose:** Project initialization and configuration scripts (one-time or rare usage)  
**File:** scripts/setup/README.md | Repository: X-Filamenta-Python

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 

---

## Scripts

### `setup_flask_structure.sh`

**Purpose:** Create recommended Flask + HTMX project structure

**What it does:**
- ✅ Creates directory structure (backend, tests, docs, scripts)
- ✅ Creates `__init__.py` files
- ✅ Generates basic templates (base, navbar, footer)
- ✅ Creates configuration files (config.py, . env. example)
- ✅ Creates static assets (CSS, JS)
- ✅ Creates entry point (app.py)

**Usage:**

```bash
# Linux/Mac
bash scripts/setup/setup_flask_structure.sh

# Windows (WSL or Git Bash)
bash scripts/setup/setup_flask_structure.sh
```

**When to use:**
- Starting a new Flask project from scratch
- Resetting project structure to recommended layout

**Note:** This will **create** files, not overwrite existing ones.

---

### `generate_gitignore.py`

**Purpose:** Generate comprehensive `.gitignore` for Flask projects

**What it does:**
- ✅ Generates `.gitignore` with patterns for: 
  - Python (`__pycache__`, `*.pyc`, venv)
  - Flask (instance/, sessions)
  - IDEs (VSCode, PyCharm, IntelliJ)
  - OS files (`.DS_Store`, `Thumbs.db`)
  - Logs, temp files, databases

**Usage:**

```powershell
# Generate (prompts if . gitignore exists)
.\.venv\Scripts\python.exe scripts\setup\generate_gitignore. py

# Force overwrite existing .gitignore
.\.venv\Scripts\python.exe scripts\setup\generate_gitignore.py --force

# Custom output path
.\.venv\Scripts\python.exe scripts\setup\generate_gitignore.py --output path/to/. gitignore
```

**When to use:**
- Starting a new project
- Updating old `.gitignore` with modern patterns
- After project structure changes

**After generation:**
1. Review the file
2. Customize "Project Specific" section
3. Commit to repository

---

## Typical Setup Workflow

**For a brand new project:**

```powershell
# 1. Create project directory
New-Item -ItemType Directory -Path "my-flask-app"
Set-Location my-flask-app

# 2. Initialize Git
git init

# 3. Generate .gitignore
python scripts/setup/generate_gitignore.py --force

# 4. Create project structure (if using bash)
bash scripts/setup/setup_flask_structure.sh

# 5. Create virtual environment
python -m venv .venv
. \. venv\Scripts\Activate.ps1

# 6. Install dependencies
pip install flask python-dotenv flask-sqlalchemy waitress

# 7. Generate requirements.txt
pip freeze > requirements. txt

# 8. Copy . env.example to .env
Copy-Item . env.example .env

# 9. Configure . env (edit with your settings)
code .env

# 10. Run app
python app.py
```

---

## Files Created by Setup Scripts

### `setup_flask_structure.sh` creates: 

```
backend/src/
├── __init__.py                    ← App factory
├── config.py                      ← Configuration
├── models/
├── routes/
│   └── main.py                    ← Main blueprint
├── services/
├── utils/
├── templates/
│   ├── layouts/
│   │   └── base.html              ← Base template
│   ├── components/
│   │   ├── navbar.html
│   │   └── footer. html
│   ├── pages/
│   │   └── index.html
│   └── partials/
└── static/
    ├── css/
    │   └── main.css
    ├── js/
    │   └── main.js
    └── img/

tests/
├── unit/
├── integration/
└── functional/

docs/
├── architecture/
├── api/
├── guides/
└── development/

scripts/
├── setup/
├── utils/
└── hooks/

config/
instance/
logs/

app.py                             ← Entry point
. env. example                     ← Environment template
. flaskenv                         ← Flask config
. editorconfig                     ← Editor settings
```

---

## Customization

### Modify Structure

Edit `setup_flask_structure.sh` to add/remove directories or files. 

### Modify . gitignore Template

Edit `generate_gitignore.py` and modify `GITIGNORE_TEMPLATE` variable.

---

## Troubleshooting

### "Permission denied" on . sh script

```bash
chmod +x scripts/setup/setup_flask_structure.sh
```

### Script creates wrong paths (Windows)

Use WSL, Git Bash, or manually create structure following the script as reference.

### . gitignore already exists

Use `--force` flag to overwrite, or manually merge changes.

---

**See also:**
- `.github/workflow-rules.md` — Project workflow
- `scripts/utils/README.md` — Utility scripts
- `scripts/hooks/README.md` — Git hooks