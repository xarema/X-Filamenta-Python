---
mode: "agent"
description: "Generate actionable completion plan for incomplete features identified in code vs roadmap analysis"
---

# Generate Feature Completion Plan

**Task:** Analyze incomplete features from code vs roadmap analysis and generate detailed, actionable plans to complete them (tests, docs, missing code).

---

## Input Required

### Source Analysis Report
${input: report: Which analysis report?  (latest|specific-date|specific-file)}

### Scope
${input:scope:Generate plan for?  (all-incomplete|specific-feature|critical-only)}

### Feature to Complete (if specific)
${input:feature:Feature name or leave empty for all}

### Plan Detail Level
${input:detail:Detail level?  (high-level|detailed|comprehensive)}

**Levels:**
- `high-level`: Tasks only (what to do)
- `detailed`: Tasks + steps + examples
- `comprehensive`: Tasks + steps + examples + code templates + acceptance criteria

### Include Time Estimates
${input:estimates:Include time estimates? (yes|no)}

---

## MANDATORY:  Pre-Planning Process

### 1. Load Analysis Report

**Find latest code vs roadmap report:**

```powershell
# Windows PowerShell
$latestReport = Get-ChildItem -Path Analysis_reports -Filter "*code-vs-roadmap. md" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

Write-Host "Using report: $($latestReport.Name)"
```

**Extract incomplete features:**

From report section **"Incorrectly Completed Features"**: 

```markdown
| Feature | Roadmap | Reality | Missing Components | Impact |
|---------|---------|---------|-------------------|--------|
| Email Verification | ✅ Complete | 🔄 70% | Tests (0), Docs | Medium |
| Session Management | ✅ Complete | 🔄 65% | Advanced features, Tests | Low |
```

**Parse for each incomplete feature:**
- `feature_name`: "Email Verification"
- `current_completion`: 70%
- `target_completion`: 100%
- `missing_components`: ["Tests", "Docs"]
- `impact`: "Medium"
- `existing_implementation`: Files already created

---

### 2. Analyze Existing Code

**For each incomplete feature, scan:**

#### A. What EXISTS (already implemented)

```python
# Example: Email Verification

Existing files: 
✅ backend/src/routes/auth.py
   - send_verification_email() route
   - verify_email_token() route
   
✅ backend/src/services/email_service.py
   - generate_verification_token()
   - send_verification_email()
   
✅ frontend/templates/auth/email-verification.html
   - Email sent confirmation page
   - Email verified success page

✅ backend/src/models/user.py
   - email_verified field
   - email_verification_token field
```

#### B. What's MISSING (needs to be created)

```python
Missing: 
❌ Tests:  tests/test_email_verification.py (0 tests)
❌ Docs: docs/features/email-verification.md
❌ Edge cases: Token expiry handling (partial)
```

#### C. What's PARTIAL (needs completion)

```python
Partial:
⚠️ Token expiry:  Code exists but not tested
⚠️ Resend verification: Route exists but no UI button
⚠️ Error handling: Basic, needs improvement
```

---

### 3. Define Acceptance Criteria

**For feature to be 100% complete:**

```markdown
Acceptance Criteria (Email Verification):

Code: 
- [x] Backend routes implemented
- [x] Service layer implemented
- [x] Database model fields added
- [x] Frontend templates created
- [ ] Token expiry handling complete
- [ ] Resend verification implemented

Tests:
- [ ] Unit tests for email service (min 10 tests)
- [ ] Integration tests for routes (min 5 tests)
- [ ] Edge case tests (expiry, invalid token, etc.)
- [ ] Test coverage ≥ 80%

Documentation:
- [ ] Feature documentation (docs/features/email-verification.md)
- [ ] API documentation (routes + parameters)
- [ ] User guide (how to verify email)

Quality: 
- [ ] Code reviewed
- [ ] Linters pass (ruff, mypy)
- [ ] No security vulnerabilities
- [ ] Translations complete (FR + EN)
```

---

## Plan Generation Workflow

### Step 1: Generate Task List

**For each incomplete feature, create structured task list:**

```markdown
# Completion Plan:  Email Verification

**Current Status:** 70% complete  
**Target:** 100% complete  
**Estimated Effort:** 6-8 hours  
**Priority:** Medium  

---

## Tasks Overview

| # | Task | Type | Effort | Priority | Dependencies |
|---|------|------|--------|----------|--------------|
| 1 | Create test file | Test | 3h | High | None |
| 2 | Write unit tests | Test | 2h | High | Task 1 |
| 3 | Write integration tests | Test | 1. 5h | High | Task 1 |
| 4 | Create documentation | Docs | 1h | Medium | None |
| 5 | Complete token expiry | Code | 1h | Medium | Task 2 |
| 6 | Add resend button | UI | 0.5h | Low | Task 5 |

**Total Estimated Time:** 9 hours  
**Recommended Sprint:** 2 days (4h/day)

---

## Task 1: Create Test File ⚡ HIGH PRIORITY

**Objective:** Create pytest test file for email verification

**File to create:** `backend/tests/test_email_verification.py`

**Steps:**

1. Create test file structure
2. Import required modules
3. Create fixtures
4. Add file header

**Template:**

```python
"""
Email Verification Tests

Purpose: Test email verification functionality (send, verify, resend, expiry)
File: backend/tests/test_email_verification.py | Repository: X-Filamenta-Python

License:  AGPL-3.0-or-later
Copyright (c) 2025 XAREMA.  All rights reserved.
"""
import pytest
from datetime import datetime, timedelta
from backend.src import create_app, db
from backend. src.models.user import User
from backend.src.services.email_service import EmailService

@pytest.fixture
def app():
    """Create test app."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create sample user (unverified)."""
    user = User(
        username="testuser",
        email="test@example.com",
        email_verified=False
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

# Tests will be added in Task 2
```

**Acceptance Criteria:**
- [x] File created at correct path
- [x] File header complete
- [x] Fixtures defined (app, client, sample_user)
- [x] Imports correct

**Estimated Time:** 30 minutes

---

## Task 2: Write Unit Tests ⚡ HIGH PRIORITY

**Objective:** Write comprehensive unit tests for email service

**File:** `backend/tests/test_email_verification.py`

**Tests to write (minimum 10):**

### Service Layer Tests

```python
def test_generate_verification_token(sample_user):
    """Test token generation."""
    token = EmailService.generate_verification_token(sample_user)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 20  # Token should be reasonably long

def test_verify_valid_token(sample_user):
    """Test verification with valid token."""
    token = EmailService.generate_verification_token(sample_user)
    
    result = EmailService.verify_token(token)
    
    assert result is True
    assert sample_user.email_verified is True

def test_verify_invalid_token():
    """Test verification with invalid token."""
    result = EmailService.verify_token("invalid-token-12345")
    
    assert result is False

def test_verify_expired_token(sample_user):
    """Test verification with expired token."""
    # Generate token
    token = EmailService.generate_verification_token(sample_user)
    
    # Manually expire token (modify created_at in DB)
    sample_user.email_verification_token_created = datetime.utcnow() - timedelta(hours=25)
    db.session.commit()
    
    result = EmailService.verify_token(token)
    
    assert result is False
    assert sample_user.email_verified is False

def test_resend_verification_email(sample_user):
    """Test resending verification email."""
    # Send first time
    token1 = EmailService.send_verification_email(sample_user)
    
    # Send again (should generate new token)
    token2 = EmailService.send_verification_email(sample_user)
    
    assert token1 != token2
    # Old token should be invalid
    assert EmailService.verify_token(token1) is False
    # New token should work
    assert EmailService.verify_token(token2) is True

def test_verify_already_verified_user(sample_user):
    """Test verifying already verified user."""
    # Verify first time
    token = EmailService.generate_verification_token(sample_user)
    EmailService.verify_token(token)
    
    # Try to verify again
    result = EmailService.verify_token(token)
    
    assert result is False  # Token should be consumed

def test_token_unique_per_user():
    """Test that each user gets unique token."""
    user1 = User(email="user1@example.com")
    user2 = User(email="user2@example.com")
    
    token1 = EmailService.generate_verification_token(user1)
    token2 = EmailService.generate_verification_token(user2)
    
    assert token1 != token2

def test_multiple_verification_attempts():
    """Test rate limiting on verification attempts."""
    # TODO: Implement after rate limiting added
    pass

def test_verification_token_encoding():
    """Test token encoding/decoding."""
    user = User(id=123, email="test@example.com")
    token = EmailService. generate_verification_token(user)
    
    decoded_user_id = EmailService.decode_token(token)
    
    assert decoded_user_id == user.id

def test_send_verification_email_smtp():
    """Test actual email sending (mocked)."""
    # TODO: Mock SMTP and verify email sent
    pass
```

**Acceptance Criteria:**
- [x] Minimum 10 tests written
- [x] All tests pass
- [x] Edge cases covered (expiry, invalid, already verified)
- [x] Code coverage ≥ 80% for email_service. py

**Estimated Time:** 2 hours

---

## Task 3: Write Integration Tests ⚡ HIGH PRIORITY

**Objective:** Test complete email verification workflow (routes)

**File:** `backend/tests/test_email_verification. py` (add to same file)

**Tests to write (minimum 5):**

### Route Tests

```python
def test_send_verification_route_success(client, sample_user):
    """Test POST /auth/send-verification."""
    # Login first
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/send-verification')
    
    assert response.status_code == 200
    assert b'verification email sent' in response.data. lower()

def test_send_verification_not_logged_in(client):
    """Test send verification when not logged in."""
    response = client.post('/auth/send-verification')
    
    assert response.status_code == 401  # Unauthorized

def test_verify_email_valid_token(client, sample_user):
    """Test GET /auth/verify-email/<token> with valid token."""
    token = EmailService.generate_verification_token(sample_user)
    
    response = client.get(f'/auth/verify-email/{token}')
    
    assert response.status_code == 200
    assert b'email verified successfully' in response.data. lower()
    
    # Check user is verified in DB
    user = User.query.get(sample_user.id)
    assert user.email_verified is True

def test_verify_email_invalid_token(client):
    """Test verify with invalid token."""
    response = client.get('/auth/verify-email/invalid-token-123')
    
    assert response. status_code == 400
    assert b'invalid' in response.data.lower()

def test_verify_email_expired_token(client, sample_user):
    """Test verify with expired token."""
    token = EmailService.generate_verification_token(sample_user)
    
    # Expire token
    sample_user.email_verification_token_created = datetime.utcnow() - timedelta(hours=25)
    db.session.commit()
    
    response = client.get(f'/auth/verify-email/{token}')
    
    assert response.status_code == 400
    assert b'expired' in response.data.lower()

def test_resend_verification_rate_limit(client, sample_user):
    """Test rate limiting on resend."""
    # Login
    client.post('/auth/login', data={
        'email':  'test@example.com',
        'password': 'password123'
    })
    
    # Send multiple times rapidly
    for i in range(12):  # Rate limit is 10/hour
        response = client.post('/auth/send-verification')
    
    assert response.status_code == 429  # Too Many Requests
```

**Acceptance Criteria:**
- [x] Minimum 5 integration tests
- [x] All tests pass
- [x] Tests use test client (HTTP requests)
- [x] Tests cover success + error cases

**Estimated Time:** 1.5 hours

---

## Task 4: Create Documentation 📚 MEDIUM PRIORITY

**Objective:** Document email verification feature

**File to create:** `docs/features/email-verification.md`

**Template:**

```markdown
# Email Verification Feature

**Status:** ✅ Complete  
**Version:** 1.0.0  
**Last Updated:** YYYY-MM-DD

---

## Overview

Email verification ensures users have access to the email address they registered with. A verification email is sent upon registration, containing a unique token link. 

---

## User Flow

1. User registers with email + password
2. System sends verification email with token link
3. User clicks link in email
4. System verifies token and marks email as verified
5. User can now access full features

---

## Technical Implementation

### Routes

#### POST `/auth/send-verification`

Send verification email to logged-in user.

**Authentication:** Required (logged-in user)

**Rate Limit:** 10 requests/hour

**Request:** No body required

**Response:**

```json
{
  "message": "Verification email sent to your@email.com",
  "status": "success"
}
```

**Errors:**
- `401 Unauthorized`: User not logged in
- `400 Bad Request`: Email already verified
- `429 Too Many Requests`: Rate limit exceeded

---

#### GET `/auth/verify-email/<token>`

Verify email using token from email link.

**Authentication:** Not required

**Parameters:**
- `token` (string, required): Verification token from email

**Response:**

```html
<!-- Renders email-verified. html template -->
Email verified successfully!  You can now log in.
```

**Errors:**
- `400 Bad Request`: Invalid or expired token
- `404 Not Found`: Token not found

---

### Database Schema

**User Model:**

```python
class User(db.Model):
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(255), nullable=True)
    email_verification_token_created = db.Column(db.DateTime, nullable=True)
```

---

### Token Generation

Tokens are generated using `itsdangerous. URLSafeTimedSerializer`:

- **Expiry:** 24 hours
- **Algorithm:** HMAC-SHA256
- **Secret:** `FLASK_SECRET_KEY` from environment

---

### Email Template

**Subject:** `Verify your email - X-Filamenta`

**Body:**

```html
Hello {{ user.username }},

Please verify your email address by clicking the link below:

{{ verification_url }}

This link will expire in 24 hours.

If you didn't create an account, please ignore this email. 

Thanks,
X-Filamenta Team
```

---

## Security Considerations

1. **Token Expiry:** Tokens expire after 24 hours
2. **Single Use:** Tokens are consumed after verification
3. **Rate Limiting:** Max 10 verification emails per hour
4. **HTTPS Only:** Verification links only work over HTTPS in production
5. **No Email Enumeration:** Same response for valid/invalid emails

---

## Testing

**Test Coverage:** 92% (15 tests, 100% pass)

**Test Files:**
- `backend/tests/test_email_verification.py`

**Run Tests:**

```bash
pytest backend/tests/test_email_verification.py -v
```

---

## Configuration

**Environment Variables:**

```bash
# SMTP Configuration (required)
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=noreply@example.com
SMTP_PASSWORD=smtp-password

# Email Verification (optional)
EMAIL_VERIFICATION_EXPIRY=86400  # 24 hours in seconds
EMAIL_VERIFICATION_RATE_LIMIT=10  # Max emails per hour
```

---

## Troubleshooting

### User didn't receive email

1. Check spam folder
2. Verify SMTP configuration
3. Check email service logs
4. Resend verification email

### Token expired

1. User can request new verification email
2. Go to `/auth/send-verification` (while logged in)

### Email already verified

- User can log in normally
- No action needed

---

## Future Improvements

- [ ] Add email verification reminder (after 7 days)
- [ ] Allow changing email (re-verification required)
- [ ] Admin panel:  manually verify user emails

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.
```

**Acceptance Criteria:**
- [x] Documentation file created
- [x] All sections complete (Overview, Routes, Security, etc.)
- [x] Code examples included
- [x] Troubleshooting section added
- [x] Links to test files

**Estimated Time:** 1 hour

---

## Task 5: Complete Token Expiry Handling 💻 MEDIUM PRIORITY

**Objective:** Complete token expiry handling (currently partial)

**File to modify:** `backend/src/services/email_service.py`

**Current State:**
```python
# Partial implementation
def verify_token(token:  str) -> bool:
    try:
        data = serializer.loads(token)
        user_id = data['user_id']
        user = User.query.get(user_id)
        
        # TODO: Check expiry
        
        user.email_verified = True
        db.session.commit()
        return True
    except:
        return False
```

**Complete Implementation:**

```python
def verify_token(token: str) -> dict:
    """
    Verify email verification token.
    
    Args:
        token: Verification token from email
        
    Returns: 
        Dictionary with: 
        - success (bool): Whether verification succeeded
        - message (str): Human-readable message
        - error (str): Error code if failed
    """
    try:
        # Decode token (with expiry check built-in)
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        data = serializer. loads(
            token,
            max_age=current_app.config. get('EMAIL_VERIFICATION_EXPIRY', 86400)  # 24h default
        )
        
        user_id = data['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return {
                'success': False,
                'message': 'User not found',
                'error': 'USER_NOT_FOUND'
            }
        
        if user.email_verified:
            return {
                'success': False,
                'message': 'Email already verified',
                'error': 'ALREADY_VERIFIED'
            }
        
        # Verify token matches current token in DB
        if user.email_verification_token != token:
            return {
                'success': False,
                'message': 'Token has been superseded',
                'error': 'TOKEN_SUPERSEDED'
            }
        
        # Mark as verified
        user.email_verified = True
        user.email_verification_token = None  # Consume token
        user.email_verification_token_created = None
        db.session.commit()
        
        logger.info(f"Email verified for user {user.id}")
        
        return {
            'success':  True,
            'message': 'Email verified successfully',
            'error': None
        }
        
    except SignatureExpired:
        logger.warning(f"Expired verification token: {token[: 20]}...")
        return {
            'success': False,
            'message': 'Verification link has expired.  Please request a new one.',
            'error': 'TOKEN_EXPIRED'
        }
    except BadSignature:
        logger.warning(f"Invalid verification token: {token[:20]}...")
        return {
            'success':  False,
            'message': 'Invalid verification link',
            'error': 'INVALID_TOKEN'
        }
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return {
            'success': False,
            'message': 'An error occurred during verification',
            'error': 'INTERNAL_ERROR'
        }
```

**Update Route:**

```python
# backend/src/routes/auth.py

@bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token:  str):
    """Verify email with token."""
    result = EmailService.verify_token(token)
    
    if result['success']:
        flash('Email verified successfully!  You can now log in.', 'success')
        return render_template('auth/email-verified.html', success=True)
    else:
        flash(result['message'], 'error')
        return render_template('auth/email-verified. html', 
                             success=False, 
                             error_code=result['error'])
```

**Acceptance Criteria:**
- [x] Token expiry properly checked
- [x] Error codes defined
- [x] Token consumed after verification
- [x] All edge cases handled
- [x] Tests pass (Task 2 tests)

**Estimated Time:** 1 hour

---

## Task 6: Add Resend Verification Button 🎨 LOW PRIORITY

**Objective:** Add UI button to resend verification email

**File to modify:** `frontend/templates/dashboard/member. html`

**Add notification if email not verified:**

```html
<!-- After header, before main content -->
{% if current_user.is_authenticated and not current_user. email_verified %}
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    <strong>{{ t('email_verification. unverified_title') or '⚠️ Email not verified' }}</strong>
    <p class="mb-2">
        {{ t('email_verification. unverified_message') or 'Please verify your email to access all features.' }}
    </p>
    <button 
        class="btn btn-sm btn-primary" 
        hx-post="/auth/send-verification" 
        hx-target="#verification-status"
        hx-swap="outerHTML"
    >
        {{ t('email_verification. resend_button') or 'Resend Verification Email' }}
    </button>
    <div id="verification-status"></div>
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
{% endif %}
```

**Add translations:**

**`backend/src/i18n/fr.json`:**
```json
{
  "email_verification":  {
    "unverified_title": "⚠️ Email non vérifié",
    "unverified_message": "Veuillez vérifier votre email pour accéder à toutes les fonctionnalités.",
    "resend_button":  "Renvoyer l'email de vérification",
    "email_sent": "Email de vérification envoyé ! ",
    "check_inbox": "Vérifiez votre boîte de réception."
  }
}
```

**`backend/src/i18n/en.json`:**
```json
{
  "email_verification": {
    "unverified_title": "⚠️ Email not verified",
    "unverified_message": "Please verify your email to access all features.",
    "resend_button": "Resend Verification Email",
    "email_sent": "Verification email sent! ",
    "check_inbox":  "Check your inbox."
  }
}
```

**Create HTMX response partial:**

**`frontend/templates/partials/_verification_sent.html`:**
```html
<!-- Partial:  Verification Email Sent
     Purpose: Feedback after resending verification email
     Target: #verification-status
     Swap: outerHTML
-->
<div id="verification-status" class="alert alert-success mt-2">
    <strong>{{ t('email_verification.email_sent') or '✓ Verification email sent!' }}</strong>
    <p class="mb-0 small">{{ t('email_verification. check_inbox') or 'Check your inbox.' }}</p>
</div>
```

**Update route to return partial:**

```python
@bp.route("/send-verification", methods=["POST"])
@login_required
def send_verification():
    """Send verification email (HTMX endpoint)."""
    if current_user.email_verified:
        return jsonify({"error": "Email already verified"}), 400
    
    # Send email
    EmailService.send_verification_email(current_user)
    
    # Return partial for HTMX
    if request.headers.get('HX-Request'):
        return render_template('partials/_verification_sent.html'), 200
    
    # Fallback for non-HTMX
    flash('Verification email sent!', 'success')
    return redirect(url_for('main.dashboard'))
```

**Acceptance Criteria:**
- [x] Alert displayed when email not verified
- [x] Resend button functional (HTMX)
- [x] Translations added (FR + EN)
- [x] Success feedback shown
- [x] Alert dismissible

**Estimated Time:** 30 minutes

---

## Summary

### Total Effort Estimate

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| 1. Create test file | HIGH | 0.5h | None |
| 2. Write unit tests | HIGH | 2h | Task 1 |
| 3. Write integration tests | HIGH | 1.5h | Task 1 |
| 4. Create documentation | MEDIUM | 1h | None |
| 5. Complete token expiry | MEDIUM | 1h | Task 2 |
| 6. Add resend button | LOW | 0.5h | Task 5 |

**Total:** ~6. 5 hours (1-2 days)

---

### Recommended Order

**Day 1 (4 hours):**
1. Task 1: Create test file (0.5h)
2. Task 2: Write unit tests (2h)
3. Task 3: Write integration tests (1.5h)

**Day 2 (2. 5 hours):**
4. Task 5: Complete token expiry (1h)
5. Task 4: Create documentation (1h)
6. Task 6: Add resend button (0.5h)

---

### Definition of Done

Feature "Email Verification" is 100% complete when: 

- [x] All 6 tasks completed
- [x] All tests pass (15 tests minimum, 100% pass rate)
- [x] Test coverage ≥ 80% for email_service.py
- [x] Documentation exists and is complete
- [x] Linters pass (ruff, mypy)
- [x] Code reviewed
- [x] Translations complete (FR + EN)
- [x] Feature works in dev AND prod mode
- [x] No console errors
- [x] Security review passed

---

**Plan generated successfully ✅**
```

---

## Validation Checklist

Before finalizing plan: 

### Completeness
- [ ] All missing components identified
- [ ] Tasks cover code + tests + docs
- [ ] Dependencies between tasks clear
- [ ] Time estimates realistic

### Actionability
- [ ] Each task has clear objective
- [ ] Steps detailed enough to execute
- [ ] Code templates provided
- [ ] Acceptance criteria defined

### Quality
- [ ] Tasks prioritized (High/Medium/Low)
- [ ] Definition of Done included
- [ ] Recommended order provided
- [ ] Total effort estimated

---

## Output Files

**Generated files:**

```
Analysis_reports/YYYY-MM-DD_HH-mm_completion-plan-[feature]. md  ← Detailed plan
Analysis_reports/YYYY-MM-DD_HH-mm_completion-summary.md         ← Summary (all features)
```

**Summary format (if multiple features):**

```markdown
# Feature Completion Summary

**Date:** YYYY-MM-DD  
**Features to Complete:** 3  
**Total Effort:** 18 hours (3-4 days)

---

## Features by Priority

### HIGH Priority (Complete ASAP)

| Feature | Current | Target | Effort | Missing |
|---------|---------|--------|--------|---------|
| Email Verification | 70% | 100% | 6. 5h | Tests, Docs |

### MEDIUM Priority

| Feature | Current | Target | Effort | Missing |
|---------|---------|--------|--------|---------|
| Session Management | 65% | 100% | 8h | Advanced features, Tests |

### LOW Priority

| Feature | Current | Target | Effort | Missing |
|---------|---------|--------|--------|---------|
| Advanced Search | 40% | 100% | 12h | Backend, Tests, Docs |

---

## Recommended Sprint Plan

**Sprint 1 (Week 1):**
- Complete Email Verification (6.5h)
- Start Session Management (4h)

**Sprint 2 (Week 2):**
- Complete Session Management (4h)
- Start Advanced Search (6h)

**Sprint 3 (Week 3):**
- Complete Advanced Search (6h)

---

**Full plans available in:**
- `completion-plan-email-verification.md`
- `completion-plan-session-management. md`
- `completion-plan-advanced-search.md`
```

---

## Don'ts

- ❌ Generate plan without analyzing existing code
- ❌ Skip time estimates (developers need to plan)
- ❌ Forget to prioritize tasks
- ❌ Provide vague tasks ("fix tests" → specific tests needed)
- ❌ Ignore dependencies between tasks
- ❌ Skip acceptance criteria (how to know it's done?)
- ❌ Forget translations (if feature has UI)
- ❌ Skip code templates (make it actionable)

---

## References

- `.github/prompts/analyze-code-vs-roadmap.prompt. md` — Identify incomplete features
- `.github/prompts/update-roadmap.prompt.md` — Update roadmap after completion
- `.github/copilot-instructions.md` — General rules
- `.github/workflow-rules.md` — Testing workflow

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 