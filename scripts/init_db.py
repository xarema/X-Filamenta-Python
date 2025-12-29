#!/usr/bin/env python
"""
------------------------------------------------------------------------------
Purpose: Database initialization and migration script
Description: Initialize database, create tables, and run migrations for
             X-Filamenta-Python on any platform.

File: scripts/init_db.py | Repository: X-Filamenta-Python
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
- Run with: python scripts/init_db.py
- Usage: python scripts/init_db.py [command]
  - init: Initialize database and create tables
  - reset: Reset database (drop and recreate)
  - drop: Drop all tables
  - create: Create tables only
  - seed: Create sample data (if available)
------------------------------------------------------------------------------
"""

import os
import sys
from pathlib import Path

from backend.src.app import create_app, db
from backend.src.config import get_config

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def init_database(app):
    """Initialize the database and create all tables."""
    with app.app_context():
        try:
            print("📊 Initializing database...")
            print(f"   Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

            # Create all tables
            db.create_all()
            print("✅ Database initialized successfully!")
            print("   All tables created.")

            return True
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False


def reset_database(app):
    """Reset database by dropping and recreating all tables."""
    with app.app_context():
        try:
            print("⚠️  Resetting database...")
            print("   Dropping all tables...")
            db.drop_all()

            print("   Creating tables...")
            db.create_all()

            print("✅ Database reset successfully!")
            return True
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            return False


def drop_database(app):
    """Drop all tables from the database."""
    with app.app_context():
        try:
            print("⚠️  Dropping all tables...")
            confirmation = input("Are you sure? Type 'yes' to confirm: ")

            if confirmation.lower() != "yes":
                print("❌ Cancelled.")
                return False

            db.drop_all()
            print("✅ All tables dropped successfully!")
            return True
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
            return False


def create_tables(app):
    """Create all tables without dropping."""
    with app.app_context():
        try:
            print("📊 Creating tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False


def seed_database(app):
    """Seed database with sample data (if available)."""
    with app.app_context():
        try:
            print("🌱 Seeding database with sample data...")

            # TODO: Implement seed data logic here
            # Example:
            # user = User(username='admin', email='admin@example.com')
            # db.session.add(user)
            # db.session.commit()

            print("✅ Database seeded successfully!")
            print("   (Currently no seed data defined)")
            return True
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            return False


def show_database_info(app):
    """Display current database information."""
    with app.app_context():
        print("\n📊 Database Information:")
        print(f"   Type: {app.config['SQLALCHEMY_DATABASE_URI'].split(':')[0]}")
        print(f"   URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"   Echo: {app.config['SQLALCHEMY_ECHO']}")
        print()


def main():
    """Main entry point."""
    env = os.getenv("FLASK_ENV", "development")
    command = sys.argv[1] if len(sys.argv) > 1 else "init"

    print(f"\n{'=' * 70}")
    print("X-Filamenta-Python — Database Initialization")
    print(f"{'=' * 70}\n")
    print(f"Environment: {env}")

    # Load configuration
    config = get_config(env)

    # Create Flask app
    app = create_app(config=config)

    # Show database info
    show_database_info(app)

    # Execute command
    commands = {
        "init": init_database,
        "reset": reset_database,
        "drop": drop_database,
        "create": create_tables,
        "seed": seed_database,
    }

    if command not in commands:
        print(f"❌ Unknown command: {command}")
        print("\nAvailable commands:")
        for cmd in commands:
            print(f"   - {cmd}")
        print()
        sys.exit(1)

    print(f"Running: {command}\n")
    result = commands[command](app)

    if not result:
        print("\n❌ Operation failed!")
        sys.exit(1)

    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
