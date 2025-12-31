"""
------------------------------------------------------------------------------
Purpose: Phase 4 Part 1 — Integration tests for install wizard
Description: Validate /install/step admin and db_test branches

File: backend/tests/integration/test_install_phase4_part1.py | Repository: X-Filamenta-Python
Created: 2025-12-27T12:55:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
------------------------------------------------------------------------------
"""

from backend.src.app import create_app


def test_install_admin_invalid_password():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post(
        "/install/step", data={"step": "admin", "admin_password": "short"}
    )
    assert resp.status_code == 400


def test_install_db_test_sqlite_memory():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post(
        "/install/step", data={"step": "db_test", "db_uri": "sqlite:///:memory:"}
    )
    assert resp.status_code == 200
    # check that template contains an indicator of db test result
    assert b"Wizard DB test" in resp.data or b"db_test" in resp.data
