---
Purpose: Bug Report - Infinite Redirect Loop on Dashboard/Pages
Description: After successful installation, accessing the dashboard or feature page causes infinite redirect loop

File: Analysis_reports/2025-12-30_09-32_redirect-loop-bug.md | Repository: X-Filamenta-Python
Created: 2025-12-30T09:32:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal
- Severity: CRITICAL
- Priority: BLOCKER

---

## BUG REPORT: Infinite Redirect Loop

### Summary
After successful installation completion (finalize_install called), navigating to dashboard or pages causes Firefox to report "The page isn't redirecting properly - infinite redirect loop"

### Symptoms
1. Installation wizard completes successfully
2. User logs in successfully
3. When accessing `/dashboard` or `/features`, browser reports redirect loop
4. Server logs show repeated database queries but no errors
5. CSS/JS resources blocked by CSP

### Affected Code
- File: `backend/src/app.py` (line 248: `enforce_installation()`)
- File: `backend/src/routes/install.py` (line 525: `finalize_install()`)  
- File: `backend/src/services/install_service.py` (line 331: `mark_installed()`)

### Root Cause Analysis

**Hypothesis 1**: The `enforce_installation()` guard is working correctly:
- `installed.flag` file EXISTS ✅
- `InstallService.is_installed()` should return `True`
- Request paths like `/dashboard` should NOT trigger redirect

**Hypothesis 2**: There's a DIFFERENT redirect happening AFTER installation
- Possibly in `Flask-Login` or authentication middleware
- Possibly in `before_request` hooks
- Need to check ALL `@app.before_request` decorators

### Evidence
```
2025-12-30 09:32:47,489 [INFO] SELECT users.id ...  # Login attempt
2025-12-30 09:32:48,105 [INFO] SELECT users.id ...  # User lookup
[Repeated 20+ times with identical database queries]
[No ERROR logs - just repeated SELECTs and ROLLBACKs]
```

### Reproduction Steps
1. Start server: `python run_prod.py`
2. Complete installation wizard
3. Login with admin credentials
4. Click any nav link or try to access `/dashboard`
5. Observe: Infinite redirect loop in Firefox

### CSP Violations Noted
```
Content-Security-Policy: The page's settings blocked a style (style-src-elem) at 
https://unpkg.com/tabulator-tables@5.4.0/dist/css/tabulator.min.css
```
- Multiple external resource CDN URLs blocked
- This is SEPARATE from redirect issue but needs CSP update

### Investigation Needed
1. ✅ Check if `installed.flag` exists - YES
2. ❓ Run `InstallService.is_installed(project_root)` manually in debug mode
3. ❓ Trace ALL `before_request` hooks in execution order
4. ❓ Check if `user_loader` callback in Flask-Login has redirect logic
5. ❓ Review authentication decorators on dashboard/feature routes

### Proposed Fix (Pending Investigation)
1. Add debug logging to `enforce_installation()` to trace execution
2. Verify `is_installed()` returns `True` at runtime
3. Check for OTHER redirect-producing hooks
4. Possibly add redirect=False parameter to some decorators

### Next Steps
1. Add comprehensive logging to identify which hook is causing redirect
2. Run manual tests in debug mode
3. Check Flask-Login user_loader callback
4. Verify authentication flow is not causing circular redirects

---

## FILES AFFECTED
- backend/src/app.py
- backend/src/routes/install.py  
- backend/src/services/install_service.py
- backend/src/routes/auth.py (likely - check user_loader)

## TEST COMMANDS
```bash
# Manual verification
python -c "from backend.src.services.install_service import InstallService; print(InstallService.is_installed('.'))"

# Debug logging
FLASK_DEBUG=1 python run_prod.py
```

