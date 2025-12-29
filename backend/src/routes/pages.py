"""
------------------------------------------------------------------------------
Purpose: Public pages routes
Description: Flask Blueprint for public pages (about, contact, features)

File: backend/src/routes/pages.py | Repository: X-Filamenta-Python
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
- Static and dynamic public pages
- About, contact, features, legal pages
- Internationalization (FR/EN) support
- HTMX optional enhancements
------------------------------------------------------------------------------
"""

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# ---- Blueprint Definition ----
pages = Blueprint("pages", __name__)


# ---- Routes ----


@pages.route("/about")
def about() -> str:
    """
    About page

    Returns:
        Rendered about.html template
    """
    return render_template("pages/about.html")


@pages.route("/contact", methods=["GET", "POST"])
def contact():  # type: ignore[no-untyped-def]
    """
    Contact page with form

    GET: Returns rendered contact.html template
    POST: Process contact form (returns JSON response)

    Returns:
        GET: Rendered contact.html
        POST: JSON response with status
    """
    if request.method == "POST":
        # Form processing handled by API endpoint
        return jsonify(status="success", message="Message envoyé"), 200

    return render_template("pages/contact.html")


@pages.route("/features")
def features() -> str:
    """
    Features page

    Returns:
        Rendered features.html template
    """
    return render_template("pages/features.html")


@pages.route("/preferences")
def preferences() -> str:
    """
    User preferences page

    Returns:
        Rendered preferences.html template
    """
    return render_template("pages/preferences.html")


@pages.route("/profile")
def profile() -> str:
    """
    User profile page

    Returns:
        Rendered profile.html template
    """
    # TODO: Create profile template
    return render_template("pages/profile.html", user={"username": "Guest"})


@pages.route("/dashboard")
def dashboard() -> str:
    """
    Member dashboard page (requires authentication)

    Returns:
        Rendered dashboard/member.html template
    """
    # Check if user is authenticated
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    # TODO: Get real user data from database
    from backend.src.services.user_service import UserService

    user_service = UserService()
    user = user_service.get_by_id(session["user_id"])

    if not user:
        # User not found, clear session and redirect
        session.clear()
        return redirect(url_for("auth.login_page"))

    # Mock data for now
    stats = {"content_count": 0, "activity_count": 0}

    recent_activity = []

    return render_template(
        "dashboard/member.html",
        current_user=user,
        stats=stats,
        recent_activity=recent_activity,
    )


@pages.route("/content")
def content_list() -> str:
    """
    Content list page

    Returns:
        Rendered content list template
    """
    # TODO: Create content list template
    return render_template("pages/content.html")
