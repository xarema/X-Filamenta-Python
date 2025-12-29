"""
------------------------------------------------------------------------------
Purpose: 2FA/TOTP service
Description: Service for two-factor authentication using TOTP

File: backend/src/services/totp_service.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:30:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Notes:
- TOTP-based two-factor authentication
- QR code generation for easy setup
- Backup codes generation
------------------------------------------------------------------------------
"""

import base64
import io
import json
import secrets

import pyotp
import qrcode
from werkzeug.security import generate_password_hash

from backend.src.models.user import User


class TOTPService:
    """Service for TOTP-based 2FA"""

    @staticmethod
    def generate_secret() -> str:
        """
        Generate a random TOTP secret (base32)

        Returns:
            Base32 encoded secret string (32 characters)
        """
        import pyotp

        return str(pyotp.random_base32())

    def generate_provisioning_uri(
        user: User, secret: str, issuer: str = "X-Filamenta"
    ) -> str:
        """
        Generate provisioning URI for QR code

        Args:
            user: User object
            secret: TOTP secret
            issuer: Issuer name (app name)

        Returns:
            Provisioning URI string
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=user.email, issuer_name=issuer)

    @staticmethod
    def generate_qr_code(provisioning_uri: str) -> str:
        """
        Generate QR code image as base64 data URI

        Args:
            provisioning_uri: TOTP provisioning URI

        Returns:
            Base64 encoded QR code image (data URI)
        """
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_base64}"

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """
        Verify TOTP code

        Args:
            secret: Base32 encoded TOTP secret
            code: 6-digit TOTP code

        Returns:
            True if code is valid, False otherwise
        """
        if not secret or not code:
            return False

        try:
            totp = pyotp.TOTP(secret)
            # valid_window=1 allows codes from 30s before/after
            return totp.verify(code, valid_window=1)
        except Exception:
            return False

    @staticmethod
    def generate_backup_codes(count: int = 10) -> tuple[list[str], str]:
        """
        Generate backup codes for 2FA recovery

        Args:
            count: Number of backup codes to generate

        Returns:
            Tuple of (plain codes list, hashed codes JSON string)
        """
        codes = []
        hashed_codes = []

        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = secrets.token_hex(4).upper()  # 8 chars
            codes.append(code)
            hashed_codes.append(generate_password_hash(code))

        # Store hashed codes as JSON
        codes_json = json.dumps(hashed_codes)

        return codes, codes_json

    @staticmethod
    def verify_backup_code(user: User, code: str) -> bool:
        """
        Verify and consume a backup code

        Args:
            user: User object
            code: Backup code to verify

        Returns:
            True if code is valid and consumed, False otherwise
        """
        if not user.backup_codes or not code:
            return False

        try:
            from werkzeug.security import check_password_hash

            hashed_codes = json.loads(user.backup_codes)

            # Check if code matches any hashed code
            for i, hashed_code in enumerate(hashed_codes):
                if check_password_hash(hashed_code, code.upper()):
                    # Remove used code
                    hashed_codes.pop(i)
                    user.backup_codes = json.dumps(hashed_codes)
                    return True

            return False
        except Exception:
            return False
