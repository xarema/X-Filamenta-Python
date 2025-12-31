---
Purpose: Test suite documentation and guidelines for X-Filamenta-Python
Description: Comprehensive guide for running, writing, and maintaining tests

File: backend/tests/README.md | Repository: X-Filamenta-Python
Created: 2025-12-30T00:00:00+00:00
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
- Follow this guide when writing or running tests
- All tests use pytest framework
- Database uses in-memory SQLite for isolation and speed
---

# X-Filamenta-Python Test Suite Documentation

## Quick Start

### Install Test Dependencies

```bash
pip install pytest pytest-cov pytest-xdist pytest-mock pytest-flask
```

### Run All Tests

```bash
pytest backend/tests/ -v
```

### Run Tests with Coverage Report

```bash
pytest backend/tests/ -v --cov=backend.src --cov-report=html
```

## Test Structure

### Directory Organization

```
backend/tests/
├── conftest.py                          # Shared pytest fixtures & configuration
├── pytest.ini                           # Pytest configuration
├── README.md                            # This file
│
├── test_models/                         # Model unit tests
│   ├── test_user.py                    # User model tests
│   ├── test_settings.py                # Settings model tests
│   ├── test_content.py                 # Content model tests
│   └── test_admin_history.py           # Admin history model tests
│
├── test_services/                       # Service unit & integration tests
│   ├── test_email_service.py           # Email verification & password reset
│   ├── test_auth_service.py            # Authentication logic
│   ├── test_cache_service.py           # Caching (filesystem/Redis)
│   ├── test_user_service.py            # User operations
│   └── test_i18n_service.py            # Internationalization
│
├── test_routes/                         # Route integration tests
│   ├── test_auth_routes.py             # Authentication endpoints
│   ├── test_admin_routes.py            # Admin panel routes
│   ├── test_public_routes.py           # Public pages
│   ├── test_install_routes.py          # Installation wizard
│   ├── test_content_routes.py          # Content management
│   └── test_error_handlers.py          # Error handling
│
├── test_integration/                    # End-to-end scenarios
│   ├── test_user_registration_flow.py  # Full signup & verification
│   ├── test_login_logout_flow.py       # Login/logout scenarios
│   ├── test_password_reset_flow.py     # Password reset process
│   ├── test_2fa_flow.py                # Two-factor authentication
│   └── test_admin_workflow.py          # Admin operations
│
└── test_edge_cases/                     # Edge cases & security
    ├── test_security.py                # XSS, SQL injection, etc.
    ├── test_race_conditions.py         # Concurrent access
    ├── test_unicode_handling.py        # Unicode & internationalization
    └── test_malformed_inputs.py        # Invalid data handling
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest backend/tests/

# Run with verbose output
pytest backend/tests/ -v

# Run specific test file
pytest backend/tests/test_models/test_user.py -v

# Run specific test class
pytest backend/tests/test_models/test_user.py::TestUserModel -v

# Run specific test function
pytest backend/tests/test_models/test_user.py::TestUserModel::test_user_creation -v
```

### Coverage Reports

```bash
# Generate HTML coverage report (saved to htmlcov/)
pytest backend/tests/ --cov=backend.src --cov-report=html

# Show coverage in terminal with missing lines
pytest backend/tests/ --cov=backend.src --cov-report=term-missing

# Check coverage threshold (fail if < 80%)
pytest backend/tests/ --cov=backend.src --cov-fail-under=80
```

### Performance & Optimization

```bash
# Run tests in parallel (4 workers)
pytest backend/tests/ -n 4

# Show slowest 10 tests
pytest backend/tests/ --durations=10

# Stop on first failure
pytest backend/tests/ -x

# Stop after N failures
pytest backend/tests/ --maxfail=3
```

### Filtering Tests

```bash
# Run only unit tests
pytest backend/tests/ -m unit

# Run only integration tests
pytest backend/tests/ -m integration

# Run tests excluding slow tests
pytest backend/tests/ -m "not slow"

# Run tests by keyword
pytest backend/tests/ -k "test_user"

# Run tests matching pattern
pytest backend/tests/ -k "email or verification"
```

## Writing Tests

### Test File Naming

- Test files: `test_<feature>.py`
- Test classes: `Test<Feature><Category>` (e.g., `TestUserModel`, `TestAuthRoutes`)
- Test functions: `test_<what>_<condition>_<expected>` (e.g., `test_user_creation_with_valid_data_succeeds`)

### Test Structure (AAA Pattern)

```python
def test_feature_description(fixture1, fixture2):
    """Test that feature does X when Y (1-2 lines max).
    
    Optionally add more detail in extended docstring.
    """
    # ---- ARRANGE ----
    # Setup: create test data, mocks, etc.
    test_data = create_test_data()
    
    # ---- ACT ----
    # Execute: call function/endpoint under test
    result = function_under_test(test_data)
    
    # ---- ASSERT ----
    # Verify: check expected outcome
    assert result == expected_value
    assert result.status_code == 200
```

### Example Tests

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.unit
def test_user_creation_with_valid_data_succeeds(sample_user):
    """Test creating a user with valid data."""
    # Arrange
    assert sample_user.id is None  # Not yet saved
    
    # Act
    db.session.add(sample_user)
    db.session.commit()
    
    # Assert
    assert sample_user.id is not None
    assert sample_user.username == "testuser"


@pytest.mark.integration
def test_login_route_with_valid_credentials_succeeds(client, sample_user):
    """Test login route accepts valid credentials."""
    # Arrange (sample_user fixture already created)
    
    # Act
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "SecurePass123!",
    })
    
    # Assert
    assert response.status_code == 302  # Redirect to dashboard
    assert "dashboard" in response.location.lower()


@pytest.mark.edge_case
def test_login_route_with_nonexistent_email_fails(client):
    """Test login rejects nonexistent email."""
    response = client.post("/auth/login", data={
        "email": "nonexistent@example.com",
        "password": "AnyPassword123!",
    })
    
    assert response.status_code == 401
    assert b"invalid" in response.data.lower()


@pytest.mark.unit
@patch("backend.src.services.email_service.send_email")
def test_send_verification_email_mocked(mock_send, sample_user):
    """Test email sending with mocked SMTP."""
    # Arrange
    mock_send.return_value = True
    
    # Act
    result = EmailService.send_verification_email(sample_user)
    
    # Assert
    assert result is True
    mock_send.assert_called_once()
```

## Fixtures Guide

### Database Fixtures

```python
def test_user_operations(_db, sample_user):
    """Tests have access to database."""
    # _db is the SQLAlchemy db instance
    count = _db.session.query(User).count()
    assert count == 1  # sample_user was created by fixture
```

### User Fixtures

```python
# sample_user: unverified, no 2FA
def test_unverified_user(sample_user):
    assert sample_user.email_verified is False

# verified_user: verified, no 2FA
def test_verified_user(verified_user):
    assert verified_user.email_verified is True

# admin_user: admin with all privileges
def test_admin(admin_user):
    assert admin_user.is_admin is True

# user_with_2fa: verified with 2FA enabled
def test_2fa_user(user_with_2fa):
    assert user_with_2fa.totp_enabled is True

# multiple_users: 10 users with varying states
def test_bulk_operations(multiple_users):
    assert len(multiple_users) == 10
```

### Authentication Fixtures

```python
# logged_in_client: authenticated session
def test_protected_route(logged_in_client):
    response = logged_in_client.get("/dashboard")
    assert response.status_code == 200

# admin_client: admin authenticated session
def test_admin_only_route(admin_client):
    response = admin_client.get("/admin")
    assert response.status_code == 200
```

### Mock Fixtures

```python
# mock_smtp: prevents actual email sends
def test_email_with_mock(mock_smtp):
    EmailService.send_verification_email(user)
    assert mock_smtp.send_message.called

# mock_cache: prevents filesystem/Redis access
def test_cache_with_mock(mock_cache):
    cache.set("key", "value")
    mock_cache.set.assert_called_with("key", "value")
```

## Best Practices

### ✅ DO

- ✅ Use descriptive test names
- ✅ Test one thing per test
- ✅ Use fixtures for setup
- ✅ Mock external services
- ✅ Test both happy path and error cases
- ✅ Test edge cases (empty, null, unicode, etc.)
- ✅ Use parametrize for multiple similar tests
- ✅ Keep tests fast (< 1 second for unit tests)
- ✅ Use pytest markers for test categorization
- ✅ Add docstrings explaining test purpose

### ❌ DON'T

- ❌ Test framework internals (Flask, SQLAlchemy, etc.)
- ❌ Write flaky tests (random failures)
- ❌ Skip edge cases
- ❌ Use `sleep()` in tests (use mocks instead)
- ❌ Write slow tests (> 1 second)
- ❌ Test implementation details
- ❌ Have shared state between tests
- ❌ Commit failing tests
- ❌ Use real external services (email, SMS, etc.)
- ❌ Hardcode values (use fixtures)

## Coverage Goals

| Module | Minimum | Target | Ideal |
|--------|---------|--------|-------|
| Critical services (auth, email) | 90% | 95% | 98% |
| Main models | 85% | 90% | 95% |
| Routes | 80% | 90% | 95% |
| Utilities | 75% | 85% | 90% |
| **Overall** | **80%** | **85%** | **90%+** |

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Every push to `main` and `develop`
- Every pull request
- Manual trigger via workflow_dispatch

See `.github/workflows/test.yml` for configuration.

### Running Tests Locally Before Commit

```bash
# Recommended pre-commit check
pytest backend/tests/ --cov=backend.src --cov-fail-under=80 -x
```

## Troubleshooting

### Tests Fail Locally but Pass in CI

**Solution:**
```bash
# Clean pytest cache
pytest --cache-clear

# Reset database
rm -rf instance/*.db

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Coverage Not Updating

**Solution:**
```bash
# Delete coverage data
rm -rf .coverage htmlcov/

# Run again with fresh data
pytest --cov --cov-report=html
```

### Tests Run Slowly

**Solution:**
```bash
# Run with parallel execution
pytest -n auto

# Run only unit tests (faster)
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Fixtures Not Found

**Solution:**
```bash
# Ensure conftest.py is in backend/tests/
# Ensure test file is in backend/tests/ subdirectory
# Restart IDE/editor

# Verify conftest.py is valid
pytest --collect-only backend/tests/conftest.py
```

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Flask Plugin](https://pytest-flask.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-sessionmaker)
- `.github/copilot-instructions.md` — General AI rules
- `.github/python.instructions.md` — Python-specific rules

## Questions or Issues?

- Check existing test files for examples
- Review `conftest.py` for available fixtures
- Run `pytest --co` to see all available tests
- Use `-v` flag for verbose output
- Run `pytest -h` for all available options

---

**Last Updated:** 2025-12-30  
**Status:** Ready for Phase 1 test generation  
**Next Steps:** Generate unit tests for core models and services

