"""
------------------------------------------------------------------------------
Purpose: CSRF protection service
Description: Generate and validate CSRF tokens for form protection

File: backend/src/services/csrf_service.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:10:00+00:00
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
- CSRF protection for non-HTMX forms
- Token generation and validation
- Session-based tokens
------------------------------------------------------------------------------
"""

import secrets

from flask import session


class CSRFService:
    """Service for CSRF token generation and validation"""

    TOKEN_LENGTH = 32  # bytes
    SESSION_KEY = "_csrf_token"

    @staticmethod
    def generate_token() -> str:
        """
        Generate a new CSRF token and store it in session

        Returns:
            CSRF token string (hex)
        """
        token = secrets.token_hex(CSRFService.TOKEN_LENGTH)
        session[CSRFService.SESSION_KEY] = token
        return token

    @staticmethod
    def get_token() -> str:
        """
        Get existing CSRF token or generate a new one

        Returns:
            CSRF token string (hex)
        """
        token = session.get(CSRFService.SESSION_KEY)
        if not token:
            token = CSRFService.generate_token()
        return token

    @staticmethod
    def validate_token(token: str | None) -> bool:
        """
        Validate a CSRF token against the session token

        Args:
            token: Token to validate

        Returns:
            True if valid, False otherwise
        """
        if not token:
            return False

        session_token = session.get(CSRFService.SESSION_KEY)
        if not session_token:
            return False

        # Constant-time comparison to prevent timing attacks
        return secrets.compare_digest(token, session_token)

    @staticmethod
    def clear_token() -> None:
        """Clear CSRF token from session"""
        session.pop(CSRFService.SESSION_KEY, None)
