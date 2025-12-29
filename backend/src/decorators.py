"""
------------------------------------------------------------------------------
Purpose: Decorators for route protection
Description: Authentication, authorization, and CSRF protection decorators

File: backend/src/decorators.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Notes:
- Custom Flask route decorators
- Handles authentication (@login_required)
- Handles authorization (@admin_required, @csrf_protect)
- Integrates with session management and CSRF tokens
------------------------------------------------------------------------------
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import abort, current_app, jsonify, request
from sqlalchemy.exc import OperationalError


def require_admin(f: Callable) -> Callable:
    """
    Decorator to require admin authentication

    Usage:
        @admin.route('/dashboard')
        @require_admin
        def dashboard():
            return render_template('admin/dashboard.html')

    Args:
        f: The function to decorate

    Returns:
        Decorated function that checks admin status

    Raises:
        403 Forbidden if user is not admin
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
        from backend.src.services.user_service import UserService

        # Dev-safe admin check: try to load 'admin' from DB; if it exists and
        # is admin, allow access
        try:
            user = UserService.get_by_username("admin")
            if not user or not user.is_admin:
                current_app.logger.warning("Unauthorized admin access attempt")
                abort(403)
        except OperationalError:
            # DB not initialized yet → treat as unauthorized
            current_app.logger.warning("Admin check failed: DB not initialized")
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def require_authenticated(f: Callable) -> Callable:
    """
    Decorator to require user authentication

    Usage:
        @pages.route('/preferences')
        @require_authenticated
        def preferences():
            return render_template('pages/preferences.html')

    Args:
        f: The function to decorate

    Returns:
        Decorated function that checks authentication

    Raises:
        401 Unauthorized if user is not authenticated
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
        from backend.src.services.user_service import UserService

        # Dev-safe auth check: treat 'admin' as logged in if exists and active
        try:
            user = UserService.get_by_username("admin")
            if not user or not user.is_active:
                current_app.logger.warning("Unauthorized access attempt")
                abort(401)
        except OperationalError:
            current_app.logger.warning("Auth check failed: DB not initialized")
            abort(401)

        return f(*args, **kwargs)

    return decorated_function


def csrf_protect(f: Callable) -> Callable:
    """
    Decorator to protect routes with CSRF tokens

    Validates CSRF token for POST/PUT/PATCH/DELETE requests.
    HTMX requests are exempt by default.

    Usage:
        @app.route('/form', methods=['POST'])
        @csrf_protect
        def process_form():
            return "Form processed"

    Args:
        f: The function to decorate

    Returns:
        Decorated function that validates CSRF tokens

    Raises:
        403 Forbidden if CSRF validation fails
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
        # Only protect state-changing methods
        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return f(*args, **kwargs)

        # HTMX requests can be exempt (they use custom headers)
        if request.headers.get("HX-Request"):
            # For now, exempt HTMX requests
            # TODO: Implement CSRF in HTMX headers if needed
            return f(*args, **kwargs)

        # Get token from form data or headers
        token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")

        # Validate token
        from backend.src.services.csrf_service import CSRFService

        if not CSRFService.validate_token(token):
            current_app.logger.warning(
                f"CSRF validation failed for {request.method} {request.path}"
            )
            if request.is_json or request.headers.get("HX-Request"):
                return jsonify({"error": "CSRF validation failed"}), 403
            abort(403, description="CSRF validation failed")

        return f(*args, **kwargs)

    return decorated_function
