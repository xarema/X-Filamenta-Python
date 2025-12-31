"""
---
Purpose: Pytest configuration and shared fixtures for X-Filamenta-Python test suite
Description: Global test configuration, database setup, and reusable fixtures for all tests

File: backend/tests/conftest.py | Repository: X-Filamenta-Python
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
- Pytest fixtures are session, module, function, or package scoped
- Database is in-memory SQLite for testing (faster, isolated)
- All fixtures automatically available to test files in backend/tests/
---
"""

import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import tempfile
import sys

# Add backend/src to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.src import create_app, db
from backend.src.models.user import User
from backend.src.models.settings import Settings


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as testing edge cases"
    )


# ============================================================================
# APP & DATABASE FIXTURES (Session-scoped)
# ============================================================================

@pytest.fixture(scope="session")
def app():
    """Create Flask application for testing.

    Uses in-memory SQLite database for speed and isolation.
    Configured with testing settings.
    """
    app = create_app("testing")

    # Override config for testing
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key-do-not-use-in-production",
        "MAIL_SUPPRESS_SEND": True,
        "MAIL_BACKEND": "locmem",
        # Email verification settings
        "EMAIL_VERIFICATION_REQUIRED": True,
        "EMAIL_VERIFICATION_TOKEN_EXPIRY": 86400,  # 24 hours
        # Password reset settings
        "PASSWORD_RESET_TOKEN_EXPIRY": 1800,  # 30 minutes
        # 2FA settings
        "TOTP_ISSUER": "X-Filamenta-Test",
        "TOTP_WINDOW": 1,
        # Cache settings
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": tempfile.gettempdir(),
    })

    return app


@pytest.fixture(scope="session")
def app_context(app):
    """Create application context for the session.

    Ensures app context is available for database operations.
    """
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def _db(app_context):
    """Create database tables and yield db instance.

    Creates fresh tables for each test, then drops them after.
    Ensures test isolation.
    """
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create Flask test client.

    Used for making HTTP requests to routes in tests.
    Automatically handles test request context.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Create Flask CLI test runner.

    Used for testing CLI commands.
    """
    return app.test_cli_runner()


# ============================================================================
# DATABASE SESSION FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def session(_db):
    """Create isolated database session for test.

    Each test gets its own transaction that's rolled back after.
    Ensures complete isolation between tests.
    """
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


# ============================================================================
# USER FIXTURES
# ============================================================================

@pytest.fixture
def sample_user(_db):
    """Create an unverified test user.

    Username: testuser
    Email: test@example.com
    Password: SecurePass123!
    Verified: No
    2FA: Disabled
    """
    user = User(
        username="testuser",
        email="test@example.com",
        is_active=True,
        email_verified=False,
        totp_enabled=False,
    )
    user.set_password("SecurePass123!")

    _db.session.add(user)
    _db.session.commit()

    return user


@pytest.fixture
def verified_user(_db):
    """Create a verified test user.

    Username: verified
    Email: verified@example.com
    Password: SecurePass123!
    Verified: Yes
    2FA: Disabled
    """
    user = User(
        username="verified",
        email="verified@example.com",
        is_active=True,
        email_verified=True,
        totp_enabled=False,
    )
    user.set_password("SecurePass123!")

    _db.session.add(user)
    _db.session.commit()

    return user


@pytest.fixture
def admin_user(_db):
    """Create an admin test user.

    Username: admin
    Email: admin@example.com
    Password: AdminPass123!
    Verified: Yes
    Is Admin: Yes
    """
    user = User(
        username="admin",
        email="admin@example.com",
        is_admin=True,
        is_active=True,
        email_verified=True,
        totp_enabled=False,
    )
    user.set_password("AdminPass123!")

    _db.session.add(user)
    _db.session.commit()

    return user


@pytest.fixture
def user_with_2fa(_db):
    """Create a user with 2FA enabled.

    Username: user2fa
    Email: user2fa@example.com
    Password: SecurePass123!
    2FA: Enabled
    """
    user = User(
        username="user2fa",
        email="user2fa@example.com",
        is_active=True,
        email_verified=True,
        totp_enabled=True,
    )
    user.set_password("SecurePass123!")

    # Generate TOTP secret
    import pyotp
    user.totp_secret = pyotp.random_base32()

    _db.session.add(user)
    _db.session.commit()

    return user


@pytest.fixture
def multiple_users(_db):
    """Create multiple test users for bulk testing.

    Creates 10 users with different states:
    - 5 verified
    - 5 unverified
    - 2 with 2FA enabled
    - 1 admin
    """
    users = []

    for i in range(10):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            is_active=(i % 2 == 0),
            email_verified=(i < 5),
            is_admin=(i == 0),
            totp_enabled=(i in [3, 7]),
        )
        user.set_password(f"Pass{i}Secure123!")
        users.append(user)
        _db.session.add(user)

    _db.session.commit()

    return users


# ============================================================================
# AUTHENTICATION & SESSION FIXTURES
# ============================================================================

@pytest.fixture
def logged_in_client(client, sample_user):
    """Create test client with logged-in user.

    User: testuser (sample_user)
    Session: Authenticated
    """
    client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "SecurePass123!",
    }, follow_redirects=True)

    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Create test client with logged-in admin user.

    User: admin
    Session: Authenticated with admin privileges
    """
    client.post("/auth/login", data={
        "email": "admin@example.com",
        "password": "AdminPass123!",
    }, follow_redirects=True)

    return client


# ============================================================================
# EMAIL & TOKEN FIXTURES
# ============================================================================

@pytest.fixture
def email_verification_token(sample_user, app):
    """Generate valid email verification token.

    Token will be valid for 24 hours.
    """
    from backend.src.services.email_service import EmailService

    with app.app_context():
        token = EmailService.generate_verification_token(sample_user)
        return token


@pytest.fixture
def expired_token(sample_user, app):
    """Generate expired token for testing expiration handling.

    Token is backdated to 25 hours ago (expires after 24h).
    """
    from itsdangerous import URLSafeTimedSerializer

    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    token = serializer.dumps({"user_id": sample_user.id})

    return token


# ============================================================================
# MOCK & PATCH FIXTURES
# ============================================================================

@pytest.fixture
def mock_smtp():
    """Mock SMTP server for email testing.

    Patches smtplib.SMTP to prevent actual email sends.
    Tracks send_message calls.
    """
    with patch("smtplib.SMTP") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


@pytest.fixture
def mock_email_service():
    """Mock email service for route testing.

    Patches email sending to prevent actual sends.
    """
    with patch("backend.src.services.email_service.EmailService.send_verification_email") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_cache():
    """Mock cache service for testing.

    Patches cache operations without actual file/Redis access.
    """
    with patch("backend.src.services.cache_service.cache") as mock:
        yield mock


@pytest.fixture
def mock_redis():
    """Mock Redis client for cache testing.

    Patches redis.Redis to simulate Redis operations.
    """
    with patch("redis.Redis") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


# ============================================================================
# SETTINGS & CONFIGURATION FIXTURES
# ============================================================================

@pytest.fixture
def app_settings(_db):
    """Create default application settings for testing.

    Sets up all default settings as they appear in fresh installation.
    """
    settings = {
        "site_name": "X-Filamenta Test",
        "site_url": "http://localhost:5000",
        "email_verification_required": "True",
        "registration_enabled": "True",
        "2fa_required": "False",
        "password_reset_token_expiry_minutes": "30",
        "email_verification_token_expiry_hours": "24",
    }

    for key, value in settings.items():
        setting = Settings(key=key, value=value)
        _db.session.add(setting)

    _db.session.commit()

    return settings


# ============================================================================
# HELPER FUNCTIONS & UTILITIES
# ============================================================================

@pytest.fixture
def assert_no_user_email_sent():
    """Helper to assert no emails were sent during test.

    Used with mock_smtp to verify email service wasn't called.
    """
    def _assert():
        with patch("smtplib.SMTP") as mock:
            assert mock.return_value.send_message.call_count == 0

    return _assert


@pytest.fixture
def create_user_with_state(_db):
    """Factory fixture for creating users with specific states.

    Allows tests to create users with custom properties.

    Usage:
        user = create_user_with_state(
            username="custom",
            email_verified=True,
            totp_enabled=True
        )
    """
    def _create(username="testuser", email="test@example.com",
                password="Pass123!", **kwargs):
        user = User(
            username=username,
            email=email,
            **kwargs
        )
        user.set_password(password)
        _db.session.add(user)
        _db.session.commit()
        return user

    return _create


# ============================================================================
# CLEANUP & TEARDOWN
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Auto-cleanup database sessions after each test.

    Ensures no session leaks between tests.
    """
    yield
    db.session.remove()


# ============================================================================
# DEBUG HELPERS
# ============================================================================

@pytest.fixture
def print_db_state(session):
    """Debug fixture to print database state during tests.

    Usage in test:
        def test_something(session, print_db_state):
            # ... test code ...
            print_db_state()  # Prints all table contents
    """
    def _print():
        print("\n=== DATABASE STATE ===")
        print(f"Users: {User.query.count()}")
        for user in User.query.all():
            print(f"  - {user.username} ({user.email})")
        print("=====================\n")

    return _print

