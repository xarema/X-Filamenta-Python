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

    # ---- Cache & Sessions ----
    # Initialize cache service (auto-detects Redis/Filesystem/Memory)
    from backend.src.services.cache_service import CacheBackend, cache_service

    # Configure Flask-Session based on cache backend
    if cache_service.backend == CacheBackend.REDIS:
        # Use Redis for sessions (distributed, persistent)
        app.config["SESSION_TYPE"] = "redis"
        app.config["SESSION_REDIS"] = cache_service.client.redis
        app.logger.info("Sessions: Using Redis backend")
    elif cache_service.backend == CacheBackend.FILESYSTEM:
        # Use Filesystem for sessions (cPanel compatible)
        app.config["SESSION_TYPE"] = "filesystem"
        # Use Flask's instance_path to ensure correct path resolution
        session_dir = os.path.join(app.instance_path, "sessions")
        app.config["SESSION_FILE_DIR"] = session_dir
        # Create directory if it doesn't exist
        os.makedirs(session_dir, exist_ok=True)
        app.logger.info(f"Sessions: Using Filesystem backend at {session_dir}")
    else:
        # Fallback to default Flask sessions (memory, not persistent)
        app.config["SESSION_TYPE"] = "null"
        app.logger.warning("Sessions: Using Memory backend (not persistent!)")

    # Common session config
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_KEY_PREFIX"] = "xf:"
    app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24 hours

    # Cookie security settings
    app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in HTTPS only
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JS access
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection
    app.config["SESSION_COOKIE_PATH"] = "/"  # Ensure cookie is sent to all paths
    # Note: Don't set DOMAIN for localhost/development

    # Initialize Flask-Session
    from flask_session import Session

    Session(app)

    # ---- Compression ----
    # Enable Gzip compression for responses
    from flask_compress import Compress

    Compress(app)

    # ---- Assets (CSS/JS bundling) ----
    # Bundle and minify CSS/JS in production
    if not app.config.get("TESTING"):
        from backend.src.assets import init_assets

        init_assets(app)

    # ---- Rate Limiting ----
    from backend.src.services.rate_limiter import limiter

    limiter.init_app(app)

    # ---- Security Middleware ----
    # Add HTTP security headers to all responses
    from backend.src.middleware import add_cache_headers

    app.after_request(add_security_headers)
    app.after_request(add_cache_headers)

    # ---- Logging ----
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # ---- Blueprints Registration ----
    from backend.src.routes.admin import admin
    from backend.src.routes.admin_cache import admin_cache
    from backend.src.routes.admin_i18n import admin_i18n
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
    app.register_blueprint(admin_cache)
    app.register_blueprint(admin_i18n)
    app.register_blueprint(install)
    app.register_blueprint(lang_bp)
    # ---- Flask-Login Configuration ----
    from flask_login import LoginManager, current_user

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"  # Match the GET handler function name
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id: int) -> Any:
        """Load user by ID for Flask-Login"""
        from backend.src.models.user import User
        return User.query.get(int(user_id))

    # ---- Translations (i18n) ----
    from backend.src.utils.i18n import init_translations, t

    init_translations(project_root)

    # Make t() available in all templates
    @app.context_processor
    def inject_translation_function() -> dict[str, object]:
        return {"t": t}

    # Inject current language and auto-detect it
    @app.context_processor
    def inject_language() -> dict[str, object]:
        from backend.src.utils.i18n import _translations
        from flask import session
        import logging

        logger = logging.getLogger(__name__)

        # Déterminer la langue (ordre de priorité: session → navigateur → défaut)
        lang = session.get("lang")

        if not lang and _translations:
            # Détecte depuis le navigateur si pas en session
            lang = _translations.detect_browser_language()
            logger.info(f"Language detected from browser: {lang}")
            # Sauvegarde dans la session
            session["lang"] = lang
            session.modified = True

        logger.debug(f"Context language: {lang}")
        return {"lang": lang or "en"}

    # Inject all translations (full dictionary for fallback rendering)
    @app.context_processor
    def inject_translations() -> dict[str, object]:
        from backend.src.utils.i18n import _translations
        from flask import session

        lang = session.get("lang", "en")
        translations_dict = {}

        if _translations and hasattr(_translations, 'translations'):
            # Try requested language first
            translations_dict = _translations.translations.get(lang, {})

            # Fallback to English if language not found
            if not translations_dict:
                translations_dict = _translations.translations.get("en", {})

            # Double fallback: return empty dict wrapped in a safe structure
            # to prevent undefined errors in templates
            if not translations_dict:
                translations_dict = {"_empty": True}

        return {"translations": translations_dict if translations_dict else {"_empty": True}}


    # ---- Installation Guard ----
    # Cache installation status to prevent file I/O on every request
    # This avoids race conditions and redirect loops
    app._install_status_cache = {"installed": None, "timestamp": 0}  # type: ignore[attr-defined]
    INSTALL_CACHE_TTL = 5  # Refresh cache every 5 seconds

    @app.before_request
    def enforce_installation() -> Any:
        from flask import redirect, request, session
        import time

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
            "/login",
            "/logout",
            "/register",
            "/auth",
        )
        if any(request.path.startswith(p) for p in allowed_prefixes):
            return None

        from backend.src.services.install_service import InstallService

        # Check cache first (avoid filesystem I/O on every request)
        cache = app._install_status_cache  # type: ignore[attr-defined]
        current_time = time.time()

        # Use cache if it exists and is fresh
        if (cache["installed"] is not None and
            current_time - cache["timestamp"] < INSTALL_CACHE_TTL):
            is_installed = cache["installed"]
            app.logger.debug(f"Installation status (cached): {is_installed}")
        else:
            # Refresh from filesystem
            is_installed = InstallService.is_installed(project_root)
            cache["installed"] = is_installed
            cache["timestamp"] = current_time
            app.logger.debug(f"Installation status (from file): {is_installed}")

        if not is_installed:
            # ANTI-REDIRECT-LOOP: Track redirect count
            redirect_count = int(request.headers.get("X-Redirect-Count", 0))
            if redirect_count >= 3:
                app.logger.error(
                    f"CIRCULAR REDIRECT DETECTED: {request.path} (count={redirect_count})"
                )
                # Break the loop by returning 503 Service Unavailable
                return "Installation in progress", 503

            app.logger.info("Redirecting to installation page: %s", request.path)
            response = redirect("/install/")
            # Increment redirect counter in response header
            response.headers["X-Redirect-Count"] = str(redirect_count + 1)
            return response
        return None

    # ---- Context Processors ----
    @app.context_processor
    def inject_user() -> dict[str, object]:
        """Inject current_user into templates (Flask-Login)"""
        # current_user est déjà disponible via Flask-Login
        # On le passe explicitement pour compatibilité
        from flask_login import current_user
        return {"current_user": current_user}

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

    # ---- CLI Commands ----
    try:
        from backend.src.cli import admin

        admin.init_app(app)
    except ImportError:
        app.logger.warning("CLI commands not available")

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
    # Development runner (prefer using `run_prod.py` for production)
    # Debug mode controlled by FLASK_DEBUG environment variable
    app = create_app()
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
