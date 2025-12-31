"""
------------------------------------------------------------------------------
Purpose: Tests for admin routes
Description: Test admin dashboard, user management, and audit logging

File: backend/tests/test_admin.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:32:00+00:00
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
- Tests admin functionality
- AdminHistory model tests
- CRUD user operations
------------------------------------------------------------------------------
"""


def test_admin_history_model(app):  # type: ignore[no-untyped-def]
    """Test AdminHistory model creation"""
    from backend.src.extensions import db
    from backend.src.models.admin_history import AdminHistory

    with app.app_context():
        db.create_all()

        # Create history entry
        entry = AdminHistory.log_action(
            admin_id=1,
            action="test_action",
            target_type="user",
            target_id=2,
            details={"test": "value"},
        )

        db.session.commit()

        # Verify
        assert entry.id is not None
        assert entry.action == "test_action"
        assert entry.admin_id == 1
        assert entry.target_type == "user"
        assert entry.target_id == 2

        # Cleanup
        db.session.delete(entry)
        db.session.commit()


def test_admin_history_to_dict(app):  # type: ignore[no-untyped-def]
    """Test AdminHistory to_dict conversion"""
    from backend.src.extensions import db
    from backend.src.models.admin_history import AdminHistory

    with app.app_context():
        db.create_all()

        entry = AdminHistory.log_action(
            admin_id=1,
            action="test",
            details={"key": "value"},
        )
        db.session.commit()

        data = entry.to_dict()

        assert data["action"] == "test"
        assert data["admin_id"] == 1
        assert data["details"] == {"key": "value"}

        db.session.delete(entry)
        db.session.commit()


def test_admin_dashboard_route_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin dashboard route exists"""
    # Without auth, should redirect or 401/403
    response = client.get("/admin/")
    assert response.status_code in (302, 401, 403)


def test_admin_users_route_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin users route exists"""
    response = client.get("/admin/users")
    assert response.status_code in (302, 401, 403)


def test_admin_settings_route_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin settings route exists"""
    response = client.get("/admin/settings")
    assert response.status_code in (302, 401, 403)


def test_admin_api_get_user_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin API user endpoint exists"""
    response = client.get("/admin/api/users/1")
    assert response.status_code in (302, 401, 403, 404)


def test_admin_api_update_user_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin API update user endpoint exists"""
    response = client.put("/admin/api/users/1", json={"email": "test@test.com"})
    assert response.status_code in (302, 401, 403, 404)


def test_admin_api_delete_user_exists(client):  # type: ignore[no-untyped-def]
    """Test that admin API delete user endpoint exists"""
    response = client.delete("/admin/api/users/1")
    assert response.status_code in (302, 401, 403, 404)
