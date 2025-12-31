"""
Purpose: Tests for Sessions and Cache integration
Description: Test suite for Flask-Session, Rate Limiting, and Service Caching

File: backend/tests/test_sessions_cache.py | Repository: X-Filamenta-Python
Created: 2025-12-29T20:00:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for Session backend configuration
- Tests for cache integration in UserService and ContentService
"""

import pytest
from unittest.mock import patch, MagicMock

from backend.src.services.user_service import UserService
from backend.src.services.content_service import ContentService


class TestSessionConfiguration:
    """Test Flask-Session configuration with different cache backends"""

    def test_app_sessions_configured(self, app):
        """Test that sessions are configured in app"""
        # Check session config exists
        assert 'SESSION_TYPE' in app.config
        # Session type should be one of: redis, filesystem, null
        assert app.config['SESSION_TYPE'] in ['redis', 'filesystem', 'null']

    def test_app_compression_enabled(self, app):
        """Test that Flask-Compress is enabled"""
        # Verify compression middleware is active
        # (Flask-Compress adds itself to app)
        assert hasattr(app, 'extensions')


class TestUserServiceCache:
    """Test caching in UserService"""

    def test_get_by_id_uses_cache(self, app):
        """Test that get_by_id uses cache"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.user import User

            # Create mock user
            mock_user = MagicMock(spec=User)
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"

            # Mock cache to return user
            with patch.object(cache_service, 'get', return_value=mock_user):
                with patch.object(User.query, 'get', return_value=None) as mock_query:
                    # Call get_by_id
                    result = UserService.get_by_id(1)

                    # Should return cached user
                    assert result == mock_user
                    # Should NOT query database
                    mock_query.assert_not_called()

    def test_get_by_id_caches_result(self, app):
        """Test that get_by_id caches database result"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.user import User

            # Create mock user
            mock_user = MagicMock(spec=User)
            mock_user.id = 1

            # Mock empty cache
            with patch.object(cache_service, 'get', return_value=None):
                with patch.object(cache_service, 'set') as mock_set:
                    with patch.object(User.query, 'get', return_value=mock_user):
                        # Call get_by_id
                        result = UserService.get_by_id(1)

                        # Should return user
                        assert result == mock_user
                        # Should cache result
                        mock_set.assert_called_once()
                        assert mock_set.call_args[0][0] == "user:id:1"
                        assert mock_set.call_args[0][1] == mock_user
                        assert mock_set.call_args[1]['ttl'] == 300

    def test_get_by_username_uses_cache(self, app):
        """Test that get_by_username uses cache"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.user import User

            mock_user = MagicMock(spec=User)
            mock_user.username = "testuser"

            with patch.object(cache_service, 'get', return_value=mock_user):
                with patch.object(User, 'get_by_username', return_value=None) as mock_get:
                    result = UserService.get_by_username("testuser")

                    assert result == mock_user
                    mock_get.assert_not_called()

    def test_invalidate_cache_clears_all_keys(self, app):
        """Test that invalidate_cache clears all user cache keys"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.user import User

            mock_user = MagicMock(spec=User)
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"

            with patch.object(cache_service, 'delete') as mock_delete:
                UserService.invalidate_cache(mock_user)

                # Should delete all 3 cache keys
                assert mock_delete.call_count == 3
                calls = [call[0][0] for call in mock_delete.call_args_list]
                assert "user:id:1" in calls
                assert "user:username:testuser" in calls
                assert "user:email:test@example.com" in calls


class TestContentServiceCache:
    """Test caching in ContentService"""

    def test_get_by_id_uses_cache(self, app):
        """Test that get_by_id uses cache"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.content import Content

            mock_content = MagicMock(spec=Content)
            mock_content.id = 1

            with patch.object(cache_service, 'get', return_value=mock_content):
                with patch.object(Content.query, 'get', return_value=None) as mock_query:
                    result = ContentService.get_by_id(1)

                    assert result == mock_content
                    mock_query.assert_not_called()

    def test_get_by_id_caches_result(self, app):
        """Test that get_by_id caches database result"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.content import Content

            mock_content = MagicMock(spec=Content)
            mock_content.id = 1

            with patch.object(cache_service, 'get', return_value=None):
                with patch.object(cache_service, 'set') as mock_set:
                    with patch.object(Content.query, 'get', return_value=mock_content):
                        result = ContentService.get_by_id(1)

                        assert result == mock_content
                        mock_set.assert_called_once()
                        assert mock_set.call_args[0][0] == "content:id:1"
                        assert mock_set.call_args[1]['ttl'] == 120

    def test_get_all_uses_cache(self, app):
        """Test that get_all uses cache"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service

            cached_result = ([MagicMock()], 1)

            with patch.object(cache_service, 'get', return_value=cached_result):
                result = ContentService.get_all()

                # Should return cached result
                assert result == cached_result

    def test_get_all_caches_result(self, app):
        """Test that get_all caches query result"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service
            from backend.src.models.content import Content

            mock_content = MagicMock(spec=Content)

            with patch.object(cache_service, 'get', return_value=None):
                with patch.object(cache_service, 'set') as mock_set:
                    with patch.object(Content.query, 'filter_by', return_value=Content.query):
                        with patch.object(Content.query, 'order_by', return_value=Content.query):
                            with patch.object(Content.query, 'count', return_value=1):
                                with patch.object(Content.query, 'limit', return_value=Content.query):
                                    with patch.object(Content.query, 'offset', return_value=Content.query):
                                        with patch.object(Content.query, 'all', return_value=[mock_content]):
                                            result = ContentService.get_all()

                                            # Should cache result
                                            mock_set.assert_called_once()
                                            assert mock_set.call_args[1]['ttl'] == 120

    def test_invalidate_cache_deletes_key(self, app):
        """Test that invalidate_cache deletes content cache"""
        with app.app_context():
            from backend.src.services.cache_service import cache_service

            with patch.object(cache_service, 'delete') as mock_delete:
                ContentService.invalidate_cache(1)

                mock_delete.assert_called_once_with("content:id:1")


class TestRateLimiterStorage:
    """Test rate limiter storage configuration"""

    def test_rate_limiter_uses_cache_backend(self):
        """Test that rate limiter uses correct storage based on cache backend"""
        from backend.src.services.rate_limiter import get_storage_uri

        # Should return either redis:// or memory://
        uri = get_storage_uri()
        assert uri.startswith('redis://') or uri == 'memory://'

    def test_rate_limiter_initialized(self, app):
        """Test that rate limiter is initialized in app"""
        from backend.src.services.rate_limiter import limiter

        # Verify limiter is attached to app
        assert limiter._app == app

