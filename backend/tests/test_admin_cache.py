"""
Purpose: Tests for Admin Cache routes
Description: Test suite for admin cache management interface

File: backend/tests/test_admin_cache.py | Repository: X-Filamenta-Python
Created: 2025-12-29T20:30:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for admin cache settings page
- Tests for cache operations (test, clear)
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAdminCacheAccess:
    """Test admin cache page access control"""

    def test_cache_page_requires_admin(self, client):
        """Test that cache page requires admin access"""
        # Try to access without login
        response = client.get("/admin/cache/")

        # Should return 403 Forbidden (or 302 redirect)
        assert response.status_code in [302, 403]


class TestAdminCacheSettings:
    """Test admin cache settings page"""

    def test_cache_settings_page_loads(self, client, admin_user):
        """Test that cache settings page loads for admin"""
        # Login as admin (mock)
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            response = client.get("/admin/cache/")

            assert response.status_code == 200
            # Should contain cache settings
            assert b"cache" in response.data.lower() or b"Cache" in response.data


class TestRedisConnectionTest:
    """Test Redis connection testing endpoints"""

    def test_test_redis_endpoint(self, client, admin_user):
        """Test simple Redis connection test endpoint"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
                mock_test.return_value = (True, "Success", {
                    "version": "7.0.0",
                    "memory_used": "1M",
                    "uptime_days": 10,
                    "connected_clients": 5
                })

                response = client.post(
                    "/admin/cache/test-redis",
                    json={
                        "host": "localhost",
                        "port": 6379,
                        "password": "",
                        "db": 0
                    }
                )

                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                assert 'info' in data

    def test_test_redis_advanced_endpoint(self, client, admin_user):
        """Test advanced Redis connection test endpoint"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.test_redis_advanced') as mock_test:
                mock_test.return_value = (True, "Success", {
                    "write_time_ms": 2.5,
                    "read_time_ms": 1.2,
                    "permissions": "OK"
                })

                response = client.post(
                    "/admin/cache/test-advanced",
                    json={
                        "host": "localhost",
                        "port": 6379,
                        "password": "",
                        "db": 0
                    }
                )

                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                assert 'info' in data

    def test_test_redis_failure(self, client, admin_user):
        """Test Redis test with connection failure"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
                mock_test.return_value = (False, "Connection refused", None)

                response = client.post(
                    "/admin/cache/test-redis",
                    json={
                        "host": "localhost",
                        "port": 6379
                    }
                )

                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is False


class TestCacheClear:
    """Test cache clearing operations"""

    def test_clear_cache_endpoint(self, client, admin_user):
        """Test cache clear endpoint"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.flush') as mock_flush:
                response = client.post("/admin/cache/clear")

                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                # Verify flush was called
                mock_flush.assert_called_once()

    def test_clear_cache_error(self, client, admin_user):
        """Test cache clear with error"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.flush') as mock_flush:
                mock_flush.side_effect = Exception("Cache error")

                response = client.post("/admin/cache/clear")

                assert response.status_code == 500
                data = response.get_json()
                assert data['success'] is False


class TestCacheStats:
    """Test cache statistics endpoint"""

    def test_cache_stats_endpoint(self, client, admin_user):
        """Test cache stats endpoint"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.id
            sess['is_admin'] = True

        with patch('backend.src.decorators.require_admin', lambda f: f):
            with patch('backend.src.services.cache_service.CacheService.get_info') as mock_info:
                mock_info.return_value = {
                    "backend": "redis",
                    "info": {"type": "redis", "version": "7.0.0"}
                }

                response = client.get("/admin/cache/stats")

                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
                assert 'backend' in data
                assert 'info' in data

