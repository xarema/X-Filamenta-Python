---
Purpose: Index of AI instructions for GitHub Copilot
Description: Central directory for all AI coding instructions and rules

File: .github/instructions/README.md | Repository: X-Filamenta-Python
Created: 2025-12-31T16:33:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

---

# 📚 AI Instructions Directory

## 🎯 Purpose

This directory contains all AI coding instructions, rules, and conventions for GitHub Copilot and AI agents working on the X-Filamenta-Python project.

## 📂 Organization

### Core Instructions

| File | Purpose | Auto-loaded for |
|------|---------|-----------------|
| **[copilot-instructions.md](./copilot-instructions.md)** | Main AI ruleset (principles, security, conventions) | All interactions |
| **[python.instructions.md](./python.instructions.md)** | Python/Flask-specific rules | `*.py` files |
| **[frontend.instructions.md](./frontend.instructions.md)** | HTMX/Bootstrap/i18n rules | `*.html`, `*.css`, `*.js` files |
| **[powershell.instructions.md](./powershell.instructions.md)** | PowerShell/Windows rules | PowerShell contexts |
| **[workflow-rules.md](./workflow-rules.md)** | Routes, servers, testing workflow | Manual reference |
| **[git-commit-instructions.md](./git-commit-instructions.md)** | Commit message conventions | Commit operations |
| **[user-preferences.md](./user-preferences.md)** | User coding preferences | Manual reference |

### Quick Reference

| File | Purpose |
|------|---------|
| **[ai-quick-rules.md](./ai-quick-rules.md)** | Quick reference for common patterns |
| **[ai-modification-checklist.md](./ai-modification-checklist.md)** | Pre-modification checklist |
| **[ai-reminder.md](./ai-reminder.md)** | Important reminders for AI agents |
| **[ai-broken-routes-blacklist.md](./ai-broken-routes-blacklist.md)** | Routes to avoid modifying |
| **[read-before-any-change.md](./read-before-any-change.md)** | Critical pre-change requirements |

## 🚀 Quick Start for AI Agents

### 1. **Starting a new task?**
   → Read: `copilot-instructions.md` (Section 12 for domain-specific rules index)

### 2. **Working with Python/Flask?**
   → Read: `python.instructions.md`

### 3. **Working with templates/frontend?**
   → Read: `frontend.instructions.md`

### 4. **Making commits?**
   → Read: `git-commit-instructions.md`

### 5. **Unsure about something?**
   → Read: `read-before-any-change.md` + `ai-reminder.md`

## 🔄 Cross-References

### From copilot-instructions.md

The main instructions file (Section 12) references all domain-specific files:
- Python/Flask → `python.instructions.md`
- Frontend (HTMX/Bootstrap) → `frontend.instructions.md`
- PowerShell → `powershell.instructions.md`
- Workflows → `workflow-rules.md`
- Git commits → `git-commit-instructions.md`
- User preferences → `user-preferences.md`

### Agent Prompts
For complex multi-file modifications, see: `../.github/prompts/`

## 📝 File Headers (Mandatory)

Every file in this directory must include the standard header:

```markdown
---
Purpose: <short purpose>
Description: <optional longer description>

File: .github/instructions/<filename> | Repository: X-Filamenta-Python
Created: <YYYY-MM-DDTHH:mm:ss±HH:MM>
Last modified (Git): <YYYY-MM-DDTHH:mm:ss±HH:MM> | Commit: <short-sha>

Distributed by: XAREMA | Coder: AleGabMar
App version: <x.y.z> | File version: <x.y.z>

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: <Draft | Stable | Deprecated>
- Classification: <Public | Internal | Confidential>
---
```

## 🔐 Security & Privacy

All instruction files follow these principles:
- ✅ Never contain secrets, tokens, or credentials
- ✅ Enforce input validation and sanitization
- ✅ Require parameterized queries (no SQL injection)
- ✅ Mandate security scans before release

See `copilot-instructions.md` Section 2 for details.

## 🎨 Code Conventions

Enforced across all instructions:
- **Line length:** 88 characters (Black/Prettier)
- **Encoding:** UTF-8 with LF line endings
- **Versioning:** Semantic Versioning (SemVer)
- **Testing:** pytest for Python, manual for frontend

## 📊 Version Control

All instruction files are versioned:
- **App version:** Tracks application version (e.g., `0.0.1-Alpha`)
- **File version:** Tracks instruction file version independently

## 🛠️ Maintenance

### Updating Instructions

1. Edit the relevant `.md` file
2. Update `Last modified` and `File version` in header
3. Update CHANGELOG.md with changes
4. Commit with message: `docs(instructions): [description]`

### Adding New Instructions

1. Create new `.md` file with standard header
2. Add entry to this README in appropriate section
3. Update `copilot-instructions.md` Section 12 if domain-specific
4. Commit with message: `docs(instructions): add [name]`

### Deprecating Instructions

1. Move file to `../.github/archives/`
2. Update status in header to `Deprecated`
3. Remove from this README
4. Add deprecation note in CHANGELOG.md

## 📖 Related Documentation

- **Prompts:** `../.github/prompts/` - Agent prompt templates
- **Incidents:** `../../docs/incidents/` - Bug tracking and incident history
- **Analysis Reports:** `../../Analysis_reports/` - Project analysis documentation

## 🔍 Search & Reference

**Find instructions by topic:**
```bash
# Search all instruction files
grep -r "keyword" .github/instructions/

# List all instruction files
ls -1 .github/instructions/*.md
```

**Common topics:**
- Security → `copilot-instructions.md` (Section 2)
- File headers → `copilot-instructions.md` (Section 4)
- Testing → `python.instructions.md` (Testing section)
- i18n → `frontend.instructions.md` (i18n section)
- Commits → `git-commit-instructions.md`

---

**Last Updated:** 2025-12-31  
**Total Instruction Files:** 12  
**Status:** Active
