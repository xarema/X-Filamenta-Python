---
name: "i18n-comprehensive-audit-and-fix.prompt"
version: "1.0.0"
description: "Complete audit and fixing of i18n (translation) system issues"
tags: ["i18n", "translations", "audit", "critical"]

---

# 🌍 Comprehensive i18n Audit and Fix

## 📋 Objective

Identify, analyze, and fix ALL translation-related bugs affecting:
- Missing translation keys
- Session language persistence
- Cache serialization errors  
- Admin pages missing translations
- Preferences save errors

## 🔍 Phase 1: Audit (Current State Analysis)

###1.1 Verify Translation Files Load

```bash
# Test: Load all translation files and report stats
python -c "
import json
import os

trans_dir = 'backend/src/i18n/translations'
for filename in sorted(os.listdir(trans_dir)):
    if filename.endswith('.json'):
        with open(os.path.join(trans_dir, filename)) as f:
            data = json.load(f)
            keys = len(json.dumps(data).split('.'))
            print(f'{filename}: {len(data)} root keys, ~{keys} total keys')
"
```

### 1.2 Find All Missing Translation Keys in Templates

```bash
# Extract all t('...') calls from templates
grep -rh "t('" frontend/templates/ | \
  grep -oE "t\('[^']+'\)" | \
  sed "s/t('//g; s/')//" | \
  sort | uniq > /tmp/used_keys.txt

# Compare with available keys
python -c "
import json
with open('backend/src/i18n/translations/en.json') as f:
    data = json.load(f)
    
# Flatten keys
def flatten(d, parent=''):
    keys = []
    for k, v in d.items():
        full_key = f'{parent}.{k}' if parent else k
        if isinstance(v, dict):
            keys.extend(flatten(v, full_key))
        else:
            keys.append(full_key)
    return keys

all_keys = flatten(data)
with open('/tmp/available_keys.txt', 'w') as f:
    f.write('\n'.join(sorted(all_keys)))
"

# Find missing keys
comm -23 /tmp/used_keys.txt /tmp/available_keys.txt
```

### 1.3 Test Session Language Persistence

```bash
# Check session configuration in app.py
grep -A 5 "SESSION_" backend/src/app.py | head -20

# Verify session directory exists
ls -la instance/sessions/ | head -5
```

### 1.4 Check Cache Service Configuration

```bash
# Review cache service code
grep -n "def set" backend/src/services/cache_service.py | head -5
grep -n "JSON serializable" -r backend/src/
```

### 1.5 Validate i18n Module Initialization

```bash
# Trace initialization flow
grep -n "init_translations" backend/src/app.py
grep -n "_translations =" backend/src/utils/i18n.py

# Check logging output
tail -20 z_serverprod.log | grep -i "lang\|translation\|i18n"
```

---

## ✅ Phase 2: Fix Implementation

### 2.1 Add Missing Translation Keys

**File:** `backend/src/i18n/translations/en.json`

**Action:** Add missing admin dashboard keys if not present:

```json
{
  "admin": {
    "dashboard": {
      "stats": {
        "errors": "System Errors",
        "visits": "Page Visits"  
      },
      "management": "Dashboard Management"
    }
  }
}
```

### 2.2 Fix Session Language Loading

**File:** `backend/src/app.py` (app.py line ~210)

**Ensure:**
- Session language is set on first request
- Language persists across requests
- Fallback to browser detection works

**Code to verify:**
```python
@app.context_processor
def inject_language() -> dict[str, object]:
    lang = session.get("lang")
    if not lang and _translations:
        lang = _translations.detect_browser_language()
        session["lang"] = lang
        session.modified = True
    return {"lang": lang or "en"}
```

### 2.3 Fix Cache Serialization

**File:** Identify which route/service sets User object in cache

**Replace:**
```python
# WRONG:
cache_service.set(f"user_{user.id}", user)

# CORRECT:
cache_service.set(f"user_{user.id}", {
    "id": user.id,
    "username": user.username,
    "email": user.email
})
```

### 2.4 Implement Missing Endpoints

**Routes to verify exist:**
- POST `/api/preferences` (save user preferences)
- POST `/api/settings` (save admin settings)

---

## 🧪 Phase 3: Testing & Validation

### Test 1: Translation Loading

```bash
python -c "
from backend.src.utils.i18n import _translations, init_translations
import os

init_translations(os.getcwd())
print(f'Loaded languages: {_translations.supported_langs}')
print(f'Sample translation: {_translations.get(\"auth.login.title\", \"en\")}')
"
```

### Test 2: Session Language Persistence

```bash
# Start server and manually test in browser:
1. Go to /login
2. Change language to FR (should set session["lang"] = "fr")
3. Navigate to /about
4. Verify French translation still applied
```

### Test 3: Cache Serialization

```bash
python -c "
from backend.src.services.cache_service import cache_service

# Test JSON serializable data
test_data = {'id': 1, 'name': 'Test'}
cache_service.set('test_key', test_data)
result = cache_service.get('test_key')
print(f'Cache works: {result == test_data}')
"
```

### Test 4: Admin Pages

```bash
# After login, test each admin page:
1. /admin → Dashboard with stats
2. /admin/users → User table with translations
3. /admin/settings → Settings form with labels
```

### Test 5: Error Pages

```bash
# Test translated error pages:
1. /nonexistent → 404 page (should show translated message)
2. Check console for no i18n errors
```

---

## 📊 Success Criteria

- [ ] All `t()` calls in templates return translated strings (not key names)
- [ ] Session language persists across page navigation
- [ ] No "Object of type User is not JSON serializable" errors
- [ ] Admin pages display with full translations (FR + EN)
- [ ] Preferences save successfully with AJAX
- [ ] Error pages display translated messages
- [ ] Browser language detection works (no manual lang set needed first time)
- [ ] All logs clean (no i18n-related warnings)

---

## 🔧 Debugging Commands

```bash
# Monitor live server output
tail -f z_serverprod.log | grep -i "lang\|translation\|cache\|error"

# Check specific translation key
python -c "
from backend.src.utils.i18n import _translations, init_translations
init_translations('.')
print(_translations.get('pages.about.security', 'en'))
"

# List all loaded translations
python -c "
from backend.src.utils.i18n import get_all_translations
en_trans = get_all_translations('en')
print('Root keys:', list(en_trans.keys()))
print('Admin keys:', list(en_trans.get('admin', {}).keys()))
"

# Start minimal test server
FLASK_APP=backend/src/app.py FLASK_DEBUG=1 flask run --port 5001
```

---

## 📝 Expected Outcome

✅ Application with:
- Complete i18n support (FR + EN fully functional)
- Session-persistent language selection
- No translation-related errors
- Clean admin interface with all translations
- Fully functional preferences and settings pages

---


