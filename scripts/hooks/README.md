# Git Hooks

**Purpose:** Automated code quality checks before commits  
**File:** scripts/hooks/README.md | Repository: X-Filamenta-Python

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

---

## Overview

This directory contains Git hooks to enforce code quality before commits. 

**Available hooks:**
- ✅ `pre-commit` — Run linting, formatting, type checking, i18n validation, and tests

---

## Installation Methods

### **Method 1: Python `pre-commit` Package (RECOMMENDED)**

**Cross-platform, automatic, standard.**

#### Install Package

```powershell
# Install pre-commit package
. \. venv\Scripts\pip. exe install pre-commit

# Install hooks
. \.venv\Scripts\pre-commit. exe install
```

#### Configuration

Configuration is in `.pre-commit-config.yaml` at project root. 

#### Usage

Hooks run automatically on `git commit`.

**Manual run (test all files):**
```powershell
.\.venv\Scripts\pre-commit.exe run --all-files
```

**Update hooks:**
```powershell
.\.venv\Scripts\pre-commit.exe autoupdate
```

**Bypass (NOT RECOMMENDED):**
```powershell
git commit --no-verify -m "message"
```

---

### **Method 2: Manual Installation (Bash)**

**For Linux/Mac users who prefer shell scripts.**

#### Install

```bash
# Create symlink
ln -s ../../scripts/hooks/pre-commit.sh .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit
```

#### Usage

Runs automatically on `git commit`.

**Test manually:**
```bash
bash scripts/hooks/pre-commit. sh
```

---

### **Method 3: Manual Installation (PowerShell)**

**For Windows users (less reliable than pre-commit package).**

#### Install

```powershell
# Copy script
Copy-Item scripts\hooks\pre-commit.ps1 . git\hooks\pre-commit
```

**Note:** PowerShell hooks in Git may not execute reliably on Windows.  Use **Method 1** instead.

---

## What Gets Checked

All methods run the same checks:

| Check | Tool | What It Does |
|-------|------|--------------|
| **Linting** | Ruff | Checks Python code for errors and style issues |
| **Formatting** | Ruff | Ensures code follows Black style (88 chars) |
| **Type Checking** | Mypy | Validates type hints |
| **i18n Validation** | check_i18n.py | Checks translation files for missing keys and hardcoded text |
| **Tests** | pytest | Runs all unit and integration tests |

---

## Hooks Available

### `pre-commit`

**Runs before every commit.**

**Checks:**
1. ✅ Ruff linting
2. ✅ Ruff formatting
3. ✅ Mypy type checking
4. ✅ i18n translation validation
5. ✅ pytest tests

**If any check fails:**
- ❌ Commit is blocked
- 📝 Fix issues and try again

**Bypass (emergency only):**
```powershell
git commit --no-verify -m "hotfix: critical bug"
```

---

## Troubleshooting

### Hook Not Running

**Check installation:**
```powershell
# Method 1 (pre-commit package)
.\.venv\Scripts\pre-commit. exe run --all-files

# Method 2/3 (manual)
Test-Path .git\hooks\pre-commit  # Should return True
```

### Hook Fails with "Command not found"

**Ensure virtual environment is activated:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Or use full paths in hook scripts (already configured).**

### Slow Hook Execution

**Skip tests during commit (run separately):**

Edit `.pre-commit-config.yaml` and comment out pytest hook temporarily.

---

## Customization

### Add New Checks

**Method 1 (pre-commit package):**

Edit `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks: 
      # ...  existing hooks ...
      
      - id: custom-check
        name: Custom Validation
        entry: . venv/Scripts/python. exe scripts/utils/custom_check.py
        language: system
        pass_filenames: false
```

**Method 2/3 (manual scripts):**

Edit `scripts/hooks/pre-commit.sh` or `pre-commit.ps1` and add your check. 

### Skip Specific Checks

**Method 1:**

Use `SKIP` environment variable:

```powershell
$env:SKIP = "mypy,pytest"
git commit -m "message"
```

**Method 2/3:**

Comment out check in script. 

---

## CI/CD Integration

Pre-commit hooks are **also enforced in CI/CD** (`.github/workflows/ci.yml`).

This ensures:
- ✅ No one bypasses hooks with `--no-verify`
- ✅ Consistent quality on all branches
- ✅ Pull requests are validated before merge

---

## Best Practices

1. ✅ **Always run hooks** — Don't use `--no-verify` unless emergency
2. ✅ **Fix issues immediately** — Don't accumulate technical debt
3. ✅ **Test before commit** — Run checks manually:  `.venv/Scripts/pre-commit. exe run --all-files`
4. ✅ **Keep hooks fast** — If tests slow, consider splitting into `pre-push` hook
5. ✅ **Update regularly** — Run `pre-commit autoupdate` monthly

---

## Reference Scripts

### `pre-commit. sh` (Bash)

Bash implementation for Linux/Mac.

**Location:** `scripts/hooks/pre-commit.sh`

### `pre-commit.ps1` (PowerShell)

PowerShell implementation for Windows (reference only, use pre-commit package instead).

**Location:** `scripts/hooks/pre-commit.ps1`

---

**For questions or issues, see:** `.github/workflow-rules.md`