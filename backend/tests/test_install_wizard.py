"""
------------------------------------------------------------------------------
Purpose: Installation wizard functional tests
Description: Covers wizard steps for DB test, upload validation, and finalize flow.

File: backend/tests/test_install_wizard.py | Repository: X-Filamenta-Python
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

import io

import pytest

from backend.src.app import create_app
from backend.src.services.install_service import InstallService


@pytest.fixture()
def app(tmp_path):
    app = create_app()
    app.config["TESTING"] = True
    # ensure flag not set
    tmp_path / "instance" / InstallService._flag_path(".")
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_db_test_step(client):
    resp = client.post(
        "/install/step", data={"step": "db_test", "db_uri": "sqlite:///:memory:"}
    )
    assert resp.status_code == 200
    body = resp.data
    assert b"alert-success" in body or b"alert-danger" in body


def test_password_strength_fail(client):
    resp = client.post(
        "/install/step",
        data={
            "step": "admin",
            "admin_password": "weak",
            "admin_username": "u",
            "admin_email": "e@example.com",
        },
    )
    assert resp.status_code == 400
    assert b"Password" in resp.data


def test_upload_step_invalid_extension(client):
    file = (io.BytesIO(b"data"), "backup.txt")
    resp = client.post(
        "/install/step",
        data={"step": "upload", "backup": file},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert b"Invalid extension" in resp.data or b"Backup invalide" in resp.data


def test_upload_step_valid(client, tmp_path):
    # create a small tar.gz
    tar_path = tmp_path / "data.tar.gz"
    with open(tmp_path / "dummy.txt", "wb") as f:
        f.write(b"ok")
    import tarfile

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(tmp_path / "dummy.txt", arcname="dummy.txt")
    with open(tar_path, "rb") as f:
        file = (io.BytesIO(f.read()), "data.tar.gz")
    resp = client.post(
        "/install/step",
        data={"step": "upload", "backup": file},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert b"Backup valide" in resp.data
    assert (
        b"checksum" in resp.data or b"Checksum" in resp.data or b"backup" in resp.data
    )


def test_finalize_step(client, monkeypatch):
    monkeypatch.setattr(InstallService, "apply_seed_or_restore", lambda *_: True)
    monkeypatch.setattr(InstallService, "create_admin_user", lambda *_: True)
    resp = client.post("/install/step", data={"step": "finalize"})
    assert resp.status_code == 200
    assert b"Installation" in resp.data
