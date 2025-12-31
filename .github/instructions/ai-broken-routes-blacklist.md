---
Purpose: Broken routes tracking (Internal Reference)
Description: Routes that have failed in the past - DO NOT USE THESE PATTERNS

File: .github/ai-broken-routes-blacklist.md | Repository: X-Filamenta-Python
Created: 2025-12-30T09:35:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Active
- Classification: Internal

Notes:
- NEVER use these route patterns
- If you must modify a route listed here, create an incident report first
- Last updated: 2025-12-30
---

# BLACKLIST: Routes That Have FAILED

## Routes That Caused Issues (DO NOT USE THESE PATTERNS)

### 1. `url_for("install.welcome")` (BROKEN - 2025-12-28)
- **Error:** `BuildError: Could not build url for endpoint 'install.welcome'`
- **Reason:** Route doesn't exist - should use `url_for("install.install_step")`
- **Status:** NEVER use "install.welcome"
- **Fix:** Use correct endpoint name

### 2. Route redirect loops (BROKEN - 2025-12-30)
- **Error:** "Firefox: redirecting request in a way that will never complete"
- **Reason:** Missing `instance/INSTALLED` flag file
- **Status:** Always check that flag exists before testing redirects
- **Fix:** Create `instance/INSTALLED` flag file

### 3. `/login` route (BROKEN - Status 404)
- **Issue:** Flask couldn't find `/login` route
- **Reason:** Auth routes are under `/auth/login` not `/login`
- **Status:** Use `/auth/login` endpoint
- **Fix:** Verify endpoint names match routes

---

## Routes That WORK (Safe to Use)

✅ `/auth/login` - GET: Login page display
✅ `/auth/login` - POST: Login form processing
✅ `/auth/logout` - POST: Logout
✅ `/` - Redirects to dashboard (auth) or login (no auth)
✅ `/install/step` - Installation wizard
✅ `/admin/*` - Admin panel routes

---

## When Adding New Routes

CHECKLIST:
1. [ ] Endpoint name matches `url_for()` calls
2. [ ] Route path is correct
3. [ ] HTTP method is correct (GET/POST)
4. [ ] Return statement is present
5. [ ] Test route exists before committing
6. [ ] Verify no circular redirects

---


