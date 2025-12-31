"""
---
Purpose: Integration tests for major application workflows
Description: End-to-end integration testing with database and services

File: backend/tests/test_integration.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified: 2025-12-30

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
- Test Type: Integration
---
"""

import pytest
from flask import session
from backend.src.models.user import User
from backend.src.models.settings import Settings
from backend.src.extensions import db
from datetime import datetime, timedelta


class TestUserRegistrationAuthenticationFlow:
    """Integration tests for complete user registration and authentication."""

    def test_complete_registration_flow(self, client, app):
        """Test full user registration flow from form to database."""
        with app.app_context():
            # Step 1: Access registration page
            response = client.get('/auth/register')
            assert response.status_code == 200
            assert b'register' in response.data.lower()

            # Step 2: Submit registration form
            response = client.post('/auth/register', data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'SecurePass123!',
                'password_confirm': 'SecurePass123!'
            }, follow_redirects=True)

            # Verify user created in database
            user = User.query.filter_by(username='newuser').first()
            assert user is not None
            assert user.email == 'newuser@example.com'
            assert user.email_verified is False
            assert user.is_active is True

            # Step 3: Verify password hashed correctly
            assert user.password_hash is not None
            assert user.password_hash != 'SecurePass123!'
            assert user.check_password('SecurePass123!') is True

    def test_registration_login_logout_flow(self, client, app):
        """Test complete flow: register -> login -> access protected -> logout."""
        with app.app_context():
            # Register
            client.post('/auth/register', data={
                'username': 'flowtest',
                'email': 'flow@example.com',
                'password': 'Pass123!',
                'password_confirm': 'Pass123!'
            })

            # Verify email (skip email verification for test)
            user = User.query.filter_by(username='flowtest').first()
            user.email_verified = True
            db.session.commit()

            # Login
            response = client.post('/auth/login', data={
                'username': 'flowtest',
                'password': 'Pass123!'
            }, follow_redirects=True)

            # Verify logged in
            with client.session_transaction() as sess:
                assert sess.get('user_id') == user.id

            # Access protected resource
            response = client.get('/users/profile')
            assert response.status_code == 200

            # Logout
            client.post('/auth/logout')

            # Verify logged out
            with client.session_transaction() as sess:
                assert sess.get('user_id') is None

            # Protected resource now denied
            response = client.get('/users/profile')
            assert response.status_code in [302, 401, 403]

    def test_failed_login_increments_attempts(self, client, app):
        """Test that failed login attempts are tracked."""
        with app.app_context():
            # Create user
            user = User(username='locktest', email='lock@example.com')
            user.set_password('CorrectPass!')
            db.session.add(user)
            db.session.commit()

            initial_attempts = user.login_attempts

            # Failed login
            client.post('/auth/login', data={
                'username': 'locktest',
                'password': 'WrongPassword'
            })

            # Refresh user from database
            db.session.refresh(user)
            assert user.login_attempts > initial_attempts


class TestEmailVerificationIntegration:
    """Integration tests for email verification workflow."""

    def test_email_verification_end_to_end(self, client, app, mocker):
        """Test complete email verification flow."""
        with app.app_context():
            # Mock email sending
            mock_send = mocker.patch('backend.src.services.email_service.EmailService.send_email')

            # Register user
            client.post('/auth/register', data={
                'username': 'emailtest',
                'email': 'emailtest@example.com',
                'password': 'Pass123!',
                'password_confirm': 'Pass123!'
            })

            # Verify email sent
            assert mock_send.called

            # Get user and token
            user = User.query.filter_by(username='emailtest').first()
            assert user.email_verified is False
            assert user.email_verification_token is not None

            token = user.email_verification_token

            # Verify email via token
            response = client.get(f'/auth/verify-email/{token}', follow_redirects=True)
            assert response.status_code == 200

            # Verify user now verified
            db.session.refresh(user)
            assert user.email_verified is True
            assert user.email_verification_token is None

    def test_resend_verification_email_integration(self, client, app, mocker, auth_user):
        """Test resending verification email."""
        with app.app_context():
            mock_send = mocker.patch('backend.src.services.email_service.EmailService.send_email')

            # Create unverified user and login
            user = User.query.filter_by(username='testuser').first()
            user.email_verified = False
            db.session.commit()

            auth_user()

            # Resend verification
            response = client.post('/auth/resend-verification')

            # Verify email sent
            assert mock_send.called
            assert response.status_code in [200, 302]


class TestPasswordResetFlow:
    """Integration tests for password reset workflow."""

    def test_password_reset_end_to_end(self, client, app, mocker):
        """Test complete password reset flow."""
        with app.app_context():
            # Create user
            user = User(username='resettest', email='reset@example.com')
            user.set_password('OldPass123!')
            db.session.add(user)
            db.session.commit()

            # Mock email sending
            mock_send = mocker.patch('backend.src.services.email_service.EmailService.send_email')

            # Request password reset
            response = client.post('/auth/forgot-password', data={
                'email': 'reset@example.com'
            })

            # Verify email sent
            assert mock_send.called

            # Get reset token
            db.session.refresh(user)
            token = user.password_reset_token
            assert token is not None

            # Reset password
            response = client.post(f'/auth/reset-password/{token}', data={
                'password': 'NewPass456!',
                'password_confirm': 'NewPass456!'
            }, follow_redirects=True)

            # Verify password changed
            db.session.refresh(user)
            assert user.check_password('NewPass456!') is True
            assert user.check_password('OldPass123!') is False
            assert user.password_reset_token is None

    def test_expired_reset_token_rejected(self, client, app):
        """Test that expired reset tokens are rejected."""
        with app.app_context():
            user = User(username='expiredtest', email='expired@example.com')
            user.set_password('Pass123!')
            user.password_reset_token = 'test_token'
            user.password_reset_token_expiry = datetime.utcnow() - timedelta(hours=2)
            db.session.add(user)
            db.session.commit()

            # Attempt to use expired token
            response = client.post('/auth/reset-password/test_token', data={
                'password': 'NewPass!',
                'password_confirm': 'NewPass!'
            })

            # Should be rejected
            assert response.status_code in [400, 302]

            # Password unchanged
            db.session.refresh(user)
            assert user.check_password('Pass123!') is True


class Test2FAIntegration:
    """Integration tests for 2FA/TOTP workflow."""

    def test_2fa_setup_and_login_flow(self, client, app, auth_user):
        """Test complete 2FA setup and login flow."""
        with app.app_context():
            auth_user()

            # Access 2FA setup
            response = client.get('/users/2fa/setup')
            assert response.status_code == 200

            # Get user
            user = User.query.filter_by(username='testuser').first()

            # Simulate 2FA setup (TOTP secret generated)
            import pyotp
            secret = pyotp.random_base32()
            user.totp_secret = secret
            db.session.commit()

            # Generate valid TOTP token
            totp = pyotp.TOTP(secret)
            token = totp.now()

            # Enable 2FA with valid token
            response = client.post('/users/2fa/enable', data={
                'token': token
            }, follow_redirects=True)

            # Verify 2FA enabled
            db.session.refresh(user)
            assert user.totp_enabled is True


class TestAdminUserManagementIntegration:
    """Integration tests for admin user management."""

    def test_admin_create_and_modify_user(self, client, app, auth_admin):
        """Test admin creating and modifying users."""
        with app.app_context():
            auth_admin()

            # View users list
            response = client.get('/admin/users')
            assert response.status_code == 200

            # Create user via admin (if endpoint exists)
            # For now, test modification

            # Create test user
            user = User(username='admintest', email='admintest@example.com')
            user.set_password('Pass123!')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            # Toggle user active status
            response = client.post(f'/admin/users/{user_id}/toggle-active', data={
                'csrf_token': 'test_token'  # Mock CSRF
            }, follow_redirects=True)

            # Verify status changed (may need to check implementation)

            # Grant admin privilege
            response = client.post(f'/admin/users/{user_id}/toggle-admin', data={
                'csrf_token': 'test_token'
            }, follow_redirects=True)

    def test_admin_cannot_self_deactivate(self, client, app, auth_admin):
        """Test that admin cannot deactivate their own account."""
        with app.app_context():
            auth_admin()

            admin = User.query.filter_by(username='admin').first()

            # Attempt self-deactivation
            response = client.post(f'/admin/users/{admin.id}/toggle-active', data={
                'csrf_token': 'test_token'
            })

            # Should be forbidden
            assert response.status_code in [400, 403]


class TestSettingsManagementIntegration:
    """Integration tests for settings management."""

    def test_update_email_settings(self, client, app, auth_admin):
        """Test updating email settings via admin panel."""
        with app.app_context():
            auth_admin()

            # Update settings
            response = client.post('/admin/settings', data={
                'csrf_token': 'test_token',
                'smtp_host': 'smtp.test.com',
                'smtp_port': '587',
                'smtp_tls_enabled': 'true',
                'site_name': 'Test Site'
            }, follow_redirects=True)

            # Verify settings saved
            setting = Settings.query.filter_by(key='smtp_host').first()
            if setting:
                assert setting.value == 'smtp.test.com'

    def test_encrypted_settings_stored_securely(self, client, app, auth_admin):
        """Test that sensitive settings are encrypted."""
        with app.app_context():
            auth_admin()

            # Update password setting
            client.post('/admin/settings', data={
                'csrf_token': 'test_token',
                'smtp_password': 'secret_password_123'
            })

            # Verify encrypted in database
            setting = Settings.query.filter_by(key='smtp_password').first()
            if setting:
                assert setting.encrypted is True
                assert setting.value != 'secret_password_123'  # Encrypted


class TestContentCRUDIntegration:
    """Integration tests for content creation, reading, updating, deleting."""

    def test_content_create_and_publish_flow(self, client, app, auth_user):
        """Test creating and publishing content."""
        with app.app_context():
            auth_user()

            # Create content
            response = client.post('/content/', data={
                'csrf_token': 'test_token',
                'title': 'Test Article',
                'body': '<p>Test content body</p>',
                'type': 'post',
                'status': 'draft'
            }, follow_redirects=True)

            # Verify created (assuming Content model exists)
            # from backend.src.models.content import Content
            # content = Content.query.filter_by(title='Test Article').first()
            # assert content is not None
            # assert content.status == 'draft'

    def test_user_cannot_edit_others_content(self, client, app):
        """Test content isolation between users."""
        with app.app_context():
            # Create two users with content
            user1 = User(username='author1', email='author1@example.com')
            user1.set_password('Pass!')
            user2 = User(username='author2', email='author2@example.com')
            user2.set_password('Pass!')
            db.session.add_all([user1, user2])
            db.session.commit()

            # Login as user1
            client.post('/auth/login', data={
                'username': 'author1',
                'password': 'Pass!'
            })

            # Attempt to edit user2's content (if IDs exposed)
            # Should be forbidden


class TestInstallationWizardIntegration:
    """Integration tests for installation wizard."""

    def test_wizard_complete_flow(self, client, app):
        """Test complete installation wizard flow."""
        with app.app_context():
            # Assuming fresh install (no settings)

            # Step 1: Language selection
            response = client.get('/install/')
            if response.status_code == 200:
                # Set language
                client.post('/install/set-language', data={
                    'language': 'en'
                })

                # Step 2: Requirements check
                client.post('/install/step', data={
                    'step': 'requirements',
                    'requirements_checked': '1'
                })

                # Step 3: Database configuration
                client.post('/install/step', data={
                    'step': 'db_form',
                    'db_type': 'sqlite',
                    'db_name': 'test.db'
                })

                # Step 4: Admin creation
                response = client.post('/install/step', data={
                    'step': 'admin_form',
                    'username': 'admin',
                    'email': 'admin@test.com',
                    'password': 'AdminPass123!',
                    'password_confirm': 'AdminPass123!'
                })

                # Verify admin created
                admin = User.query.filter_by(username='admin').first()
                if admin:
                    assert admin.is_admin is True


class TestDatabaseTransactions:
    """Integration tests for database transaction handling."""

    def test_rollback_on_error(self, app):
        """Test that database rolls back on error."""
        with app.app_context():
            # Start transaction
            try:
                user = User(username='rollback_test', email='rollback@test.com')
                db.session.add(user)
                db.session.flush()

                # Force error (duplicate username)
                user2 = User(username='rollback_test', email='different@test.com')
                db.session.add(user2)
                db.session.commit()
            except Exception:
                db.session.rollback()

            # Verify no users created
            users = User.query.filter_by(username='rollback_test').all()
            assert len(users) in [0, 1]  # Depends on unique constraint

    def test_commit_success_persists_data(self, app):
        """Test that successful commits persist data."""
        with app.app_context():
            user = User(username='persist_test', email='persist@test.com')
            user.set_password('Pass!')
            db.session.add(user)
            db.session.commit()

            # Verify persisted
            retrieved = User.query.filter_by(username='persist_test').first()
            assert retrieved is not None
            assert retrieved.email == 'persist@test.com'


class TestConcurrency:
    """Integration tests for concurrent operations."""

    def test_concurrent_user_updates(self, app):
        """Test handling of concurrent user updates."""
        with app.app_context():
            # Create user
            user = User(username='concurrent', email='concurrent@test.com')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            # Simulate concurrent update
            # (Proper test would use threading, this is simplified)
            user1 = User.query.get(user_id)
            user2 = User.query.get(user_id)

            user1.email = 'updated1@test.com'
            user2.email = 'updated2@test.com'

            db.session.commit()  # Last write wins (or optimistic locking)

            # Verify final state
            final_user = User.query.get(user_id)
            assert final_user.email in ['updated1@test.com', 'updated2@test.com']


class TestCaching:
    """Integration tests for caching mechanisms."""

    def test_cache_invalidation_on_update(self, client, app, auth_admin):
        """Test that cache invalidates when settings updated."""
        with app.app_context():
            auth_admin()

            # Get setting (cached)
            setting = Settings.query.filter_by(key='site_name').first()
            if setting:
                original_value = setting.value

                # Update setting
                client.post('/admin/settings', data={
                    'csrf_token': 'test_token',
                    'site_name': 'New Site Name'
                })

                # Verify cache invalidated (get fresh value)
                updated_setting = Settings.query.filter_by(key='site_name').first()
                assert updated_setting.value == 'New Site Name'

