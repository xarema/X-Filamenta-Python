"""
------------------------------------------------------------------------------
Purpose: User model
Description: SQLAlchemy model for User entity

File: backend/src/models/user.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal
------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, cast

from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin

from backend.src.extensions import db


class UserRole(str, Enum):
    """User role enumeration"""

    MEMBER = "member"
    ADMIN = "admin"


class User(UserMixin, db.Model):
    """
    User model

    Represents a user in the system with authentication and authorization.
    Inherits from UserMixin for Flask-Login integration.
    """

    __tablename__ = "users"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Authorization
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(20), default=UserRole.MEMBER.value, nullable=False)

    # 2FA / Security
    totp_secret = db.Column(db.String(32), nullable=True)  # Base32 encoded secret
    totp_enabled = db.Column(db.Boolean, default=False, nullable=False)
    backup_codes = db.Column(db.Text, nullable=True)  # JSON array of hashed codes

    # Security tracking
    last_login = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)  # IPv6 max length
    login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)

    # Email verification
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    email_verification_token_expiry = db.Column(db.DateTime, nullable=True)

    # Password reset
    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    preferences = db.relationship(
        "UserPreferences",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    content = db.relationship(
        "Content", back_populates="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation"""
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        """
        Hash and set password

        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if password matches

        Args:
            password: Plain text password to check

        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def is_locked(self) -> bool:
        """
        Check if account is currently locked

        Returns:
            True if locked, False otherwise
        """
        if not self.locked_until:
            return False
        return bool(datetime.utcnow() < self.locked_until)

    def increment_login_attempts(self) -> None:
        """Increment failed login attempts and lock if threshold reached"""
        self.login_attempts += 1

        # Lock account after 5 failed attempts for 15 minutes
        if self.login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)

    def reset_login_attempts(self) -> None:
        """Reset failed login attempts and unlock account"""
        self.login_attempts = 0
        self.locked_until = None

    def update_last_login(self, ip_address: str | None = None) -> None:
        """
        Update last login timestamp and IP

        Args:
            ip_address: IP address of login (optional)
        """
        self.last_login = datetime.utcnow()
        if ip_address:
            self.last_login_ip = ip_address
        self.reset_login_attempts()

    def get_role(self) -> UserRole:
        """
        Get user role as enum

        Returns:
            UserRole enum
        """
        try:
            return UserRole(self.role)
        except ValueError:
            return UserRole.MEMBER

    def has_role(self, role: UserRole) -> bool:
        """
        Check if user has specific role

        Args:
            role: Role to check

        Returns:
            True if user has role, False otherwise
        """
        return self.get_role() == role

    def can_setup_2fa(self) -> bool:
        """
        Check if user can setup 2FA

        Returns:
            True if user can setup 2FA (not already enabled)
        """
        return not self.totp_enabled

    def enable_2fa(self, secret: str) -> None:
        """
        Enable 2FA with given secret

        Args:
            secret: Base32 encoded TOTP secret
        """
        self.totp_secret = secret
        self.totp_enabled = True

    def disable_2fa(self) -> None:
        """Disable 2FA"""
        self.totp_secret = None
        self.totp_enabled = False
        self.backup_codes = None

    def verify_totp(self, code: str) -> bool:
        """
        Verify TOTP code

        Args:
            code: 6-digit TOTP code

        Returns:
            True if code is valid, False otherwise
        """
        if not self.totp_enabled or not self.totp_secret:
            return False

        try:
            import pyotp

            totp = pyotp.TOTP(self.totp_secret)
            return bool(totp.verify(code, valid_window=1))
        except ImportError:
            # PyOTP not installed
            return False

    def generate_email_verification_token(self) -> str:
        """Generate email verification token with expiry."""
        from backend.src.models.settings import Settings
        from backend.src.services.email_service import EmailToken

        token = EmailToken.generate()
        expiry_hours = Settings.get("email_verification_token_expiry_hours", 24)
        self.email_verification_token = token
        self.email_verification_token_expiry = datetime.utcnow() + timedelta(
            hours=int(expiry_hours)
        )
        return token

    def verify_email_token(self, token: str) -> bool:
        """
        Verify email verification token.

        Args:
            token: Token to verify

        Returns:
            True if token is valid and not expired
        """
        if not self.email_verification_token:
            return False

        if self.email_verification_token != token:
            return False

        if not self.email_verification_token_expiry:
            return False

        return datetime.utcnow() <= self.email_verification_token_expiry

    def mark_email_verified(self) -> None:
        """Mark email as verified and clear token."""
        self.email_verified = True
        self.email_verification_token = None
        self.email_verification_token_expiry = None

    def generate_password_reset_token(self) -> str:
        """Generate password reset token with expiry."""
        from backend.src.models.settings import Settings
        from backend.src.services.email_service import EmailToken

        token = EmailToken.generate()
        expiry_minutes = Settings.get("password_reset_token_expiry_minutes", 60)
        self.password_reset_token = token
        self.password_reset_token_expiry = datetime.utcnow() + timedelta(
            minutes=int(expiry_minutes)
        )
        return token

    def verify_password_reset_token(self, token: str) -> bool:
        """
        Verify password reset token.

        Args:
            token: Token to verify

        Returns:
            True if token is valid and not expired
        """
        if not self.password_reset_token:
            return False

        if self.password_reset_token != token:
            return False

        if not self.password_reset_token_expiry:
            return False

        return datetime.utcnow() <= self.password_reset_token_expiry

    def reset_password_with_token(self, token: str, new_password: str) -> bool:
        """
        Reset password using token.

        Args:
            token: Password reset token
            new_password: New password

        Returns:
            True if reset successful
        """
        if not self.verify_password_reset_token(token):
            return False

        self.set_password(new_password)
        self.password_reset_token = None
        self.password_reset_token_expiry = None
        return True

    def to_dict(self, include_email: bool = False) -> dict:
        """
        Convert user to dictionary

        Args:
            include_email: Whether to include email in response

        Returns:
            Dictionary representation of user
        """
        data = {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

        if include_email:
            data["email"] = self.email

        return data

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return True

    @staticmethod
    def get_by_username(username: str) -> Optional["User"]:
        """
        Get user by username

        Args:
            username: Username to search for

        Returns:
            User object or None
        """
        return cast(Optional["User"], User.query.filter_by(username=username).first())

    @staticmethod
    def get_by_email(email: str) -> Optional["User"]:
        """
        Get user by email

        Args:
            email: Email to search for

        Returns:
            User object or None
        """
        return cast(Optional["User"], User.query.filter_by(email=email).first())
