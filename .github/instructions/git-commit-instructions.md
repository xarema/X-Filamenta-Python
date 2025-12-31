# Git Commit Instructions — Conventional Commits

**Purpose:** Git commit message format and conventions  
**File:** `.github/git-commit-instructions.md` | Repository:  X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 

**Metadata:**
- Status:  Stable
- Classification: Internal

---

## Format

Use [Conventional Commits](https://www.conventionalcommits.org/) with optional scope. 

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

---

## Types

| Type | Description | When to Use |
|------|-------------|-------------|
| `feat` | New feature | Adding new functionality |
| `fix` | Bug fix | Fixing a bug |
| `refactor` | Code refactoring | Restructuring code without changing behavior |
| `perf` | Performance improvement | Optimizing performance |
| `test` | Adding/updating tests | Test-related changes |
| `docs` | Documentation | README, comments, docstrings |
| `chore` | Maintenance | Dependencies, build config, tooling |
| `build` | Build system | Webpack, npm scripts, Make |
| `ci` | CI/CD changes | GitHub Actions, CI config |
| `style` | Code style | Formatting, whitespace (no logic change) |
| `revert` | Revert previous commit | Undoing a commit |

---

## Scopes (Optional but Recommended)

Use scopes to indicate which part of the project is affected. 

**Common scopes:**
- `backend` — Backend code (Flask, services, models)
- `frontend` — Frontend code (templates, CSS, JS)
- `templates` — Jinja2 templates specifically
- `api` — API routes/endpoints
- `auth` — Authentication/authorization
- `wizard` — Installation wizard
- `i18n` — Internationalization/translations
- `deps` — Dependencies
- `ci` — CI/CD workflows
- `db` — Database models/migrations
- `tests` — Test files
- `docs` — Documentation

**Examples:**
```
feat(wizard): add database configuration step
fix(api): prevent null pointer in user endpoint
refactor(backend): extract validation into service layer
docs(readme): update installation instructions
chore(deps): upgrade Flask to 3.0.0
```

---

## Subject Line Rules

1. **Use imperative mood** (present tense)
   - ✅ "add feature" (not "added feature" or "adds feature")
   - ✅ "fix bug" (not "fixed bug")
   
2. **No period at the end**
   - ✅ `feat: add user authentication`
   - ❌ `feat: add user authentication. `

3. **Max ~72 characters**
   - Keep it concise
   - Details go in the body

4. **Capitalize first letter**
   - ✅ `feat: Add user profile page`
   - ❌ `feat: add user profile page`

---

## Body (Optional)

**When to add a body:**
- Complex changes that need explanation
- Breaking changes
- Multiple related changes
- Context about WHY (not just WHAT)

**Format:**
- Separate from subject with blank line
- Use bullet points for multiple items
- Explain motivation and context
- Max ~72 chars per line

**Example:**

```
refactor(api): extract validation into service layer

- Moved all validation logic from routes to user_service. py
- Added custom exceptions (ValidationError, UserNotFoundError)
- Updated tests to cover service layer
- Routes are now thin (just HTTP handling)

This improves testability and separation of concerns.
```

---

## Footer (Optional)

**Use for:**
- Breaking changes (REQUIRED)
- Issue references
- Co-authors

**Breaking changes:**

```
feat(api): change user endpoint response format

BREAKING CHANGE: /api/users now returns array under "data" key instead of root. 
Migration:  Update API clients to access response. data instead of response directly.
```

**Issue references:**

```
fix(auth): prevent session hijacking

Fixes #123
Closes #456
Related to #789
```

**Co-authors:**

```
feat(wizard): add step 6

Co-authored-by: John Doe <john@example.com>
```

---

## Examples

### Simple Feature

```
feat(wizard): add network configuration step
```

### Bug Fix with Scope

```
fix(frontend): prevent double submit on HTMX forms
```

### Refactoring with Body

```
refactor(api): extract validation into service layer

- Moved validation logic to user_service.py
- Routes now delegate to service layer
- Improved testability and separation of concerns
```

### Breaking Change

```
feat(api): migrate to v2 endpoints

BREAKING CHANGE: All endpoints now prefixed with /api/v2/ instead of /api/. 
Migration: Update all API calls to use new prefix. 

Closes #100
```

### Documentation

```
docs(readme): add development setup instructions
```

### Dependencies

```
chore(deps): upgrade Flask to 3.0.0
```

### Multiple Changes (use body)

```
feat(wizard): improve step navigation

- Add breadcrumb with 2-line layout
- Add "Previous" button to all steps except first
- Add progress indicator (X of Y steps)
- Persist step data in session

Closes #42
```

---

## Special Cases

### Security Fixes

**Use `fix` type with `[SECURITY]` tag:**

```
fix(auth): prevent SQL injection in login endpoint [SECURITY]

- Migrated to parameterized queries
- Added input validation
- Updated tests with injection attempts

Fixes CVE-2025-1234
```

### Hotfixes

**Use appropriate type (`fix`, `refactor`, etc.) with urgency note:**

```
fix(api): critical null pointer in payment processing

URGENT: Production hotfix for payment failures.
Root cause: Missing null check in transaction validation. 

Fixes #999
```

### Reverts

```
revert: feat(wizard): add step 6

This reverts commit abc123def456.
Reason: Breaking production wizard flow, needs redesign.
```

---

## Commit Workflow

### Before Committing

```powershell
# 1. Stage changes
git add .

# 2. Review staged changes
git status
git diff --staged

# 3. Run checks (see below)

# 4. Commit with conventional message
git commit -m "feat(wizard): add database config step"
```

### Pre-Commit Checks (Recommended)

```powershell
# Linting
. venv\Scripts\ruff. exe check .

# Formatting
.venv\Scripts\ruff.exe format --check .

# Type checking
.venv\Scripts\mypy. exe backend/src

# Tests
.venv\Scripts\pytest.exe

# Frontend (if applicable)
npm run lint
npm run fmt -- --check
```

**ALL should pass before committing.**

---

## Multi-Line Commits

**Use editor for complex commits:**

```powershell
# Opens editor (Notepad, VS Code, vim, etc.)
git commit

# Then write multi-line message:
```

**In editor:**

```
feat(api): add user authentication with JWT

- Implemented JWT token generation and validation
- Added login and logout endpoints
- Added @require_auth decorator for protected routes
- Updated tests with authentication scenarios
- Added documentation for authentication flow

Breaking change: All protected endpoints now require Authorization header. 
Migration: Add "Authorization:  Bearer <token>" header to API requests. 

Closes #50
Closes #51
Related to #52
```

---

## Common Mistakes

### ❌ Wrong

```
# Missing type
Added new feature

# Past tense
feat:  added user profile

# Period at end
feat:  add user profile. 

# Too vague
fix:  bug fix

# Not capitalized
feat:  add feature

# Missing scope (when it would help)
feat: add step 6
```

### ✅ Correct

```
feat(wizard): add user profile step

fix(api): prevent null pointer in user endpoint

refactor(backend): extract service layer

docs(readme): add API documentation

chore(deps): upgrade dependencies
```

---

## Tooling (Optional)

### Commitizen (helps write conventional commits)

```powershell
# Install
. venv\Scripts\pip.exe install commitizen

# Use interactive commit
. venv\Scripts\cz. exe commit
```

### Commit Message Linting (CI/CD)

**Add to `.github/workflows/ci.yml`** (optional):

```yaml
- name: Check commit message format
  run: |
    # Use commitlint or similar tool
    npx commitlint --from HEAD~1 --to HEAD --verbose
```

---

## Summary

**Quick reference:**

```
<type>(<scope>): <subject>

[body]

[footer]
```

**Types:** feat, fix, refactor, perf, test, docs, chore, build, ci, style  
**Scopes:** backend, frontend, api, auth, wizard, deps, ci, etc.  
**Subject:** Imperative, capitalized, no period, ~72 chars  
**Body:** Optional, explain WHY, use bullets  
**Footer:** Breaking changes, issue refs, co-authors

---

**See Also:**
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- `.github/copilot-instructions.md` — General project rules
- `.github/workflow-rules.md` — Pre-commit workflow

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.