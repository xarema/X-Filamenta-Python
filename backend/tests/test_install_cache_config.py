"""
Purpose: Tests for wizard cache configuration step
Description: Test suite for cache_config and cache_test steps in wizard

File: backend/tests/test_install_cache_config.py | Repository: X-Filamenta-Python
Created: 2025-12-29T19:40:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for cache configuration wizard steps
"""

import pytest
from unittest.mock import patch, MagicMock

from backend.src.services.install_service import InstallService


class TestCacheConfigStep:
    """Test cache configuration wizard step"""

    def test_cache_config_step_redis_available(self, client):
        """Test cache_config step when Redis was detected in requirements"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_config",
                "redis_available": True,
                "redis_version": "7.0.0"
            }

        response = client.post(
            "/install/step",
            data={"step": "cache_config"}
        )

        assert response.status_code == 200
        # Verify wizard state is preserved
        with client.session_transaction() as sess:
            state = sess.get("wizard_state", {})
            assert state.get("redis_available") is True

    def test_cache_config_step_redis_unavailable(self, client):
        """Test cache_config step when Redis was not detected"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_config",
                "redis_available": False,
                "redis_version": None
            }

        response = client.post(
            "/install/step",
            data={"step": "cache_config"}
        )

        assert response.status_code == 200
        # Verify state
        with client.session_transaction() as sess:
            state = sess.get("wizard_state", {})
            assert state.get("redis_available") is False


class TestCacheTestStep:
    """Test cache test wizard step"""

    def test_cache_test_redis_success(self, client):
        """Test cache_test with successful Redis connection"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_test",
                "redis_available": True
            }

        with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
            mock_test.return_value = (True, "Success", {
                "version": "7.0.0",
                "memory_used": "1.2M",
                "uptime_days": 10,
                "connected_clients": 5
            })

            response = client.post(
                "/install/step",
                data={
                    "step": "cache_test",
                    "cache_backend": "redis",
                    "redis_host": "localhost",
                    "redis_port": "6379",
                    "redis_password": "",
                    "redis_db": "0"
                }
            )

            assert response.status_code == 200
            # Should show success message
            assert b"success" in response.data.lower() or b"7.0.0" in response.data

    def test_cache_test_redis_failure_fallback(self, client):
        """Test cache_test with Redis failure, fallback to filesystem"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_test",
                "redis_available": True
            }

        with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
            mock_test.return_value = (False, "Connection refused", None)

            response = client.post(
                "/install/step",
                data={
                    "step": "cache_test",
                    "cache_backend": "redis",
                    "redis_host": "localhost",
                    "redis_port": "6379",
                    "redis_password": "",
                    "redis_db": "0"
                }
            )

            assert response.status_code == 200
            # Should show fallback message
            assert b"filesystem" in response.data.lower() or b"fallback" in response.data.lower()

    def test_cache_test_filesystem_no_test(self, client):
        """Test cache_test with filesystem backend (no test needed)"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_test",
                "redis_available": False
            }

        response = client.post(
            "/install/step",
            data={
                "step": "cache_test",
                "cache_backend": "filesystem"
            }
        )

        assert response.status_code == 200
        # Should show success without testing
        assert b"filesystem" in response.data.lower()


class TestCacheStateManagement:
    """Test cache configuration state management"""

    def test_cache_config_saved_to_state(self, client):
        """Test that cache configuration is saved to wizard state"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_test"
            }

        with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
            mock_test.return_value = (True, "Success", {"version": "7.0.0"})

            response = client.post(
                "/install/step",
                data={
                    "step": "cache_test",
                    "cache_backend": "redis",
                    "redis_host": "custom.host",
                    "redis_port": "6380",
                    "redis_password": "secret",
                    "redis_db": "1"
                }
            )

            # Check state was updated
            with client.session_transaction() as sess:
                state = sess.get("wizard_state", {})
                assert state.get("cache_backend") == "redis"
                assert state.get("redis_host") == "custom.host"
                assert state.get("redis_port") == 6380
                assert state.get("redis_password") == "secret"
                assert state.get("redis_db") == 1

    def test_cache_fallback_updates_state(self, client):
        """Test that failed Redis test updates state to filesystem"""
        with client.session_transaction() as sess:
            sess["wizard_state"] = {
                "step": "cache_test"
            }

        with patch('backend.src.services.cache_service.CacheService.test_redis_connection') as mock_test:
            mock_test.return_value = (False, "Connection error", None)

            response = client.post(
                "/install/step",
                data={
                    "step": "cache_test",
                    "cache_backend": "redis",
                    "redis_host": "localhost",
                    "redis_port": "6379"
                }
            )

            # Check state was updated to filesystem
            with client.session_transaction() as sess:
                state = sess.get("wizard_state", {})
                assert state.get("cache_backend") == "filesystem"
                assert state.get("cache_test_failed") is True
                assert "cache_test_error" in state

