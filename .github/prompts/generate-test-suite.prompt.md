---
mode: "agent"
description: "Generate comprehensive test suite (unit + integration + e2e) for a feature or module"
---

# Generate Test Suite

**Task:** Generate complete test suite (unit tests, integration tests, edge cases) for a specific feature or module with full code coverage.

---

## Input Required

### Target to Test
${input: target: What to test?   (feature|module|route|service|model|function)}

### Target Name
${input:name:Name of feature/module/route/etc. }

### Test Type
${input:type:Test types to generate?   (unit|integration|e2e|all)}

### Coverage Goal
${input:coverage:Target coverage?   (80%|90%|100%)}

### Include Edge Cases
${input:edge_cases:Include edge case tests?  (yes|no|comprehensive)}

### Test Framework
${input:framework:Framework?   (pytest|unittest|jest|mocha)}

---

## MANDATORY:  Pre-Generation Process

### 1. Analyze Target Code

**Locate target files:**

```powershell
# Example: Test "Email Verification" feature

# Find related files
Get-ChildItem -Path backend/src -Recurse -Filter "*email*" | Select-Object FullName

# Found: 
# - backend/src/routes/auth. py (send_verification, verify_email routes)
# - backend/src/services/email_service.py (EmailService class)
# - backend/src/models/user.py (User. email_verified field)
```

**Extract code structure:**

```python
# backend/src/services/email_service.py

class EmailService:
    @staticmethod
    def generate_verification_token(user:  User) -> str:
        """Generate unique verification token."""
        pass
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify email token."""
        pass
    
    @staticmethod
    def send_verification_email(user: User) -> bool:
        """Send verification email."""
        pass
    
    @staticmethod
    def resend_verification_email(user:  User) -> bool:
        """Resend verification email."""
        pass
```

**Identify:**
- [ ] All public methods/functions
- [ ] Input parameters & types
- [ ] Return types
- [ ] Possible exceptions
- [ ] Dependencies (DB, external APIs, etc.)
- [ ] Side effects (DB writes, emails sent, etc.)

---

### 2. Define Test Scope

**Test Coverage Matrix:**

| Component | Unit Tests | Integration Tests | E2E Tests | Edge Cases |
|-----------|-----------|-------------------|-----------|------------|
| `EmailService. generate_token()` | ✅ | ❌ | ❌ | ✅ |
| `EmailService.verify_token()` | ✅ | ❌ | ❌ | ✅ |
| `EmailService.send_email()` | ✅ (mocked) | ✅ (SMTP) | ❌ | ✅ |
| Route `/auth/send-verification` | ❌ | ✅ | ✅ | ✅ |
| Route `/auth/verify-email/<token>` | ❌ | ✅ | ✅ | ✅ |
| User model `email_verified` | ✅ | ✅ | ❌ | ✅ |

**Test categories to generate:**
- Unit tests:  15 tests
- Integration tests: 8 tests
- Edge case tests: 12 tests
- **Total: 35 tests**

---

## Test Generation Workflow

### Step 1: Generate Test File Structure

**File:** `backend/tests/test_email_verification.py`

```python
"""
Email Verification Test Suite

Purpose: Comprehensive tests for email verification feature
Coverage Target: ≥90%

File:  backend/tests/test_email_verification.py | Repository: X-Filamenta-Python
License:  AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved. 
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from backend.src import create_app, db
from backend.src.models.user import User
from backend. src.services.email_service import EmailService


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def app():
    """Create and configure test app."""
    app = create_app("testing")
    app.config.update({
        'TESTING':  True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'EMAIL_VERIFICATION_EXPIRY': 86400,  # 24 hours
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db. drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """Create unverified user."""
    user = User(
        username="testuser",
        email="test@example.com",
        email_verified=False
    )
    user.set_password("SecurePass123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def verified_user(app):
    """Create verified user."""
    user = User(
        username="verified",
        email="verified@example. com",
        email_verified=True
    )
    user.set_password("SecurePass123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def mock_smtp():
    """Mock SMTP server."""
    with patch('smtplib.SMTP') as mock: 
        instance = MagicMock()
        mock.return_value = instance
        yield instance


# ============================================================================
# UNIT TESTS - EmailService
# ============================================================================

class TestEmailServiceUnit:
    """Unit tests for EmailService (isolated, no DB/network)."""
    
    def test_generate_token_returns_string(self, app, sample_user):
        """Test token generation returns valid string."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            assert isinstance(token, str)
            assert len(token) > 20
            assert '.' in token  # JWT-like structure
    
    def test_generate_token_unique_per_user(self, app):
        """Test each user gets unique token."""
        with app.app_context():
            user1 = User(id=1, email="user1@example.com")
            user2 = User(id=2, email="user2@example.com")
            
            token1 = EmailService. generate_verification_token(user1)
            token2 = EmailService.generate_verification_token(user2)
            
            assert token1 != token2
    
    def test_generate_token_different_each_time(self, app, sample_user):
        """Test token changes on regeneration."""
        with app.app_context():
            token1 = EmailService.generate_verification_token(sample_user)
            token2 = EmailService.generate_verification_token(sample_user)
            
            assert token1 != token2
    
    def test_verify_valid_token_success(self, app, sample_user):
        """Test verifying valid token succeeds."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            result = EmailService.verify_token(token)
            
            assert result['success'] is True
            assert result['error'] is None
            assert 'verified' in result['message']. lower()
    
    def test_verify_invalid_token_fails(self, app):
        """Test verifying invalid token fails."""
        with app.app_context():
            result = EmailService.verify_token("invalid-token-123")
            
            assert result['success'] is False
            assert result['error'] == 'INVALID_TOKEN'
    
    def test_verify_token_marks_user_verified(self, app, sample_user):
        """Test verification updates user. email_verified."""
        with app.app_context():
            assert sample_user.email_verified is False
            
            token = EmailService.generate_verification_token(sample_user)
            EmailService.verify_token(token)
            
            db.session.refresh(sample_user)
            assert sample_user. email_verified is True
    
    def test_verify_token_consumes_token(self, app, sample_user):
        """Test token can only be used once."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            # First use:  success
            result1 = EmailService.verify_token(token)
            assert result1['success'] is True
            
            # Second use: fail (already verified)
            result2 = EmailService.verify_token(token)
            assert result2['success'] is False
            assert result2['error'] == 'ALREADY_VERIFIED'
    
    def test_verify_expired_token_fails(self, app, sample_user):
        """Test expired token is rejected."""
        with app.app_context():
            # Generate token
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = serializer.dumps({'user_id': sample_user. id})
            
            # Mock expiry by patching serializer. loads
            with patch.object(URLSafeTimedSerializer, 'loads', side_effect=SignatureExpired("Expired")):
                result = EmailService. verify_token(token)
            
            assert result['success'] is False
            assert result['error'] == 'TOKEN_EXPIRED'
            assert 'expired' in result['message'].lower()
    
    def test_verify_malformed_token_fails(self, app):
        """Test malformed token is rejected."""
        with app.app_context():
            result = EmailService.verify_token("not. a.valid.token")
            
            assert result['success'] is False
            assert result['error'] in ['INVALID_TOKEN', 'INTERNAL_ERROR']
    
    def test_send_email_with_mock_smtp(self, app, sample_user, mock_smtp):
        """Test email sending (SMTP mocked)."""
        with app.app_context():
            result = EmailService.send_verification_email(sample_user)
            
            assert result is True
            mock_smtp.send_message.assert_called_once()
    
    def test_send_email_stores_token_in_db(self, app, sample_user):
        """Test token is stored in user record."""
        with app.app_context():
            EmailService.send_verification_email(sample_user)
            
            db.session.refresh(sample_user)
            assert sample_user.email_verification_token is not None
            assert sample_user.email_verification_token_created is not None
    
    def test_resend_invalidates_old_token(self, app, sample_user):
        """Test resending generates new token."""
        with app. app_context():
            # First send
            EmailService.send_verification_email(sample_user)
            token1 = sample_user.email_verification_token
            
            # Resend
            EmailService.send_verification_email(sample_user)
            token2 = sample_user.email_verification_token
            
            assert token1 != token2
            
            # Old token should fail
            result = EmailService.verify_token(token1)
            assert result['success'] is False


# ============================================================================
# INTEGRATION TESTS - Routes
# ============================================================================

class TestEmailVerificationRoutes:
    """Integration tests for email verification routes."""
    
    def test_send_verification_requires_login(self, client):
        """Test /auth/send-verification requires authentication."""
        response = client.post('/auth/send-verification')
        
        assert response.status_code == 302  # Redirect to login
        assert b'login' in response.data. lower() or response.location. endswith('/auth/login')
    
    def test_send_verification_when_logged_in(self, client, sample_user):
        """Test sending verification when logged in."""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        })
        
        # Send verification
        response = client.post('/auth/send-verification')
        
        assert response.status_code == 200
        assert b'sent' in response.data. lower()
    
    def test_send_verification_already_verified(self, client, verified_user):
        """Test cannot send verification if already verified."""
        # Login
        client.post('/auth/login', data={
            'email': 'verified@example.com',
            'password': 'SecurePass123!'
        })
        
        # Try to send
        response = client.post('/auth/send-verification')
        
        assert response.status_code == 400
        assert b'already verified' in response.data.lower()
    
    def test_verify_email_with_valid_token(self, client, sample_user, app):
        """Test GET /auth/verify-email/<token> with valid token."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
        
        response = client.get(f'/auth/verify-email/{token}')
        
        assert response.status_code == 200
        assert b'verified' in response.data.lower()
        
        # Check DB
        with app.app_context():
            user = User.query.get(sample_user.id)
            assert user.email_verified is True
    
    def test_verify_email_with_invalid_token(self, client):
        """Test verification with invalid token."""
        response = client.get('/auth/verify-email/invalid-token-abc123')
        
        assert response.status_code == 400
        assert b'invalid' in response.data.lower()
    
    def test_verify_email_htmx_request(self, client, sample_user, app):
        """Test HTMX request returns partial."""
        with app.app_context():
            token = EmailService. generate_verification_token(sample_user)
        
        response = client.get(
            f'/auth/verify-email/{token}',
            headers={'HX-Request': 'true'}
        )
        
        assert response.status_code == 200
        assert b'<div' in response.data  # Partial HTML
    
    def test_rate_limiting_send_verification(self, client, sample_user):
        """Test rate limiting on send-verification."""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        })
        
        # Send multiple times (rate limit:  10/hour)
        responses = []
        for i in range(12):
            response = client.post('/auth/send-verification')
            responses.append(response. status_code)
        
        # Last request should be rate limited
        assert 429 in responses  # Too Many Requests


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEmailVerificationEdgeCases: 
    """Edge cases and error scenarios."""
    
    def test_token_with_deleted_user(self, app):
        """Test token for deleted user."""
        with app. app_context():
            user = User(id=999, email="temp@example.com")
            db.session.add(user)
            db.session.commit()
            
            token = EmailService. generate_verification_token(user)
            
            # Delete user
            db.session.delete(user)
            db.session.commit()
            
            # Try to verify
            result = EmailService. verify_token(token)
            
            assert result['success'] is False
            assert result['error'] == 'USER_NOT_FOUND'
    
    def test_concurrent_verification_attempts(self, app, sample_user):
        """Test race condition:  multiple verification attempts."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            # Simulate concurrent requests
            result1 = EmailService.verify_token(token)
            result2 = EmailService.verify_token(token)
            
            # Only one should succeed
            assert result1['success'] is True
            assert result2['success'] is False
            assert result2['error'] == 'ALREADY_VERIFIED'
    
    def test_token_from_different_app_instance(self, app, sample_user):
        """Test token generated with different SECRET_KEY."""
        with app. app_context():
            # Generate token with original key
            token = EmailService.generate_verification_token(sample_user)
        
        # Change secret key
        app.config['SECRET_KEY'] = 'different-secret-key'
        
        with app.app_context():
            result = EmailService.verify_token(token)
            
            # Should fail (signature mismatch)
            assert result['success'] is False
            assert result['error'] == 'INVALID_TOKEN'
    
    def test_token_expiry_boundary(self, app, sample_user):
        """Test token at exact expiry boundary."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            # Set token created exactly 24h ago
            sample_user.email_verification_token_created = datetime.utcnow() - timedelta(hours=24)
            db.session.commit()
            
            result = EmailService.verify_token(token)
            
            # Should be expired
            assert result['success'] is False
            assert result['error'] == 'TOKEN_EXPIRED'
    
    def test_malicious_token_injection(self, app):
        """Test SQL injection via token."""
        with app.app_context():
            malicious_token = "'; DROP TABLE users; --"
            
            result = EmailService.verify_token(malicious_token)
            
            assert result['success'] is False
            # DB should still exist
            assert User.query.count() >= 0
    
    def test_unicode_in_email(self, app):
        """Test verification with unicode email."""
        with app.app_context():
            user = User(email="测试@example.com", username="unicode_test")
            db.session. add(user)
            db.session.commit()
            
            token = EmailService.generate_verification_token(user)
            result = EmailService.verify_token(token)
            
            assert result['success'] is True
    
    def test_very_long_token(self, app, sample_user):
        """Test handling of extremely long token."""
        with app. app_context():
            long_token = "a" * 10000
            
            result = EmailService. verify_token(long_token)
            
            assert result['success'] is False
    
    def test_empty_token(self, app):
        """Test verification with empty token."""
        with app.app_context():
            result = EmailService.verify_token("")
            
            assert result['success'] is False
    
    def test_null_token(self, app):
        """Test verification with None token."""
        with app.app_context():
            result = EmailService.verify_token(None)
            
            assert result['success'] is False


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestEmailVerificationPerformance:
    """Performance and load tests."""
    
    def test_bulk_token_generation(self, app):
        """Test generating many tokens quickly."""
        with app.app_context():
            users = [User(id=i, email=f"user{i}@example.com") for i in range(100)]
            
            import time
            start = time.time()
            
            tokens = [EmailService.generate_verification_token(u) for u in users]
            
            duration = time.time() - start
            
            assert len(tokens) == 100
            assert len(set(tokens)) == 100  # All unique
            assert duration < 1.0  # Should be fast (<1 second)
    
    def test_verification_performance(self, app, sample_user):
        """Test verification speed."""
        with app.app_context():
            token = EmailService.generate_verification_token(sample_user)
            
            import time
            start = time.time()
            
            EmailService.verify_token(token)
            
            duration = time. time() - start
            
            assert duration < 0.1  # Should be very fast (<100ms)


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

Unit Tests: 12 tests
Integration Tests: 7 tests
Edge Case Tests: 8 tests
Performance Tests: 2 tests

Total: 29 tests

Expected Coverage:  ≥90%

Run tests: 
    pytest backend/tests/test_email_verification.py -v --cov

Run specific test class:
    pytest backend/tests/test_email_verification.py:: TestEmailServiceUnit -v

Run with coverage report:
    pytest backend/tests/test_email_verification.py --cov=backend.src.services.email_service --cov-report=html
"""
```

---

### Step 2: Generate Test Configuration

**File:** `backend/tests/conftest.py` (if not exists)

```python
"""
Pytest Configuration and Shared Fixtures

Purpose: Global test configuration and reusable fixtures
File: backend/tests/conftest. py | Repository: X-Filamenta-Python
"""
import pytest
from backend.src import create_app, db


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app


@pytest.fixture(scope='function')
def _db(app):
    """Create database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture
def session(_db):
    """Create database session."""
    connection = _db.engine.connect()
    transaction = connection.begin()
    
    session = _db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    _db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()
```

---

### Step 3: Generate Test Documentation

**File:** `backend/tests/README.md`

```markdown
# Test Suite Documentation

## Running Tests

### Run all tests
```bash
pytest backend/tests/ -v
```

### Run specific test file
```bash
pytest backend/tests/test_email_verification.py -v
```

### Run with coverage
```bash
pytest backend/tests/ --cov=backend.src --cov-report=html
```

### Run specific test class
```bash
pytest backend/tests/test_email_verification.py::TestEmailServiceUnit -v
```

### Run specific test
```bash
pytest backend/tests/test_email_verification.py:: TestEmailServiceUnit::test_generate_token_returns_string -v
```

## Coverage Goals

- **Minimum:** 80%
- **Target:** 90%
- **Ideal:** 95%+

## Test Organization

```
tests/
├── conftest.py                      # Global fixtures
├── test_email_verification.py       # Email verification tests
├── test_auth.py                     # Authentication tests
├── test_models/
│   ├── test_user.py
│   └── test_content.py
└── test_services/
    ├── test_email_service.py
    └── test_cache_service.py
```

## Writing New Tests

### Naming Convention

- Test files: `test_<feature>. py`
- Test classes: `Test<Feature><TestType>` (e.g., `TestEmailServiceUnit`)
- Test functions: `test_<what>_<condition>_<expected>` (e.g., `test_verify_token_expired_fails`)

### Test Structure

```python
def test_feature_description(fixture1, fixture2):
    """Test that feature does X when Y."""
    # Arrange
    setup_data = create_test_data()
    
    # Act
    result = function_under_test(setup_data)
    
    # Assert
    assert result == expected_value
```

## CI/CD Integration

Tests run automatically on:
- Every commit (GitHub Actions)
- Every pull request
- Before deployment

## Troubleshooting

### Tests fail locally but pass in CI
- Check Python version (`python --version`)
- Ensure clean database (`flask db upgrade`)
- Clear pytest cache (`pytest --cache-clear`)

### Coverage not updating
- Delete `.coverage` file
- Run `pytest --cov --cov-report=html` again
```

---

### Step 4: Generate GitHub Action Workflow

**File:** `.github/workflows/tests.yml`

```yaml
name: Test Suite

on:
  push: 
    branches: [main, develop]
  pull_request: 
    branches: [main, develop]

jobs:
  test: 
    runs-on: ubuntu-latest
    
    strategy:
      matrix: 
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      
      - name:  Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name:  Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests
        run: |
          pytest backend/tests/ -v --cov=backend.src --cov-report=xml --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name:  codecov-${{ matrix.python-version }}
      
      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80
```

---

## Validation Checklist

### Test Quality
- [ ] All public methods tested
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Performance tested (if applicable)

### Code Quality
- [ ] Type hints on all test functions
- [ ] Docstrings on all test functions
- [ ] Fixtures properly scoped
- [ ] No hardcoded values (use fixtures/constants)
- [ ] Tests are deterministic (no flaky tests)

### Coverage
- [ ] Coverage ≥ target percentage
- [ ] All critical paths covered
- [ ] All branches covered
- [ ] All exceptions covered

### Documentation
- [ ] Test file has header
- [ ] Test functions have docstrings
- [ ] README explains how to run tests
- [ ] CI/CD configured

---

## Don'ts

- ❌ Test framework code (Flask, SQLAlchemy, etc.)
- ❌ Write flaky tests (random failures)
- ❌ Skip edge cases
- ❌ Use `sleep()` in tests (use mocks)
- ❌ Test implementation details (test behavior)
- ❌ Ignore coverage warnings
- ❌ Commit failing tests
- ❌ Skip docstrings on tests

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage. py Documentation](https://coverage.readthedocs.io/)
- `.github/copilot-instructions.md` — General rules
- `.github/workflow-rules.md` — Testing workflow

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.