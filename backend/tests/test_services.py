"""
------------------------------------------------------------------------------
Purpose: Test suite for services
Description: Tests for UserService, PreferencesService, ContentService

File: backend/tests/test_services.py | Repository: X-Filamenta-Python
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

from backend.src.app import create_app, db
from backend.src.services.content_service import ContentService
from backend.src.services.preferences_service import PreferencesService
from backend.src.services.user_service import UserService


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


# ---- UserService Tests ----


def test_user_service_create(app):
    """Test creating a user"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("password123")
        assert not user.is_admin


def test_user_service_create_admin(app):
    """Test creating an admin user"""
    with app.app_context():
        user = UserService.create(
            "admin",
            "admin@example.com",
            "admin123",
            is_admin=True,
        )

        assert user is not None
        assert user.is_admin


def test_user_service_get_by_username(app):
    """Test getting user by username"""
    with app.app_context():
        UserService.create("testuser", "test@example.com", "password123")
        user = UserService.get_by_username("testuser")

        assert user is not None
        assert user.username == "testuser"


def test_user_service_get_by_email(app):
    """Test getting user by email"""
    with app.app_context():
        UserService.create("testuser", "test@example.com", "password123")
        user = UserService.get_by_email("test@example.com")

        assert user is not None
        assert user.email == "test@example.com"


def test_user_service_authenticate_success(app):
    """Test successful authentication"""
    with app.app_context():
        UserService.create("testuser", "test@example.com", "password123")
        user = UserService.authenticate("testuser", "password123")

        assert user is not None
        assert user.username == "testuser"


def test_user_service_authenticate_fail(app):
    """Test failed authentication"""
    with app.app_context():
        UserService.create("testuser", "test@example.com", "password123")
        user = UserService.authenticate("testuser", "wrongpassword")

        assert user is None


def test_user_service_update(app):
    """Test updating user"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        updated = UserService.update(user.id, username="newusername")

        assert updated is not None
        assert updated.username == "newusername"


def test_user_service_delete(app):
    """Test soft delete"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        result = UserService.delete(user.id)

        assert result is True

        # User should still exist but be inactive
        deleted_user = UserService.get_by_id(user.id)
        assert deleted_user is not None
        assert not deleted_user.is_active


# ---- PreferencesService Tests ----


def test_preferences_service_get_or_create(app):
    """Test getting or creating preferences"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        prefs = PreferencesService.get(user.id)

        assert prefs is not None
        assert prefs.theme == "light"
        assert prefs.language == "fr"
        assert prefs.notifications is True


def test_preferences_service_update_theme(app):
    """Test updating theme"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        result = PreferencesService.update_theme(user.id, "dark")

        assert result is True

        prefs = PreferencesService.get(user.id)
        assert prefs.theme == "dark"


def test_preferences_service_update_language(app):
    """Test updating language"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        result = PreferencesService.update_language(user.id, "en")

        assert result is True

        prefs = PreferencesService.get(user.id)
        assert prefs.language == "en"


def test_preferences_service_to_dict(app):
    """Test converting preferences to dict"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        prefs_dict = PreferencesService.to_dict(user.id)

        assert "theme" in prefs_dict
        assert "language" in prefs_dict
        assert "notifications" in prefs_dict


# ---- ContentService Tests ----


def test_content_service_create(app):
    """Test creating content"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        content = ContentService.create(
            title="Test Post", body="This is a test post", author_id=user.id
        )

        assert content is not None
        assert content.title == "Test Post"
        assert content.type == "post"
        assert content.status == "draft"


def test_content_service_get_all(app):
    """Test getting all content"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")

        ContentService.create("Post 1", "Body 1", user.id)
        ContentService.create("Post 2", "Body 2", user.id)

        items, total = ContentService.get_all()

        assert total == 2
        assert len(items) == 2


def test_content_service_pagination(app):
    """Test content pagination"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")

        # Create 5 posts
        for i in range(5):
            ContentService.create(f"Post {i}", f"Body {i}", user.id)

        items, total = ContentService.get_all(page=1, per_page=2)

        assert total == 5
        assert len(items) == 2


def test_content_service_publish(app):
    """Test publishing content"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")
        content = ContentService.create("Test Post", "Body", user.id)

        published = ContentService.publish(content.id)

        assert published is not None
        assert published.status == "published"


def test_content_service_search(app):
    """Test content search"""
    with app.app_context():
        user = UserService.create("testuser", "test@example.com", "password123")

        ContentService.create("Python Tutorial", "Learn Python", user.id)
        ContentService.create("Flask Guide", "Learn Flask", user.id)

        items, total = ContentService.search("Python")

        assert total == 1
        assert items[0].title == "Python Tutorial"


def test_content_service_get_by_author(app):
    """Test getting content by author"""
    with app.app_context():
        user1 = UserService.create("user1", "user1@example.com", "pass")
        user2 = UserService.create("user2", "user2@example.com", "pass")

        ContentService.create("Post 1", "Body 1", user1.id)
        ContentService.create("Post 2", "Body 2", user1.id)
        ContentService.create("Post 3", "Body 3", user2.id)

        items, total = ContentService.get_by_author(user1.id)

        assert total == 2
        assert all(item.author_id == user1.id for item in items)
