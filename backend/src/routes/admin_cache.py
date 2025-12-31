"""
Purpose: Admin cache management routes
Description: Admin interface for cache configuration and monitoring

File: backend/src/routes/admin_cache.py | Repository: X-Filamenta-Python
Created: 2025-12-29T20:15:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Admin cache configuration interface
- Cache statistics and monitoring
- Cache clearing operations
"""

from flask import Blueprint, jsonify, render_template, request, session

from backend.src.decorators import require_admin
from backend.src.services.cache_service import CacheService

admin_cache = Blueprint("admin_cache", __name__, url_prefix="/admin/cache")


@admin_cache.route("/", methods=["GET"])
@require_admin
def cache_settings():
    """
    Display cache settings page.

    Shows:
    - Current cache backend
    - Configuration options
    - Statistics
    - Actions (clear cache, test connection)
    """
    cache_svc = CacheService()

    # Get cache info
    info = cache_svc.get_info()
    backend = cache_svc.backend.value

    # Get current configuration (from wizard state or defaults)
    from backend.src.services.install_service import InstallService

    wizard_state = InstallService.get_wizard_state(session)

    config = {
        "backend": wizard_state.get("cache_backend", backend),
        "redis_host": wizard_state.get("redis_host", "localhost"),
        "redis_port": wizard_state.get("redis_port", "6379"),
        "redis_password": wizard_state.get("redis_password", ""),
        "redis_db": wizard_state.get("redis_db", "0"),
    }

    return render_template(
        "admin/cache.html", backend=backend, info=info, config=config
    )


@admin_cache.route("/test-redis", methods=["POST"])
@require_admin
def test_redis():
    """
    Test Redis connection (AJAX endpoint).

    Expected JSON:
        {
            "host": "localhost",
            "port": 6379,
            "password": "secret",
            "db": 0
        }

    Returns:
        JSON with success status and info
    """
    data = request.get_json()

    cache_svc = CacheService()
    success, message, info = cache_svc.test_redis_connection(
        host=data.get("host", "localhost"),
        port=int(data.get("port", 6379)),
        password=data.get("password") or None,
        db=int(data.get("db", 0)),
    )

    if success:
        return jsonify({"success": True, "message": message, "info": info})
    else:
        return jsonify({"success": False, "message": message}), 200


@admin_cache.route("/test-advanced", methods=["POST"])
@require_admin
def test_redis_advanced():
    """
    Test Redis connection with write/read (AJAX endpoint).

    Returns:
        JSON with advanced test results
    """
    data = request.get_json()

    cache_svc = CacheService()
    success, message, info = cache_svc.test_redis_advanced(
        host=data.get("host", "localhost"),
        port=int(data.get("port", 6379)),
        password=data.get("password") or None,
        db=int(data.get("db", 0)),
    )

    if success:
        return jsonify({"success": True, "message": message, "info": info})
    else:
        return jsonify({"success": False, "message": message}), 200


@admin_cache.route("/clear", methods=["POST"])
@require_admin
def clear_cache():
    """
    Clear all cache (AJAX endpoint).

    Returns:
        JSON with success status
    """
    try:
        cache_svc = CacheService()
        cache_svc.flush()

        return jsonify({"success": True, "message": "Cache cleared successfully"})
    except Exception as e:
        return jsonify(
            {"success": False, "message": f"Error clearing cache: {str(e)}"}
        ), 500


@admin_cache.route("/stats", methods=["GET"])
@require_admin
def cache_stats():
    """
    Get cache statistics (AJAX endpoint).

    Returns:
        JSON with cache stats
    """
    cache_svc = CacheService()
    info = cache_svc.get_info()

    return jsonify({"success": True, "backend": cache_svc.backend.value, "info": info})
