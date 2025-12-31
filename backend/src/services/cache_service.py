"""
Purpose: Cache Service with multi-backend support
Description: Auto-detecting cache backend with fallback

File: backend/src/services/cache_service.py | Repository: X-Filamenta-Python
Created: 2025-12-29T18:45:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Multi-backend cache service (Redis, Filesystem, Memory)
- Auto-detection with fallback strategy
- Support for both standard and advanced connection tests
"""

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# ---- Backend Detection & Selection ----


class CacheBackend(str, Enum):
    """Supported cache backends"""

    REDIS = "redis"
    FILESYSTEM = "filesystem"
    MEMORY = "memory"


class CacheService:
    """
    Cache service with automatic backend detection and fallback strategy.

    Priority:
    1. Redis (if available)
    2. Filesystem (if writable)
    3. Memory (fallback)
    """

    def __init__(self):
        """Initialize cache service with auto-detection"""
        self.logger = logging.getLogger(__name__)
        self.backend = self._detect_backend()
        self.client = self._init_client()
        self.logger.info(f"Cache backend initialized: {self.backend.value}")

    # ---- Backend Detection ----

    def _detect_backend(self) -> CacheBackend:
        """
        Auto-detect best cache backend available.

        Priority:
        1. Redis available? → REDIS
        2. Filesystem writable? → FILESYSTEM
        3. Fallback → MEMORY

        Returns:
            CacheBackend enum value
        """
        # Try Redis first
        if self._redis_available():
            self.logger.debug("Redis detected, using Redis backend")
            return CacheBackend.REDIS

        # Fallback to Filesystem
        if self._filesystem_writable():
            self.logger.debug("Filesystem writable, using Filesystem backend")
            return CacheBackend.FILESYSTEM

        # Last resort: Memory
        self.logger.warning("Using Memory backend (not persistent!)")
        return CacheBackend.MEMORY

    def _redis_available(self) -> bool:
        """
        Check if Redis is available on localhost:6379.

        Returns:
            True if Redis responds to ping, False otherwise
        """
        try:
            import redis

            r = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True,
                socket_connect_timeout=2,
            )
            r.ping()
            return True
        except Exception as e:
            self.logger.debug(f"Redis not available: {str(e)}")
            return False

    def _filesystem_writable(self) -> bool:
        """
        Check if filesystem cache directory is writable.

        Returns:
            True if cache dir exists/writable, False otherwise
        """
        try:
            cache_dir = os.getenv("CACHE_DIR", "./cache")
            Path(cache_dir).mkdir(parents=True, exist_ok=True)

            # Test write
            test_file = Path(cache_dir) / ".test_write"
            test_file.write_text("test")
            test_file.unlink()

            return True
        except Exception as e:
            self.logger.debug(f"Filesystem not writable: {str(e)}")
            return False

    # ---- Client Initialization ----

    def _init_client(self) -> Any:
        """
        Initialize cache client based on detected backend.

        Returns:
            Cache client (RedisCache, FilesystemCache, or MemoryCache)
        """
        if self.backend == CacheBackend.REDIS:
            return RedisCache()
        elif self.backend == CacheBackend.FILESYSTEM:
            return FilesystemCache()
        else:
            return MemoryCache()

    # ---- Public Cache API ----

    def get(self, key: str) -> Any | None:
        """Get value from cache"""
        return self.client.get(key)

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL"""
        self.client.set(key, value, ttl)

    def delete(self, key: str) -> None:
        """Delete key from cache"""
        self.client.delete(key)

    def flush(self) -> None:
        """Clear all cache"""
        self.client.flush()

    def get_info(self) -> dict[str, Any]:
        """Get cache backend info"""
        return {"backend": self.backend.value, "info": self.client.get_info()}

    # ---- Connection Testing ----

    def test_redis_connection(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str | None = None,
        db: int = 0,
    ) -> tuple[bool, str, dict | None]:
        """
        Test Redis connection (simple ping + info).

        Args:
            host: Redis host
            port: Redis port
            password: Redis password (optional)
            db: Redis database number

        Returns:
            Tuple: (success, message, info_dict or None)
        """
        try:
            import redis

            r = redis.Redis(
                host=host,
                port=port,
                password=password or None,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5,
            )

            # Test ping
            r.ping()

            # Get info
            info = r.info()

            return (
                True,
                "Redis connection successful",
                {
                    "version": info.get("redis_version", "unknown"),
                    "memory_used": info.get("used_memory_human", "0"),
                    "uptime_days": info.get("uptime_in_days", 0),
                    "connected_clients": info.get("connected_clients", 0),
                },
            )

        except Exception as e:
            return False, f"Connection error: {str(e)}", None

    def test_redis_advanced(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str | None = None,
        db: int = 0,
    ) -> tuple[bool, str, dict | None]:
        """
        Advanced Redis test (write + read operations).

        Tests actual permissions and performance.

        Args:
            host: Redis host
            port: Redis port
            password: Redis password (optional)
            db: Redis database number

        Returns:
            Tuple: (success, message, info_dict or None)
        """
        try:
            import redis

            r = redis.Redis(
                host=host,
                port=port,
                password=password or None,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5,
            )

            # Test write
            test_key = "_cache_test_write"
            test_value = f"test_{int(time.time())}"

            start = time.time()
            r.set(test_key, test_value, ex=10)
            write_time = (time.time() - start) * 1000  # ms

            # Test read
            start = time.time()
            result = r.get(test_key)
            read_time = (time.time() - start) * 1000  # ms

            # Cleanup
            r.delete(test_key)

            if result != test_value:
                return False, "Write/Read value mismatch", None

            return (
                True,
                "Advanced test successful",
                {
                    "write_time_ms": round(write_time, 2),
                    "read_time_ms": round(read_time, 2),
                    "permissions": "OK (read+write)",
                },
            )

        except Exception as e:
            return False, f"Advanced test error: {str(e)}", None


# ---- Redis Backend ----


class RedisCache:
    """Redis cache backend wrapper"""

    def __init__(self):
        """Initialize Redis connection"""
        import redis

        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None) or None,
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Any | None:
        """Get value from Redis"""
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            self.logger.error(f"Redis get error: {str(e)}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in Redis with TTL"""
        try:
            # Serialize SQLAlchemy models if needed
            serializable_value = value
            if hasattr(value, 'to_dict') and callable(value.to_dict):
                serializable_value = value.to_dict(include_email=True)

            # Try to serialize the value
            serialized = json.dumps(serializable_value)
            self.redis.setex(key, ttl, serialized)
        except (TypeError, ValueError) as e:
            # Ignore non-serializable objects (SQLAlchemy models, etc.)
            self.logger.debug(f"Skipping cache for non-serializable object: {type(value).__name__}")
        except Exception as e:
            self.logger.error(f"Redis set error: {str(e)}")

    def delete(self, key: str) -> None:
        """Delete key from Redis"""
        try:
            self.redis.delete(key)
        except Exception as e:
            self.logger.error(f"Redis delete error: {str(e)}")

    def flush(self) -> None:
        """Clear all keys in Redis database"""
        try:
            self.redis.flushdb()
        except Exception as e:
            self.logger.error(f"Redis flush error: {str(e)}")

    def get_info(self) -> dict[str, Any]:
        """Get Redis info"""
        try:
            info = self.redis.info()
            return {
                "type": "redis",
                "version": info.get("redis_version", "unknown"),
                "memory": info.get("used_memory_human", "0"),
                "keys": self.redis.dbsize(),
            }
        except Exception:
            return {"type": "redis", "error": "Unable to get info"}


# ---- Filesystem Backend ----


class FilesystemCache:
    """Filesystem cache backend (JSON files with TTL)"""

    def __init__(self):
        """Initialize filesystem cache directory"""
        self.cache_dir = Path(os.getenv("CACHE_DIR", "./cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Any | None:
        """Get value from filesystem cache"""
        try:
            file_path = self._key_to_path(key)
            if not file_path.exists():
                return None

            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            # Check expiry
            if data["expires_at"] < time.time():
                file_path.unlink()
                return None

            return data["value"]
        except Exception as e:
            self.logger.debug(f"Filesystem get error: {str(e)}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in filesystem cache with TTL"""
        try:
            # NEVER cache User objects - Flask-Session handles them
            from backend.src.models.user import User
            if isinstance(value, User):
                self.logger.debug(f"Skipping cache for User object (user_id={value.id})")
                return

            file_path = self._key_to_path(key)

            # Serialize SQLAlchemy models if needed
            serializable_value = value
            if hasattr(value, 'to_dict') and callable(value.to_dict):
                try:
                    serializable_value = value.to_dict(include_email=True)
                except TypeError:
                    # to_dict() doesn't accept parameters, try without
                    serializable_value = value.to_dict()
            elif hasattr(value, '__mapper__'):
                # SQLAlchemy mapped object without to_dict()
                try:
                    serializable_value = {c.name: getattr(value, c.name)
                                         for c in value.__mapper__.columns}
                except Exception:
                    # Can't serialize, skip cache
                    self.logger.debug(f"Skipping cache for non-serializable object (key={key})")
                    return

            data = {
                "value": serializable_value,
                "expires_at": time.time() + ttl,
                "created_at": datetime.now().isoformat(),
            }

            # Try to serialize - skip if not JSON serializable
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except (TypeError, ValueError) as e:
            # Log non-serializable values for debugging (don't error, just skip)
            self.logger.debug(f"Skipping cache for non-serializable value (key={key}, type={type(value).__name__}, error={str(e)})")
        except Exception as e:
            self.logger.debug(f"Filesystem set error (non-critical): {str(e)}")

    def delete(self, key: str) -> None:
        """Delete key from filesystem cache"""
        try:
            file_path = self._key_to_path(key)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            self.logger.error(f"Filesystem delete error: {str(e)}")

    def flush(self) -> None:
        """Clear all cache files"""
        try:
            for file_path in self.cache_dir.glob("*.json"):
                file_path.unlink()
        except Exception as e:
            self.logger.error(f"Filesystem flush error: {str(e)}")

    def get_info(self) -> dict[str, Any]:
        """Get filesystem cache info"""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in cache_files)

            return {
                "type": "filesystem",
                "directory": str(self.cache_dir),
                "entries": len(cache_files),
                "size_bytes": total_size,
            }
        except Exception:
            return {"type": "filesystem", "error": "Unable to get info"}

    def _key_to_path(self, key: str) -> Path:
        """Convert cache key to filesystem path"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"


# ---- Memory Backend ----


class MemoryCache:
    """In-memory cache backend (volatile, for dev/testing)"""

    def __init__(self):
        """Initialize memory cache"""
        self.cache: dict[str, dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Any | None:
        """Get value from memory cache"""
        if key not in self.cache:
            return None

        data = self.cache[key]

        # Check expiry
        if data["expires_at"] < time.time():
            del self.cache[key]
            return None

        return data["value"]

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in memory cache with TTL"""
        self.cache[key] = {"value": value, "expires_at": time.time() + ttl}

    def delete(self, key: str) -> None:
        """Delete key from memory cache"""
        if key in self.cache:
            del self.cache[key]

    def flush(self) -> None:
        """Clear all cache"""
        self.cache.clear()

    def get_info(self) -> dict[str, Any]:
        """Get memory cache info"""
        return {
            "type": "memory",
            "entries": len(self.cache),
            "warning": "Memory cache is volatile (not persistent)",
        }


# ---- Global Instance ----

# Initialize global cache service
cache_service = CacheService()
