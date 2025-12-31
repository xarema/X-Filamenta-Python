"""
------------------------------------------------------------------------------
Purpose: Backend source package initialization
Description: Marks this directory as a Python package and provides package-level
             documentation for the X-Filamenta-Python backend application.

File: backend/src/__init__.py | Repository: X-Filamenta-Python
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

Package Structure:
------------------
backend/src/
├── app.py              # Application factory (create_app())
├── config.py           # Configuration classes (Dev, Test, Prod)
├── extensions.py       # Flask extensions registry (db, etc.)
├── middleware.py       # WSGI middleware (logging, security headers)
├── decorators.py       # Custom decorators (login_required, admin_required)
├── assets.py           # Static assets management
├── models/             # SQLAlchemy ORM models
│   ├── user.py         # User model with authentication
│   ├── content.py      # Content/post model
│   └── settings.py     # Application settings model
├── routes/             # Flask blueprints for routes
│   ├── main.py         # Main/public routes
│   ├── auth.py         # Authentication routes
│   ├── admin.py        # Admin panel routes
│   ├── install.py      # Installation wizard routes
│   └── pages.py        # Static pages routes
├── services/           # Business logic layer
│   ├── user_service.py         # User management
│   ├── email_service.py        # Email sending
│   ├── install_service.py      # Installation logic
│   └── cache_service.py        # Caching (Redis/Filesystem)
├── i18n/               # Internationalization
│   └── translations/   # Language files (en.json, fr.json)
└── utils/              # Helper functions
    ├── validation.py   # Input validation
    ├── security.py     # Security helpers (hashing, tokens)
    └── formatters.py   # Data formatters

Usage:
------
The application entry point is app.py:create_app().

    from backend.src.app import create_app

    app = create_app()  # Creates Flask app with all extensions

For production deployment:

    from backend.wsgi import app  # Pre-created app instance

Importing components:

    from backend.src.extensions import db
    from backend.src.models.user import User
    from backend.src.services.user_service import UserService

Architecture:
-------------
This backend follows a layered architecture:

1. Routes (blueprints): Handle HTTP requests/responses
2. Services: Business logic and orchestration
3. Models: Data access layer (ORM)
4. Utils: Reusable helper functions

Features:
---------
- Multi-database support (SQLite, MySQL, PostgreSQL)
- Multi-deployment (cPanel, VPS, Docker, local dev)
- Internationalization (i18n) with EN/FR support
- Email verification and password reset
- 2FA/TOTP authentication
- Admin panel with user management
- Installation wizard for first-time setup
- Cache layer (Redis or Filesystem fallback)
- Rate limiting and CSRF protection
- Security headers and input validation

Testing:
--------
Tests are located in backend/tests/:

    pytest backend/tests/                    # Run all tests
    pytest backend/tests/test_auth.py        # Run auth tests
    pytest --cov=backend/src                 # With coverage

For more information, see docs/ directory.

Notes:
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

from .app import create_app
from .extensions import db
