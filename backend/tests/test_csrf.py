"""
------------------------------------------------------------------------------
Purpose: Tests for CSRF protection
Description: Test CSRF token generation, validation, and protection decorator

File: backend/tests/test_csrf.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:15:00+00:00
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
- Tests CSRF protection mechanisms
- Validates token generation and validation
------------------------------------------------------------------------------
"""


def test_csrf_token_generation(app):  # type: ignore[no-untyped-def]
    """Test that CSRF token is generated and stored in session"""
    from backend.src.services.csrf_service import CSRFService

    with app.app_context(), app.test_request_context():
        token = CSRFService.generate_token()

        assert token is not None
        assert len(token) == CSRFService.TOKEN_LENGTH * 2  # hex encoding
        assert isinstance(token, str)


def test_csrf_token_get_or_create(app):  # type: ignore[no-untyped-def]
    """Test that get_token creates a token if none exists"""
    from backend.src.services.csrf_service import CSRFService

    with app.app_context(), app.test_request_context():
        # Clear any existing token
        CSRFService.clear_token()

        # Get token (should create new one)
        token1 = CSRFService.get_token()
        assert token1 is not None

        # Get again (should return same token)
        token2 = CSRFService.get_token()
        assert token1 == token2


def test_csrf_token_validation_success(app):  # type: ignore[no-untyped-def]
    """Test that valid CSRF token passes validation"""
    from backend.src.services.csrf_service import CSRFService

    with app.app_context(), app.test_request_context():
        token = CSRFService.generate_token()

        assert CSRFService.validate_token(token) is True


def test_csrf_token_validation_failure(app):  # type: ignore[no-untyped-def]
    """Test that invalid CSRF token fails validation"""
    from backend.src.services.csrf_service import CSRFService

    with app.app_context(), app.test_request_context():
        CSRFService.generate_token()

        # Wrong token
        assert CSRFService.validate_token("wrong_token") is False

        # None token
        assert CSRFService.validate_token(None) is False


def test_csrf_token_in_template_context(client, app):  # type: ignore[no-untyped-def]
    """Test that CSRF token service works and returns valid tokens"""
    from backend.src.services.csrf_service import CSRFService

    with app.test_request_context():
        # Test that context processor provides csrf_token
        # (The actual injection is tested in integration tests)
        token = CSRFService.get_token()

        # Token should be valid hex string
        assert len(token) == 64  # 32 bytes hex = 64 chars
        assert all(c in "0123456789abcdef" for c in token)


def test_csrf_protect_decorator_allows_get(client):  # type: ignore[no-untyped-def]
    """Test that CSRF decorator allows GET requests"""
    # GET request should pass without CSRF token
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_csrf_protect_decorator_blocks_post_without_token(client, app):  # type: ignore[no-untyped-def]
    """Test that CSRF decorator blocks POST without valid token"""
    from flask import Blueprint

    from backend.src.decorators import csrf_protect

    # Create test blueprint with CSRF protected route
    test_bp = Blueprint("test_csrf", __name__)

    @test_bp.route("/test-csrf", methods=["POST"])
    @csrf_protect
    def test_route():  # type: ignore[no-untyped-def]
        return "Success"

    app.register_blueprint(test_bp)

    with app.test_client() as test_client:
        # POST without token should fail
        response = test_client.post("/test-csrf", data={})
        assert response.status_code == 403


def test_csrf_protect_decorator_allows_htmx(client, app):  # type: ignore[no-untyped-def]
    """Test that CSRF decorator allows HTMX requests"""
    from flask import Blueprint

    from backend.src.decorators import csrf_protect

    # Create test blueprint with CSRF protected route
    test_bp = Blueprint("test_csrf_htmx", __name__)

    @test_bp.route("/test-csrf-htmx", methods=["POST"])
    @csrf_protect
    def test_route():  # type: ignore[no-untyped-def]
        return "Success"

    app.register_blueprint(test_bp)

    with app.test_client() as test_client:
        # POST with HTMX header should pass (exempt)
        response = test_client.post(
            "/test-csrf-htmx", data={}, headers={"HX-Request": "true"}
        )
        assert response.status_code == 200
