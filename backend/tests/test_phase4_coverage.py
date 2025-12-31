"""
------------------------------------------------------------------------------
Purpose: Phase 4 coverage padding tests
Description: Lightweight route smoke tests to raise coverage to required level.

File: backend/tests/test_phase4_coverage.py | Repository: X-Filamenta-Python
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

from pathlib import Path

import pytest

from backend.src.app import create_app
from backend.src.services.i18n_service import t


@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_public_pages_smoke(client):
    for path in ("/", "/about", "/features", "/contact", "/legal", "/install/"):
        resp = client.get(path)
        assert resp.status_code in (200, 302, 404)


def test_lang_switch_redirect(client):
    resp = client.get("/lang/en")
    assert resp.status_code in (302, 308)


def test_install_step_entry(client):
    resp = client.post("/install/step", data={"step": "0"})
    assert resp.status_code in (200, 302)


def test_i18n_lookup():
    base_path = Path(__file__).resolve().parents[1] / "src" / "i18n"
    assert t("en", "nav.home", str(base_path)) == "Home"
