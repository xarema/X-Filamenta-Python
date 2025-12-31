---
Purpose: Main entry point for AI instructions - redirects to detailed instructions
Description: Short reference file pointing to organized instruction directory

File: .github/AI_INSTRUCTIONS.md | Repository: X-Filamenta-Python
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

# 🤖 AI Instructions for X-Filamenta-Python

## 📍 Quick Navigation

**All detailed AI instructions are now organized in:** [`instructions/`](./instructions/)

### 🎯 Start Here

**→ [Main Instructions Index](./instructions/README.md)** - Complete overview of all instructions

### 🚀 Quick Links

| What are you doing? | Read this file |
|---------------------|----------------|
| **Any coding task** | [instructions/copilot-instructions.md](./instructions/copilot-instructions.md) |
| **Python/Flask code** | [instructions/python.instructions.md](./instructions/python.instructions.md) |
| **HTML/CSS/JS/HTMX** | [instructions/frontend.instructions.md](./instructions/frontend.instructions.md) |
| **PowerShell scripts** | [instructions/powershell.instructions.md](./instructions/powershell.instructions.md) |
| **Git commits** | [instructions/git-commit-instructions.md](./instructions/git-commit-instructions.md) |
| **Testing/Workflows** | [instructions/workflow-rules.md](./instructions/workflow-rules.md) |
| **User preferences** | [instructions/user-preferences.md](./instructions/user-preferences.md) |

### ⚡ Essential Quick References

- **[Quick Rules](./instructions/ai-quick-rules.md)** - Common patterns
- **[Pre-Change Checklist](./instructions/ai-modification-checklist.md)** - Before modifying code
- **[Critical Reminders](./instructions/ai-reminder.md)** - Important notes
- **[Read Before Changes](./instructions/read-before-any-change.md)** - Mandatory reading

### 🎭 Agent Prompts

For complex multi-file tasks, use specialized prompts:

**→ [Prompts Directory](./prompts/)** - 27+ agent prompt templates  
**→ [Prompts Reference (HTML)](./prompts/index.html)** - Interactive searchable reference

### 📋 Incidents & Bugs

Bug reports and incident tracking:

**→ [Incidents Directory](../docs/incidents/)** - Organized by type (bugs, fixes, analysis)

---

## 📖 Quick Rules Summary

### ✅ Always Do
- Read `instructions/copilot-instructions.md` for main rules
- Check domain-specific instructions for your file type
- Follow file header requirements (Section 4)
- Update CHANGELOG.md for changes
- Run tests before committing

### ❌ Never Do
- Commit secrets or credentials
- Skip security validation
- Modify code without reading instructions
- Remove working code without justification
- Ignore existing conventions

---

## 🔄 Migration Notice

**Previous location:** Instructions were scattered in `.github/` root  
**New location:** Organized in `.github/instructions/` directory  
**Migration date:** 2025-12-31

All instruction files have been reorganized for better discoverability and maintainability.

---

## 📚 Documentation Structure

```
.github/
├── AI_INSTRUCTIONS.md          ← You are here (main entry point)
├── instructions/               ← All AI instructions (organized)
│   ├── README.md              ← Complete index
│   ├── copilot-instructions.md ← Main rules
│   ├── python.instructions.md
│   ├── frontend.instructions.md
│   └── ...
├── prompts/                    ← Agent prompt templates
│   ├── index.html             ← Interactive reference
│   └── *.prompt.md
└── workflows/                  ← GitHub Actions CI/CD

docs/
└── incidents/                  ← Bug tracking & incident history
    ├── README.md
    ├── bugs/
    ├── fixes/
    └── analysis/
```

---

**For full details, see:** [instructions/README.md](./instructions/README.md)
