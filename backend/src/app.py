"""
------------------------------------------------------------------------------
Purpose: Flask application factory
Description: Creates and configures the Flask application instance with
             routes and configuration.

File: backend/src/app.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

import logging
import os
from typing import Any

from flask import Flask

from backend.src.extensions import db
from backend.src.middleware import add_security_headers

# ---- Database initialization ----
# db = SQLAlchemy()  # moved to extensions


def create_app(config: object | None = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config: Configuration object (optional). If not provided, configuration
                is loaded from environment variables.

    Returns:
        Flask: Configured application instance with routes and error handlers.

    Notes:
        - Reads configuration from environment variables with FLASK_ prefix
        - Sets up basic logging at INFO level
        - Registers blueprints for routes
        - Initializes SQLAlchemy database
        - Configures templates and static folders
    """
    # Configure template and static folders
    project_root = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    template_folder = os.path.abspath(
        os.path.join(project_root, "frontend", "templates")
    )
    static_folder = os.path.abspath(os.path.join(project_root, "frontend", "static"))

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
        static_url_path="/static",
    )

    # ---- Configuration ----
    if config is None:
        from backend.src.config import get_config

        config = get_config()

    app.config.from_object(config)

    # Database initialization
    db.init_app(app)

    # ---- Models Registration ----
    # Import models so SQLAlchemy knows about them
    from backend.src.models.user import User
    from backend.src.models.settings import Settings
    from backend.src.models.preferences import UserPreferences
    from backend.src.models.content import Content
    from backend.src.models.admin_history import AdminHistory

    # ---- Rate Limiting ----
    from backend.src.services.rate_limiter import limiter

    limiter.init_app(app)

    # ---- Security Middleware ----
    # Add HTTP security headers to all responses
    app.after_request(add_security_headers)

    # ---- Logging ----
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # ---- Blueprints Registration ----
    from backend.src.routes.admin import admin
    from backend.src.routes.admin_users import admin_users
    from backend.src.routes.api import api
    from backend.src.routes.auth import auth
    from backend.src.routes.auth_2fa import auth_2fa
    from backend.src.routes.install import install
    from backend.src.routes.lang import lang_bp
    from backend.src.routes.main import main
    from backend.src.routes.pages import pages

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(pages)
    app.register_blueprint(auth)
    app.register_blueprint(auth_2fa)
    app.register_blueprint(admin)
    app.register_blueprint(admin_users)
    app.register_blueprint(install)
    app.register_blueprint(lang_bp)

    # ---- Translations (i18n) ----
    from backend.src.utils.i18n import init_translations, t

    init_translations(project_root)

    # Make t() available in all templates
    @app.context_processor
    def inject_translation_function() -> dict[str, object]:
        return dict(t=t)

    # ---- Installation Guard ----
    @app.before_request
    def enforce_installation() -> Any:
        from flask import redirect, request

        if app.config.get("TESTING") or os.environ.get("PYTEST_CURRENT_TEST"):
            return None

        allowed_prefixes = (
            "/install",
            "/static",
            "/api",
            "/errors",
            "/legal",
            "/lang",
            "/favicon.ico",
        )
        if any(request.path.startswith(p) for p in allowed_prefixes):
            return None

        from backend.src.services.install_service import InstallService

        if not InstallService.is_installed(project_root):
            app.logger.info("Redirecting to installation page: %s", request.path)
            return redirect("/install/")
        return None

    # ---- Context Processors ----
    @app.context_processor
    def inject_user() -> dict[str, object]:
        """Inject current_user into templates (mock for now)"""

        class MockUser:
            username = "Guest"
            is_authenticated = False
            is_admin = False

        return {"current_user": MockUser()}

    @app.context_processor
    def inject_csrf_token() -> dict[str, object]:
        """
        Inject csrf_token function.
        Flask-WTF provides this, but provide fallback for tests.
        """
        try:
            from flask_wtf.csrf import generate_csrf  # type: ignore[import-untyped]
        except ModuleNotFoundError:

            def generate_csrf() -> str:
                return "test-csrf-token"

        return {"csrf_token": generate_csrf}

    # ---- Error Handlers ----
    from flask import render_template, request

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple[str, int]:
        """Handle 404 errors"""
        app.logger.warning(f"404 Not Found: {request.method} {request.path}")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error: Exception) -> tuple[str, int]:
        """Handle 500 errors"""
        app.logger.error(f"500 Server Error: {error}", exc_info=True)
        return render_template("errors/500.html"), 500

    return app


if __name__ == "__main__":
    # Tiny dev runner (prefer using `python -m backend.src` instead)
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
