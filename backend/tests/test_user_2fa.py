"""
------------------------------------------------------------------------------
Purpose: Tests for User Model 2FA functionality
Description: Unit tests for User model 2FA methods and security features

File: backend/tests/test_user_2fa.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:55:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Tests User model 2FA methods
- Account locking functionality
- Role management
------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta

import pyotp


def test_user_enable_2fa(app):  # type: ignore[no-untyped-def]
    """Test enabling 2FA for user"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="test2fa",
            email="2fa@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        secret = "JBSWY3DPEHPK3PXP"

        # Enable 2FA
        user.enable_2fa(secret)

        assert user.totp_secret == secret
        assert user.totp_enabled is True

        db.session.delete(user)
        db.session.commit()


def test_user_disable_2fa(app):  # type: ignore[no-untyped-def]
    """Test disabling 2FA for user"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testdisable",
            email="disable@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        user.totp_secret = "SECRET123"
        user.totp_enabled = True
        user.backup_codes = '["code1", "code2"]'

        db.session.add(user)
        db.session.commit()

        # Disable 2FA
        user.disable_2fa()

        assert user.totp_secret is None
        assert user.totp_enabled is False
        assert user.backup_codes is None

        db.session.delete(user)
        db.session.commit()


def test_user_can_setup_2fa(app):  # type: ignore[no-untyped-def]
    """Test can_setup_2fa method"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        # User without 2FA can setup
        user1 = User(
            username="cansetup",
            email="cansetup@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        db.session.add(user1)
        db.session.commit()

        assert user1.can_setup_2fa() is True

        # User with 2FA enabled cannot setup again
        user1.enable_2fa("SECRET")
        assert user1.can_setup_2fa() is False

        db.session.delete(user1)
        db.session.commit()


def test_user_verify_totp(app):  # type: ignore[no-untyped-def]
    """Test TOTP code verification via User model"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testverify",
            email="verify@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )

        secret = "JBSWY3DPEHPK3PXP"
        user.enable_2fa(secret)
        db.session.add(user)
        db.session.commit()

        # Generate valid code
        totp = pyotp.TOTP(secret)
        valid_code = totp.now()

        # Valid code should work
        assert user.verify_totp(valid_code) is True

        # Invalid code should fail
        assert user.verify_totp("000000") is False

        db.session.delete(user)
        db.session.commit()


def test_user_verify_totp_disabled(app):  # type: ignore[no-untyped-def]
    """Test TOTP verification when 2FA is disabled"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testdisabled",
            email="disabled@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        # Should fail if 2FA not enabled
        assert user.verify_totp("123456") is False

        db.session.delete(user)
        db.session.commit()


def test_user_is_locked(app):  # type: ignore[no-untyped-def]
    """Test account locking detection"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testlocked",
            email="locked@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        # Not locked initially
        assert user.is_locked() is False

        # Lock account (future time)
        user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        assert user.is_locked() is True

        # Expired lock (past time)
        user.locked_until = datetime.utcnow() - timedelta(minutes=1)
        assert user.is_locked() is False

        db.session.delete(user)
        db.session.commit()


def test_user_increment_login_attempts(app):  # type: ignore[no-untyped-def]
    """Test login attempt increment and auto-lock"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testattempts",
            email="attempts@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        # Start with 0 attempts
        assert user.login_attempts == 0
        assert user.is_locked() is False

        # Increment attempts
        user.increment_login_attempts()
        assert user.login_attempts == 1
        assert user.is_locked() is False

        # Continue incrementing
        for _ in range(4):
            user.increment_login_attempts()

        # Should be locked after 5 attempts
        assert user.login_attempts == 5
        assert user.is_locked() is True
        assert user.locked_until is not None

        db.session.delete(user)
        db.session.commit()


def test_user_reset_login_attempts(app):  # type: ignore[no-untyped-def]
    """Test resetting login attempts"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testreset",
            email="reset@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        user.login_attempts = 5
        user.locked_until = datetime.utcnow() + timedelta(minutes=15)

        db.session.add(user)
        db.session.commit()

        # Reset
        user.reset_login_attempts()

        assert user.login_attempts == 0
        assert user.locked_until is None
        assert user.is_locked() is False

        db.session.delete(user)
        db.session.commit()


def test_user_update_last_login(app):  # type: ignore[no-untyped-def]
    """Test updating last login timestamp and IP"""
    from backend.src.extensions import db
    from backend.src.models.user import User

    with app.app_context():
        db.create_all()

        user = User(
            username="testlogin",
            email="login@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        user.login_attempts = 3
        user.locked_until = datetime.utcnow() + timedelta(minutes=5)

        db.session.add(user)
        db.session.commit()

        # Update last login
        test_ip = "192.168.1.1"
        user.update_last_login(test_ip)

        assert user.last_login is not None
        assert user.last_login_ip == test_ip
        # Should reset attempts
        assert user.login_attempts == 0
        assert user.locked_until is None

        db.session.delete(user)
        db.session.commit()


def test_user_get_role(app):  # type: ignore[no-untyped-def]
    """Test getting user role as enum"""
    from backend.src.extensions import db
    from backend.src.models.user import User, UserRole

    with app.app_context():
        db.create_all()

        # Member role
        user1 = User(
            username="member",
            email="member@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
            role="member",
        )
        db.session.add(user1)
        db.session.commit()

        assert user1.get_role() == UserRole.MEMBER

        # Admin role
        user2 = User(
            username="admin2",
            email="admin2@example.com",
            password_hash="hash",
            is_admin=True,
            is_active=True,
            role="admin",
        )
        db.session.add(user2)
        db.session.commit()

        assert user2.get_role() == UserRole.ADMIN

        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()


def test_user_has_role(app):  # type: ignore[no-untyped-def]
    """Test checking user role"""
    from backend.src.extensions import db
    from backend.src.models.user import User, UserRole

    with app.app_context():
        db.create_all()

        user = User(
            username="roletest",
            email="roletest@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
            role="member",
        )
        db.session.add(user)
        db.session.commit()

        assert user.has_role(UserRole.MEMBER) is True
        assert user.has_role(UserRole.ADMIN) is False

        # Change to admin
        user.role = UserRole.ADMIN.value
        assert user.has_role(UserRole.ADMIN) is True
        assert user.has_role(UserRole.MEMBER) is False

        db.session.delete(user)
        db.session.commit()
