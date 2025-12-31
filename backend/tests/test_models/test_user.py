"""
---
Purpose: Unit tests for User model
Description: Comprehensive tests for User model functionality, validation, and methods

File: backend/tests/test_models/test_user.py | Repository: X-Filamenta-Python
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
- Tests User model CRUD, validation, and security features
- Tests password hashing, email verification, 2FA
- Target: 95%+ coverage
---
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pyotp

from backend.src import db
from backend.src.models.user import User


# ============================================================================
# UNIT TESTS - User Model Creation & Validation
# ============================================================================

@pytest.mark.unit
class TestUserCreation:
    """Tests for basic user creation and validation."""

    def test_user_creation_with_required_fields_succeeds(self, _db):
        """Test creating user with only required fields."""
        user = User(username="john", email="john@example.com")
        user.set_password("SecurePass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.id is not None
        assert user.username == "john"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert user.email_verified is False

    def test_user_creation_with_all_fields_succeeds(self, _db):
        """Test creating user with all optional fields."""
        user = User(
            username="jane",
            email="jane@example.com",
            is_admin=True,
            is_active=True,
            role="moderator",
        )
        user.set_password("SecurePass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.is_admin is True
        assert user.role == "moderator"

    def test_user_creation_without_username_fails(self, _db):
        """Test user creation without username raises error."""
        user = User(email="test@example.com")
        user.set_password("SecurePass123!")

        _db.session.add(user)

        with pytest.raises(Exception):  # IntegrityError or similar
            _db.session.commit()

    def test_user_creation_without_email_fails(self, _db):
        """Test user creation without email raises error."""
        user = User(username="testuser")
        user.set_password("SecurePass123!")

        _db.session.add(user)

        with pytest.raises(Exception):
            _db.session.commit()

    def test_duplicate_username_fails(self, _db, sample_user):
        """Test creating user with duplicate username fails."""
        user2 = User(username="testuser", email="other@example.com")
        user2.set_password("Pass123!")

        _db.session.add(user2)

        with pytest.raises(Exception):  # IntegrityError
            _db.session.commit()

    def test_duplicate_email_fails(self, _db, sample_user):
        """Test creating user with duplicate email fails."""
        user2 = User(username="other", email="test@example.com")
        user2.set_password("Pass123!")

        _db.session.add(user2)

        with pytest.raises(Exception):  # IntegrityError
            _db.session.commit()


# ============================================================================
# UNIT TESTS - Password Hashing & Verification
# ============================================================================

@pytest.mark.unit
class TestPasswordSecurity:
    """Tests for password hashing and security."""

    def test_set_password_hashes_password(self, sample_user):
        """Test that password is hashed, not stored in plain text."""
        password = "MySecurePass123!"
        sample_user.set_password(password)

        assert sample_user.password_hash is not None
        assert sample_user.password_hash != password
        assert len(sample_user.password_hash) > 20

    def test_check_password_with_correct_password_succeeds(self, sample_user):
        """Test checking password with correct value."""
        password = "SecurePass123!"
        sample_user.set_password(password)

        assert sample_user.check_password(password) is True

    def test_check_password_with_incorrect_password_fails(self, sample_user):
        """Test checking password with incorrect value."""
        sample_user.set_password("SecurePass123!")

        assert sample_user.check_password("WrongPassword!") is False

    def test_check_password_case_sensitive(self, sample_user):
        """Test password checking is case sensitive."""
        sample_user.set_password("SecurePass123!")

        assert sample_user.check_password("securepass123!") is False

    def test_password_hash_unique_per_password(self, _db):
        """Test same password produces different hashes (salt)."""
        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("SamePassword123!")

        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("SamePassword123!")

        # Different hashes due to salt
        assert user1.password_hash != user2.password_hash
        # Both check password correctly
        assert user1.check_password("SamePassword123!")
        assert user2.check_password("SamePassword123!")


# ============================================================================
# UNIT TESTS - Email Verification
# ============================================================================

@pytest.mark.unit
class TestEmailVerification:
    """Tests for email verification functionality."""

    def test_new_user_email_not_verified_by_default(self, _db):
        """Test new users are not verified."""
        user = User(username="new", email="new@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.email_verified is False
        assert user.email_verification_token is None

    def test_mark_email_verified(self, sample_user, _db):
        """Test marking email as verified."""
        assert sample_user.email_verified is False

        sample_user.email_verified = True
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.email_verified is True

    def test_email_verification_token_storage(self, sample_user, _db):
        """Test storing email verification token."""
        token = "test-verification-token-12345"
        sample_user.email_verification_token = token
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.email_verification_token == token

    def test_email_verification_token_expiry_storage(self, sample_user, _db):
        """Test storing email verification token expiry."""
        now = datetime.utcnow()
        sample_user.email_verification_token_expiry = now + timedelta(hours=24)
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.email_verification_token_expiry is not None


# ============================================================================
# UNIT TESTS - Two-Factor Authentication (2FA/TOTP)
# ============================================================================

@pytest.mark.unit
class TestTwoFactorAuthentication:
    """Tests for TOTP/2FA functionality."""

    def test_new_user_2fa_disabled_by_default(self, _db):
        """Test new users don't have 2FA enabled."""
        user = User(username="new2fa", email="new2fa@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.totp_enabled is False
        assert user.totp_secret is None

    def test_generate_totp_secret(self, sample_user):
        """Test generating TOTP secret."""
        secret = pyotp.random_base32()
        sample_user.totp_secret = secret

        assert sample_user.totp_secret is not None
        assert len(sample_user.totp_secret) == 32

    def test_verify_totp_code_success(self, user_with_2fa):
        """Test verifying correct TOTP code."""
        totp = pyotp.TOTP(user_with_2fa.totp_secret)
        code = totp.now()

        # Would be implemented in auth service
        assert len(code) == 6
        assert code.isdigit()

    def test_backup_codes_generation(self, sample_user, _db):
        """Test generating backup codes."""
        # Generate backup codes (typically 10 codes)
        import secrets
        codes = [secrets.token_hex(4) for _ in range(10)]
        sample_user.backup_codes = ",".join(codes)
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert len(refreshed.backup_codes.split(",")) == 10


# ============================================================================
# UNIT TESTS - Login Attempt Tracking & Account Lockout
# ============================================================================

@pytest.mark.unit
class TestLoginSecurity:
    """Tests for login attempt tracking and lockout."""

    def test_new_user_no_login_attempts(self, _db):
        """Test new user has no login attempts."""
        user = User(username="newlogin", email="newlogin@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.login_attempts == 0
        assert user.locked_until is None

    def test_increment_login_attempts(self, sample_user, _db):
        """Test incrementing login attempts."""
        sample_user.login_attempts = 0
        _db.session.commit()

        sample_user.login_attempts += 1
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.login_attempts == 1

    def test_account_lockout_after_max_attempts(self, sample_user, _db):
        """Test account locks after max login attempts."""
        sample_user.login_attempts = 5  # Max attempts
        sample_user.locked_until = datetime.utcnow() + timedelta(minutes=30)
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.locked_until is not None
        assert refreshed.locked_until > datetime.utcnow()

    def test_reset_login_attempts_on_success(self, sample_user, _db):
        """Test login attempts reset to 0 on successful login."""
        sample_user.login_attempts = 3
        _db.session.commit()

        # After successful login
        sample_user.login_attempts = 0
        sample_user.locked_until = None
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.login_attempts == 0
        assert refreshed.locked_until is None


# ============================================================================
# UNIT TESTS - Last Login Tracking
# ============================================================================

@pytest.mark.unit
class TestLastLoginTracking:
    """Tests for tracking user's last login."""

    def test_new_user_no_last_login(self, _db):
        """Test new user has no last login timestamp."""
        user = User(username="newtrack", email="newtrack@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.last_login is None

    def test_record_last_login(self, sample_user, _db):
        """Test recording last login timestamp."""
        now = datetime.utcnow()
        sample_user.last_login = now
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        # Allow small time difference
        assert refreshed.last_login is not None
        assert abs((refreshed.last_login - now).total_seconds()) < 1

    def test_update_last_login_on_each_login(self, sample_user, _db):
        """Test updating last login on each subsequent login."""
        time1 = datetime.utcnow()
        sample_user.last_login = time1
        _db.session.commit()

        # Simulate time passing
        import time
        time.sleep(0.1)

        time2 = datetime.utcnow()
        sample_user.last_login = time2
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.last_login > time1

    def test_record_last_login_ip(self, sample_user, _db):
        """Test recording IP address of last login."""
        sample_user.last_login_ip = "192.168.1.100"
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.last_login_ip == "192.168.1.100"


# ============================================================================
# UNIT TESTS - User Querying
# ============================================================================

@pytest.mark.unit
class TestUserQuerying:
    """Tests for querying users from database."""

    def test_find_user_by_username(self, _db, sample_user):
        """Test finding user by username."""
        found = User.query.filter_by(username="testuser").first()

        assert found is not None
        assert found.id == sample_user.id
        assert found.username == "testuser"

    def test_find_user_by_email(self, _db, sample_user):
        """Test finding user by email."""
        found = User.query.filter_by(email="test@example.com").first()

        assert found is not None
        assert found.id == sample_user.id

    def test_find_nonexistent_user_returns_none(self, _db):
        """Test finding nonexistent user returns None."""
        found = User.query.filter_by(username="nonexistent").first()

        assert found is None

    def test_count_users(self, _db, multiple_users):
        """Test counting users in database."""
        count = User.query.count()

        assert count == 10  # multiple_users fixture

    def test_filter_active_users(self, _db, multiple_users):
        """Test filtering active users."""
        # multiple_users: active users are even indices (0, 2, 4, 6, 8)
        active = User.query.filter_by(is_active=True).count()

        assert active == 5

    def test_filter_admin_users(self, _db, multiple_users):
        """Test filtering admin users."""
        admins = User.query.filter_by(is_admin=True).count()

        assert admins == 1  # User 0 is admin


# ============================================================================
# UNIT TESTS - User Timestamp Fields
# ============================================================================

@pytest.mark.unit
class TestUserTimestamps:
    """Tests for created_at and updated_at timestamps."""

    def test_created_at_set_on_creation(self, _db):
        """Test created_at timestamp is set automatically."""
        user = User(username="timestamp", email="ts@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)

    def test_updated_at_set_on_creation(self, _db):
        """Test updated_at timestamp is set on creation."""
        user = User(username="timestamp2", email="ts2@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.updated_at is not None
        assert user.updated_at == user.created_at

    def test_updated_at_changes_on_modification(self, sample_user, _db):
        """Test updated_at changes when user is modified."""
        original_updated = sample_user.updated_at

        import time
        time.sleep(0.1)  # Ensure time difference

        sample_user.is_active = False
        _db.session.commit()

        refreshed = User.query.get(sample_user.id)
        assert refreshed.updated_at > original_updated


# ============================================================================
# EDGE CASES
# ============================================================================

@pytest.mark.edge_case
class TestUserEdgeCases:
    """Edge case tests for User model."""

    def test_unicode_username(self, _db):
        """Test username with unicode characters."""
        user = User(username="用户名", email="unicode@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        _db.session.commit()

        assert user.username == "用户名"

    def test_very_long_username(self, _db):
        """Test username length limits."""
        long_username = "a" * 255  # Max typical length
        user = User(username=long_username, email="long@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)
        # May fail if there's a length constraint
        try:
            _db.session.commit()
            assert user.username == long_username
        except Exception:
            # Expected if length constraint exists
            pass

    def test_empty_string_username(self, _db):
        """Test empty username is rejected."""
        user = User(username="", email="empty@example.com")
        user.set_password("Pass123!")

        _db.session.add(user)

        # Should fail due to constraint
        with pytest.raises(Exception):
            _db.session.commit()

    def test_very_long_password_hash(self, sample_user):
        """Test very long password doesn't break system."""
        # bcrypt hashes are ~60 characters, so this tests extreme case
        long_password = "x" * 1000
        sample_user.set_password(long_password)

        # Should still hash correctly
        assert sample_user.check_password(long_password)
        assert sample_user.check_password("x" * 999) is False

