"""
------------------------------------------------------------------------------
Purpose: Tests for authentication routes
Description: Unit tests for login, logout, and session management

File: backend/tests/test_auth.py | Repository: X-Filamenta-Python
Created: 2025-12-27T14:30:00+00:00
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
- Tests for authentication routes
- Tests for session management
------------------------------------------------------------------------------
"""


def test_login_page_get(client):  # type: ignore[no-untyped-def]
    """Test GET /auth/login returns login page"""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Connexion" in response.data or b"login" in response.data.lower()


def test_login_success(client, app):  # type: ignore[no-untyped-def]
    """Test successful login with valid credentials"""
    from backend.src.services.user_service import UserService

    # Create a test user
    with app.app_context():
        user_service = UserService()
        user_service.create(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )

    # Attempt login
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "TestPass123!"},
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("success") is True
    assert "redirect" in data


def test_login_invalid_credentials(client, app):  # type: ignore[no-untyped-def]
    """Test login with invalid credentials returns 401"""
    from backend.src.services.user_service import UserService

    # Create a test user
    with app.app_context():
        user_service = UserService()
        user_service.create(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )

    # Attempt login with wrong password
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "WrongPassword"},
        content_type="application/json",
    )

    assert response.status_code == 401
    data = response.get_json()
    assert data is not None
    assert "error" in data


def test_login_missing_fields(client):  # type: ignore[no-untyped-def]
    """Test login with missing fields returns 400"""
    response = client.post(
        "/auth/login", json={"username": "testuser"}, content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data is not None
    assert "error" in data


def test_login_inactive_user(client, app):  # type: ignore[no-untyped-def]
    """Test login with inactive user returns 401"""
    from backend.src.services.user_service import UserService

    # Create an inactive test user
    with app.app_context():
        user_service = UserService()
        created_user = user_service.create(
            username="inactiveuser",
            email="inactive@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )
        # Deactivate user
        user_service.update(created_user.id, is_active=False)

    # Attempt login
    response = client.post(
        "/auth/login",
        json={"username": "inactiveuser", "password": "TestPass123!"},
        content_type="application/json",
    )

    assert response.status_code == 401
    data = response.get_json()
    assert data is not None
    assert "error" in data
    assert "désactivé" in data["error"].lower()


def test_logout(client, app):  # type: ignore[no-untyped-def]
    """Test logout clears session"""
    from backend.src.services.user_service import UserService

    # Create and login a test user
    with app.app_context():
        user_service = UserService()
        user_service.create(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )

    # Login
    client.post(
        "/auth/login",
        json={"username": "testuser", "password": "TestPass123!"},  # noqa: S106
        content_type="application/json",
    )

    # Logout
    response = client.post("/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("success") is True


def test_status_authenticated(client, app):  # type: ignore[no-untyped-def]
    """Test /auth/status returns user info when authenticated"""
    from backend.src.services.user_service import UserService

    # Create and login a test user
    with app.app_context():
        user_service = UserService()
        user_service.create(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )

    # Login
    client.post(
        "/auth/login",
        json={"username": "testuser", "password": "TestPass123!"},  # noqa: S106
        content_type="application/json",
    )

    # Check status
    response = client.get("/auth/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("authenticated") is True
    assert "user" in data
    assert data["user"]["username"] == "testuser"


def test_status_not_authenticated(client):  # type: ignore[no-untyped-def]
    """Test /auth/status returns not authenticated when no session"""
    response = client.get("/auth/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("authenticated") is False


def test_dashboard_requires_authentication(client):  # type: ignore[no-untyped-def]
    """Test /dashboard redirects to login if not authenticated"""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302  # Redirect
    assert "/auth/login" in response.location


def test_dashboard_authenticated(client, app):  # type: ignore[no-untyped-def]
    """Test /dashboard accessible when authenticated"""
    from backend.src.services.user_service import UserService

    # Create and login a test user
    with app.app_context():
        user_service = UserService()
        user_service.create(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",  # noqa: S106
            is_admin=False,
        )

    # Login
    client.post(
        "/auth/login",
        json={"username": "testuser", "password": "TestPass123!"},  # noqa: S106
        content_type="application/json",
    )

    # Access dashboard
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Tableau de bord" in response.data or b"dashboard" in response.data.lower()
