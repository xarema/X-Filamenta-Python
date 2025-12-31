---
mode: "agent"
description:  "Migrate a dependency to a new version across the entire codebase"
---

# Migrate Dependency

**Task:** Safely migrate a dependency (library, framework, tool) to a new version across the entire project.

---

## Input Required

### Dependency Details
- **Dependency name:** ${input: dependency: e.g., "Flask", "Bootstrap", "SQLAlchemy"}
- **Current version:** ${input:current_version:e.g., "2.3.0"}
- **Target version:** ${input:target_version:e.g., "3.0.0"}
- **Ecosystem:** ${input:ecosystem:Python (pip) | JavaScript (npm) | CSS/Framework}

### Migration Reason
${input:reason:Why migrate? (security patch, new features, deprecation, etc.)}

### Breaking Changes Known
${input:breaking_changes:List known breaking changes from changelog/migration guide}

---

## MANDATORY:  Pre-Migration Process

### 1. Read Documentation

**Review official migration guides:**
- [ ] Read dependency's CHANGELOG
- [ ] Read official migration/upgrade guide
- [ ] Check for deprecation warnings
- [ ] Identify breaking changes
- [ ] Note new features/improvements

### 2. Impact Analysis

**Create analysis report:**
- Location: `Analysis_reports/YYYY-MM-DD_HH-mm_migrate-<dependency>-v<version>.md`

**Content:**
- Current usage across project (search codebase)
- Affected files/modules
- Breaking changes impact
- Required code changes
- Testing strategy
- Rollback plan
- Estimated effort

### 3. Backup & Branch

```powershell
# Create feature branch
git checkout -b migrate-<dependency>-v<version>

# Optional: Backup database
Copy-Item "instance\filamenta. db" "instance\filamenta. db.backup-$(Get-Date -Format 'yyyyMMdd')"
```

---

## Migration Process

### Step 1: Update Dependency

#### Python (pip)

**Update `requirements.txt` or `pyproject.toml`:**

```toml
# Before
flask = "^2.3.0"

# After
flask = "^3.0.0"
```

**Install:**
```powershell
.\. venv\Scripts\pip. exe install --upgrade flask

# Or reinstall all
.\.venv\Scripts\pip.exe install -r requirements.txt --upgrade
```

**Lock dependencies:**
```powershell
.\.venv\Scripts\pip.exe freeze > requirements.lock
```

#### JavaScript (npm)

**Update `package.json`:**
```json
{
  "dependencies": {
    "bootstrap": "^5.3.0"
  }
}
```

**Install:**
```powershell
npm install bootstrap@latest

# Or
npm update bootstrap
```

---

### Step 2: Find All Usages

**Search codebase for affected patterns:**

```powershell
# Find imports (Python)
Get-ChildItem -Recurse -Include *.py | Select-String "from flask import" | Select-Object -Unique Path

# Find CDN links (HTML)
Get-ChildItem -Recurse -Include *.html | Select-String "bootstrap@5. 2" | Select-Object -Unique Path

# Find API usage
Get-ChildItem -Recurse -Include *.py | Select-String "deprecated_function"
```

**Document findings in analysis report.**

---

### Step 3: Apply Breaking Changes

**Common migration patterns:**

#### Example:  Flask 2.x → 3.x

**Breaking change:  `flask. json` module reorganized**

**Before (Flask 2.x):**
```python
from flask. json import jsonify
```

**After (Flask 3.x):**
```python
from flask import jsonify  # Still works
# Or
import json
from flask import Response

def my_route():
    return Response(json.dumps(data), mimetype="application/json")
```

#### Example: Bootstrap 5.2 → 5.3

**Breaking change:  Utility classes renamed**

**Before:**
```html
<div class="ms-auto">... </div>  <!-- margin-start -->
```

**After (still works, but deprecated warning):**
```html
<div class="ms-auto">...</div>  <!-- Still supported -->
```

**New recommended (if breaking in future):**
```html
<div class="margin-start-auto">...</div>
```

---

### Step 4: Update Code Systematically

**For each affected file:**

1. **Open file**
2. **Apply required changes** (from breaking changes list)
3. **Update imports/API calls**
4. **Remove deprecated code**
5. **Add file header update** (Last modified, commit)
6. **Run linters** on that file
7. **Test that file's functionality**

**Example workflow per file:**

```powershell
# Edit file
code backend/src/routes/users.py

# After changes, lint
. \.venv\Scripts\ruff. exe check backend/src/routes/users.py
. \.venv\Scripts\mypy. exe backend/src/routes/users.py

# Run related tests
.\.venv\Scripts\pytest.exe tests/test_users.py -v
```

---

### Step 5: Update Templates/Frontend (if applicable)

**For framework migrations (Bootstrap, HTMX, etc.):**

**Update CDN links:**
```html
<!-- Before -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- After -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

**Update class names/attributes:**
```html
<!-- If breaking change -->
<!-- Before -->
<div class="old-class">...</div>

<!-- After -->
<div class="new-class">...</div>
```

**Search and replace carefully:**
```powershell
# Find all affected templates
Get-ChildItem -Recurse -Include *.html | Select-String "old-class"

# Manual review + replace (DO NOT use automated replace without review)
```

---

### Step 6: Run Full Test Suite

**Automated tests:**
```powershell
# Python tests
.\.venv\Scripts\pytest.exe -v --cov

# Linters
.\.venv\Scripts\ruff.exe check . 
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\mypy.exe backend/src

# Frontend tests (if applicable)
npm run lint
npm run test
```

**Fix all failures before continuing.**

---

### Step 7: Manual Testing

**Kill servers and test:**

```powershell
# Kill servers
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Dev mode testing
.\.venv\Scripts\python.exe backend\src\app.py
```

**Test checklist:**
- [ ] All routes accessible
- [ ] No console errors (browser DevTools)
- [ ] No server errors (terminal logs)
- [ ] UI displays correctly (all pages)
- [ ] Forms submit successfully
- [ ] AJAX/HTMX interactions work
- [ ] Translations display
- [ ] Responsive design intact (test mobile viewport)

**Repeat in prod mode:**
```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
. \.venv\Scripts\python. exe run_prod. py
```

---

### Step 8: Performance Testing (if major version)

**Compare before/after:**

**Metrics to check:**
- Page load times
- Database query performance
- Memory usage
- Bundle size (frontend)

**Tools:**
```powershell
# Backend profiling (if needed)
.\.venv\Scripts\pip.exe install flask-profiler

# Frontend bundle size
npm run build
# Check dist/ folder size
```

---

### Step 9: Documentation

**Update CHANGELOG. md:**

```markdown
## [Unreleased]

### Changed
- **BREAKING:** Migrated to Flask 3.0.0 (#issue)
  - Updated all imports and API calls
  - Removed deprecated `flask.json` usage
  - Tested all endpoints
  - No user-facing changes
  
### Dependencies
- Upgraded Flask from 2.3.0 to 3.0.0
- Upgraded SQLAlchemy from 1.4.x to 2.0.x (compatible with Flask 3)
```

**Update `requirements.txt` / `package.json`:**
- Ensure new versions pinned
- Update lock files

**Create migration report:**
- Location: `Analysis_reports/YYYY-MM-DD_HH-mm_migrate-<dependency>-complete.md`
- Content: 
  - Migration summary
  - Files changed (list)
  - Breaking changes applied
  - Test results
  - Performance impact (if measured)
  - Issues encountered + solutions
  - Rollback notes

---

## Rollback Plan

**If migration fails:**

### 1. Revert Code Changes

```powershell
# Discard all changes
git checkout . 

# Or revert to specific commit
git revert <commit-hash>
```

### 2. Reinstall Old Dependency

**Python:**
```powershell
# Edit requirements.txt (restore old version)
# Then reinstall
.\.venv\Scripts\pip.exe install -r requirements.txt --force-reinstall
```

**JavaScript:**
```powershell
npm install <dependency>@<old-version>
```

### 3. Restore Database (if needed)

```powershell
Copy-Item "instance\filamenta.db. backup-YYYYMMDD" "instance\filamenta.db" -Force
```

### 4. Test Rollback

- Run tests
- Start server
- Verify functionality restored

---

## Common Migration Scenarios

### Scenario 1: Flask 2.x → 3.x

**Breaking changes:**
- `flask.json` module reorganized
- Some Werkzeug APIs changed
- Click 8. x required

**Fix:**
```python
# Update imports
from flask import jsonify  # Still works in 3.x

# Update Click commands (if using CLI)
import click
# (No changes needed for basic usage)
```

---

### Scenario 2: Bootstrap 5.2 → 5.3

**Breaking changes:**
- Minimal (mostly additions)
- Some utility classes deprecated (warnings)

**Fix:**
```html
<!-- Update CDN version -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Review deprecation warnings in browser console -->
<!-- Update deprecated classes if found -->
```

---

### Scenario 3: SQLAlchemy 1.4 → 2.0

**Breaking changes:**
- New query API (ORM)
- `engine. execute()` removed → use `session.execute()`
- `Query` object methods changed

**Fix:**
```python
# Before (1.4)
users = User.query.filter_by(active=True).all()
result = db.engine.execute("SELECT * FROM users")

# After (2.0)
users = db.session.execute(
    db.select(User).filter_by(active=True)
).scalars().all()

result = db.session.execute(db.text("SELECT * FROM users"))
```

---

## Files Created/Modified

```
requirements.txt (or pyproject.toml)          ← Update dependency version
package.json                                  ← Update dependency version (if JS)
backend/src/**/*.py                           ← Apply breaking changes
backend/src/templates/**/*.html               ← Update CDN/class names (if frontend)
tests/**/*.py                                 ← Update test assertions (if API changed)
CHANGELOG.md                                  ← Document migration
Analysis_reports/<timestamp>_migrate-<dep>.md ← Migration report
```

---

## Validation Checklist

- [ ] Analysis report created (pre-migration)
- [ ] Feature branch created
- [ ] Backup created (database, if applicable)
- [ ] Official migration guide read
- [ ] Breaking changes identified
- [ ] Dependency updated in manifest files
- [ ] All usages found and documented
- [ ] Code changes applied systematically
- [ ] File headers updated
- [ ] Linters pass (Ruff, Mypy, npm lint)
- [ ] All automated tests pass
- [ ] Manual testing complete (dev mode)
- [ ] Manual testing complete (prod mode)
- [ ] No console errors
- [ ] No server errors/warnings
- [ ] Performance acceptable (if measured)
- [ ] CHANGELOG. md updated
- [ ] Migration report created
- [ ] Rollback plan documented and tested

---

## Don'ts

- ❌ Update dependency without reading changelog
- ❌ Skip impact analysis
- ❌ Apply changes without testing each file
- ❌ Use automated find-replace for code (manual review required)
- ❌ Skip manual testing
- ❌ Commit without all tests passing
- ❌ Forget to update CHANGELOG
- ❌ Leave deprecated code (if removal is safe)
- ❌ Ignore deprecation warnings
- ❌ Skip rollback plan preparation

---

## References

- `.github/copilot-instructions. md` — General rules
- `.github/python.instructions.md` — Python dependencies
- `.github/frontend.instructions.md` — Frontend dependencies
- `.github/workflow-rules.md` — Testing workflow
- Dependency's official changelog/migration guide

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.