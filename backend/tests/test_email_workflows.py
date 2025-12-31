"""
Purpose: Tests for email verification and password reset workflows
Description: Complete test suite for Phase 1 email verification and password reset

File: backend/tests/test_email_workflows.py | Repository: X-Filamenta-Python
Created: 2025-12-29T16:00:00+00:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for email verification and password reset workflows
- Coverage: routes, models, email service
"""

import pytest
from datetime import datetime, timedelta
from backend.src.models.user import User
from backend.src.models.settings import Settings
from backend.src.extensions import db


class TestEmailVerificationWorkflow:
    """Test email verification workflow"""

    def test_send_verification_authenticated(self, client, auth_user):
        """Test sending verification email when authenticated"""
        response = client.post("/auth/send-verification")
        assert response.status_code == 200
        assert b"email-sent" in response.data or b"Email" in response.data

    def test_send_verification_unauthenticated(self, client):
        """Test sending verification email without authentication"""
        response = client.post("/auth/send-verification")
        assert response.status_code == 401

    def test_generate_email_verification_token(self, test_user):
        """Test generating email verification token"""
        token = test_user.generate_email_verification_token()
        assert token is not None
        assert len(token) > 0
        assert test_user.email_verification_token == token
        assert test_user.email_verification_token_expiry is not None

    def test_verify_email_token_valid(self, test_user):
        """Test verifying email with valid token"""
        token = test_user.generate_email_verification_token()
        db.session.commit()

        assert test_user.verify_email_token(token) is True

    def test_verify_email_token_invalid(self, test_user):
        """Test verifying email with invalid token"""
        test_user.generate_email_verification_token()
        db.session.commit()

        assert test_user.verify_email_token("invalid_token") is False

    def test_verify_email_token_expired(self, test_user):
        """Test verifying email with expired token"""
        token = test_user.generate_email_verification_token()
        # Manually set expiry to past
        test_user.email_verification_token_expiry = datetime.utcnow() - timedelta(
            hours=1
        )
        db.session.commit()

        assert test_user.verify_email_token(token) is False

    def test_mark_email_verified(self, test_user):
        """Test marking email as verified"""
        token = test_user.generate_email_verification_token()
        db.session.commit()

        test_user.mark_email_verified()
        db.session.commit()

        assert test_user.email_verified is True
        assert test_user.email_verification_token is None
        assert test_user.email_verification_token_expiry is None

    def test_verify_email_route_valid(self, client, app, test_user):
        """Test verify email route with valid token"""
        token = test_user.generate_email_verification_token()
        db.session.commit()

        response = client.get(f"/auth/verify-email/{token}")
        assert response.status_code == 200

        # Check user email verified
        user = User.query.filter_by(id=test_user.id).first()
        assert user.email_verified is True

    def test_verify_email_route_invalid_token(self, client):
        """Test verify email route with invalid token"""
        response = client.get("/auth/verify-email/invalid_token")
        assert response.status_code == 302  # Redirect

    def test_verify_email_route_expired_token(self, client, test_user):
        """Test verify email route with expired token"""
        token = test_user.generate_email_verification_token()
        test_user.email_verification_token_expiry = datetime.utcnow() - timedelta(
            hours=1
        )
        db.session.commit()

        response = client.get(f"/auth/verify-email/{token}")
        assert response.status_code == 302  # Redirect


class TestPasswordResetWorkflow:
    """Test password reset workflow"""

    def test_generate_password_reset_token(self, test_user):
        """Test generating password reset token"""
        token = test_user.generate_password_reset_token()
        assert token is not None
        assert len(token) > 0
        assert test_user.password_reset_token == token
        assert test_user.password_reset_token_expiry is not None

    def test_verify_password_reset_token_valid(self, test_user):
        """Test verifying password reset token"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        assert test_user.verify_password_reset_token(token) is True

    def test_verify_password_reset_token_invalid(self, test_user):
        """Test verifying invalid password reset token"""
        test_user.generate_password_reset_token()
        db.session.commit()

        assert test_user.verify_password_reset_token("invalid_token") is False

    def test_verify_password_reset_token_expired(self, test_user):
        """Test verifying expired password reset token"""
        token = test_user.generate_password_reset_token()
        # Manually set expiry to past
        test_user.password_reset_token_expiry = datetime.utcnow() - timedelta(minutes=5)
        db.session.commit()

        assert test_user.verify_password_reset_token(token) is False

    def test_reset_password_with_token_valid(self, test_user):
        """Test resetting password with valid token"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        new_password = "NewSecurePassword123"
        result = test_user.reset_password_with_token(token, new_password)

        assert result is True
        assert test_user.check_password(new_password) is True
        assert test_user.password_reset_token is None
        assert test_user.password_reset_token_expiry is None

    def test_reset_password_with_token_invalid(self, test_user):
        """Test resetting password with invalid token"""
        result = test_user.reset_password_with_token("invalid_token", "NewPassword")
        assert result is False

    def test_forgot_password_page(self, client):
        """Test forgot password page loads"""
        response = client.get("/auth/forgot-password")
        assert response.status_code == 200
        assert b"forgot" in response.data.lower() or b"password" in response.data.lower()

    def test_forgot_password_submit_valid(self, client, test_user):
        """Test submitting forgot password form with valid email"""
        response = client.post(
            "/auth/forgot-password",
            data={"email": test_user.email},
            follow_redirects=False,
        )
        assert response.status_code == 200 or response.status_code == 302

    def test_forgot_password_submit_invalid(self, client):
        """Test submitting forgot password form with invalid email"""
        response = client.post(
            "/auth/forgot-password",
            data={"email": "nonexistent@example.com"},
            follow_redirects=False,
        )
        # Should still show success page for security
        assert response.status_code == 200 or response.status_code == 302

    def test_reset_password_page_valid(self, client, test_user):
        """Test reset password page with valid token"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        response = client.get(f"/auth/reset-password/{token}")
        assert response.status_code == 200

    def test_reset_password_page_invalid(self, client):
        """Test reset password page with invalid token"""
        response = client.get("/auth/reset-password/invalid_token")
        assert response.status_code == 302  # Redirect

    def test_reset_password_submit_valid(self, client, test_user):
        """Test submitting reset password form with valid token"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        response = client.post(
            f"/auth/reset-password/{token}",
            data={
                "password": "NewSecurePassword123",
                "password_confirm": "NewSecurePassword123",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302  # Redirect to login

    def test_reset_password_submit_mismatch(self, client, test_user):
        """Test submitting reset password with mismatched passwords"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        response = client.post(
            f"/auth/reset-password/{token}",
            data={
                "password": "NewSecurePassword123",
                "password_confirm": "DifferentPassword123",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200  # Form re-displayed

    def test_reset_password_submit_short(self, client, test_user):
        """Test submitting reset password with too short password"""
        token = test_user.generate_password_reset_token()
        db.session.commit()

        response = client.post(
            f"/auth/reset-password/{token}",
            data={
                "password": "Short1",
                "password_confirm": "Short1",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200  # Form re-displayed with error


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
def auth_user(client, test_user):
    """Authenticate test user"""
    client.post(
        "/auth/login",
        json={"username": test_user.username, "password": "testpassword123"},
    )
    return test_user

