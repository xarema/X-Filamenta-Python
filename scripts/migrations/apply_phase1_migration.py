#!/usr/bin/env python
"""
Purpose: Apply database migrations for Phase 1
Description: Script to initialize Settings model and apply migrations

File: scripts/migrations/apply_phase1_migration.py | Repository: X-Filamenta-Python
Created: 2025-12-29T03:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Apply Settings model migration and initialize defaults
"""

import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.src.app import create_app
from backend.src.extensions import db
from backend.src.models.settings import Settings


def apply_migration():
    """Apply Phase 1 migration - create Settings table and defaults."""
    app = create_app()

    with app.app_context():
        print("Starting Phase 1 migration...")
        print()

        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("  Tables created successfully")
        print()

        # Initialize default settings
        print("Initializing default settings...")
        Settings.init_defaults()
        print("  Default settings initialized:")

        settings = Settings.query.all()
        for setting in settings:
            print(f"    - {setting.key}")

        print()
        print("Phase 1 migration completed successfully!")
        print()
        print("Summary:")
        print(f"  Total settings: {len(settings)}")
        print(f"  Encrypted fields: {len(Settings.ENCRYPTED_FIELDS)}")
        print()


if __name__ == "__main__":
    apply_migration()

