# Workflow Rules — Modification Process

**Purpose:** Mandatory workflow before modifying routes, servers, or critical components  
**File:** `.github/workflow-rules.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

**Metadata:**
- Status: Stable
- Classification: Internal

---

## 1) Mandatory Process BEFORE Route/Server Modifications

### 1.1 Kill All Servers

**ALWAYS kill Python processes before modifying:**

```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

**Why:**
- Prevents file lock conflicts
- Ensures clean state
- Avoids "Address already in use" errors
- Prevents testing old code

### 1.2 Read Relevant Documentation

**Before ANY modification, read:**
- ✅ `.github/copilot-instructions.md` — General rules
- ✅ `.github/user-preferences.md` — User preferences
- ✅ `.github/workflow-rules.md` — This file
- ✅ `.github/incidents-history.md` — Past incidents (avoid repeating)
- ✅ Domain-specific `.instructions.md` (Python, Frontend, PowerShell)

### 1.3 Consult Incident History

**Check `.github/incidents-history.md` for:**
- Routes that failed in the past
- Known issues with specific patterns
- Solutions that worked
- Patterns to avoid

**DO NOT reuse a failed route/pattern without understanding the root cause.**

---

## 2) Route Modification Checklist

### 2.1 Before Modifying Routes

- [ ] All Python processes stopped
- [ ] `.github/incidents-history.md` checked for this route
- [ ] This file read completely
- [ ] Clear plan documented (what, why, how)
- [ ] User/team approval obtained (if structural change)

### 2.2 During Modification

- [ ] Follow Flask Blueprint conventions
- [ ] Add/update type hints
- [ ] Add/update docstrings
- [ ] Add/update tests (pytest)
- [ ] Add/update i18n translations (if UI text)
- [ ] Update CHANGELOG.md

### 2.3 After Modification

- [ ] Kill all servers again
- [ ] Run linters: 
  ```powershell
  .\.venv\Scripts\ruff.exe check .
  .\.venv\Scripts\ruff.exe format --check . 
  .\.venv\Scripts\mypy.exe backend/src
  ```
- [ ] Run tests:
  ```powershell
  .\.venv\Scripts\pytest.exe -v
  ```
- [ ] Test in **dev mode** (debug=True):
  ```powershell
  .\.venv\Scripts\python.exe backend\src\app.py
  ```
- [ ] Verify in browser (all affected routes)
- [ ] Check dev logs for errors
- [ ] Kill servers again
- [ ] Test in **prod mode** (Waitress):
  ```powershell
  .\.venv\Scripts\python.exe run_prod.py
  ```
- [ ] Verify in browser again
- [ ] Check prod logs
- [ ] **ONLY THEN** ask user to test

---

## 3) Server Management

### 3.1 Development Server

**Start:**
```powershell
.\.venv\Scripts\python.exe backend\src\app.py
```

**Configuration:**
- Debug mode: `True`
- Auto-reload:  Enabled
- Port: 5000 (default)
- Verbose logging

**Use for:**
- Development
- Debugging
- Initial testing
- Identifying issues

### 3.2 Production Server

**Start:**
```powershell
.\.venv\Scripts\python.exe run_prod.py
```

**Configuration:**
- Debug mode: `False`
- Auto-reload: Disabled
- Port: 5000
- WSGI server: Waitress
- Production logging

**Use for:**
- Final validation
- Performance testing
- Pre-deployment checks

### 3.3 Kill Servers (Before/After Changes)

**Standard kill:**
```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

**Aggressive kill (if standard doesn't work):**
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Get-Process python.exe -ErrorAction SilentlyContinue
```

**Kill by port (if port stuck):**
```powershell
$processId = (Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue).OwningProcess
if ($processId) { Stop-Process -Id $processId -Force }
```

### 3.4 Verify Server Stopped

```powershell
# Check no Python processes
Get-Process python.exe -ErrorAction SilentlyContinue | Measure-Object

# Check port 5000 free
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
# If nothing displayed = port free ✅
```

---

## 4) Testing Workflow

### 4.1 Clean Database Before Tests (Optional)

**User preference:** YES (see `.github/user-preferences.md`)

```powershell
# Delete all databases
Remove-Item "instance\*.db" -Force -ErrorAction SilentlyContinue

# Verify deleted
Test-Path "instance\*.db"  # Should return False
```

**When to clean:**
- Testing wizard installation flow
- Testing first-run experience
- Reproducing fresh install bugs
- When database schema changed

**When NOT to clean:**
- Testing existing user flows
- Testing migrations
- Testing data persistence

### 4.2 Test Phases

#### Phase 1: Development Testing (Always First)

```powershell
# 1. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Clean DB (if testing fresh install)
Remove-Item "instance\*.db" -Force -ErrorAction SilentlyContinue

# 3. Start dev server
.\.venv\Scripts\python.exe backend\src\app.py

# 4. Test in browser
# - Open http://localhost:5000
# - Test all affected routes
# - Verify all UI elements
# - Check browser console for errors

# 5. Monitor logs
# - Check terminal output for errors/warnings
# - Verify expected log messages

# 6. Stop server (Ctrl+C or kill)
```

#### Phase 2: Production Testing (Final Validation)

```powershell
# 1. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Clean DB (if testing fresh install)
Remove-Item "instance\*.db" -Force -ErrorAction SilentlyContinue

# 3. Start prod server
.\.venv\Scripts\python.exe run_prod.py

# 4. Test in browser (same as Phase 1)
# 5. Monitor logs
# 6. Stop server
```

### 4.3 Automated Tests

**Always run before committing:**

```powershell
# Linting
.\.venv\Scripts\ruff.exe check . 

# Formatting
.\.venv\Scripts\ruff.exe format --check .

# Type checking
.\.venv\Scripts\mypy.exe backend/src

# Unit/integration tests
.\.venv\Scripts\pytest.exe -v

# Frontend linting (if applicable)
npm run lint

# Frontend formatting (if applicable)
npm run fmt -- --check
```

**All must pass ✅ before saying "it's ready".**

---

## 5) Wizard-Specific Workflow

### 5.1 Wizard UI Rules

**Breadcrumb (Fil d'Ariane):**
- ✅ **ALWAYS 2 lines**
- ✅ Line 1: Steps 1, 2, 3
- ✅ Line 2: Steps 4, 5
- ❌ NEVER 1 line with wrap

**Buttons:**
- ✅ **IN partials** (step templates)
- ❌ **NOT in `_wizard_content. html`**
- Prevents duplication

**Translations:**
- ✅ **NO hardcoded text**
- ✅ All text in `backend/src/i18n/{fr,en}. json`
- ✅ Use `{{ t('key') or 'Fallback' }}`

### 5.2 Adding a Wizard Step

**Process:**
1. Read `.github/prompts/add-wizard-step.prompt. md`
2. Use Agent mode (or manual if preferred)
3. Update: 
   - Routes (`backend/src/routes/wizard.py`)
   - Templates (`backend/src/templates/wizard/stepX.html`)
   - Partials (if needed)
   - Translations (`backend/src/i18n/*. json`)
   - Breadcrumb configuration
   - Tests (`tests/test_wizard.py`)
   - CHANGELOG.md
4. Follow testing workflow (dev → prod)

---

## 6) Error Response Workflow

### 6.1 When Error Occurs

**DO NOT immediately say "try again" to user.**

**Instead:**
1. ✅ Analyze error logs
2. ✅ Identify root cause
3. ✅ Check `.github/incidents-history.md` for similar issues
4. ✅ Propose fix
5. ✅ Implement fix
6. ✅ Test fix (dev + prod)
7. ✅ Verify 100% working
8. ✅ **THEN** ask user to test

### 6.2 Document Incident

**If error was significant, add to `.github/incidents-history.md`:**
- Date
- Component affected
- Symptoms
- Root cause
- Solution applied
- Prevention measures

---

## 7) File Organization Rules

### 7.1 Debug/Test Scripts

**Location:** `scripts/`

**Structure:**
```
scripts/
├── debug/          ← Debugging scripts
├── tests/          ← Manual test scripts
└── utils/          ← Utility scripts
```

**❌ DO NOT store at project root.**

### 7.2 Logs

**Location:** `logs/` (add to `.gitignore`)

**Naming:** `app.log`, `error.log`, `access.log`

---

## 8) Git Workflow

### 8.1 Commit Message

**Use Conventional Commits** (see `.github/git-commit-instructions.md`)

**Examples:**
```
feat(wizard): add database configuration step
fix(routes): prevent duplicate button rendering
refactor(api): extract validation into service layer
docs(readme): update installation instructions
```

### 8.2 Before Commit

```powershell
# 1. Run all checks
.\.venv\Scripts\ruff.exe check . 
.\.venv\Scripts\ruff.exe format --check . 
.\.venv\Scripts\mypy.exe backend/src
.\.venv\Scripts\pytest.exe

# 2. Update CHANGELOG. md

# 3. Verify file headers

# 4. Commit
git add .
git commit -m "feat(wizard): add step 6"
```

---

## 9) Common Pitfalls (Learn from History)

### 9.1 Design Errors

❌ **Duplicate buttons**
- **Issue:** Buttons defined in both wrapper and partials
- **Solution:** Keep buttons ONLY in partials
- **Prevention:** Review template structure before adding UI

❌ **Hardcoded text**
- **Issue:** Text not translatable, breaks i18n
- **Solution:** Always use `{{ t('key') or 'Fallback' }}`
- **Prevention:** Enable i18n linter (TODO)

❌ **Breadcrumb wrap**
- **Issue:** Responsive wrap makes UI inconsistent
- **Solution:** Fixed 2-line layout
- **Prevention:** Test on mobile viewport

### 9.2 Process Errors

❌ **Modify without killing servers**
- **Issue:** File locks, old code running
- **Solution:** Always kill before modification
- **Prevention:** Add to checklist (this file)

❌ **Test before finalizing**
- **Issue:** User sees errors
- **Solution:** AI tests thoroughly before asking user
- **Prevention:** Follow testing workflow (Section 4)

❌ **Use `python` directly**
- **Issue:** Doesn't work on Windows
- **Solution:** Always use `.\. venv\Scripts\python.exe`
- **Prevention:** PowerShell rules (`.github/powershell. instructions.md`)

### 9.3 Route Errors

(See `.github/incidents-history.md` for detailed history)

**General prevention:**
- Read incident history before changing routes
- Test both dev and prod modes
- Verify logs for warnings
- Check browser console

---

## 10) Emergency Procedures

### 10.1 Server Won't Stop

```powershell
# Try standard kill
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait
Start-Sleep -Seconds 2

# Verify
Get-Process python.exe -ErrorAction SilentlyContinue

# If still running, nuclear option
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

### 10.2 Port Won't Release

```powershell
# Find process
$pid = (Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue).OwningProcess

# Kill process
if ($pid) { Stop-Process -Id $pid -Force }

# Wait and verify
Start-Sleep -Seconds 2
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
```

### 10.3 Database Corrupted

```powershell
# Backup current (if needed)
Copy-Item "instance\filamenta.db" "instance\filamenta.db.backup"

# Delete corrupted
Remove-Item "instance\*. db" -Force

# Recreate with migrations
. \.venv\Scripts\flask. exe db upgrade

# Or start fresh (wizard will recreate)
.\.venv\Scripts\python. exe backend\src\app.py
```

---

## 11) Don'ts

- ❌ Modify routes without killing servers
- ❌ Skip testing in dev mode before prod
- ❌ Reuse failed routes without analysis
- ❌ Commit without running linters/tests
- ❌ Say "try it" before testing yourself
- ❌ Forget to update CHANGELOG. md
- ❌ Leave debug code in production
- ❌ Hardcode configuration (use env vars)

---

## 12) Quick Reference

| Task | Command |
|------|---------|
| **Kill servers** | `Get-Process python.exe \| Stop-Process -Force` |
| **Clean DB** | `Remove-Item "instance\*.db" -Force` |
| **Dev server** | `.\.venv\Scripts\python.exe backend\src\app.py` |
| **Prod server** | `.\.venv\Scripts\python.exe run_prod.py` |
| **Lint** | `.\.venv\Scripts\ruff.exe check .` |
| **Format** | `.\.venv\Scripts\ruff.exe format --check .` |
| **Type check** | `.\.venv\Scripts\mypy.exe backend/src` |
| **Tests** | `.\.venv\Scripts\pytest.exe -v` |

---

**See Also:**
- `.github/incidents-history.md` — Detailed incident history
- `.github/user-preferences.md` — User preferences
- `.github/powershell.instructions.md` — PowerShell commands
- `.github/copilot-instructions.md` — General rules