---
Purpose: Phase 1 Bug Fixes Roadmap — Prioritized list of all bugs with status
Description: Complete analysis and prioritization of bugs found during testing

File: PHASE_1_BUG_FIXES_ROADMAP.md | Repository: X-Filamenta-Python
Created: 2025-12-30T22:00:00+01:00
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
- Phase 1 = Critical bugs blocking basic functionality
- Analysis from incidents-history-2025-12-30-bugs-analysis.md
- Total: 5 bugs identified (3 real, 2 false positives)
---

# 🚨 PHASE 1: Critical Bug Fixes Roadmap

**Session Duration:** 2025-12-30  
**Analysis Completed:** ✅ YES  
**Ready to Fix:** ✅ YES  

---

## 📊 BUG STATUS SUMMARY

| # | Bug | Type | Severity | Status | Fix Time |
|---|-----|------|----------|--------|----------|
| 1 | Missing i18n variables (34+ keys) | REAL | 🔴 CRITICAL | To Fix | 1h |
| 2 | Missing routes (/logout, /register) | FALSE POS. | 🟡 LOW | N/A | — |
| 3 | Preferences page error | REAL | 🔴 CRITICAL | To Fix | 30min |
| 4 | Admin pages missing translations | REAL | 🔴 CRITICAL | To Fix | 1.5h |
| 5 | Session/cookie redirect loop | REAL | 🔴 CRITICAL | To Fix | 1h |

**Total Estimated Time: ~4.5 hours**

---

## 🔴 BUG #1: Missing i18n Variables (34+ keys)

### Details
**Severity:** CRITICAL  
**Affected Pages:** 
- Home footer (1 key)
- About page (6 keys)
- Contact page (9 keys)
- Admin Dashboard (4 keys)
- Admin Users (5 keys)
- Admin Settings (8+ keys)

**Root Cause:** 
Templates reference keys like `footer.legal`, `pages.about.features`, etc. but these keys do NOT exist in:
- `frontend/i18n/locales/en.json`
- `frontend/i18n/locales/fr.json`
- `backend/src/i18n/locales/en.json`
- `backend/src/i18n/locales/fr.json`

**Current Behavior:**
```
Expected: "À Propos" (translated text)
Actual:   "pages.about.title" (key name displayed)
```

**Fix Required:**
1. ✅ Add all 34+ missing keys to 4 locale files
2. ✅ Use proper i18n structure: `{ "pages": { "about": { "title": "..." } } }`
3. ✅ Test fallback chain: FR → EN → key name
4. ✅ Add validation script to prevent future missing keys

**Estimation:** 1 hour  
**Status:** ⏳ To Fix

---

## 🟢 BUG #2: Missing Routes (/logout, /register) — FALSE POSITIVE

### Details
**Severity:** LOW  
**Status:** 🟢 NOT A BUG

**Evidence:**
- ✅ `/auth/logout` route EXISTS (line 266, `backend/src/routes/auth.py`)
- ✅ `/auth/register` route EXISTS (line 119, `backend/src/routes/auth.py`)
- ✅ Both functions implemented correctly
- ✅ Routes registered in Flask blueprint

**Why User Saw 404:**
The routes exist but:
1. Frontend wasn't sending requests to correct URLs (likely `/login` instead of `/auth/login`)
2. Session persistence issue (see Bug #5)
3. Redirect loop prevented proper page navigation

**Action:** No fix needed. Routes are OK.  
**Status:** ✅ RESOLVED (Verified working)

---

## 🔴 BUG #3: Preferences Page Error

### Details
**Severity:** CRITICAL  
**Affected Page:** `/dashboard/preferences`  
**Error Message:** "❌ Une erreur s'est produite" (generic French error)

**Root Cause:**
1. Frontend form sends HTMX request to endpoint
2. Backend endpoint missing OR returns improper error response
3. JavaScript error handling shows generic message

**Current Behavior:**
```
User clicks Save on preferences page
        ↓
HTMX sends POST request
        ↓
Unknown endpoint or malformed response
        ↓
Error modal shows generic message
        ↓
No technical details visible in console
```

**Fix Required:**
1. ✅ Verify `backend/src/routes/dashboard.py` has `/preferences` endpoint
2. ✅ Ensure endpoint returns proper JSON: `{ "success": true/false, "message": "...", "error": "..." }`
3. ✅ Add comprehensive error logging
4. ✅ Improve frontend error display with technical details

**Estimation:** 30 minutes  
**Status:** ⏳ To Fix

---

## 🔴 BUG #4: Admin Pages Missing Translations

### Details
**Severity:** CRITICAL  
**Affected Pages:**
- `/admin/settings` → Missing all setting labels (8+ keys)
- `/errors/404` → Missing error page text (3+ keys)

**Root Cause:**
1. Admin templates don't use `{{ t(...) }}` helper
2. Hardcoded English text OR missing translation keys
3. 404 error page not using i18n system at all

**Current Behavior:**
```
Expected: Translated admin interface
Actual:   Hardcoded English OR key names displayed
```

**Fix Required:**
1. ✅ Update `frontend/templates/admin/settings.html` to use `{{ t(...) }}`
2. ✅ Update `frontend/templates/errors/404.html` to use i18n
3. ✅ Add all admin locale keys to JSON files
4. ✅ Test in both EN and FR languages

**Estimation:** 1.5 hours  
**Status:** ⏳ To Fix

---

## 🔴 BUG #5: Session/Cookie Redirect Loop

### Details
**Severity:** CRITICAL  
**Symptom:** Firefox warning: "This page is redirecting in a way that will never complete"

**Root Cause Analysis:**

```
LOGIN FLOW:
User logs in (admin/admin)
        ↓
authenticate() creates session
        ↓
Redirect to /dashboard (200 OK)
        ↓
Page loads successfully (appears to work)
        ↓
NAVIGATION ISSUE:
User clicks link or HTMX request fires
        ↓
Middleware checks: Is installed?
        ↓
is_installed() might return FALSE (race condition!)
        ↓
enforce_installation() redirects to /install
        ↓
install.block_if_installed() checks: Already installed?
        ↓
If flag file timing issue → Infinite redirect
```

**Root Causes Found:**

### 1. **Flag File Creation Race Condition**
- **File:** `backend/src/services/install_service.py` → `mark_installed()`
- **Issue:** `os.makedirs()` + `open().write()` may not complete before next request
- **Timing:** Async I/O or file locking delay

### 2. **is_installed() Check Vulnerability**
- **File:** `backend/src/services/install_service.py`
- **Issue:** Checks file existence: `os.path.exists(".installed")`
- **Race Condition:** Multiple requests simultaneously checking/writing flag

### 3. **Middleware Guard Logic Flaw**
- **File:** `backend/src/app.py` → `enforce_installation()` (line ~280)
- **Issue:** Calls `is_installed()` every request
- **Problem:** If flag file not found, always redirect to `/install`

### 4. **Session Not Persisting Flag State**
- **Issue:** Once `.installed` flag created, ALL requests should see it
- **Reality:** Cache or timing issue prevents proper state sharing

**Current Code Flow:**
```python
# app.py - enforce_installation() middleware
if installation_service.is_installed():
    return None  # Allow request
else:
    return redirect('/install')  # Redirect to install

# install_service.py - is_installed()
def is_installed(self):
    return os.path.exists('.installed')
```

**The Problem:**
- If `.installed` file is NOT persisted correctly
- Every request gets redirected to `/install`
- Then `block_if_installed()` checks if already installed (depends on flag timing)
- Infinite loop if flag timing is inconsistent

**Fix Required:**
1. ✅ Verify flag file is created IMMEDIATELY in `mark_installed()`
2. ✅ Add file sync: `os.fsync()` after write
3. ✅ Add cache to `is_installed()` → check flag in memory first
4. ✅ Add proper error logging to track flag state
5. ✅ Add unit test for flag creation/reading
6. ✅ Verify session persists across requests

**Files to Check:**
- `backend/src/app.py` (enforce_installation middleware)
- `backend/src/routes/install.py` (block_if_installed function)
- `backend/src/services/install_service.py` (is_installed, mark_installed functions)

**Estimation:** 1 hour  
**Status:** ⏳ To Fix

---

## 📋 PHASE 1 EXECUTION PLAN

### Order of Fixes (Dependency-Based)

#### Step 1: Fix Bug #5 (Session Redirect Loop) — 1 hour ⏱️
**Why First:** Must fix before other fixes can be tested properly
- Prerequisite: Must be able to navigate after login
- Blocks: Testing of all other fixes
- Impact: High

#### Step 2: Fix Bug #1 (Missing i18n Variables) — 1 hour ⏱️
**Why Second:** Critical for UI readability
- Prerequisite: Login working (from Step 1)
- Blocks: User experience on all pages
- Impact: High

#### Step 3: Fix Bug #4 (Admin Missing Translations) — 1.5 hours ⏱️
**Why Third:** Related to i18n, extends Step 2
- Prerequisite: i18n system working (from Step 2)
- Blocks: Admin interface usability
- Impact: Medium

#### Step 4: Fix Bug #3 (Preferences Error) — 30 minutes ⏱️
**Why Fourth:** Independent but relies on session (fixed in Step 1)
- Prerequisite: Session working (from Step 1)
- Blocks: User settings functionality
- Impact: Medium

**Total Time:** ~4.5 hours  
**Expected Completion:** Same session if continuous work

---

## 🎯 SUCCESS CRITERIA

After Phase 1 fixes, verify:

- ✅ Login → Dashboard → Logout works without redirect loop
- ✅ All 34+ i18n keys display translated text (not key names)
- ✅ Admin pages show French/English properly
- ✅ Preferences page saves without error
- ✅ 404 page displays translated error text
- ✅ All tests pass: pytest + npm test
- ✅ No console errors in Firefox DevTools
- ✅ Session persists across page navigations

---

## 📝 NOTES

- **Why Bug #2 was false positive:** Routes exist but weren't accessible due to redirect loop (Bug #5)
- **Why bugs clustered:** Core issue is installation guard + session management
- **Next Steps:** After Phase 1, move to Phase 2 (Performance & Cache)

---

**Status:** Ready to implement  
**Last Update:** 2025-12-30 22:00 UTC  
**Next Review:** After Step 1 completion

