"""
Purpose: Tests for admin settings routes
Description: Test suite for GET/POST /admin/settings and /admin/settings/test-smtp

File: backend/tests/test_admin_settings.py | Repository: X-Filamenta-Python
Created: 2025-12-29T16:45:00+00:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for admin settings management
- Requires admin authentication
"""

import pytest
import json
from backend.src.models.user import User
from backend.src.models.settings import Settings
from backend.src.extensions import db


class TestAdminSettings:
    """Test admin settings routes"""

    def test_settings_page_requires_admin(self, client, test_user):
        """Test settings page requires admin privileges"""
        # Login as regular user
        client.post(
            "/auth/login",
            json={"username": test_user.username, "password": "testpassword123"},
        )

        response = client.get("/admin/settings")
        assert response.status_code == 403

    def test_settings_page_loads_admin(self, client, admin_user):
        """Test settings page loads for admin user"""
        response = client.get("/admin/settings")
        assert response.status_code == 200
        assert b"settings" in response.data.lower()

    def test_settings_page_not_authenticated(self, client):
        """Test settings page requires authentication"""
        response = client.get("/admin/settings")
        assert response.status_code == 302  # Redirect to login

    def test_get_all_settings(self, app):
        """Test getting all settings from database"""
        with app.app_context():
            Settings.init_defaults()
            all_settings = Settings.get_all()

            assert isinstance(all_settings, dict)
            assert "smtp_host" in all_settings
            assert "site_name" in all_settings

    def test_save_settings_smtp(self, client, admin_user):
        """Test saving SMTP settings"""
        response = client.post(
            "/admin/settings",
            data={
                "smtp_host": "smtp.test.com",
                "smtp_port": "587",
                "smtp_user": "testuser",
                "smtp_password": "testpass",
                "smtp_tls_enabled": "on",
                "smtp_from_email": "test@example.com",
                "smtp_from_name": "Test",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302

        # Verify settings saved
        assert Settings.get("smtp_host") == "smtp.test.com"
        assert Settings.get("smtp_port") == "587"

    def test_save_settings_email_verification(self, client, admin_user):
        """Test saving email verification settings"""
        response = client.post(
            "/admin/settings",
            data={
                "email_verification_required": "on",
                "email_verification_token_expiry_hours": "48",
                "password_reset_token_expiry_minutes": "120",
                "password_reset_rate_limit_per_hour": "3",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302

        assert Settings.get("email_verification_required") is True
        assert Settings.get("email_verification_token_expiry_hours") == "48"

    def test_save_settings_feature_flags(self, client, admin_user):
        """Test saving feature flags"""
        response = client.post(
            "/admin/settings",
            data={
                "registration_enabled": "on",
                "2fa_required": "on",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302

        assert Settings.get("registration_enabled") is True
        assert Settings.get("2fa_required") is True

    def test_test_smtp_endpoint_requires_admin(self, client, test_user):
        """Test SMTP test endpoint requires admin"""
        # Login as regular user
        client.post(
            "/auth/login",
            json={"username": test_user.username, "password": "testpassword123"},
        )

        response = client.post("/admin/settings/test-smtp")
        assert response.status_code == 403

    def test_test_smtp_endpoint_admin(self, client, admin_user):
        """Test SMTP test endpoint for admin user"""
        response = client.post(
            "/admin/settings/test-smtp",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "success" in data
        assert "message" in data

    def test_test_smtp_invalid_config(self, client, admin_user, app):
        """Test SMTP test with invalid configuration"""
        with app.app_context():
            # Set invalid SMTP host
            Settings.set("smtp_host", "invalid.host.that.does.not.exist")
            Settings.set("smtp_port", "9999")

        response = client.post(
            "/admin/settings/test-smtp",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is False

    def test_settings_encryption(self, app):
        """Test that sensitive settings are encrypted"""
        with app.app_context():
            Settings.set("smtp_password", "mysecretpassword")

            # Get from database
            setting = Settings.query.filter_by(key="smtp_password").first()

            # Value should be encrypted (not plain text)
            assert setting.encrypted is True
            assert setting.value != "mysecretpassword"

            # But get_value() should decrypt
            assert Settings.get("smtp_password") == "mysecretpassword"

    def test_settings_get_method(self, app):
        """Test Settings.get() method"""
        with app.app_context():
            Settings.set("test_key", "test_value")

            # Get existing key
            value = Settings.get("test_key")
            assert value == "test_value"

            # Get non-existing with default
            value = Settings.get("nonexistent", "default_value")
            assert value == "default_value"

    def test_settings_init_defaults(self, app):
        """Test initializing default settings"""
        with app.app_context():
            # Clear all settings first
            Settings.query.delete()
            db.session.commit()

            # Initialize defaults
            Settings.init_defaults()

            # Verify defaults exist
            smtp_host = Settings.get("smtp_host")
            assert smtp_host == "smtp.mailtrap.io"

            site_name = Settings.get("site_name")
            assert site_name == "X-Filamenta"


@pytest.fixture
def test_user(app):
    """Create test user"""
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            is_active=True,
            is_admin=False,
        )
        user.set_password("testpassword123")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()


@pytest.fixture
def admin_user(app):
    """Create admin user"""
    with app.app_context():
        user = User(
            username="adminuser",
            email="admin@example.com",
            is_active=True,
            is_admin=True,
        )
        user.set_password("adminpass123")
        db.session.add(user)
        db.session.commit()

        # Login to get session
        from flask import session

        yield user

        db.session.delete(user)
        db.session.commit()

