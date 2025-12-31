"""
------------------------------------------------------------------------------
Purpose: Smoke tests for Flask application
Description: Basic health-check tests to verify the application starts
             and responds correctly.

File: backend/tests/test_smoke.py | Repository: X-Filamenta-Python
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

from backend.src.app import create_app


def test_index_returns_ok() -> None:
    """
    Test that the index route returns HTTP 200 with 'OK' response.

    Validates:
        - Status code is 200 (success)
        - Response body contains expected text
        - Application factory creates a working app instance
    """
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == "OK"
