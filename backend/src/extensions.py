"""
------------------------------------------------------------------------------
Purpose: Flask extensions registry
Description: Centralizes extension instances (SQLAlchemy) for import across app.

File: backend/src/extensions.py | Repository: X-Filamenta-Python
Created: 2025-12-27T12:50:00+00:00
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
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

from flask_sqlalchemy import SQLAlchemy

# ---- Flask Extensions Registry ----
#
# This module centralizes all Flask extension instances to avoid circular imports.
# Extensions are created here as uninitialized instances and initialized later
# in the application factory (app.py) using the init_app() pattern.
#
# Usage:
#   from backend.src.extensions import db
#
#   # In models:
#   class User(db.Model):
#       ...
#
#   # In app factory:
#   db.init_app(app)
#
# Available Extensions:
#   - db: SQLAlchemy ORM instance for database operations
#
# Future Extensions (to be added):
#   - mail: Flask-Mail for email sending
#   - migrate: Flask-Migrate for database migrations
#   - login_manager: Flask-Login for user session management
#   - babel: Flask-Babel for internationalization
# ---- End Documentation ----


# SQLAlchemy Database Extension
# ------------------------------
# Global SQLAlchemy instance providing ORM functionality.
# Initialized in app factory with db.init_app(app).
#
# Configuration:
#   - SQLALCHEMY_DATABASE_URI: Database connection string (from config.py)
#   - SQLALCHEMY_TRACK_MODIFICATIONS: Disabled for performance
#   - SQLALCHEMY_ENGINE_OPTIONS: Pool size, timeouts, etc.
#
# Models:
#   Define models by extending db.Model:
#
#   class MyModel(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#       name = db.Column(db.String(100))
#
db = SQLAlchemy()
