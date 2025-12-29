"""
------------------------------------------------------------------------------
Purpose: Rate limiting configuration and utilities
Description: Flask-Limiter setup and custom rate limit decorators

File: backend/src/services/rate_limiter.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:05:00+00:00
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
- Rate limiting configuration
- Protection against brute-force attacks
- Custom limit decorators for different routes
------------------------------------------------------------------------------
"""

from collections.abc import Callable
from typing import Any

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize limiter (will be configured in app factory)
# Default limits are DISABLED to avoid blocking dev/test
# Use explicit decorators on sensitive routes instead
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No default limit - apply explicitly per route
    storage_uri="memory://",
)


def get_user_identifier() -> str:
    """
    Get user identifier for rate limiting

    Uses IP address + user_id if authenticated for more granular control

    Returns:
        Identifier string for rate limiting
    """
    from flask import session

    ip = get_remote_address()
    user_id = session.get("user_id")

    if user_id:
        return f"{ip}:{user_id}"
    return ip


# Custom rate limit decorators for specific use cases


def login_rate_limit() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Rate limit decorator for login routes

    Limits: 5 attempts per minute, 20 per hour
    Prevents brute-force password attacks
    """
    return limiter.limit(  # type: ignore[no-any-return]
        "5 per minute, 20 per hour",
        key_func=get_user_identifier,
        error_message="Trop de tentatives de connexion. Réessayez plus tard.",
    )


def two_fa_rate_limit() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Rate limit decorator for 2FA verification routes

    Limits: 10 attempts per minute, 30 per hour
    Prevents brute-force TOTP code guessing
    """
    return limiter.limit(  # type: ignore[no-any-return]
        "10 per minute, 30 per hour",
        key_func=get_user_identifier,
        error_message=(
            "Trop de tentatives de vérification 2FA. Réessayez dans quelques minutes."
        ),
    )


def api_rate_limit() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Rate limit decorator for API routes

    Limits: 100 per hour
    General API protection
    """
    return limiter.limit(  # type: ignore[no-any-return]
        "100 per hour",
        key_func=get_user_identifier,
        error_message="Limite d'API atteinte. Réessayez plus tard.",
    )


def strict_rate_limit() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Rate limit decorator for sensitive operations

    Limits: 3 per minute, 10 per hour
    For very sensitive operations (password reset, admin actions)
    """
    return limiter.limit(  # type: ignore[no-any-return]
        "3 per minute, 10 per hour",
        key_func=get_user_identifier,
        error_message=(
            "Limite stricte atteinte. Contactez l'administrateur si nécessaire."
        ),
    )
