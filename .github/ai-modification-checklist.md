---
Purpose: Copilot modification checklist (Internal Reference)
Description: Rules AI must follow BEFORE EVERY modification - INTERNAL USE ONLY

File: .github/ai-modification-checklist.md | Repository: X-Filamenta-Python
Created: 2025-12-30T09:35:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Notes:
- MANDATORY: AI must complete ALL items before finishing ANY modification
- Failure to follow = INCIDENT REPORT REQUIRED
---

# AI MODIFICATION CHECKLIST (BEFORE EVERY CHANGE)

## PHASE 1: ANALYSIS (MANDATORY)

- [ ] Read ENTIRE `.github/copilot-instructions.md` (main rules)
- [ ] Read ENTIRE `.github/python.instructions.md` (Python rules)
- [ ] Read ENTIRE `.github/powershell.instructions.md` (PowerShell rules)
- [ ] Read ENTIRE `.github/user-preferences.md` (User preferences)
- [ ] Understand the FULL context of what will be modified
- [ ] Identify ALL files that might be affected
- [ ] Check `.github/incidents-history-*.md` for KNOWN BROKEN ROUTES/PATTERNS

## PHASE 2: VALIDATION (MANDATORY)

- [ ] Verify the modification won't break existing functionality
- [ ] Check if this pattern has been used successfully before
- [ ] Verify all dependencies/imports will work
- [ ] Test the FULL file after modification (not just the changed part)

## PHASE 3: EXECUTION (MANDATORY)

- [ ] Make the modification (ONE FILE AT A TIME)
- [ ] After each edit, RE-READ the ENTIRE file
- [ ] Check for syntax errors (missing commas, quotes, etc.)
- [ ] Check for missing imports or undefined variables

## PHASE 4: VERIFICATION (MANDATORY)

- [ ] Verify the file syntax is valid
- [ ] Run any applicable validation commands (py_compile, json validation, etc.)
- [ ] Check that the change actually solves the problem
- [ ] Ensure no new errors were introduced

## PHASE 5: DOCUMENTATION (MANDATORY)

- [ ] Create/update incident report if applicable
- [ ] Update CHANGELOG.md if change affects features
- [ ] Update file headers with new timestamp
- [ ] Document any known issues in incident history

## SPECIAL RULES

### Routes
- NEVER modify a route without verifying ALL related code first
- Check `.github/ai-broken-routes-blacklist.md` BEFORE touching a route
- If unsure about a route, CREATE AN INCIDENT REPORT instead

### Entry Points (run_prod.py, app.py)
- NEVER modify without reading the ENTIRE file first
- Test full application startup after any change
- Verify all imports resolve correctly

### Database Migrations
- NEVER modify without running alembic validation
- Always test against actual database

### Templates & Frontend
- NEVER add buttons/UI elements without asking user first
- ALL text must use i18n translation keys (NEVER hardcoded)
- ALL CSS classes must use Bootstrap conventions

---

## INCIDENT TRIGGERS

If ANY of these happen, STOP and CREATE AN INCIDENT REPORT:

- ❌ Route not found error appears in logs
- ❌ Import errors when starting app
- ❌ Database connection fails
- ❌ Template rendering fails
- ❌ Modification conflicts with previous fixes
- ❌ Code modification breaks existing functionality
- ❌ User reports different behavior than expected

---


