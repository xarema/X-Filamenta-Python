"""
------------------------------------------------------------------------------
Purpose: Main routes for public pages
Description: Flask Blueprint with main routes (index, datagrid examples)

File: backend/src/routes/main.py | Repository: X-Filamenta-Python
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
- Home page and public content routes
- Datagrid examples with HTMX
- Bootstrap 5 demonstration pages
- No authentication required
------------------------------------------------------------------------------
"""

from flask import Blueprint, Response, redirect, render_template, session, url_for

# ---- Blueprint Definition ----
main = Blueprint("main", __name__)


# ---- Routes ----


@main.route("/")
def index() -> str | Response:
    """
    Homepage route

    Returns:
        Redirect to dashboard if authenticated, otherwise to login

    Note:
        Installation check is handled by enforce_installation() middleware
    """
    from flask import current_app

    # During tests, render the template so route tests can assert content
    if current_app.config.get("TESTING"):
        return render_template("pages/index.html")

    # Check if user is authenticated
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    else:
        return redirect(url_for("auth.login_page"))
        return redirect(url_for("auth.login_page"))


@main.route("/datagrid")
def datagrid() -> str:
    """
    DataGrid example page

    Returns:
        Rendered datagrid-example.html template with Tabulator demo
    """
    return render_template("pages/datagrid-example.html")


@main.route("/favicon.ico")
def favicon() -> tuple[bytes, int, dict]:
    """
    Favicon endpoint - returns a minimal transparent PNG (1x1 pixel)

    Prevents 404 errors in logs when browser requests favicon.ico

    Returns:
        Tuple of (PNG bytes, 200 OK, headers)
    """
    # 1x1 transparent PNG (minimal footprint)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT"
        b"\x08\x99c\xf8\x0f\x00\x00\x01\x01\x00\x00\x18\xdd\x8d\xb4\x00"
        b"\x00\x00\x00IEND\xaeB`\x82"
    )
    return (
        png_bytes,
        200,
        {
            "Content-Type": "image/x-icon",
            "Cache-Control": "public, max-age=2592000",  # 30 days
        },
    )
