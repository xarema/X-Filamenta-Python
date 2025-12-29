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

# Global SQLAlchemy instance to be initialized in app factory
# Import this as `from backend.src.extensions import db`

db = SQLAlchemy()
