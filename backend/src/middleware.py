"""
Purpose: Security middleware for Flask application
Description: Adds HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)

File: backend/src/middleware.py | Repository: X-Filamenta-Python
Created: 2025-12-28T18:05:00+01:00
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
- Flask after_request middleware for security headers
- Content-Security-Policy (XSS protection)
- X-Frame-Options (clickjacking protection)
- X-Content-Type-Options (MIME sniffing prevention)
- HSTS (force HTTPS in production)
"""

from flask import Response


def add_security_headers(response: Response) -> Response:
    """
    Add HTTP security headers to all responses.

    Implements defense-in-depth security headers:
    - Content-Security-Policy: Restrict resource loading origins
    - X-Frame-Options: Prevent clickjacking attacks
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-XSS-Protection: Legacy XSS protection for older browsers
    - Strict-Transport-Security: Force HTTPS (production only)

    Args:
        response: Flask Response object

    Returns:
        Response object with security headers added

    Note:
        This should be registered as app.after_request(add_security_headers)
        in the Flask application factory.
    """
    # Content-Security-Policy - Strict but allows Bootstrap/CDN resources
    # default-src 'self' = only allow same-origin resources by default
    # script-src = allow inline (needed for HTMX/Alpine) + CDNs (jsdelivr, unpkg, cloudflare)
    # style-src = allow inline Bootstrap + CDNs
    # img-src = allow data URLs + HTTPS
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net https://cdn.jsdelivr.net unpkg.com https://unpkg.com cdnjs.cloudflare.com https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net https://cdn.jsdelivr.net unpkg.com https://unpkg.com cdnjs.cloudflare.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https: blob:; "
        "font-src 'self' cdn.jsdelivr.net https://cdn.jsdelivr.net unpkg.com https://unpkg.com cdnjs.cloudflare.com https://cdnjs.cloudflare.com data:; "
        "connect-src 'self' https: wss:; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    # X-Frame-Options - Prevent clickjacking by not allowing iframe embedding
    response.headers["X-Frame-Options"] = "DENY"

    # X-Content-Type-Options - Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # X-XSS-Protection - Legacy XSS protection for older browsers
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Referrer-Policy - Control referrer information
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions-Policy - Control browser features (replaces Feature-Policy)
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), "
        "payment=(), usb=(), magnetometer=(), gyroscope=()"
    )

    # Strict-Transport-Security (HSTS) - Force HTTPS
    # Only add when HTTPS is actually used (avoid localhost dev issues)
    from flask import current_app, request

    if current_app.config.get("PREFERRED_URL_SCHEME") == "https" and request.is_secure:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    return response


def add_cache_headers(response: Response) -> Response:
    """
    Add cache headers for static assets optimization.

    Sets appropriate cache headers based on content type:
    - Static assets (CSS/JS/images): 1 year cache (immutable)
    - Generated bundles (/gen/): 1 year cache (hash in filename)
    - HTML: no-cache (always validate)
    - API responses: no-store (never cache)

    Args:
        response: Flask Response object

    Returns:
        Response: Modified response with cache headers
    """
    from flask import request

    path = request.path

    # Static assets: long cache (1 year)
    if path.startswith("/static/"):
        # CSS, JS, images, fonts with extensions
        if (
            any(
                path.endswith(ext)
                for ext in [
                    ".css",
                    ".js",
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".svg",
                    ".woff",
                    ".woff2",
                    ".ttf",
                    ".eot",
                    ".ico",
                ]
            )
            or "/gen/" in path
        ):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            # Other static files: 1 hour cache
            response.headers["Cache-Control"] = "public, max-age=3600"

    # API responses: no cache
    elif path.startswith("/api/"):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    # HTML pages: validate with server
    elif response.content_type and "text/html" in response.content_type:
        response.headers["Cache-Control"] = "no-cache, must-revalidate"

    return response
