"""
------------------------------------------------------------------------------
Purpose: Pytest configuration and shared fixtures
Description: Provides fixtures for test application and client setup.

File: backend/tests/conftest.py | Repository: X-Filamenta-Python
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

import pytest

from backend.src.app import create_app


@pytest.fixture
def app():
    """Create and configure test application."""
    app = create_app()
    app.config["TESTING"] = True

    # Create tables for tests
    from backend.src.extensions import db

    with app.app_context():
        db.create_all()

    yield app

    # Cleanup
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for making requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner for testing CLI commands."""
    return app.test_cli_runner()
