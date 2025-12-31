"""
------------------------------------------------------------------------------
Purpose: Application configuration management
Description: Loads and provides configuration for different environments
             (development, testing, production). Supports multiple database
             backends (SQLite, MySQL, PostgreSQL) and deployment targets
             (cPanel, VPS, Docker).

File: backend/src/config.py | Repository: X-Filamenta-Python
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
- Load from environment variables when possible
- Supports SQLite, MySQL, PostgreSQL
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, env vars must be set manually


def _build_database_uri() -> str:
    """
    Build database URI based on environment variables.

    Supports:
    - SQLite (default for development)
    - MySQL: MySQL://user:password@host:port/dbname
    - PostgreSQL: postgresql://user:password@host:port/dbname

    Returns:
        str: Database URI string
    """
    # If explicit URI is set, use it
    if db_uri := os.getenv("SQLALCHEMY_DATABASE_URI"):
        return db_uri

    # Build from individual components
    db_type = os.getenv("DB_TYPE", "sqlite").lower()

    if db_type == "mysql":
        db_user = os.getenv("DB_USER", "filamenta")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "filamenta")

        if db_password:
            return (
                f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        return f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"

    elif db_type == "postgresql":
        db_user = os.getenv("DB_USER", "filamenta")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "filamenta")

        if db_password:
            return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"

    # Default: SQLite
    base_dir = Path(__file__).parent.parent.parent
    instance_dir = base_dir / "instance"
    instance_dir.mkdir(exist_ok=True)
    # Utiliser le même nom par défaut que le wizard
    db_path = instance_dir / "x-filamenta_python.db"
    return f"sqlite:///{db_path}"


class Config:
    """
    Base configuration for all environments.

    This class defines common settings used across development, testing,
    and production environments. Environment-specific classes (DevelopmentConfig,
    TestingConfig, ProductionConfig) inherit from this base.

    Environment Variables:
        FLASK_SECRET_KEY: Secret key for session signing (REQUIRED in production)
        FLASK_DEBUG: Enable debug mode (default: False)
        FLASK_ENV: Environment name (development, testing, production)
        SQLALCHEMY_DATABASE_URI: Full database connection string
        DB_TYPE: Database type (sqlite, mysql, postgresql)
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME: DB connection params
        DEPLOYMENT_TARGET: Deployment platform (development, cpanel, vps, docker)
        PREFERRED_URL_SCHEME: URL scheme (http or https)
        SECURE_SSL_REDIRECT: Force HTTPS redirect (production only)

    Usage:
        # In app factory:
        from backend.src.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

        # Or from environment:
        config_class = os.getenv('FLASK_CONFIG', 'development')
        app.config.from_object(f'backend.src.config.{config_class}Config')

    Security Notes:
        - FLASK_SECRET_KEY is MANDATORY in production
        - Use SESSION_COOKIE_SECURE=True with HTTPS
        - Enable SECURE_SSL_REDIRECT in production
        - Never commit secrets to version control

    Database Configuration:
        Supports multiple backends via SQLALCHEMY_DATABASE_URI:
        - SQLite: sqlite:///path/to/db.db (default for development)
        - MySQL: mysql+pymysql://user:pass@host:port/dbname
        - PostgreSQL: postgresql://user:pass@host:port/dbname

        Or set individual DB_* environment variables and DB_TYPE.
    """

    # Project root
    BASE_DIR = Path(__file__).parent.parent.parent

    # Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    if not SECRET_KEY:
        if (
            os.getenv("FLASK_ENV") == "production"
            or os.getenv("DEPLOYMENT_TARGET") == "production"
        ):
            raise ValueError(
                "FLASK_SECRET_KEY required in production! "
                "Generate: python -c 'import secrets; "
                "print(secrets.token_hex(32))'"
            )
        # Dev default (NOT for production)
        SECRET_KEY = "dev-key-change-in-production-immediately"  # noqa: S105

    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    # Database
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() in (
        "true",
        "1",
        "yes",
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Verify connections before using
        "pool_recycle": 3600,  # Recycle connections after 1 hour
        "pool_size": 10,  # Number of connections to maintain
        "max_overflow": 20,  # Max additional connections when pool full
        "pool_timeout": 30,  # Timeout waiting for connection (seconds)
        "echo_pool": False,  # Don't log pool activity (perf)
    }

    # Flask-specific
    JSON_SORT_KEYS = False
    _url_scheme_env = os.getenv("PREFERRED_URL_SCHEME", "http")
    PREFERRED_URL_SCHEME = "https" if _url_scheme_env == "https" else "http"

    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Security headers (for production)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() in (
        "true",
        "1",
        "yes",
    )

    # Deployment-specific
    DEPLOYMENT_TARGET = os.getenv(
        "DEPLOYMENT_TARGET", "development"
    )  # development, cpanel, vps, docker


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    PREFERRED_URL_SCHEME = "http"
    SECURE_SSL_REDIRECT = False
    DEPLOYMENT_TARGET = "development"


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    DEPLOYMENT_TARGET = "testing"


class ProductionConfig(Config):
    """Production environment configuration (generic).

    Security Critical: This configuration enforces production-level constraints.
    All variables must be validated and hardened.
    """

    DEBUG = False
    SQLALCHEMY_ECHO = False
    DEPLOYMENT_TARGET = "production"

    # SECURITY: Force HTTPS in production
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # SECURITY: Strict session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"

    @staticmethod
    def validate_production_config() -> dict:
        """Validate that all required production variables are set.

        Returns:
            dict: Validation result with keys:
                - valid (bool): Whether config is valid
                - errors (list): List of error messages
                - warnings (list): List of warning messages
        """
        errors = []
        warnings = []

        # CRITICAL: Secret key
        secret_key = os.getenv("FLASK_SECRET_KEY")
        if not secret_key:
            errors.append("FLASK_SECRET_KEY not set")
        elif len(secret_key) < 32:
            errors.append(f"FLASK_SECRET_KEY too short ({len(secret_key)} chars, min 32)")
        elif secret_key == "dev-key-change-in-production-immediately":
            errors.append("FLASK_SECRET_KEY is still development default")

        # CRITICAL: Debug must be False
        debug_value = os.getenv("FLASK_DEBUG", "False").lower()
        if debug_value in ("true", "1", "yes"):
            errors.append("FLASK_DEBUG must be False in production")

        # CRITICAL: Environment
        flask_env = os.getenv("FLASK_ENV", "").lower()
        if flask_env != "production":
            errors.append(f"FLASK_ENV must be 'production', got '{flask_env}'")

        # CRITICAL: Database
        db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
        if not db_uri:
            db_type = os.getenv("DB_TYPE", "sqlite").lower()
            if db_type not in ("postgresql", "mysql"):
                warnings.append("Using SQLite - NOT recommended for production")
        elif "sqlite" in db_uri.lower():
            warnings.append("SQLite database detected - NOT recommended for production")

        # CRITICAL: Email config for verification
        smtp_server = os.getenv("SMTP_SERVER", "").strip()
        if not smtp_server or "example.com" in smtp_server:
            warnings.append("SMTP_SERVER not properly configured for email features")

        # CRITICAL: HTTPS
        url_scheme = os.getenv("PREFERRED_URL_SCHEME", "http")
        if url_scheme != "https":
            warnings.append("PREFERRED_URL_SCHEME should be 'https' in production")

        # SECURITY: Session cookies
        secure_cookies = os.getenv("SESSION_COOKIE_SECURE", "true").lower()
        if secure_cookies not in ("true", "1", "yes"):
            errors.append("SESSION_COOKIE_SECURE must be True in production")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


class CPanelConfig(ProductionConfig):
    """cPanel-specific configuration."""

    DEPLOYMENT_TARGET = "cpanel"
    # cPanel typically runs under public_html
    # Application subpath set via environment
    APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "/filamenta")


class VPSConfig(ProductionConfig):
    """VPS/Linux-specific configuration."""

    DEPLOYMENT_TARGET = "vps"


class DockerConfig(ProductionConfig):
    """Docker-specific configuration."""

    DEPLOYMENT_TARGET = "docker"


def get_config(env: str | None = None) -> Config:
    """
    Get configuration object based on environment.

    Args:
        env: Environment name or deployment target
             (development, testing, production, cpanel, vps, docker).
             Defaults to FLASK_ENV environment variable or 'development'.

    Returns:
        Config: Configuration object for the specified environment.

    Raises:
        ValueError: If production config is invalid
    """
    env = env or os.getenv("FLASK_ENV", "development").lower()

    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
        "cpanel": CPanelConfig,
        "vps": VPSConfig,
        "docker": DockerConfig,
    }

    config_class = configs.get(env, DevelopmentConfig)
    config = config_class()

    # Validate production config
    if env in ("production", "cpanel", "vps", "docker"):
        # Call static method for validation (mypy requires explicit annotation)
        ProductionConfig.validate_production_config()

    return config
