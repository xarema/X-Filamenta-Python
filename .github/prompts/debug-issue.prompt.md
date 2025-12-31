---
mode: "agent"
description: "Debug and fix issues (bugs, errors, failures) with systematic approach and root cause analysis"
---

# Debug Issue

**Task:** Systematically debug and fix an issue (bug, error, test failure) using root cause analysis and best practices.

---

## Input Required

### Issue Description
${input: issue: Describe the issue (error message, unexpected behavior, etc.)}

### Issue Type
${input:type:Issue type?   (bug|error|test-failure|performance|security)}

### Severity
${input:severity: Severity?   (critical|high|medium|low)}

### Where Does It Occur
${input:location:Where?   (route|service|model|template|test|deployment)}

### Steps to Reproduce
${input:reproduce:Steps to reproduce (if known)}

### Expected vs Actual
${input:expected: Expected behavior vs actual behavior}

### Environment
${input:environment:Environment?   (dev|prod|test|docker|cpanel)}

---

## MANDATORY:   Pre-Debug Process

### 1. Gather Information

**Collect all relevant data:**

#### A. Error Messages

```
Full error trace:  
Traceback (most recent call last):
  File "backend/src/routes/auth.py", line 45, in verify_email
    result = EmailService. verify_token(token)
  File "backend/src/services/email_service.py", line 78, in verify_token
    data = serializer.loads(token, max_age=app.config['EMAIL_VERIFICATION_EXPIRY'])
AttributeError: 'NoneType' object has no attribute 'config'
```

**Extract:**
- Exception type:  `AttributeError`
- Error location: `email_service.py:78`
- Root cause hint: `'NoneType' object` → `app` is `None`

#### B.  Logs

```powershell
# Check application logs
Get-Content logs/app.log -Tail 50

# Check error logs
Get-Content logs/error.log -Tail 50

# Check server logs (if deployed)
ssh user@server "tail -50 /var/log/nginx/error.log"
```

#### C. Recent Changes

```powershell
# What changed recently? 
git log --oneline --since="3 days ago"

# What files were modified?
git diff HEAD~5 --name-only
```

#### D. Environment Variables

```powershell
# Check . env file
cat .env

# Verify critical variables
echo $FLASK_SECRET_KEY
echo $DATABASE_URL
```

---

### 2. Reproduce the Issue

**Create minimal reproduction:**

```python
# test_reproduce_issue.py
"""
Minimal reproduction of issue #123

Issue: AttributeError when verifying email token
Severity: High
"""
import pytest
from backend.src import create_app
from backend.src.services.email_service import EmailService
from backend.src.models.user import User

def test_reproduce_email_verification_error():
    """Reproduce AttributeError in verify_token."""
    app = create_app('testing')
    
    with app.app_context():
        user = User(id=1, email="test@example.com")
        token = EmailService.generate_verification_token(user)
        
        # This should fail with AttributeError
        result = EmailService.verify_token(token)
        
        # If we get here, issue is fixed
        assert result['success'] is True
```

**Run reproduction:**

```powershell
pytest test_reproduce_issue.py -v
```

**Expected result:**
- Test **fails** with same error (issue reproduced)
- Or test **passes** (issue NOT reproduced → investigate why)

---

## Debug Workflow

### Step 1: Root Cause Analysis (5 Whys)

**Example:  AttributeError in email verification**

```markdown
# Root Cause Analysis - Issue #123

**Issue:** AttributeError:  'NoneType' object has no attribute 'config'

**5 Whys:**

1. **Why does error occur?**
   → Because `app` is `None` when calling `app.config['EMAIL_VERIFICATION_EXPIRY']`

2. **Why is `app` None?**
   → Because `current_app` proxy is not available outside request context

3. **Why is current_app not available?**
   → Because `verify_token()` is called from background task / CLI / test without app context

4. **Why wasn't this caught earlier?**
   → Because tests always ran with `app.app_context()` active

5. **Why was code written this way?**
   → Developer assumed `current_app` would always be available (incorrect assumption)

**Root Cause:** 
Code assumes Flask app context is always active, but `verify_token()` can be called from contexts where `current_app` is not available (background tasks, CLI, tests).

**Solution:**
Pass app/config as parameter OR ensure method always called within app context.
```

---

### Step 2: Identify Fix Strategy

**Fix strategies based on root cause:**

| Root Cause | Fix Strategy | Example |
|------------|--------------|---------|
| Missing app context | Add context manager | `with app.app_context(): ...` |
| Hardcoded value | Use config/env var | `app.config.get('KEY', default)` |
| Missing validation | Add input validation | `if not user:  raise ValueError()` |
| Race condition | Add locking/transaction | `with db.session.begin_nested(): ...` |
| Memory leak | Fix resource cleanup | Use context managers |
| SQL injection | Use parameterized queries | `db.execute(text("...  WHERE id=:id"), {"id": user_id})` |
| Missing dependency | Add to requirements. txt | Check imports |
| Wrong logic | Refactor algorithm | Simplify, add tests |

**For our example:**

**Strategy:** Refactor `verify_token()` to accept `app` parameter OR always require app context

**Chosen approach:** Accept app as parameter (more flexible)

---

### Step 3: Implement Fix

**Before (buggy code):**

```python
# backend/src/services/email_service.py

from flask import current_app
from itsdangerous import URLSafeTimedSerializer

class EmailService:
    @staticmethod
    def verify_token(token:  str) -> dict:
        """Verify email verification token."""
        try:
            # BUG: Assumes current_app is available
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            data = serializer. loads(
                token,
                max_age=current_app.config['EMAIL_VERIFICATION_EXPIRY']  # ← ERROR HERE
            )
            
            # ...  rest of code
```

**After (fixed code):**

```python
# backend/src/services/email_service.py

from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService: 
    @staticmethod
    def verify_token(token: str, app: Optional['Flask'] = None) -> dict:
        """
        Verify email verification token. 
        
        Args:
            token:  Verification token from email
            app: Flask app instance (optional, uses current_app if not provided)
            
        Returns:
            Dictionary with success, message, error
            
        Raises:
            RuntimeError: If no app context available and app not provided
        """
        # Get app instance
        if app is None:
            try:
                app = current_app._get_current_object()
            except RuntimeError:
                logger.error("verify_token called outside app context without app parameter")
                raise RuntimeError(
                    "verify_token must be called within Flask app context "
                    "or with app parameter"
                )
        
        try:
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            expiry = app.config. get('EMAIL_VERIFICATION_EXPIRY', 86400)
            
            data = serializer. loads(token, max_age=expiry)
            
            # ... rest of code (unchanged)
            
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return {
                'success': False,
                'message': str(e),
                'error':  'VERIFICATION_FAILED'
            }
```

**Changes made:**
1. ✅ Added `app` parameter (optional)
2. ✅ Added fallback to `current_app` if `app` not provided
3. ✅ Added clear error if neither available
4. ✅ Added type hints
5. ✅ Added logging
6. ✅ Improved docstring

---

### Step 4: Add Regression Test

**Purpose:** Ensure bug never comes back

**File:** `backend/tests/test_email_verification.py`

```python
def test_verify_token_without_app_context():
    """
    Regression test for Issue #123.
    
    Bug: AttributeError when verify_token called outside app context
    Fix: Accept app parameter
    """
    app = create_app('testing')
    
    # Create user and token WITHIN context
    with app.app_context():
        user = User(id=1, email="test@example.com")
        db.session.add(user)
        db.session.commit()
        token = EmailService.generate_verification_token(user)
    
    # Call verify_token OUTSIDE context (this used to fail)
    # Now we pass app explicitly
    result = EmailService.verify_token(token, app=app)
    
    assert result['success'] is True
    
    # Verify user is marked as verified
    with app.app_context():
        user = User.query.get(1)
        assert user. email_verified is True


def test_verify_token_without_app_raises_error():
    """Test verify_token without app or context raises clear error."""
    with pytest.raises(RuntimeError, match="app context"):
        EmailService.verify_token("dummy-token")
```

---

### Step 5: Update Callers (if needed)

**Find all places that call `verify_token()`:**

```powershell
# Search codebase
Get-ChildItem -Path backend/src -Recurse -Filter *.py | 
    Select-String "verify_token" | 
    Select-Object Path, LineNumber, Line
```

**Update routes:**

```python
# backend/src/routes/auth. py

@bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token:  str):
    """Verify email with token."""
    # Before: result = EmailService.verify_token(token)
    # After: (no change needed, current_app is available in route)
    result = EmailService.verify_token(token)  # Works fine in request context
    
    if result['success']:
        flash('Email verified! ', 'success')
        return render_template('auth/email-verified.html', success=True)
    else:
        flash(result['message'], 'error')
        return render_template('auth/email-verified.html', success=False)
```

**Update CLI commands:**

```python
# backend/src/cli. py

@app.cli. command()
@click.argument('token')
def verify_email_cli(token):
    """Verify email from command line."""
    # Before: result = EmailService.verify_token(token)  # ← Would fail! 
    # After: Pass app explicitly
    result = EmailService.verify_token(token, app=current_app._get_current_object())
    
    if result['success']: 
        click.echo('✓ Email verified')
    else:
        click. echo(f'✗ Verification failed: {result["message"]}')
```

---

### Step 6: Validate Fix

**Run tests:**

```powershell
# Run specific test
pytest backend/tests/test_email_verification.py::test_verify_token_without_app_context -v

# Run all email verification tests
pytest backend/tests/test_email_verification.py -v

# Run full test suite
pytest backend/tests/ -v

# Check coverage
pytest backend/tests/ --cov=backend.src. services.email_service
```

**Manual testing:**

```powershell
# Kill servers
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force

# Test in dev mode
. \.venv\Scripts\python.exe backend\src\app.py

# Test verification flow: 
# 1. Register user
# 2. Check email for token
# 3. Click verification link
# 4. Verify success message
```

**Expected results:**
- ✅ All tests pass
- ✅ No errors in console
- ✅ Feature works in browser
- ✅ No regression in other features

---

## Debug Report

**Generate:** `Analysis_reports/YYYY-MM-DD_HH-mm_debug-issue-NNN.md`

```markdown
# Debug Report - Issue #123

**Date:** 2025-01-27  
**Issue:** AttributeError in email verification  
**Severity:** High  
**Status:** ✅ Fixed  

---

## Issue Summary

**Error:**
```
AttributeError: 'NoneType' object has no attribute 'config'
```

**Location:** `backend/src/services/email_service.py:78`

**Trigger:** Calling `verify_token()` outside Flask app context (e.g., CLI, background task)

---

## Root Cause Analysis

**5 Whys:**

1. Why error?  → `app` is `None`
2. Why None? → `current_app` not available outside request context
3. Why not available? → Method called from CLI/background task
4. Why not caught? → Tests always used `app.app_context()`
5. Why written this way? → Incorrect assumption about context

**Root Cause:** Code assumes Flask app context always active. 

---

## Solution

**Strategy:** Make `verify_token()` work both inside and outside app context.

**Implementation:**
- Added optional `app` parameter
- Fallback to `current_app` if not provided
- Clear error if neither available
- Improved logging and error handling

**Files Modified:**
- `backend/src/services/email_service.py` (15 lines changed)
- `backend/tests/test_email_verification.py` (2 new tests added)

---

## Testing

**Regression Tests Added:**
- `test_verify_token_without_app_context()` — Verify fix works
- `test_verify_token_without_app_raises_error()` — Verify error handling

**Test Results:**
```
backend/tests/test_email_verification.py ................ ....  [100%]

31 passed in 2.45s
```

**Coverage:** 94% (email_service.py)

---

## Validation

**Manual Testing:**
- ✅ Web verification flow works
- ✅ CLI command works:  `flask verify-email-cli <token>`
- ✅ Background tasks work
- ✅ No errors in logs

**Performance:**
- No performance impact (same execution time)

---

## Prevention

**To prevent similar issues:**

1. ✅ Added pattern to coding guidelines: 
   - Services should not assume app context
   - Pass app as parameter for CLI/background tasks

2. ✅ Added test category:  "Context-independent tests"
   - Test services outside app context
   - Test CLI commands

3. ✅ Updated code review checklist: 
   - Check for `current_app` usage in services
   - Verify tests cover all execution contexts

---

## Related Issues

- None (first occurrence)

---

## References

- Original issue: GitHub #123
- Pull request: #124
- Commit: abc123def

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved. 
```

---

## Common Debug Scenarios

### Scenario 1: Test Failure

**Issue:** Test fails intermittently (flaky test)

**Debug approach:**

1. **Identify pattern:**
   ```powershell
   # Run test 100 times
   for ($i=1; $i -le 100; $i++) {
       pytest backend/tests/test_flaky. py::test_name -v
       if ($LASTEXITCODE -ne 0) {
           Write-Host "Failed on iteration $i"
           break
       }
   }
   ```

2. **Common causes:**
   - Race condition (use locking)
   - Time-dependent logic (mock `datetime.now()`)
   - Random data (use fixed seed)
   - External dependency (mock API calls)
   - Database state (ensure clean state per test)

3. **Fix:**
   ```python
   # Before (flaky)
   def test_token_expiry():
       token = generate_token()
       time.sleep(86401)  # Wait 24h+1s (SLOW!)
       assert is_expired(token)
   
   # After (deterministic)
   def test_token_expiry():
       with freeze_time("2025-01-27 10:00:00"):
           token = generate_token()
       
       with freeze_time("2025-01-28 10:00:01"):  # 24h+1s later
           assert is_expired(token)
   ```

---

### Scenario 2: Production Error

**Issue:** Error in production, works in dev

**Debug approach:**

1. **Check environment differences:**
   ```bash
   # Production
   FLASK_ENV=production
   DEBUG=False
   DATABASE_URL=postgresql://...  # Different DB! 
   
   # Development
   FLASK_ENV=development
   DEBUG=True
   DATABASE_URL=sqlite:///dev.db
   ```

2. **Common causes:**
   - Missing environment variable
   - Database differences (SQLite vs PostgreSQL)
   - File permissions
   - HTTPS vs HTTP
   - Caching enabled in prod

3. **Fix:**
   ```python
   # Use environment-agnostic code
   DATABASE_URL = os.environ.get('DATABASE_URL')
   if not DATABASE_URL:
       raise ValueError("DATABASE_URL environment variable required")
   ```

---

### Scenario 3: Performance Issue

**Issue:** Route is slow (>2 seconds)

**Debug approach:**

1. **Profile the code:**
   ```python
   # Add profiling decorator
   import time
   import logging
   
   logger = logging. getLogger(__name__)
   
   def profile(func):
       def wrapper(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           duration = time.time() - start
           logger.info(f"{func.__name__} took {duration:. 2f}s")
           return result
       return wrapper
   
   @bp.route("/slow-route")
   @profile
   def slow_route():
       # This will log execution time
       pass
   ```

2. **Identify bottleneck:**
   ```python
   # Use cProfile
   import cProfile
   import pstats
   
   profiler = cProfile.Profile()
   profiler.enable()
   
   # Run slow code
   slow_function()
   
   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats(10)  # Top 10 slowest
   ```

3. **Common causes:**
   - N+1 query problem (use `joinedload()`)
   - Missing database index
   - Large data transfer
   - Synchronous external API call

4. **Fix:**
   ```python
   # Before (N+1 queries)
   users = User.query.all()
   for user in users:
       print(user.posts)  # Query per user! 
   
   # After (1 query)
   from sqlalchemy. orm import joinedload
   users = User.query.options(joinedload(User.posts)).all()
   for user in users:
       print(user.posts)  # No extra query
   ```

---

### Scenario 4: Security Vulnerability

**Issue:** SQL injection reported

**Debug approach:**

1. **Identify vulnerable code:**
   ```powershell
   # Search for string interpolation in SQL
   Get-ChildItem -Recurse -Filter *.py | 
       Select-String 'f"SELECT|f"INSERT|f"UPDATE|f"DELETE' |
       Select-Object Path, LineNumber
   ```

2. **Common vulnerabilities:**
   - SQL injection (use parameterized queries)
   - XSS (escape output, use Jinja2 auto-escape)
   - CSRF (use Flask-WTF)
   - Hardcoded secrets (use environment variables)

3. **Fix:**
   ```python
   # Before (VULNERABLE)
   query = f"SELECT * FROM users WHERE username = '{username}'"
   db.execute(query)
   
   # After (SAFE)
   from sqlalchemy import text
   query = text("SELECT * FROM users WHERE username = : username")
   db.execute(query, {"username": username})
   
   # Even better (ORM)
   user = User.query.filter_by(username=username).first()
   ```

---

## Debug Tools

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging. FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.debug("Variable value: %s", var)
logger.info("Function called with args: %s", args)
logger.warning("Deprecated function used")
logger.error("Error occurred:  %s", error)
logger.critical("Critical failure!")
```

### Python Debugger (pdb)

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or in Python 3.7+
breakpoint()

# Commands:
# n (next line)
# s (step into function)
# c (continue)
# p variable (print variable)
# l (list code)
# q (quit)
```

### Flask Debug Toolbar

```python
# Install
pip install flask-debugtoolbar

# Add to app
from flask_debugtoolbar import DebugToolbarExtension

app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
```

---

## Validation Checklist

### Before Fix
- [ ] Issue reproduced reliably
- [ ] Root cause identified (5 Whys)
- [ ] Fix strategy chosen
- [ ] Regression test planned

### After Fix
- [ ] Fix implemented
- [ ] Regression test added
- [ ] All tests pass
- [ ] Manual testing complete
- [ ] No new issues introduced
- [ ] Performance acceptable
- [ ] Debug report generated
- [ ] Prevention measures documented

---

## Don'ts

- ❌ Skip root cause analysis (fix symptoms, not cause)
- ❌ Commit commented-out debug code
- ❌ Skip regression test
- ❌ Fix without understanding
- ❌ Change too many things at once
- ❌ Ignore warnings
- ❌ Skip documentation
- ❌ Rush the fix (introduce new bugs)

---

## References

- `.github/copilot-instructions.md` — General rules
- `.github/workflow-rules.md` — Testing workflow
- `.github/incidents-history.md` — Past issues
- [Python Debugging Guide](https://docs.python.org/3/library/pdb.html)
- [Flask Debugging](https://flask.palletsprojects.com/en/latest/debugging/)

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 