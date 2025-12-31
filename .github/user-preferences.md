# User Preferences — Reference for AI

**Purpose:** Store user preferences and decisions for future AI reference  
**File:** `.github/user-preferences.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

**Metadata:**
- Status: Active (continuously updated)
- Classification: Internal

---

## 🎯 Environment & Execution

### Operating System
- **OS:** Windows 11
- **Shell:** PowerShell (pwsh or Windows PowerShell)
- **IDE:** IntelliJ IDEA (Ultimate recommended for Python + Web)

### Python / Commands
- ✅ **Always use `.venv`** for Python execution
- ❌ **NEVER use `python` directly** in PowerShell (not on PATH by default)
- ✅ **Full path required:** `.\.venv\Scripts\python.exe`
- ✅ **Or activate venv first:** `.\.venv\Scripts\Activate.ps1`

### PowerShell Output
- ❌ **NO emoji in commands/output** (formatting issues in PowerShell)
- ✅ Use clean text formatting only
- ✅ Use colors (`Write-Host -ForegroundColor`) if needed

---

## 📁 File Organization

### Debug / Test Files
- ✅ **NEVER store at project root**
- ✅ **Use dedicated folder:** `scripts/debug/` or `scripts/tests/`
- ✅ Keep root clean (only essential project files)

### Expected Structure
```
scripts/
├── debug/          ← Debugging scripts
├── tests/          ← Manual test scripts
└── utils/          ← Utility scripts (e.g., generate docs)
```

---

## 🧪 Testing Workflow

### Database Cleanup Before Tests
- **Preference:** ✅ **YES** — Always clean database to simulate fresh installation
- **Action:** Delete `instance/*. db` before wizard tests
- **When:** Testing first-run experience, wizard flow, fresh install scenarios

### Server Launch Modes

#### Phase 1: Development (Debug First)
- **Mode:** Development (`debug=True`)
- **Server:** Flask built-in dev server
- **Logs:** Verbose
- **Use for:** Debugging, identifying issues, initial testing

**Command:**
```powershell
.\.venv\Scripts\python. exe backend\src\app.py
```

#### Phase 2: Production (Final Validation)
- **Mode:** Production (`debug=False`)
- **Server:** Waitress WSGI
- **Logs:** Production-level
- **Use for:** Realistic testing, pre-deployment validation

**Command:**
```powershell
.\.venv\Scripts\python.exe run_prod.py
```

**Workflow:**
1. Test in dev mode first
2. If OK → Test in prod mode
3. Only after both pass → Ask user to test

### Test Script Preference
- **Preference:** ✅ **YES** — Create reusable test scripts
- **Location:** `scripts/tests/test_wizard_clean. py` or similar
- **Features:**
  - Automatic database cleanup
  - Server launch (dev or prod)
  - Clear instructions
  - Options for debug/prod mode

---

## 🔧 General Workflow Rules

### Before Any Modification
- ✅ **Always ask for confirmation** before making changes
- ✅ Read `.github/copilot-instructions.md` systematically
- ✅ Follow project conventions (Black, type hints, headers)
- ✅ Propose **2 options** when approach is unclear

### Debugging Approach
- ✅ Use best agent available (Plan for complex analysis)
- ✅ Backend AND Frontend debugging if needed
- ✅ Detailed logs + traceability
- ✅ Document findings in `Analysis_reports/`

### Communication Style
- ✅ Clear, structured explanations
- ✅ Step-by-step instructions when needed
- ✅ Always include context (why, not just what)
- ❌ No assumptions about unstated preferences

---

## 📚 Documentation Generation

### HTML Documentation
- **Script:** `scripts/utils/generate_html_docs.py`
- **Output:** `docs/HTML/` (146+ pages generated)
- **Includes:** All documentation + analysis reports
- **Dependencies:** `Markdown`, `Pygments`

**Generate:**
```powershell
.\.venv\Scripts\python.exe scripts\utils\generate_html_docs. py
```

**View:**
```powershell
# Default browser
Start-Process 'docs\HTML\index.html'

# Specific browser (Edge)
Start-Process microsoft-edge: file:///D:/xarema/X-Filamenta-Python/docs/HTML/index.html
```

**Install dependencies:**
```powershell
. \.venv\Scripts\pip. exe install Markdown Pygments
```

---

## 🎨 Design Preferences

### UI/UX
- **Framework:** Bootstrap 5 (utility-first)
- **HTMX:** Preferred over custom JavaScript
- **Responsive:** Mobile-first approach
- **Accessibility:** Semantic HTML, proper labels, ARIA when needed

### Wizard-Specific
- **Breadcrumb:** Always 2 fixed lines (3 steps + 2 steps)
- **Buttons:** In partials, NOT in wrapper template
- **Translations:** Mandatory for ALL text (no hardcoded text)

---

## 🌐 Internationalization (i18n)

### Languages
- **Supported:** French (fr), English (en)
- **Primary:** French
- **Fallback:** English

### Translation Rules
- ✅ Add to **BOTH** `fr.json` and `en.json` simultaneously
- ✅ Use descriptive keys: `wizard.step1.title`
- ✅ Always include fallback: `{{ t('key') or 'Fallback' }}`
- ✅ Validate JSON syntax before committing

---

## 🛠️ IntelliJ IDEA Preferences

### Plugins (Required)
- Python (official JetBrains)
- Jinja2 (template support)
- Database Tools (SQLite)
- PowerShell (syntax highlighting)

### Plugins (Optional/Recommended)
- GitHub Copilot
- Rainbow Brackets
- GitToolBox
- Markdown
- . ignore

### Configuration
- **Python interpreter:** `.venv\Scripts\python.exe`
- **Code style:** Black (88 chars)
- **Auto-format on save:** Yes
- **Terminal shell:** PowerShell

*(See `.github/intellij-setup.md` for complete configuration)*

---

## 📊 CI/CD Preferences

### Required Checks
- ✅ Ruff (linting + formatting)
- ✅ Mypy (type checking)
- ✅ pytest (all tests pass)
- ✅ pip-audit (security scan, can continue on error)
- ✅ Frontend linting (npm run lint)
- ✅ Frontend formatting (npm run fmt)

### Merge Policy
- **ALL checks must pass** before merge (except pip-audit if non-critical)
- Review Dependabot PRs within 1 week
- Test dependency updates locally before merging

---

## 📝 Historical Decisions

### 2025-12-28 — Wizard Testing Workflow
- **Q:** Clean DB before tests?  → **YES**
- **Q:** Launch mode?  → **Dev first, then Prod**
- **Q:** Create test script? → **YES**
- **Location:** `scripts/tests/`

### 2025-12-28 — File Organization
- **Q:** Where to store debug files? → **`scripts/debug/`**
- **Q:** Keep root clean? → **YES**

### 2025-12-30 — GitHub Copilot Structure
- **Q:** Instructions architecture? → **Option C (Hybrid)**
  - Main file: `copilot-instructions.md`
  - Context-specific:  `*.instructions.md` (auto-loaded)
  - Prompts: `.github/prompts/*. prompt. md`
- **Q:** File naming?  → **All lowercase**
- **Q:** Agent prompts? → **6 prompts created** (see Groupe 4)

---

## 🔄 Preferences to Add

*(Update this section as new preferences emerge)*

**To decide:**
- [ ] Preferred error handling strategy (global vs. local)
- [ ] Logging level preference (dev vs. prod)
- [ ] Performance monitoring tools
- [ ] Deployment platform (if any)

---

## 📌 Quick Reference

| Preference | Value |
|------------|-------|
| **OS** | Windows 11 |
| **Shell** | PowerShell |
| **IDE** | IntelliJ IDEA |
| **Python execution** | `.\.venv\Scripts\python.exe` |
| **Clean DB before tests** | YES |
| **Test phases** | Dev → Prod |
| **File organization** | `scripts/` subdirectories |
| **PowerShell emoji** | NO |
| **i18n fallback** | Mandatory |
| **Breadcrumb layout** | 2 fixed lines |

---

**This file is continuously updated as new preferences and decisions are made.**

**See Also:**
- `.github/copilot-instructions.md` — General project rules
- `.github/workflow-rules.md` — Workflow process
- `.github/intellij-setup.md` — IDE configuration