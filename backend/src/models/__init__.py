"""
------------------------------------------------------------------------------
Purpose: Database configuration and initialization
Description: Provides database setup, models, and session management for
             SQLAlchemy ORM integration with Flask.

File: backend/src/models/__init__.py | Repository: X-Filamenta-Python
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
- Import and register blueprints here
------------------------------------------------------------------------------
"""

# Import all models for SQLAlchemy registration
from backend.src.models.content import Content
from backend.src.models.preferences import UserPreferences
from backend.src.models.user import User

__all__ = ["User", "UserPreferences", "Content"]
