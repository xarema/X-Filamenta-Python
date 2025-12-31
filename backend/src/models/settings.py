"""
Purpose: Settings model for application configuration
Description: Key-value store with encryption support

File: backend/src/models/settings.py | Repository: X-Filamenta-Python
Created: 2025-12-29T02:30:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Supports encryption for sensitive fields (passwords, API keys)
- Uses Fernet symmetric encryption with Flask SECRET_KEY
"""

import base64
import json
from datetime import datetime
from typing import Any

from cryptography.fernet import Fernet

from backend.src.extensions import db


class Settings(db.Model):
    """
    Application settings storage model.

    Stores system-wide configuration as key-value pairs with optional encryption.
    Sensitive fields (SMTP passwords, API keys) are encrypted using Fernet.

    Attributes:
        id: Primary key
        key: Setting key name (unique)
        value: Setting value (JSON serialized if complex type)
        encrypted: Flag if value is encrypted
        description: Human-readable description
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    encrypted = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # List of fields that should be encrypted
    ENCRYPTED_FIELDS = [
        "smtp_password",
        "smtp_user",
        "sendgrid_api_key",
    ]

    # Default settings with their types and descriptions
    DEFAULTS = {
        # SMTP Configuration
        "smtp_host": {
            "value": "smtp.mailtrap.io",
            "type": "string",
            "description": "SMTP server hostname",
        },
        "smtp_port": {
            "value": "465",
            "type": "integer",
            "description": "SMTP server port",
        },
        "smtp_user": {
            "value": "",
            "type": "string",
            "description": "SMTP username",
        },
        "smtp_password": {
            "value": "",
            "type": "string",
            "description": "SMTP password (encrypted)",
        },
        "smtp_tls_enabled": {
            "value": "true",
            "type": "boolean",
            "description": "Enable TLS for SMTP",
        },
        "smtp_from_email": {
            "value": "noreply@example.com",
            "type": "string",
            "description": "Sender email address",
        },
        "smtp_from_name": {
            "value": "X-Filamenta",
            "type": "string",
            "description": "Sender display name",
        },
        # Email Verification Settings
        "email_verification_required": {
            "value": "false",
            "type": "boolean",
            "description": "Require email verification before login",
        },
        "email_verification_token_expiry_hours": {
            "value": "24",
            "type": "integer",
            "description": "Email verification token expiry (hours)",
        },
        "password_reset_token_expiry_minutes": {
            "value": "60",
            "type": "integer",
            "description": "Password reset token expiry (minutes)",
        },
        "password_reset_rate_limit_per_hour": {
            "value": "2",
            "type": "integer",
            "description": "Max password reset requests per hour",
        },
        "email_format": {
            "value": "html_with_fallback",
            "type": "enum",
            "description": "Email format: html_only, txt_only, html_with_fallback",
        },
        # Feature Flags
        "registration_enabled": {
            "value": "false",
            "type": "boolean",
            "description": "Allow user self-registration",
        },
        "2fa_required": {
            "value": "false",
            "type": "boolean",
            "description": "Require 2FA for all users",
        },
        # Site Configuration
        "site_name": {
            "value": "X-Filamenta",
            "type": "string",
            "description": "Site display name",
        },
        "site_url": {
            "value": "http://localhost:5000",
            "type": "string",
            "description": "Site base URL",
        },
        "logo_url": {
            "value": "/static/logo.png",
            "type": "string",
            "description": "Logo image URL",
        },
        "footer_text": {
            "value": "© 2025 XAREMA. All rights reserved.",
            "type": "string",
            "description": "Footer text",
        },
    }

    def __repr__(self) -> str:
        suffix = "..." if len(self.value) > 50 else ""
        return f"<Settings {self.key}={self.value[:50]}{suffix}>"

    @staticmethod
    def _get_fernet_key(app=None) -> Fernet:
        """Get Fernet cipher using Flask SECRET_KEY."""
        from flask import current_app

        app = app or current_app
        secret_key = app.config.get("SECRET_KEY", "").encode()

        # Ensure key is 32 bytes for Fernet
        if not secret_key:
            raise RuntimeError("SECRET_KEY not configured")

        key_bytes = base64.urlsafe_b64encode(secret_key[:32].ljust(32, b"\x00"))
        return Fernet(key_bytes)

    @staticmethod
    def _encrypt_value(value: str, app=None) -> str:
        """Encrypt value using Fernet."""
        cipher = Settings._get_fernet_key(app)
        encrypted = cipher.encrypt(value.encode())
        return encrypted.decode()

    @staticmethod
    def _decrypt_value(encrypted_value: str, app=None) -> str:
        """Decrypt value using Fernet."""
        try:
            cipher = Settings._get_fernet_key(app)
            decrypted = cipher.decrypt(encrypted_value.encode())
            return decrypted.decode()
        except Exception:
            # Return encrypted value if decryption fails
            return encrypted_value

    def get_value(self, app=None) -> Any:
        """
        Get setting value with type conversion and decryption if needed.

        Args:
            app: Flask app instance (uses current_app if None)

        Returns:
            Decrypted and type-converted value
        """
        value = self.value

        # Decrypt if encrypted
        if self.encrypted:
            value = self._decrypt_value(value, app)

        # Try to parse as JSON first
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value

    def set_value(self, value: Any, app=None) -> None:
        """
        Set setting value with encryption if field requires it.

        Args:
            value: Value to set
            app: Flask app instance (uses current_app if None)
        """
        # Serialize complex types to JSON
        value_str = json.dumps(value) if isinstance(value, (dict, list)) else str(value)

        # Encrypt if field is in ENCRYPTED_FIELDS
        if self.key in self.ENCRYPTED_FIELDS:
            value_str = self._encrypt_value(value_str, app)
            self.encrypted = True
        else:
            self.encrypted = False

        self.value = value_str
        self.updated_at = datetime.utcnow()

    @classmethod
    def get(cls, key: str, default: Any = None, app=None) -> Any:
        """
        Get a setting value by key.

        Args:
            key: Setting key
            default: Default value if not found
            app: Flask app instance

        Returns:
            Setting value or default
        """
        setting = cls.query.filter_by(key=key).first()

        if setting is None:
            return default

        return setting.get_value(app)

    @classmethod
    def set(cls, key: str, value: Any, description: str = None, app=None) -> "Settings":
        """
        Set a setting value, creating if not exists.

        Args:
            key: Setting key
            value: Value to set
            description: Optional description
            app: Flask app instance

        Returns:
            Settings instance
        """
        setting = cls.query.filter_by(key=key).first()

        if setting is None:
            setting = cls(key=key, description=description)
            db.session.add(setting)

        setting.set_value(value, app)
        db.session.commit()

        return setting

    @classmethod
    def get_all(cls) -> dict:
        """Get all settings as dictionary."""
        settings = cls.query.all()
        return {s.key: s.get_value() for s in settings}

    @classmethod
    def init_defaults(cls) -> None:
        """Initialize default settings in database."""

        for key, config in cls.DEFAULTS.items():
            existing = cls.query.filter_by(key=key).first()

            if existing is None:
                setting = cls(
                    key=key,
                    value=config["value"],
                    description=config.get("description"),
                )

                # Encrypt if needed
                if key in cls.ENCRYPTED_FIELDS and config["value"]:
                    setting.set_value(config["value"])

                db.session.add(setting)

        db.session.commit()

    def to_dict(self, include_encrypted: bool = False) -> dict:
        """
        Convert setting to dictionary.

        Args:
            include_encrypted: Include encrypted values (for admin view)

        Returns:
            Dictionary representation
        """
        value = self.get_value()

        # Mask encrypted values for security
        if (
            self.encrypted
            and not include_encrypted
            and isinstance(value, str)
            and value
        ):
            value = "*" * min(len(value), 10)

        return {
            "id": self.id,
            "key": self.key,
            "value": value,
            "encrypted": self.encrypted,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
