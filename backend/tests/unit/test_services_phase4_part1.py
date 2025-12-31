"""
------------------------------------------------------------------------------
Purpose: Phase 4 Part 1 — Unit tests for services
Description: Cover user/content/preferences service behaviors (happy + error cases)

File: backend/tests/unit/test_services_phase4_part1.py | Repository: X-Filamenta-Python
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

import pytest

from backend.src.app import create_app
from backend.src.extensions import db
from backend.src.services.content_service import ContentService
from backend.src.services.preferences_service import PreferencesService
from backend.src.services.user_service import UserService


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


def test_user_service_update_missing_user(app):
    with app.app_context():
        assert UserService.update(9999, username="ghost") is None


def test_user_service_update_ignores_password_hash(app):
    with app.app_context():
        user = UserService.create("u1", "u1@example.com", "Passw0rd!", is_admin=False)
        assert user is not None
        updated = UserService.update(user.id, password_hash="should_not_change")
        assert updated is not None
        # password_hash should remain a hashed value set earlier
        assert updated.password_hash == user.password_hash


def test_content_service_update_and_publish(app):
    with app.app_context():
        content = ContentService.create("Title", "Body", author_id=0)
        assert content is not None
        updated = ContentService.update(content.id, status="published")
        assert updated is not None
        assert updated.status == "published"
        archived = ContentService.archive(content.id)
        assert archived is not None
        assert archived.status == "archived"


def test_preferences_service_update_invalid_values(app):
    with app.app_context():
        assert PreferencesService.update_theme(1, "invalid") is False
        assert PreferencesService.update_language(1, "xx") is False


def test_preferences_service_update_valid_values(app):
    with app.app_context():
        assert PreferencesService.update_theme(1, "dark") is True
        assert PreferencesService.update_language(1, "en") is True
        assert PreferencesService.update_notifications(1, True) is True
