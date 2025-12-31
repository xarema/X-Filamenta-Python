"""
Purpose: Admin users management routes
Description: CRUD operations for users (create, edit, delete)

File: backend/src/routes/admin_users.py | Repository: X-Filamenta-Python
Created: 2025-12-30T00:45:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Admin-only routes for user management
- HTMX-enabled for dynamic UI
- Audit logging via AdminService
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from backend.src.decorators import require_admin
from backend.src.models.user import User
from backend.src.services.admin_service import AdminService
from backend.src.services.user_service import UserService
from backend.src.utils.i18n import t

# ---- Blueprint ----
admin_users = Blueprint("admin_users", __name__, url_prefix="/admin/users")


# ---- User List ----


@admin_users.route("/")
@require_admin
def list_users():
    """List all users with pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    active_only = request.args.get("active", "all")

    # Get users
    if active_only == "active":
        users = UserService.get_all(active_only=True)
    elif active_only == "inactive":
        users_all = UserService.get_all(active_only=False)
        users = [u for u in users_all if not u.is_active]
    else:
        users = UserService.get_all(active_only=False)

    # Pagination (simple)
    total = len(users)
    start = (page - 1) * per_page
    end = start + per_page
    users_page = users[start:end]

    return render_template(
        "admin/users_list.html",
        users=users_page,
        page=page,
        per_page=per_page,
        total=total,
        active_filter=active_only,
    )


# ---- Create User ----


@admin_users.route("/create", methods=["GET", "POST"])
@require_admin
def create_user():
    """Create new user (admin action)."""
    from backend.src.services.user_service import UserService

    # Get current admin user (assumes "admin" username for now)
    # TODO: Replace with proper session-based current_user when implemented
    admin_user = UserService.get_by_username("admin")

    if request.method == "GET":
        return render_template("admin/users_create.html")

    # POST: Create user
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    is_admin = request.form.get("is_admin") == "on"
    is_active = request.form.get("is_active", "on") == "on"
    send_email = request.form.get("send_email") == "on"

    # Validation
    if not username or not email or not password:
        flash(t("admin.users.create.error.required"), "error")
        return render_template(
            "admin/users_create.html",
            username=username,
            email=email,
        )

    if len(password) < 8:
        flash(t("admin.users.create.error.password_short"), "error")
        return render_template(
            "admin/users_create.html",
            username=username,
            email=email,
        )

    # Create via AdminService
    try:
        user = AdminService.create_user(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin,
            is_active=is_active,
            send_email=send_email,
            admin_user=admin_user,
            ip_address=request.remote_addr,
        )

        flash(
            t("admin.users.create.success").format(username=username),
            "success",
        )
        return redirect(url_for("admin_users.list_users"))

    except ValueError as e:
        flash(str(e), "error")
        return render_template(
            "admin/users_create.html",
            username=username,
            email=email,
        )


# ---- Edit User ----


@admin_users.route("/<int:user_id>/edit", methods=["GET", "POST"])
@require_admin
def edit_user(user_id: int):
    """Edit existing user."""
    from backend.src.services.user_service import UserService

    # Get current admin user
    admin_user = UserService.get_by_username("admin")

    user = User.query.get_or_404(user_id)

    if request.method == "GET":
        return render_template("admin/users_edit.html", user=user)

    # POST: Update user
    updates = {}

    # Collect updates
    if "email" in request.form:
        updates["email"] = request.form["email"].strip()
    if "is_admin" in request.form:
        updates["is_admin"] = request.form.get("is_admin") == "on"
    if "is_active" in request.form:
        updates["is_active"] = request.form.get("is_active") == "on"

    # Password change (optional)
    new_password = request.form.get("password", "").strip()
    if new_password:
        if len(new_password) < 8:
            flash(t("admin.users.edit.error.password_short"), "error")
            return render_template("admin/users_edit.html", user=user)
        updates["password"] = new_password

    # Update via AdminService
    try:
        AdminService.update_user(
            user_id=user_id,
            updates=updates,
            admin_user=admin_user,
            ip_address=request.remote_addr,
        )

        flash(
            t("admin.users.edit.success").format(username=user.username),
            "success",
        )
        return redirect(url_for("admin_users.list_users"))

    except ValueError as e:
        flash(str(e), "error")
        return render_template("admin/users_edit.html", user=user)


# ---- Delete User ----


@admin_users.route("/<int:user_id>/delete", methods=["POST"])
@require_admin
def delete_user(user_id: int):
    """Delete user (soft or hard)."""
    from backend.src.services.user_service import UserService

    # Get current admin user
    admin_user = UserService.get_by_username("admin")

    hard_delete = request.form.get("hard_delete") == "true"

    try:
        AdminService.delete_user(
            user_id=user_id,
            hard_delete=hard_delete,
            admin_user=admin_user,
            ip_address=request.remote_addr,
        )

        delete_type = "hard" if hard_delete else "soft"
        flash(
            t(f"admin.users.delete.success_{delete_type}"),
            "success",
        )

    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("admin_users.list_users"))

