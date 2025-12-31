"""
Purpose: Tests for Redis detection in installation wizard
Description: Test suite for detect_redis_standard and detect_redis_custom_port

File: backend/tests/test_install_redis_detection.py | Repository: X-Filamenta-Python
Created: 2025-12-29T19:15:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for Redis detection in wizard step "requirements"
"""

import pytest
from unittest.mock import patch, MagicMock

from backend.src.services.install_service import InstallService


class TestRedisDetection:
    """Test Redis auto-detection for wizard"""

    def test_detect_redis_standard_available(self):
        """Test detecting Redis on standard port when available"""
        with patch('redis.Redis') as mock_redis:
            # Mock successful connection
            mock_redis.return_value.ping.return_value = True
            mock_redis.return_value.info.return_value = {
                "redis_version": "7.0.0",
                "used_memory_human": "1.2M"
            }

            result = InstallService.detect_redis_standard()

            assert result["detected"] is True
            assert result["version"] == "7.0.0"
            assert result["host"] == "localhost"
            assert result["port"] == 6379
            assert "localhost" in result["message"]

    def test_detect_redis_standard_unavailable(self):
        """Test detecting Redis when not available on standard port"""
        with patch('redis.Redis') as mock_redis:
            # Mock connection failure
            mock_redis.return_value.ping.side_effect = Exception("Connection refused")

            result = InstallService.detect_redis_standard()

            assert result["detected"] is False
            assert result["version"] is None
            assert result["host"] is None
            assert result["port"] is None
            assert "Redis" in result["message"]

    def test_detect_redis_custom_port_available(self):
        """Test detecting Redis on custom port when available"""
        with patch('redis.Redis') as mock_redis:
            # Mock successful connection
            mock_redis.return_value.ping.return_value = True
            mock_redis.return_value.info.return_value = {
                "redis_version": "6.2.5",
                "used_memory_human": "2.5M"
            }

            result = InstallService.detect_redis_custom_port(6380)

            assert result["detected"] is True
            assert result["version"] == "6.2.5"
            assert result["host"] == "localhost"
            assert result["port"] == 6380
            assert "6380" in result["message"]

    def test_detect_redis_custom_port_unavailable(self):
        """Test detecting Redis on custom port when unavailable"""
        with patch('redis.Redis') as mock_redis:
            # Mock connection failure
            mock_redis.return_value.ping.side_effect = Exception("Connection timeout")

            result = InstallService.detect_redis_custom_port(6381)

            assert result["detected"] is False
            assert result["version"] is None
            assert result["port"] == 6381
            assert "6381" in result["message"]

    def test_detect_redis_import_error(self):
        """Test detecting Redis when redis module not installed"""
        with patch('redis.Redis', side_effect=ImportError("No module named 'redis'")):
            result = InstallService.detect_redis_standard()

            assert result["detected"] is False
            assert "Redis" in result["message"]

    def test_detect_redis_timeout(self):
        """Test detecting Redis with connection timeout"""
        with patch('redis.Redis') as mock_redis:
            # Mock timeout
            mock_redis.return_value.ping.side_effect = TimeoutError("Connection timeout")

            result = InstallService.detect_redis_standard()

            assert result["detected"] is False
            assert "Redis" in result["message"]


class TestWizardRedisIntegration:
    """Test Redis detection integration with wizard"""

    def test_wizard_requirements_step_redis_available(self, client):
        """Test requirements step when Redis is available"""
        with patch.object(InstallService, 'detect_redis_standard') as mock_detect:
            mock_detect.return_value = {
                "detected": True,
                "version": "7.0.0",
                "host": "localhost",
                "port": 6379,
                "message": "Redis détecté"
            }

            response = client.post(
                "/install/step",
                data={"step": "requirements"}
            )

            # Should return 200 with the page containing redis info
            assert response.status_code == 200
            # Check that redis detection is in response
            assert b"redis" in response.data.lower() or b"7.0.0" in response.data

    def test_wizard_requirements_step_redis_unavailable(self, client):
        """Test requirements step when Redis is unavailable"""
        with patch.object(InstallService, 'detect_redis_standard') as mock_detect:
            mock_detect.return_value = {
                "detected": False,
                "version": None,
                "host": None,
                "port": None,
                "message": "Redis non détecté"
            }

            response = client.post(
                "/install/step",
                data={"step": "requirements"}
            )

            # Should return 200 with the page
            assert response.status_code == 200

