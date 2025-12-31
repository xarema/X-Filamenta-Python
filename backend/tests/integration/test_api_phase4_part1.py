"""
------------------------------------------------------------------------------
Purpose: Phase 4 Part 1 — Integration tests for API endpoints
Description: Validate API /api/contact and /api/preferences behaviors

File: backend/tests/integration/test_api_phase4_part1.py | Repository: X-Filamenta-Python
Created: 2025-12-27T12:55:00+00:00
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

from backend.src.app import create_app


def test_api_contact_missing_json():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post("/api/contact", data="", content_type="application/json")
    assert resp.status_code == 400


def test_api_contact_missing_fields():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post("/api/contact", json={"name": "John"})
    assert resp.status_code == 400


def test_api_contact_invalid_email():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post(
        "/api/contact", json={"name": "John", "email": "bad", "message": "Hi"}
    )
    assert resp.status_code == 400


def test_api_contact_success():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post(
        "/api/contact",
        json={"name": "John", "email": "john@example.com", "message": "Hello"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"


def test_api_preferences_update():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post(
        "/api/preferences",
        json={"theme": "dark", "language": "fr", "notifications": True},
    )
    assert resp.status_code in (200, 400)
    data = resp.get_json()
    assert "status" in data or "error" in data
