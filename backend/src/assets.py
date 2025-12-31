"""
Purpose: Flask-Assets configuration for frontend optimization
Description: Bundle and minify CSS/JS assets for production

File: backend/src/assets.py | Repository: X-Filamenta-Python
Created: 2025-12-29T21:15:00+01:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- CSS/JS bundling and minification
- Cache busting via hashing
- Development vs Production modes
"""

from flask_assets import Bundle, Environment


def init_assets(app):
    """
    Initialize Flask-Assets with bundles.

    Creates:
    - CSS bundle (minified in production)
    - JS bundle (minified in production)
    - Cache busting via content hashing

    Args:
        app: Flask application instance
    """
    assets = Environment(app)

    # Configure assets
    assets.url = app.static_url_path
    assets.directory = app.static_folder

    # Debug mode: don't minify, easier debugging
    assets.debug = app.config.get("DEBUG", False)

    # Auto-build: rebuild when source files change
    assets.auto_build = True

    # Cache busting: append hash to filename
    assets.cache = not app.config.get("DEBUG", False)
    assets.manifest = "cache" if not app.config.get("DEBUG", False) else False

    # ---- CSS Bundle ----
    css_bundle = Bundle(
        "css/custom.css",  # Custom styles (if exists)
        filters="cssmin" if not app.config.get("DEBUG", False) else None,
        output="gen/packed.css",
    )

    # ---- JS Bundle ----
    js_bundle = Bundle(
        "js/main.js",  # Main JS (if exists)
        filters="jsmin" if not app.config.get("DEBUG", False) else None,
        output="gen/packed.js",
    )

    # Register bundles
    assets.register("css_all", css_bundle)
    assets.register("js_all", js_bundle)

    return assets
