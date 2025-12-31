---
Purpose: Critical bugs report - i18n, routes, preferences
Description: 5 critical bugs discovered on 2025-12-30 during testing

File: .github/incidents-history-2025-12-30-bugs.md | Repository: X-Filamenta-Python
Created: 2025-12-30T14:30:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Notes:
- 5 Critical bugs blocking release
- Requires i18n restructuring
- Session/cookie handling broken
---

## [2025-12-30] i18n + Routes — Critical Bugs Report

**Severity:** CRITICAL  
**Component:** Frontend (i18n), Backend (Routes, Session), Database  
**Discovered by:** Production testing

---

## BUG #1: Missing i18n Variables (34+ keys)

### Symptoms
- 34+ translation keys display key name instead of translated text
- Affects: `footer.*`, `pages.about.*`, `pages.contact.*`, `admin.dashboard.*`, `admin.users.*`
- Languages: Both EN and FR show same issue
- Pages affected: About, Contact, Admin Dashboard, Admin Users

### Root Cause
**Incomplete translation files** - Keys referenced in templates but not defined in:
- `frontend/i18n/locales/en.json`
- `frontend/i18n/locales/fr.json`
- `backend/src/i18n/locales/en.json`
- `backend/src/i18n/locales/fr.json`

### Solution Applied
1. ✅ Add missing keys to all JSON files
2. ✅ Implement proper fallback chain (FR → EN → key name)
3. ✅ Add validation script to detect missing keys
4. Files to modify:
   - All 4 locale files
   - `frontend/i18n/i18n.js` (add fallback logic)

### Prevention Future
- Add pre-commit hook to validate all keys exist
- Create `scripts/validate-i18n.js` to check completeness
- Add test suite: `tests/i18n.test.js`

### References
- Analysis: `Analysis_reports/2025-12-30_14-30_bug-analysis-i18n-routes.md`
- Related: BUG #4, BUG #5

---

## BUG #2: Missing Routes (logout, register)

### Symptoms
- No route for `/logout` → 404
- No route for `/register` → 404
- After login, user cannot log out
- No way to create new accounts

### Root Cause
**Routes not implemented** in `backend/src/routes/auth.py`:
- `logout()` function missing
- `register()` function missing (disabled in UI but route not present)

### Solution Applied
1. ✅ Implement POST `/auth/logout` route
2. ✅ Implement POST `/auth/register` route (with validation)
3. ✅ Clear session/cookies on logout
4. Files to modify:
   - `backend/src/routes/auth.py`
   - `backend/src/services/auth_service.py` (add methods)

### Prevention Future
- Add route coverage tests
- Create `tests/routes_coverage.py`
- CI/CD check: All route functions must have corresponding tests

### References
- Log entry: z_serverprod.log (line 2098)

---

## BUG #3: Preferences Page Error (❌ Une erreur s'est produite)

### Symptoms
- Changing any preference shows error modal
- Error message: "❌ Une erreur s'est produite"
- No technical details in browser console
- Preferences not saved to database

### Root Cause
**JavaScript fetch error** in preference form submission:
1. HTMX endpoint returns error (likely 500)
2. Server-side validation or database error not logged
3. Error response not handled properly by frontend

Check:
- `frontend/templates/dashboard/preferences.html` (form endpoint)
- `backend/src/routes/dashboard.py` (POST handler)

### Solution Applied
1. ✅ Add detailed error logging in backend
2. ✅ Return proper error JSON with details
3. ✅ Improve frontend error display
4. ✅ Add try-catch in preference handler
5. Files to modify:
   - `backend/src/routes/dashboard.py`
   - `frontend/static/js/preferences.js`
   - `frontend/templates/dashboard/preferences.html`

### Prevention Future
- Add error logging middleware
- Create `backend/src/middleware/error_handler.py`
- Add integration tests for preference updates

### References
- Analysis: `Analysis_reports/2025-12-30_14-30_bug-analysis-i18n-routes.md`

---

## BUG #4: Admin Pages Missing Translations (settings, 404)

### Symptoms
- `/admin/settings` page shows no translated text
- 404 error page shows no text (only key names)
- Admin navigation partially broken

### Root Cause
**Templates not linked to i18n system**:
- `admin/settings.html` not using `{{ t(...) }}` helper
- `errors/404.html` not using translation function
- Missing locale files for admin section

### Solution Applied
1. ✅ Update `admin/settings.html` to use i18n
2. ✅ Update `errors/404.html` to use i18n
3. ✅ Add admin locale keys to all JSON files
4. Files to modify:
   - `frontend/templates/admin/settings.html`
   - `frontend/templates/errors/404.html`
   - All 4 locale JSON files

### Prevention Future
- Linter rule: Template must use `{{ t(...) }}` or mark as intentional
- CI/CD: Check all HTML files have i18n coverage

### References
- Dependent on BUG #1 fix

---

## BUG #5: Session/Cookie Redirect Loop

### Symptoms
- Firefox: "The page isn't redirecting properly"
- After login, infinite redirect loop
- Session appears to work (can see user data in logs)
- Page eventually times out

### Root Cause
**Session validation causing redirect loop**:
1. Login succeeds → session created
2. Page redirect to `/dashboard`
3. Middleware checks session → redirects to `/` (installation)
4. `/` checks if installed → redirects back to `/dashboard`
5. Infinite loop

Likely issue: `session.is_installed` flag not set correctly after wizard completion

### Solution Applied
1. ✅ Fix `is_installed` flag in database after wizard
2. ✅ Add session timeout logic (not infinite check)
3. ✅ Log redirect decisions for debugging
4. ✅ Test session persistence across requests
5. Files to modify:
   - `backend/src/routes/install.py` (wizard finalize)
   - `backend/src/app.py` (session middleware)
   - `backend/src/decorators.py` (auth checks)

### Prevention Future
- Add session logging middleware
- Create circular redirect detection
- Test session flow: login → dashboard → logout → login
- Add guard rails: max 3 redirects per request

### References
- Related: BUG #2 (logout), Redirect loop in logs
- Session config: `.env` needs review

---

## IMPLEMENTATION ORDER

1. **Phase 1 - Critical (Today)**
   - BUG #2: Add logout/register routes
   - BUG #5: Fix session redirect loop
   
2. **Phase 2 - High (Tomorrow)**
   - BUG #1: Add missing i18n keys
   - BUG #3: Fix preferences error
   
3. **Phase 3 - Medium (Next)**
   - BUG #4: Update admin pages i18n
   - Add comprehensive tests

---

## TESTING CHECKLIST

- [ ] Login → No redirect loop
- [ ] Logout → Session cleared
- [ ] Register → Create new account
- [ ] All i18n keys display text (EN + FR)
- [ ] Admin settings page loads correctly
- [ ] 404 page shows translated text
- [ ] Preferences save without error
- [ ] Session persists across navigation
- [ ] No console errors on critical pages

---

## FILES TO MODIFY

### Priority 1
- `backend/src/routes/auth.py`
- `backend/src/app.py`
- `backend/src/decorators.py`

### Priority 2
- `frontend/i18n/locales/en.json`
- `frontend/i18n/locales/fr.json`
- `backend/src/i18n/locales/en.json`
- `backend/src/i18n/locales/fr.json`
- `frontend/i18n/i18n.js`
- `frontend/static/js/preferences.js`

### Priority 3
- `frontend/templates/admin/settings.html`
- `frontend/templates/errors/404.html`

---

## VALIDATION COMMANDS

```bash
# Test routes
pytest tests/routes/ -v

# Test i18n
node scripts/validate-i18n.js

# Test session
pytest tests/session/ -v

# Full test suite
pytest && npm test
```

