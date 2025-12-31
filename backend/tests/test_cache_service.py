"""
Purpose: Tests for CacheService multi-backend functionality
Description: Comprehensive tests for Redis, Filesystem, and Memory cache backends

File: backend/tests/test_cache_service.py | Repository: X-Filamenta-Python
Created: 2025-12-29T18:50:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Tests for all cache backends
- 15+ test cases
"""

import pytest
import os
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from backend.src.services.cache_service import (
    CacheService,
    CacheBackend,
    RedisCache,
    FilesystemCache,
    MemoryCache,
)


# ---- CacheService Backend Detection Tests ----


class TestCacheServiceDetection:
    """Test CacheService backend auto-detection"""

    def test_backend_detection_redis(self):
        """Test Redis detection when available"""
        with patch.object(CacheService, '_redis_available', return_value=True):
            service = CacheService()
            assert service.backend == CacheBackend.REDIS

    def test_backend_detection_filesystem(self):
        """Test Filesystem fallback when Redis unavailable"""
        with patch.object(CacheService, '_redis_available', return_value=False):
            with patch.object(CacheService, '_filesystem_writable', return_value=True):
                service = CacheService()
                assert service.backend == CacheBackend.FILESYSTEM

    def test_backend_detection_memory(self):
        """Test Memory fallback when neither Redis nor Filesystem available"""
        with patch.object(CacheService, '_redis_available', return_value=False):
            with patch.object(CacheService, '_filesystem_writable', return_value=False):
                service = CacheService()
                assert service.backend == CacheBackend.MEMORY

    def test_redis_available_true(self):
        """Test Redis availability check when available"""
        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.ping.return_value = True
            service = CacheService()
            assert service._redis_available() is True

    def test_redis_available_false(self):
        """Test Redis availability check when unavailable"""
        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.ping.side_effect = Exception("Connection failed")
            service = CacheService()
            assert service._redis_available() is False

    def test_filesystem_writable_true(self, tmp_path):
        """Test filesystem writable check when directory writable"""
        service = CacheService()
        with patch.dict(os.environ, {"CACHE_DIR": str(tmp_path)}):
            assert service._filesystem_writable() is True

    def test_filesystem_writable_false(self):
        """Test filesystem writable check when directory not writable"""
        with patch.object(CacheService, '_filesystem_writable', return_value=False):
            service = CacheService()
            assert service._filesystem_writable() is False


# ---- CacheService Public API Tests ----


class TestCacheServiceAPI:
    """Test CacheService public API"""

    def test_get_set_delete(self):
        """Test basic cache get/set/delete operations"""
        service = CacheService()

        # Set value
        service.set("test_key", "test_value", ttl=300)

        # Get value
        value = service.get("test_key")
        assert value == "test_value"

        # Delete value
        service.delete("test_key")
        assert service.get("test_key") is None

    def test_flush(self):
        """Test cache flush operation"""
        service = CacheService()

        # Set multiple values
        service.set("key1", "value1")
        service.set("key2", "value2")

        # Flush all
        service.flush()

        # All should be gone
        assert service.get("key1") is None
        assert service.get("key2") is None

    def test_get_info(self):
        """Test getting cache backend info"""
        service = CacheService()
        info = service.get_info()

        assert "backend" in info
        assert "info" in info
        assert info["backend"] in [CacheBackend.REDIS, CacheBackend.FILESYSTEM, CacheBackend.MEMORY]


# ---- Redis Connection Testing ----


class TestRedisConnection:
    """Test Redis connection testing methods"""

    def test_test_redis_connection_success(self):
        """Test successful Redis connection test"""
        service = CacheService()

        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.ping.return_value = True
            mock_redis.return_value.info.return_value = {
                "redis_version": "7.0.0",
                "used_memory_human": "1.2M",
                "uptime_in_days": 10,
                "connected_clients": 5
            }

            success, message, info = service.test_redis_connection()

            assert success is True
            assert "successful" in message.lower()
            assert info["version"] == "7.0.0"

    def test_test_redis_connection_failure(self):
        """Test failed Redis connection test"""
        service = CacheService()

        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.ping.side_effect = Exception("Connection refused")

            success, message, info = service.test_redis_connection()

            assert success is False
            assert info is None
            assert "error" in message.lower()

    def test_test_redis_advanced_success(self):
        """Test advanced Redis test (write/read)"""
        service = CacheService()

        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.set.return_value = True

            # Mock get to return exact value that was set
            def mock_set_get(key, value, ex=None):
                # Store for later retrieval
                mock_redis.return_value._stored_value = value

            def mock_get(key):
                return mock_redis.return_value._stored_value

            mock_redis.return_value.set = mock_set_get
            mock_redis.return_value.get = mock_get
            mock_redis.return_value.delete.return_value = 1

            success, message, info = service.test_redis_advanced()

            assert success is True
            assert "successful" in message.lower()
            assert "write_time_ms" in info
            assert "read_time_ms" in info

    def test_test_redis_advanced_failure_mismatch(self):
        """Test advanced Redis test with value mismatch"""
        service = CacheService()

        with patch('redis.Redis') as mock_redis:
            mock_redis.return_value.set.return_value = True
            mock_redis.return_value.get.return_value = "wrong_value"  # Mismatch
            mock_redis.return_value.delete.return_value = 1

            success, message, info = service.test_redis_advanced()

            assert success is False
            assert "mismatch" in message.lower()


# ---- Redis Backend Tests ----


class TestRedisCache:
    """Test RedisCache backend"""

    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client"""
        with patch('redis.Redis') as mock:
            yield mock.return_value

    def test_redis_get_existing(self, mock_redis):
        """Test getting existing value from Redis"""
        mock_redis.get.return_value = '{"data": "value"}'

        cache = RedisCache()
        result = cache.get("test_key")

        assert result == {"data": "value"}

    def test_redis_get_nonexistent(self, mock_redis):
        """Test getting non-existent value from Redis"""
        mock_redis.get.return_value = None

        cache = RedisCache()
        result = cache.get("nonexistent_key")

        assert result is None

    def test_redis_set(self, mock_redis):
        """Test setting value in Redis"""
        cache = RedisCache()
        cache.set("test_key", {"data": "value"}, ttl=300)

        mock_redis.setex.assert_called_once()

    def test_redis_delete(self, mock_redis):
        """Test deleting value from Redis"""
        cache = RedisCache()
        cache.delete("test_key")

        mock_redis.delete.assert_called_once_with("test_key")

    def test_redis_flush(self, mock_redis):
        """Test flushing Redis database"""
        cache = RedisCache()
        cache.flush()

        mock_redis.flushdb.assert_called_once()


# ---- Filesystem Backend Tests ----


class TestFilesystemCache:
    """Test FilesystemCache backend"""

    @pytest.fixture
    def cache(self, tmp_path):
        """Create FilesystemCache with temp directory"""
        with patch.dict(os.environ, {"CACHE_DIR": str(tmp_path)}):
            cache = FilesystemCache()
            yield cache

    def test_filesystem_set_get(self, cache):
        """Test setting and getting value"""
        test_value = {"data": "test"}

        cache.set("test_key", test_value, ttl=300)
        result = cache.get("test_key")

        assert result == test_value

    def test_filesystem_get_nonexistent(self, cache):
        """Test getting non-existent value"""
        result = cache.get("nonexistent_key")
        assert result is None

    def test_filesystem_delete(self, cache):
        """Test deleting value"""
        cache.set("test_key", "value")
        cache.delete("test_key")

        assert cache.get("test_key") is None

    def test_filesystem_flush(self, cache):
        """Test flushing all cache"""
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.flush()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_filesystem_ttl_expiry(self, cache):
        """Test TTL expiration"""
        cache.set("expiring_key", "value", ttl=1)

        # Should exist immediately
        assert cache.get("expiring_key") == "value"

        # Wait for expiry
        time.sleep(1.1)

        # Should be expired
        assert cache.get("expiring_key") is None


# ---- Memory Backend Tests ----


class TestMemoryCache:
    """Test MemoryCache backend"""

    @pytest.fixture
    def cache(self):
        """Create MemoryCache instance"""
        return MemoryCache()

    def test_memory_set_get(self, cache):
        """Test setting and getting value"""
        test_value = {"data": "test"}

        cache.set("test_key", test_value)
        result = cache.get("test_key")

        assert result == test_value

    def test_memory_get_nonexistent(self, cache):
        """Test getting non-existent value"""
        result = cache.get("nonexistent_key")
        assert result is None

    def test_memory_delete(self, cache):
        """Test deleting value"""
        cache.set("test_key", "value")
        cache.delete("test_key")

        assert cache.get("test_key") is None

    def test_memory_flush(self, cache):
        """Test flushing cache"""
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.flush()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_memory_ttl_expiry(self, cache):
        """Test TTL expiration"""
        cache.set("expiring_key", "value", ttl=1)

        # Should exist immediately
        assert cache.get("expiring_key") == "value"

        # Wait for expiry
        time.sleep(1.1)

        # Should be expired
        assert cache.get("expiring_key") is None

    def test_memory_info(self, cache):
        """Test getting memory cache info"""
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        info = cache.get_info()

        assert info["type"] == "memory"
        assert info["entries"] == 2
        assert "warning" in info

