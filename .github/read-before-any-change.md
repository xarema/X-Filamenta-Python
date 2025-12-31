# ⚠️ READ BEFORE ANY CHANGE

**Purpose:** Mandatory checklist and synthesis before modifying the project  
**File:** `.github/read-before-any-change.md` | Repository:  X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder: AleGabMar  
**App version:** 0.0.1-Alpha | File version: 2.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 

**Metadata:**
- Status:  Stable
- Classification: Internal

**Notes:**
- Human entry point before ANY modification
- AI assistants:  Read this file FIRST when asked to modify the project

---

## 🚨 MANDATORY PROCESS BEFORE ANY MODIFICATION

### 1. STOP ALL SERVERS

```powershell
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

**Why:** Prevents file lock conflicts and ensures clean state.

---

### 2. READ THESE FILES (in order)

1. ✅ `.github/copilot-instructions.md` — General project rules
2. ✅ `.github/user-preferences.md` — User preferences
3. ✅ `.github/workflow-rules.md` — Workflow rules (if modifying routes/servers/tests)
4. ✅ Domain-specific `.instructions.md`:
   - `.github/python.instructions.md` (if modifying Python)
   - `.github/frontend.instructions.md` (if modifying HTML/CSS/JS)
   - `.github/powershell.instructions.md` (if running commands)
5. ✅ This file — Complete synthesis

---

### 3. ASK BEFORE ACTING

- ❌ **DO NOT** create new buttons/UI without asking
- ❌ **DO NOT** modify design without asking
- ❌ **DO NOT** change routes without consulting `workflow-rules.md`
- ✅ **ALWAYS** propose 2 options before structural modification

---

## 📋 CRITICAL RULES (Non-Negotiable)

### Translations (i18n)

- ✅ **NO hardcoded text in templates**
- ✅ **EVERYTHING must be in `backend/src/i18n/{fr,en}. json`**
- ✅ Use `{{ t('wizard.key') or 'Fallback' }}`

### Design & UI

- ✅ Wizard breadcrumb:  **ALWAYS 2 lines** (3 steps line 1, 2 steps line 2)
- ✅ Buttons: IN partials, NOT in `_wizard_content.html`
- ✅ Bootstrap 5 classes priority, custom CSS only if necessary
- ✅ Responsive design (mobile-first)

### Routes

- ❌ **NEVER reuse a failed route** (see `incidents-history.md`)
- ✅ Always test after modification
- ✅ Kill all servers before modification
- ✅ Check logs after restart

### Python Code

- ✅ Type hints mandatory
- ✅ Black formatting (88 chars)
- ✅ No direct `python`, always `.venv`
- ✅ PowerShell:  NO emoji in output

### Files

- ✅ Headers mandatory (see `copilot-instructions.md` section 4)
- ✅ Version 0.0.1-Alpha by default
- ✅ License: AGPL-3.0-or-later
- ✅ Debug/test files in `scripts/`, NOT at root

---

## 🔄 MODIFICATION WORKFLOW

### Before Starting

1. Kill servers (`Get-Process python.exe | Stop-Process -Force`)
2. Read relevant rules files
3. **ASK** for modification plan confirmation
4. Wait for user validation

### During Modification

1. Follow project conventions (Black, type hints, headers)
2. Add translations if new text
3. Test in dev mode first
4. Check errors with appropriate tools

### After Modification

1. Kill servers
2. Test in dev mode
3. Check logs
4. If OK → Test in prod mode
5. Check prod logs
6. **ONLY THEN** tell user to try

---

## 📝 ERRORS TO NEVER REPEAT (History)

### Design Errors

- ❌ Duplicate buttons (lines 167-170 `_wizard_content.html`) — **REMOVED**
- ❌ Breadcrumb on 1 line with wrap — **FIXED** (2 fixed lines)
- ❌ Hardcoded text without translation — **ALWAYS AVOID**

### Route Errors

(See `.github/incidents-history.md` for complete history)

### Process Errors

- ❌ Modify without killing servers → Conflicts
- ❌ Test before finalizing → User sees errors
- ❌ Use `python` directly → Doesn't work on Windows

---

## 🧪 MANDATORY TESTS

### Before Saying "It's Ready"

1. ✅ `ruff check .` — No lint errors
2. ✅ `ruff format --check .` — Format OK
3. ✅ `mypy backend/src` — Type checking OK
4. ✅ Dev server → Test complete wizard
5. ✅ Kill servers
6. ✅ Prod server → Test complete wizard
7. ✅ Verify user screenshots
8. ✅ **ALL** links/buttons work
9. ✅ **ALL** translations display

### If Any Test Fails

- ❌ **DO NOT** say "try it"
- ✅ **FIX** then **RE-TEST** until 100% pass

---

## 🎯 ESSENTIAL COMMANDS

### Kill Servers

```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### Launch Dev

```powershell
.\. venv\Scripts\python.exe backend\src\app.py
```

### Launch Prod

```powershell
.\.venv\Scripts\python.exe run_prod.py
```

### Lint & Format

```powershell
.\.venv\Scripts\ruff. exe check .
.\.venv\Scripts\ruff.exe format --check .
. \.venv\Scripts\mypy. exe backend/src
```

---

## 📚 COMPLETE REFERENCE FILES

| File | Content |
|------|---------|
| `.github/copilot-instructions.md` | Complete project rules (headers, versioning, CHANGELOG, etc.) |
| `.github/user-preferences.md` | User preferences (env, tests, workflow) |
| `.github/workflow-rules.md` | Workflow rules + incident history |
| `.github/powershell.instructions.md` | All PowerShell commands + server kill commands |
| `.github/python.instructions.md` | Python/Flask rules |
| `.github/frontend.instructions.md` | HTMX/Bootstrap/i18n rules |
| `.github/copilot-modes-reference.md` | Chat/Edit/Plan/Agent modes explained |
| `.github/intellij-setup.md` | IntelliJ IDEA configuration |
| `.github/incidents-history.md` | Complete incident history |
| `backend/src/i18n/fr. json` | French translations |
| `backend/src/i18n/en.json` | English translations |

---

## ✅ FINAL CHECKLIST BEFORE COMMIT

- [ ] All servers stopped
- [ ] Project rules re-read
- [ ] Modifications tested in dev
- [ ] Modifications tested in prod
- [ ] No lint/format/type errors
- [ ] All translations added
- [ ] File headers up to date
- [ ] CHANGELOG. md updated
- [ ] User screenshots verified
- [ ] User confirms everything works

---

**Last Updated:** 2025-12-30

**Note:** If you see this file, you MUST read it BEFORE any project modification. No exceptions.