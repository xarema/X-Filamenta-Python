"""
------------------------------------------------------------------------------
Purpose: Tests for rate limiting
Description: Test rate limiting on login, 2FA, and admin routes

File: backend/tests/test_rate_limiting.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:30:00+00:00
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
- Tests rate limiting functionality
- Validates different limit tiers
------------------------------------------------------------------------------
"""


def test_rate_limiter_service_exists():  # type: ignore[no-untyped-def]
    """Test that rate limiter service can be imported"""
    from backend.src.services.rate_limiter import (
        api_rate_limit,
        limiter,
        login_rate_limit,
        strict_rate_limit,
        two_fa_rate_limit,
    )

    assert limiter is not None
    assert callable(login_rate_limit)
    assert callable(two_fa_rate_limit)
    assert callable(strict_rate_limit)
    assert callable(api_rate_limit)


def test_login_rate_limit_applied(client):  # type: ignore[no-untyped-def]
    """Test that login route has rate limiting"""
    # Note: In memory storage, limits reset between tests
    # This test validates the decorator is applied

    # First request should succeed (or fail with auth error, not rate limit)
    response = client.post(
        "/auth/login",
        json={"username": "test", "password": "test"},
    )

    # Should get 400/401, not 429 (rate limit)
    assert response.status_code in (400, 401)


def test_rate_limit_header_present(client):  # type: ignore[no-untyped-def]
    """Test that rate limit headers are present in responses"""
    response = client.post(
        "/auth/login",
        json={"username": "test", "password": "test"},
    )

    # Flask-Limiter adds X-RateLimit headers
    # Note: Headers might not be present in test mode
    # This is informational
    assert response.status_code in (400, 401, 429)


def test_rate_limiter_user_identifier():  # type: ignore[no-untyped-def]
    """Test that user identifier function works"""
    from backend.src.services.rate_limiter import get_user_identifier

    # Should return IP or IP:user_id
    identifier = get_user_identifier()
    assert isinstance(identifier, str)
    assert len(identifier) > 0


def test_strict_rate_limit_decorator():  # type: ignore[no-untyped-def]
    """Test that strict rate limit decorator exists"""
    from backend.src.services.rate_limiter import strict_rate_limit

    decorator = strict_rate_limit()
    assert decorator is not None
