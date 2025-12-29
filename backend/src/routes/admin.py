"""
------------------------------------------------------------------------------
Purpose: Admin routes
Description: Flask Blueprint for admin panel (dashboard, users, settings)

File: backend/src/routes/admin.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Notes:
- Admin dashboard and user management routes
- Requires @login_required and admin privileges
- HTMX-enabled for dynamic content updates
------------------------------------------------------------------------------
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

from backend.src.decorators import require_admin
from backend.src.services.content_service import ContentService
from backend.src.services.user_service import UserService
from backend.src.services.email_service import EmailService
from backend.src.models.settings import Settings
from backend.src.extensions import db

# ---- Blueprint Definition ----
admin = Blueprint("admin", __name__, url_prefix="/admin")


# ---- Routes ----


@admin.route("/")
@require_admin
def dashboard() -> str:
    """
    Admin dashboard

    Shows overview of app stats and metrics

    Returns:
        Rendered admin/dashboard.html template
    """
    from datetime import datetime, timedelta

    from backend.src.models.admin_history import AdminHistory

    # Get real stats from database
    all_users = UserService.get_all(active_only=False)
    active_users = [u for u in all_users if u.is_active]
    admin_users = [u for u in all_users if u.is_admin]
    users_2fa = [u for u in all_users if u.totp_enabled]

    all_content, total_content = ContentService.get_all(page=1, per_page=1)

    # Get recent admin actions (last 10)
    recent_actions = (
        AdminHistory.query.order_by(AdminHistory.timestamp.desc()).limit(10).all()
    )

    # Get users with recent logins (last 24h)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_logins = [u for u in all_users if u.last_login and u.last_login > yesterday]

    stats = {
        "total_users": len(all_users),
        "active_users": len(active_users),
        "admin_users": len(admin_users),
        "users_2fa": len(users_2fa),
        "content_items": total_content,
        "recent_logins_24h": len(recent_logins),
    }

    return render_template(
        "admin/dashboard.html", stats=stats, recent_actions=recent_actions
    )


@admin.route("/users")
@require_admin
def users() -> str:
    """
    Users management page

    Requires: Admin authentication

    List, search, and manage users (CRUD operations)

    Returns:
        Rendered admin/users.html template
    """
    # Get all users
    all_users = UserService.get_all(active_only=False)

    # Convert to dict for template
    users_data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "totp_enabled": u.totp_enabled,
            "last_login": u.last_login.isoformat() if u.last_login else None,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "login_attempts": u.login_attempts,
            "is_locked": u.is_locked(),
        }
        for u in all_users
    ]

    return render_template("admin/users.html", users=users_data)


@admin.route("/settings", methods=["GET"])
@require_admin
def settings() -> str:
    """
    Application settings page (GET).

    Requires: Admin authentication

    Display all app settings from database.

    Returns:
        Rendered admin/settings.html template with settings
    """
    all_settings = Settings.get_all()

    return render_template("admin/settings.html", settings=all_settings)


@admin.route("/settings", methods=["POST"])
@require_admin
def save_settings():
    """
    Save application settings (POST).

    Requires: Admin authentication

    Save settings to database from form data.

    Expected form fields:
        smtp_host, smtp_port, smtp_user, smtp_password, smtp_tls_enabled,
        smtp_from_email, smtp_from_name, email_verification_required,
        email_verification_token_expiry_hours, password_reset_token_expiry_minutes,
        password_reset_rate_limit_per_hour, email_format, registration_enabled,
        2fa_required, site_name, site_url, logo_url, footer_text

    Returns:
        Redirect to settings page with success message
    """
    try:
        # SMTP Settings
        Settings.set("smtp_host", request.form.get("smtp_host", ""))
        Settings.set("smtp_port", request.form.get("smtp_port", "465"))
        Settings.set("smtp_user", request.form.get("smtp_user", ""))
        Settings.set("smtp_password", request.form.get("smtp_password", ""))
        Settings.set(
            "smtp_tls_enabled",
            request.form.get("smtp_tls_enabled") == "on"
        )
        Settings.set("smtp_from_email", request.form.get("smtp_from_email", ""))
        Settings.set("smtp_from_name", request.form.get("smtp_from_name", ""))

        # Email Verification Settings
        Settings.set(
            "email_verification_required",
            request.form.get("email_verification_required") == "on"
        )
        Settings.set(
            "email_verification_token_expiry_hours",
            request.form.get("email_verification_token_expiry_hours", "24")
        )
        Settings.set(
            "password_reset_token_expiry_minutes",
            request.form.get("password_reset_token_expiry_minutes", "60")
        )
        Settings.set(
            "password_reset_rate_limit_per_hour",
            request.form.get("password_reset_rate_limit_per_hour", "2")
        )
        Settings.set("email_format", request.form.get("email_format", "html_with_fallback"))

        # Feature Flags
        Settings.set("registration_enabled", request.form.get("registration_enabled") == "on")
        Settings.set("2fa_required", request.form.get("2fa_required") == "on")

        # Site Configuration
        Settings.set("site_name", request.form.get("site_name", "X-Filamenta"))
        Settings.set("site_url", request.form.get("site_url", "http://localhost:5000"))
        Settings.set("logo_url", request.form.get("logo_url", "/static/logo.png"))
        Settings.set("footer_text", request.form.get("footer_text", ""))

        flash("Paramètres sauvegardés avec succès", "success")
        return redirect(url_for("admin.settings"))

    except Exception as e:
        flash(f"Erreur lors de la sauvegarde: {str(e)}", "error")
        return redirect(url_for("admin.settings"))


@admin.route("/settings/test-smtp", methods=["POST"])
@require_admin
def test_smtp_settings():
    """
    Test SMTP connection (POST, AJAX).

    Requires: Admin authentication

    Test if SMTP settings are valid by attempting connection.

    Returns:
        JSON with success status and message
    """
    try:
        email_service = EmailService()
        success, message = email_service.test_smtp_connection()

        return jsonify({
            "success": success,
            "message": message
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erreur test SMTP: {str(e)}"
        }), 500


# ...existing code...
@require_admin
def content() -> str:
    """
    Content management page

    Requires: Admin authentication

    Manage app content (CMS-like interface)

    Returns:
        Rendered admin/content.html template
    """
    # Get all content from database
    content_items, total = ContentService.get_all(page=1, per_page=50)
    content_list = [item.to_dict(include_body=False) for item in content_items]

    return render_template("admin/content.html", content=content_list, total=total)
