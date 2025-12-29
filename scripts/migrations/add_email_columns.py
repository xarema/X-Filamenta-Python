#!/usr/bin/env python
"""Add missing email columns to users table"""

import os
import sys
import sqlite3
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Find database file
db_path = project_root / "instance" / "x-filamenta_python.db"

print(f"Looking for database at: {db_path}")
print(f"Database exists: {db_path.exists()}")

if not db_path.exists():
    print(f"Database not found at {db_path}")
    print("Run migration first:")
    print("  python scripts/migrations/apply_phase1_migration.py")
    sys.exit(1)

try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("\nAdding missing columns to users table...")

    # Get existing columns
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    print(f"Current columns: {len(existing_columns)}")

    columns_to_add = [
        ("email_verification_token_expiry", "DATETIME"),
        ("password_reset_token", "VARCHAR(100)"),
        ("password_reset_token_expiry", "DATETIME"),
    ]

    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            sql = f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"
            print(f"  Adding: {col_name}")
            cursor.execute(sql)
        else:
            print(f"  Already exists: {col_name}")

    conn.commit()
    print("\nColumns added successfully!")

    # Verify
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Total columns now: {len(columns)}")

    conn.close()
    print("\nMigration completed!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



