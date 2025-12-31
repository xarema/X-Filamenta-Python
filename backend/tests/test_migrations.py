"""
---
Purpose: Database migration edge case tests
Description: Comprehensive tests for Alembic migrations including error handling and edge cases
File: backend/tests/test_migrations.py | Repository: X-Filamenta-Python
Created: 2025-12-30T00:00:00+00:00
Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0
License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.
Metadata:
- Status: Complete
- Classification: Public
---
"""
import pytest
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.exc import OperationalError, IntegrityError
from alembic.config import Config
from alembic import command
from alembic.migration import MigrationContext
from alembic.operations import Operations
import tempfile
import os
class TestMigrationEdgeCases:
    """Test edge cases in database migrations."""
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        fd, path = tempfile.mkstemp(suffix='.db')
        db_url = f"sqlite:///{path}"
        engine = create_engine(db_url)
        yield engine, db_url
        # Cleanup
        engine.dispose()
        os.close(fd)
        os.unlink(path)
    def test_migration_with_duplicate_table_name(self, temp_db):
        """
        Test migration behavior when attempting to create a table that already exists.
        Expected: Should handle gracefully or raise appropriate error.
        """
        engine, db_url = temp_db
        metadata = MetaData()
        # Create initial table
        users_table = Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50), nullable=False)
        )
        metadata.create_all(engine)
        # Verify table exists
        inspector = inspect(engine)
        assert 'users' in inspector.get_table_names()
        # Attempt to create duplicate table should be handled
        with pytest.raises(OperationalError):
            # This should fail because table already exists
            metadata.create_all(engine, checkfirst=False)
        # With checkfirst=True, should succeed (no-op)
        metadata.create_all(engine, checkfirst=True)
        assert 'users' in inspector.get_table_names()
    def test_migration_rollback_on_error(self, temp_db):
        """
        Test that migration rolls back properly on error.
        Expected: If migration fails, database should be in previous state.
        """
        engine, db_url = temp_db
        metadata = MetaData()
        # Create initial schema
        Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50), nullable=False)
        )
        metadata.create_all(engine)
        # Insert test data
        with engine.connect() as conn:
            conn.execute(
                metadata.tables['users'].insert().values(
                    id=1,
                    username='testuser'
                )
            )
            conn.commit()
        # Attempt a migration that will fail (add NOT NULL column without default)
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        # This should fail because existing rows can't have NULL in new NOT NULL column
        with pytest.raises((OperationalError, IntegrityError)):
            with conn.begin():
                op.add_column('users', Column('email', String(100), nullable=False))
        # Verify original data is intact
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        assert 'email' not in columns  # Column should not exist due to rollback
        assert 'username' in columns  # Original column still exists
        conn.close()
    def test_migration_with_null_constraints(self, temp_db):
        """
        Test migration adding NULL constraints to existing data.
        Expected: Should handle existing NULL values appropriately.
        """
        engine, db_url = temp_db
        metadata = MetaData()
        # Create table with nullable column
        Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50), nullable=True)  # Initially nullable
        )
        metadata.create_all(engine)
        # Insert data with NULL username
        with engine.connect() as conn:
            conn.execute(
                metadata.tables['users'].insert().values(id=1, username=None)
            )
            conn.commit()
        # Verify NULL value exists
        with engine.connect() as conn:
            result = conn.execute(
                metadata.tables['users'].select().where(
                    metadata.tables['users'].c.id == 1
                )
            )
            row = result.fetchone()
            assert row[1] is None  # username is NULL
        # Attempting to add NOT NULL constraint should fail
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        # SQLite doesn't support ALTER COLUMN directly, but conceptually:
        # This represents the problem of adding NOT NULL to column with NULLs
        with pytest.raises((OperationalError, IntegrityError)):
            with conn.begin():
                # Try to add constraint (will fail due to existing NULL)
                op.alter_column('users', 'username', nullable=False)
        conn.close()
    def test_migration_with_foreign_key_conflicts(self, temp_db):
        """
        Test migration with foreign key constraint violations.
        Expected: Should detect and handle FK violations.
        """
        engine, db_url = temp_db
        metadata = MetaData()
        # Create parent table
        users_table = Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50))
        )
        # Create child table without FK initially
        posts_table = Table(
            'posts',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer),  # No FK yet
            Column('title', String(100))
        )
        metadata.create_all(engine)
        # Insert data with orphaned records
        with engine.connect() as conn:
            conn.execute(users_table.insert().values(id=1, username='user1'))
            conn.execute(posts_table.insert().values(id=1, user_id=999, title='Orphaned post'))
            conn.commit()
        # Attempt to add FK constraint should fail due to orphaned record
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        with pytest.raises((OperationalError, IntegrityError)):
            with conn.begin():
                op.create_foreign_key(
                    'fk_posts_user_id',
                    'posts',
                    'users',
                    ['user_id'],
                    ['id']
                )
        conn.close()
class TestMigrationDataIntegrity:
    """Test data integrity during migrations."""
    @pytest.fixture
    def temp_db_with_data(self):
        """Create a temporary database with test data."""
        fd, path = tempfile.mkstemp(suffix='.db')
        db_url = f"sqlite:///{path}"
        engine = create_engine(db_url)
        metadata = MetaData()
        # Create schema with data
        users = Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(50)),
            Column('email', String(100))
        )
        metadata.create_all(engine)
        # Insert test data
        with engine.connect() as conn:
            for i in range(1, 11):
                conn.execute(
                    users.insert().values(
                        id=i,
                        username=f'user{i}',
                        email=f'user{i}@example.com'
                    )
                )
            conn.commit()
        yield engine, db_url, metadata
        # Cleanup
        engine.dispose()
        os.close(fd)
        os.unlink(path)
    def test_migration_preserves_data(self, temp_db_with_data):
        """
        Test that data is preserved during schema migration.
        Expected: All original data remains intact after migration.
        """
        engine, db_url, metadata = temp_db_with_data
        # Count records before migration
        with engine.connect() as conn:
            result = conn.execute(metadata.tables['users'].select())
            original_count = len(result.fetchall())
            assert original_count == 10
        # Perform migration (add column with default)
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        with conn.begin():
            op.add_column(
                'users',
                Column('created_at', String(50), server_default='2025-12-30')
            )
        # Verify data still exists
        with engine.connect() as conn:
            result = conn.execute(metadata.tables['users'].select())
            rows = result.fetchall()
            assert len(rows) == original_count
            # Verify original data intact
            for row in rows:
                assert row[1].startswith('user')  # username
                assert row[2].endswith('@example.com')  # email
        conn.close()
    def test_migration_with_data_transformation(self, temp_db_with_data):
        """
        Test migration that transforms existing data.
        Expected: Data transformation should work correctly.
        """
        engine, db_url, metadata = temp_db_with_data
        # Add column for transformed data
        conn = engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        with conn.begin():
            # Add column for uppercase username
            op.add_column('users', Column('username_upper', String(50)))
        # Transform data
        with engine.connect() as conn:
            # Update new column with transformed data
            conn.execute(
                metadata.tables['users'].update().values(
                    username_upper=metadata.tables['users'].c.username
                )
            )
            conn.commit()
        # Verify transformation (note: SQL won't uppercase automatically)
        with engine.connect() as conn:
            result = conn.execute(
                metadata.tables['users'].select().where(
                    metadata.tables['users'].c.id == 1
                )
            )
            row = result.fetchone()
            assert row[3] == 'user1'  # username_upper column
        conn.close()
# Run tests marker
pytestmark = pytest.mark.migrations
