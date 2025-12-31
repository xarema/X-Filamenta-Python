"""
------------------------------------------------------------------------------
Purpose: Test suite for PHASE 2 new routes
Description: Tests for pages, admin, and API endpoints

File: backend/tests/test_phase2_routes.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
------------------------------------------------------------------------------
"""

import pytest

from backend.src.app import create_app


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


# ---- Public Pages Tests ----


def test_about_page(client):
    """Test GET /about"""
    response = client.get("/about")
    assert response.status_code == 200
    # Check for content (avoiding UTF-8 issues)
    assert b"About" in response.data or b"Propos" in response.data


def test_contact_page_get(client):
    """Test GET /contact"""
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"contact" in response.data.lower()


def test_features_page(client):
    """Test GET /features"""
    response = client.get("/features")
    assert response.status_code == 200
    assert b"Features" in response.data or b"Fonctionnalites" in response.data


def test_preferences_page(client):
    """Test GET /preferences"""
    response = client.get("/preferences")
    assert response.status_code == 200
    assert b"preferences" in response.data.lower()


# ---- Admin Routes Tests ----


def test_admin_dashboard_unauthorized(client):
    """Test GET /admin/ without authentication (should fail)"""
    response = client.get("/admin/")
    # Should return 403 Forbidden (protected route)
    assert response.status_code == 403


def test_admin_users_unauthorized(client):
    """Test GET /admin/users without authentication"""
    response = client.get("/admin/users")
    assert response.status_code == 403


def test_admin_settings_unauthorized(client):
    """Test GET /admin/settings without authentication"""
    response = client.get("/admin/settings")
    assert response.status_code == 403


def test_admin_content_unauthorized(client):
    """Test GET /admin/content without authentication"""
    response = client.get("/admin/content")
    assert response.status_code == 403


# ---- API Tests ----


def test_api_config(client):
    """Test GET /api/config"""
    response = client.get("/api/config")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert "app_name" in data
    assert "version" in data


def test_api_version(client):
    """Test GET /api/version"""
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert "app_version" in data


def test_api_contact_post_valid(client):
    """Test POST /api/contact with valid data"""
    response = client.post(
        "/api/contact",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message",
        },
    )
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data["status"] == "success"


def test_api_contact_post_missing_fields(client):
    """Test POST /api/contact with missing fields"""
    response = client.post(
        "/api/contact",
        json={"name": "John Doe"},  # Missing email and message
    )
    assert response.status_code == 400
    assert response.is_json


def test_api_contact_post_invalid_email(client):
    """Test POST /api/contact with invalid email"""
    response = client.post(
        "/api/contact",
        json={
            "name": "John Doe",
            "email": "not-an-email",  # Invalid
            "message": "Hello",
        },
    )
    assert response.status_code == 400


def test_api_contact_post_message_too_long(client):
    """Test POST /api/contact with message too long"""
    response = client.post(
        "/api/contact",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "message": "x" * 5001,  # Too long
        },
    )
    assert response.status_code == 400


def test_api_contact_post_name_too_long(client):
    """Test POST /api/contact with name too long"""
    response = client.post(
        "/api/contact",
        json={
            "name": "x" * 101,  # Too long
            "email": "john@example.com",
            "message": "Hello",
        },
    )
    assert response.status_code == 400


def test_api_stats(client):
    """Test GET /api/data/stats"""
    response = client.get("/api/data/stats")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert "stats" in data


# ---- Error Handling Tests ----


def test_invalid_json_in_post(client):
    """Test POST with invalid JSON"""
    response = client.post(
        "/api/contact", data="invalid json", content_type="application/json"
    )
    # Should return 400 or 415
    assert response.status_code in [400, 415]
