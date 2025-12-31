"""
------------------------------------------------------------------------------
Purpose: Tests for TOTP Service
Description: Unit tests for 2FA TOTP service (generation, validation, QR codes, backup codes)

File: backend/tests/test_totp.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:50:00+00:00
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
- Tests TOTP service functionality
- QR code generation validation
- Backup codes security
------------------------------------------------------------------------------
"""

import json
import re

import pyotp


def test_generate_secret():  # type: ignore[no-untyped-def]
    """Test TOTP secret generation"""
    from backend.src.services.totp_service import TOTPService

    secret = TOTPService.generate_secret()

    # Should be base32 string
    assert isinstance(secret, str)
    assert len(secret) == 32  # pyotp default length
    # Base32 alphabet: A-Z, 2-7
    assert re.match(r"^[A-Z2-7]+$", secret)


def test_generate_provisioning_uri(app):  # type: ignore[no-untyped-def]
    """Test provisioning URI generation for QR code"""
    from backend.src.models.user import User
    from backend.src.services.totp_service import TOTPService

    with app.app_context():
        # Create test user
        user = User(username="testuser", email="test@example.com")
        secret = "JBSWY3DPEHPK3PXP"  # Test secret

        uri = TOTPService.generate_provisioning_uri(user, secret)

        # Should be otpauth:// URI
        assert uri.startswith("otpauth://totp/")
        assert "test@example.com" in uri
        assert secret in uri
        assert "X-Filamenta" in uri  # Default issuer


def test_generate_qr_code():  # type: ignore[no-untyped-def]
    """Test QR code image generation"""
    from backend.src.services.totp_service import TOTPService

    uri = "otpauth://totp/X-Filamenta:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=X-Filamenta"
    qr_code = TOTPService.generate_qr_code(uri)

    # Should be base64 data URI
    assert qr_code.startswith("data:image/png;base64,")
    # Should have base64 encoded data
    assert len(qr_code) > 100  # QR code should be substantial


def test_verify_code_valid():  # type: ignore[no-untyped-def]
    """Test TOTP code verification with valid code"""
    from backend.src.services.totp_service import TOTPService

    secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(secret)
    current_code = totp.now()

    # Valid code should pass
    assert TOTPService.verify_code(secret, current_code) is True


def test_verify_code_invalid():  # type: ignore[no-untyped-def]
    """Test TOTP code verification with invalid code"""
    from backend.src.services.totp_service import TOTPService

    secret = "JBSWY3DPEHPK3PXP"

    # Invalid codes should fail
    assert TOTPService.verify_code(secret, "000000") is False
    assert TOTPService.verify_code(secret, "123456") is False
    assert TOTPService.verify_code(secret, "999999") is False


def test_verify_code_empty():  # type: ignore[no-untyped-def]
    """Test TOTP code verification with empty inputs"""
    from backend.src.services.totp_service import TOTPService

    secret = "JBSWY3DPEHPK3PXP"

    # Empty inputs should fail
    assert TOTPService.verify_code("", "123456") is False
    assert TOTPService.verify_code(secret, "") is False
    assert TOTPService.verify_code("", "") is False


def test_verify_code_window():  # type: ignore[no-untyped-def]
    """Test TOTP code verification accepts codes within window"""
    from backend.src.services.totp_service import TOTPService

    secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(secret)

    # Current code should work
    current_code = totp.now()
    assert TOTPService.verify_code(secret, current_code) is True

    # Code from 30s ago should work (window=1)
    import time

    past_code = totp.at(time.time() - 30)
    assert TOTPService.verify_code(secret, past_code) is True

    # Code from 30s future should work (window=1)
    future_code = totp.at(time.time() + 30)
    assert TOTPService.verify_code(secret, future_code) is True


def test_generate_backup_codes():  # type: ignore[no-untyped-def]
    """Test backup codes generation"""
    from backend.src.services.totp_service import TOTPService

    codes, hashed_json = TOTPService.generate_backup_codes(count=10)

    # Should return 10 plain codes
    assert len(codes) == 10
    assert all(isinstance(code, str) for code in codes)
    assert all(len(code) == 8 for code in codes)  # 8 chars hex

    # Should return JSON with 10 hashed codes
    hashed_codes = json.loads(hashed_json)
    assert len(hashed_codes) == 10
    assert all(isinstance(h, str) for h in hashed_codes)
    # Hashed codes should be different from plain
    assert codes[0] not in hashed_json


def test_generate_backup_codes_custom_count():  # type: ignore[no-untyped-def]
    """Test backup codes generation with custom count"""
    from backend.src.services.totp_service import TOTPService

    codes, hashed_json = TOTPService.generate_backup_codes(count=5)

    assert len(codes) == 5
    hashed_codes = json.loads(hashed_json)
    assert len(hashed_codes) == 5


def test_verify_backup_code_valid(app):  # type: ignore[no-untyped-def]
    """Test backup code verification with valid code"""
    from backend.src.extensions import db
    from backend.src.models.user import User
    from backend.src.services.totp_service import TOTPService

    with app.app_context():
        db.create_all()

        # Create user with backup codes
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )

        codes, hashed_json = TOTPService.generate_backup_codes(count=3)
        user.backup_codes = hashed_json
        db.session.add(user)
        db.session.commit()

        # Valid code should work once
        assert TOTPService.verify_backup_code(user, codes[0]) is True

        # Same code should not work again (consumed)
        assert TOTPService.verify_backup_code(user, codes[0]) is False

        # Other codes should still work
        assert TOTPService.verify_backup_code(user, codes[1]) is True

        db.session.delete(user)
        db.session.commit()


def test_verify_backup_code_invalid(app):  # type: ignore[no-untyped-def]
    """Test backup code verification with invalid code"""
    from backend.src.extensions import db
    from backend.src.models.user import User
    from backend.src.services.totp_service import TOTPService

    with app.app_context():
        db.create_all()

        user = User(
            username="testuser2",
            email="test2@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )

        _, hashed_json = TOTPService.generate_backup_codes(count=3)
        user.backup_codes = hashed_json
        db.session.add(user)
        db.session.commit()

        # Invalid code should fail
        assert TOTPService.verify_backup_code(user, "INVALID1") is False
        assert TOTPService.verify_backup_code(user, "12345678") is False

        db.session.delete(user)
        db.session.commit()


def test_verify_backup_code_no_codes(app):  # type: ignore[no-untyped-def]
    """Test backup code verification when user has no codes"""
    from backend.src.extensions import db
    from backend.src.models.user import User
    from backend.src.services.totp_service import TOTPService

    with app.app_context():
        db.create_all()

        user = User(
            username="testuser3",
            email="test3@example.com",
            password_hash="hash",
            is_admin=False,
            is_active=True,
        )
        user.backup_codes = None
        db.session.add(user)
        db.session.commit()

        # Should fail gracefully
        assert TOTPService.verify_backup_code(user, "ANYCODE1") is False

        db.session.delete(user)
        db.session.commit()
