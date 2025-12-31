# AI Rules — Flask + HTMX + Bootstrap 5 (Monorepo)

**Purpose:** Central AI ruleset for code generation and modification  
**File:** `.github/copilot-instructions.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version: 2.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

**Metadata:**
- Status:  Stable
- Classification: Internal

**Notes:**
- This is the MAIN instruction file, always loaded by GitHub Copilot
- For domain-specific rules, see index in Section 12

---

## Table of Contents

1. [Principles](#1-principles)
2. [Security & Privacy](#2-security--privacy)
3. [Project Conventions](#3-project-conventions)
4. [Mandatory File Headers](#4-mandatory-file-headers)
5. [Code Comments & Documentation](#5-code-comments--documentation)
6. [Versioning Rules](#6-versioning-rules)
7. [Analysis Reports](#7-analysis-reports)
8. [CHANGELOG Rules](#8-changelog-rules)
9. [Testing Expectations](#9-testing-expectations)
10. [Legal / Attribution / License](#10-legal--attribution--license)
11. [CI/CD Rules](#11-cicd-rules)
12. [Domain-Specific Rules Index](#12-domain-specific-rules-index)
13. [Don'ts](#13-donts)
14. [If Unsure](#14-if-unsure)

---

## 1) Principles

- Prefer **clarity and correctness** over cleverness. 
- Keep changes **small, focused, and reviewable** (avoid "big-bang" refactors).
- Follow existing project conventions; if unclear, propose **2 options** with trade-offs.
- Do not introduce unused abstractions.  Build the simplest thing that fits. 

---

## 1.5) MANDATORY:  File Modification Verification (CRITICAL)

**BEFORE finishing ANY file modification, you MUST:**

1. ✅ **Re-read the ENTIRE file** after modification (not just the changed part)
2. ✅ **Validate syntax** (JSON, Python, XML, YAML, etc.)
3. ✅ **Check for missing/extra punctuation:**
   - Commas in JSON objects/arrays
   - Quotes (single, double, triple)
   - Parentheses, brackets, braces
   - Semicolons (if language-specific)
4. ✅ **Verify structure integrity:**
   - Proper nesting levels
   - Closing tags/braces match opening ones
   - No dangling commas or quotes
5. ✅ **Run validation commands** if applicable: 
   - JSON:  `py -c "import json; json.load(open('file.json'))"`
   - Python: `py -m py_compile file.py`
   - HTML/XML: Check for proper tag closure
6. ✅ **NEVER assume** a modification is correct without verification

**NO modification is considered complete** until all 6 steps above are done and verified.

**Cost of skipping this:** Hours of debugging simple syntax errors (missing commas, quotes, etc.)

---

## 2) Security & Privacy (non-negotiable)

- **Never** add secrets, tokens, passwords, API keys, or real credentials. 
- Read configuration from **environment variables** (with safe defaults for dev).
- Validate and sanitize **all inputs** (query params, form data, headers, JSON).
- Use **parameterized queries** (no string formatting for SQL).
- Don't log sensitive data (tokens, passwords, PII). Mask if needed. 
- Avoid insecure patterns: 
  - `eval`, `exec`, shell injection, unsafe subprocess calls
  - Trusting client-side values
  - Building HTML/JS from untrusted input without escaping

---

## 3) Project Conventions

- **Line length:**
  - **Python:** 88 (via Black)
  - **JS/TS:** 88 (via Prettier)
  - **HTML/CSS/JS:** 88 (via Prettier)
- Prefer deterministic code:  no random/time/network in tests unless mocked.
- Use UTF-8, LF line endings, and keep whitespace clean. 

---

## 4) Mandatory File Header (required for every file)

For **every file created or modified** (new or existing), add/maintain the following header **at the top of the file**
(using the comment syntax appropriate for the language). Keep it up to date.

**Header template:**

```
---
Purpose: <short purpose>
Description: <optional longer description>

File:  <relative/path/filename> | Repository: X-Filamenta-Python
Created: <YYYY-MM-DDTHH:mm:ss±HH:MM>
Last modified (Git): <YYYY-MM-DDTHH:mm:ss±HH:MM> | Commit: <short-sha>

Distributed by:  XAREMA | Coder:  AleGabMar
App version: <x.y.z> | File version: <x.y.z or revision>

License:  AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved. 

Metadata:
- Status: <Draft | Stable | Deprecated>
- Classification: <Public | Internal | Confidential>

Notes:
- Git history is the source of truth for authorship and change tracking. 
- If generated:  "Generated file — do not edit by hand."
---
```

### 4.1 Placement and Formatting Rules

- Use the correct comment style: 
  - **Python:** triple-quoted string at top of file (module docstring)
  - **JS/CSS:** block comment `/* ... */`
  - **HTML:** `<!-- ... -->`
  - **Markdown/YAML/TOML:** top-of-file comment style where possible; if not supported, add as a visible header section. 
- Keep the header **before** imports or code.
- Do not remove the header from existing files; update fields instead.

### 4.2 Fields Policy

- `File`: must be the repo-relative path. 
- `Repository`: use `X-Filamenta-Python`
- `Created`: set when the file is first created.
- `Last modified (Git)` and `Commit`: prefer to rely on git; if unavailable at generation time, use: 
  - `Last modified (Git): TBD | Commit: TBD`
    and let CI/maintainers fill it in later.
- If a file is generated, include the "Generated file — do not edit by hand." note. 
- Keep `Metadata` accurate (Draft/Stable/Deprecated; Public/Internal/Confidential).

---

## 5) Code Comments & Documentation (required)

### 5.1 Commenting Philosophy

- Comment **why**, not what (avoid stating the obvious).
- Use comments to capture **intent**, **constraints**, **trade-offs**, and **non-obvious behavior**.
- Keep comments up to date.  If code changes, update/remove stale comments.
- Prefer names and structure that reduce the need for comments.

### 5.2 Where to Comment

- Add short section headers in longer modules to show structure (e.g., `# ---- Validation ----`).
- Document public functions/classes with docstrings: 
  - what it does
  - inputs/outputs
  - important edge cases
  - exceptions / error behavior (if relevant)
- Comment non-trivial blocks: 
  - security checks
  - business rules
  - parsing/normalization
  - tricky HTMX flows / partial rendering logic

### 5.3 Variable Naming

- Use descriptive names (avoid `data`, `tmp`, `obj`).
- Make units explicit (`timeout_s`, `max_bytes`, `ttl_minutes`).
- Use consistent prefixes/suffixes: 
  - `is_*` for booleans
  - `*_id` for identifiers
  - `*_dt` or `*_at` for datetimes/timestamps

### 5.4 Template Comments (Jinja/HTML)

- Comment template sections and reusable blocks: 
  - `<!-- Header -->`, `<!-- Filters -->`, `<!-- Results list -->`
- For HTMX fragments, include a short comment describing: 
  - what the fragment is for
  - expected target/swap
  - required context variables

---

## 6) Versioning Rules (apps + files)

### 6.1 Default Starting Versions

- All apps and files start at:  **0.0.1-Alpha**
- Use this as the default for `App version` and `File version` until bumped. 

### 6.2 Version Format

Use Semantic Versioning compatible format: 

- `MAJOR.MINOR.PATCH` with optional pre-release suffix:  `-Alpha`, `-Beta`, `-RC`.

Examples:
- `0.0.1-Alpha`
- `0.1.0-Beta`
- `1.0.0`
- `2.0.0`

### 6.3 Bumping Rules (must follow)

- `v1.0.0` = **first stable release**
- `v2.0.0`, `v3.0.0`, … = **major change** (breaking changes, major redesign)
- `x.1.x` = **new feature** (minor bump)
- `x.x.1` = **bug/security fix** (patch bump)

Notes:
- Any breaking change requires a MAJOR bump and clear migration notes.
- Security fixes should prefer PATCH bumps unless behavior/API changes require MINOR/MAJOR. 

---

## 7) Analysis Reports (required)

For **each analysis** (audit, review, investigation, security/quality scan, root-cause, architectural decision),
the AI must create a **Markdown report** and save it under: 

- Folder: `Analysis_reports/`
- File extension: `.md`

### 7.1 Naming Convention

Use a timestamped filename (24h format) to avoid collisions:

`YYYY-MM-DD_HH-mm_<short-title>. md`

Examples:
- `2025-12-30_14-30_flask-error-handling-audit.md`
- `2025-12-30_14-30_htmx-fragment-review.md`

If timezone matters, include it in the report header. 

### 7.2 Report Content (minimum)

Each report must include: 
- Title + timestamp
- Context / goal
- Scope (files/modules/endpoints affected)
- Findings (bullets, prioritized)
- Decisions / recommendations
- Action items / next steps
- Risks & mitigations (if applicable)
- Commands to reproduce / verify (lint, tests, checks)
- References (links, issues, PRs) if available

### 7.3 Behavior

- Create the folder `Analysis_reports/` if missing.
- One report per analysis.  Do not overwrite older reports; create a new file per timestamp.
- Keep reports concise but complete (reviewable in PR).

---

## 8) CHANGELOG Rules (required)

### 8.1 Format

Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format with Semantic Versioning.

**Structure:**

```markdown
# CHANGELOG — X-Filamenta-Python

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features go here

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Any bug fixes

### Security
- Vulnerabilities fixed

## [X.Y.Z] - YYYY-MM-DD

(Released versions with same categories)
```

### 8.2 Categories (use only what applies)

- **Added** — for new features
- **Changed** — for changes in existing functionality
- **Deprecated** — for soon-to-be removed features
- **Removed** — for now removed features
- **Fixed** — for any bug fixes
- **Security** — in case of vulnerabilities

### 8.3 Update Rules

- **Always** update `CHANGELOG.md` when:
  - Adding a new feature
  - Fixing a bug
  - Changing behavior
  - Removing functionality
  - Security fixes
  - Version bumps

- **Where to add:**
  - Active development → `## [Unreleased]` section
  - Released version → Create new `## [X.Y.Z] - YYYY-MM-DD` section

### 8.4 Entry Format

- Use bullet points (-)
- Be concise but descriptive
- Link to issues/PRs when available
- Group related changes together
- Order:  most important first

**Examples:**

```markdown
### Added
- User authentication with JWT tokens (#42)
- Export to PDF feature for reports
- Dark mode toggle in preferences

### Fixed
- Correct SQL injection vulnerability in search endpoint (CVE-2025-1234) [SECURITY]
- Fix pagination bug when results < page size (#38)

### Changed
- **BREAKING:** API endpoint `/api/v1/users` now requires authentication
- Updated Bootstrap from 5.2 to 5.3
```

### 8.5 Version Release Process

When releasing a version: 
1. Move all `[Unreleased]` content to new version section
2. Add version number and date:  `## [X.Y.Z] - YYYY-MM-DD`
3. Update version in: 
   - `pyproject.toml`
   - `package.json`
   - File headers (`App version`)
4. Create empty `[Unreleased]` section at top
5. Commit with message: `chore: release vX.Y.Z`

### 8.6 Breaking Changes

- **MUST** be clearly marked with `**BREAKING:**` prefix
- **MUST** include migration guide or explanation
- **MUST** trigger MAJOR version bump (unless pre-1.0.0)

**Example:**

```markdown
### Changed
- **BREAKING:** Renamed `/api/users` to `/api/v2/users`
  Migration: Update all API calls to use new endpoint
```

### 8.7 Security Fixes

- Use `[SECURITY]` tag in title
- Include CVE number if applicable
- Link to security advisory if public
- Describe impact and affected versions

**Example:**

```markdown
### Security
- Fix SQL injection in search endpoint [SECURITY] (CVE-2025-1234)
  Affects: v0.1.0 to v0.2.3
  Severity: HIGH
```

### 8.8 Don'ts

- Don't use past tense ("Added feature" not "Add feature")
- Don't include internal refactoring unless user-facing
- Don't duplicate git commit messages
- Don't leave empty categories
- Don't forget to update CHANGELOG before release

---

## 9) Testing Expectations (pytest)

- Every behavior change should include tests: 
  - happy path + edge cases + error cases
- Tests must be **fast and deterministic**: 
  - No real network calls
  - Freeze/patch time when needed
- Prefer fixtures for setup. 
- For Flask: 
  - Use the test client
  - Assert status codes + minimal response content

**See:** `.github/python. instructions.md` for detailed testing rules.

---

## 10) Legal / Attribution / License (IMPORTANT)

### Copyright & License

- **License:** AGPL-3.0-or-later
- **SPDX-License-Identifier:** AGPL-3.0-or-later
- **Copyright:** © 2025 XAREMA. All rights reserved. 

### File Headers

- Preserve all existing author/copyright/license notices in current files.
- If you add a new file, include a header that follows the repository's template (see section 4).
- **Every file must include:**
  ```
  License: AGPL-3.0-or-later
  SPDX-License-Identifier: AGPL-3.0-or-later
  Copyright (c) 2025 XAREMA. All rights reserved. 
  ```

### User Interface Attribution

The application must display an author attribution accessible from the footer: 

- **Option A:** Direct text in the footer showing: 
  - Author:  AleGabMar
  - License: AGPL-3.0-or-later
  - Link to source code (repository)
- **Option B:** "Legal" or "About" link in the footer that displays the above information

**Example footer text:**

```
© 2025 AleGabMar. Licensed under AGPL-3.0-or-later.  [View source]
```

### Forks & Branding

- Do **not** hardcode "XAREMA" as branding everywhere.
- If you modify branding, **centralize it** via configuration (env var or config file).
- The **author attribution must remain** even if branding is changed. 
- Derivative works must include prominent notice of modifications.

### AGPL-3.0 Compliance

- If modifying this code and distributing it (including as SaaS), you **must**:
  - Make the source code available to users
  - Provide a link to the original source
  - Preserve all copyright and license notices
  - Include a notice of modifications
- For details, see:  https://www.gnu.org/licenses/agpl-3.0.html

---

## 11) CI/CD Rules (GitHub Actions)

### 11.1 Workflow Files

- Located in `.github/workflows/`
- Use descriptive names: `ci.yml`, `deploy.yml`, `security-scan.yml`
- Always test locally before committing (use `act` if possible)

### 11.2 Modification Rules

**BEFORE modifying any workflow:**
- Read existing workflow completely
- Understand current behavior
- Check if change affects other workflows (dependencies)
- Test with minimal change first

**NEVER:**
- Break existing jobs without team approval
- Remove security scans without justification
- Skip tests in CI (unless explicit temporary override)
- Commit workflows with secrets hardcoded

### 11.3 Required Checks

Every PR must pass:
- ✅ `ruff check . ` (Python linting)
- ✅ `ruff format --check .` (Python formatting)
- ✅ `mypy backend/src` (Type checking)
- ✅ `pytest` (All tests pass)
- ✅ `npm run lint` (Frontend linting)
- ✅ `npm run fmt -- --check` (Frontend formatting)
- ✅ `pip-audit` (Security scan — can continue on error)

### 11.4 Adding New Checks

When adding a new check:
- Add job to `ci.yml`
- Document purpose (comment in workflow)
- Set appropriate `continue-on-error` if not blocking
- Update this section with the new check

### 11.5 Dependabot Integration

- Configured in `.github/dependabot.yml`
- Auto-updates:  pip, npm, GitHub Actions
- Review Dependabot PRs within 1 week
- Test updates locally before merging

### 11.6 Workflow Maintenance

- Review workflows every 3 months
- Update actions to latest versions (via Dependabot)
- Remove obsolete jobs
- Document changes in CHANGELOG

---

## 12) Domain-Specific Rules Index

This file contains **general rules** applicable to all code.   
For **domain-specific rules**, see: 

| Domain | File | Auto-loaded for |
|--------|------|-----------------|
| **Python/Flask** | `.github/instructions/python.instructions.md` | `*.py` files |
| **Frontend (HTMX/Bootstrap/i18n)** | `.github/instructions/frontend.instructions.md` | `*.html`, `*.css`, `*.js` files |
| **PowerShell/Windows** | `.github/instructions/powershell.instructions.md` | PowerShell contexts + reference |
| **Workflow (routes, servers, tests)** | `.github/instructions/workflow-rules.md` | Manual reference |
| **User Preferences** | `.github/instructions/user-preferences.md` | Manual reference |
| **Git Commits** | `.github/instructions/git-commit-instructions.md` | Commit messages |

**Quick References:**
- **[All Instructions Index](./README.md)** - Complete overview
- **[Main Entry Point](../AI_INSTRUCTIONS.md)** - Root navigation file

**Agent Prompts:**
- Located in `.github/prompts/*.prompt.md`
- **[Interactive Reference](../prompts/index.html)** - Browse all 25+ prompts
- Use these for complex, multi-file modifications

**Incidents & Bug Tracking:**
- **[Incidents Directory](../../docs/incidents/)** - Organized by type (bugs, fixes, analysis)
- Use `report-bug.prompt.md` to create standardized bug reports

---

## 13) Don'ts

- Don't add new dependencies without a strong reason. 
- Don't mix formatting changes with logic changes unless requested.
- Don't change public interfaces without updating docs/tests.
- Don't leave TODOs without context or a tracking link. 

---

## 14) If Unsure

- Ask for clarification or propose a safe default. 
- Prefer minimal, reversible changes.
- Reference relevant `.instructions.md` files for guidance.

---

### Command Verification (CRITICAL)

**BEFORE suggesting ANY command to the user:**

1. ✅ **Verify the command syntax is correct** for the target environment (PowerShell on Windows 11)
2. ✅ **Test command logic mentally** (does it do what it claims?)
3. ✅ **Check file paths exist** (if referencing specific files)
4. ✅ **Validate tool availability** (e.g., `.venv\Scripts\ruff.exe` exists)

**IF a command might not work or you're uncertain:**

- ❌ **DO NOT** provide it without warning
- ✅ **WARN the user explicitly:**
  ```
  ⚠️ Note: This command may not work if [condition].  
  If it fails, try [alternative] instead.
  ```
- ✅ **Provide alternative(s)** immediately
- ✅ **Ask user to confirm** environment details if needed

**Example:**

```markdown
Run the following command: 

⚠️ **Note:** This assumes Ruff is installed in your venv.  If you get "command not found", install it first with:
`.venv\Scripts\pip. exe install ruff`

Command: 
`.venv\Scripts\ruff. exe check .`

**Alternative (if Ruff not installed):**
Skip this step and install Ruff first (see above).
```

**IF user reports a command failed:**

1. ✅ **Apologize** for the error
2. ✅ **Analyze why it failed** (ask for error message if not provided)
3. ✅ **Provide corrected command** with explanation
4. ✅ **Update the relevant `.instructions.md`** if it's a systemic issue
5. ✅ **Document in `.github/incidents-history.md`** if it caused significant confusion

---

### When to Create Bug Reports

**✅ CREATE for:**
- Unexpected production behavior
- Test failures revealing code issues
- Security vulnerabilities
- Performance degradation
- Data inconsistencies
- UI/UX issues affecting users

**❌ DO NOT create for:**
- Feature requests
- Questions/support
- Expected behavior
- Dev environment issues
- User error
- Intentional limitations

### Bug Tracking Files
- Individual Reports: `Analysis_reports/YYYY-MM-DD_HH-mm_bug-*. md`
- Centralized Log: `.github/incidents-history.md`
- GitHub Issues: Optional (team collaboration)

**END OF BUG REPORTING SECTION**

---

**End of Main Instructions**

**For specific tasks, always consult domain-specific `.instructions.md` files listed in Section 12.**
