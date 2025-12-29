"""
------------------------------------------------------------------------------
Purpose: Admin user management routes (CRUD)
Description: API routes for user management (create, update, delete, reset 2FA)

File: backend/src/routes/admin_users.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:25:00+00:00
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
- REST API for user CRUD operations
- Requires admin authentication
- Handles 2FA reset and password resets
- Returns JSON responses for HTMX compatibility
------------------------------------------------------------------------------
"""

from flask import Blueprint, Response, jsonify, request

from backend.src.decorators import require_admin
from backend.src.extensions import db
from backend.src.models.admin_history import AdminHistory
from backend.src.models.user import UserRole
from backend.src.services.rate_limiter import strict_rate_limit
from backend.src.services.user_service import UserService

# ---- Blueprint Definition ----
admin_users = Blueprint("admin_users", __name__, url_prefix="/admin/api/users")


# ---- Helper Functions ----


def log_admin_action(
    admin_id: int, action: str, target_id: int, details: dict = None
) -> None:
    """Log admin action to audit trail"""
    AdminHistory.log_action(
        admin_id=admin_id,
        action=action,
        target_type="user",
        target_id=target_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
    )


# ---- Routes ----


@admin_users.route("/<int:user_id>", methods=["GET"])
@require_admin
def get_user(user_id: int) -> Response | tuple[Response, int]:
    """
    Get user details

    Args:
        user_id: User ID

    Returns:
        JSON user data or 404
    """
    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "role": user.role,
            "totp_enabled": user.totp_enabled,
            "email_verified": user.email_verified,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "login_attempts": user.login_attempts,
            "is_locked": user.is_locked(),
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
    )


@admin_users.route("/<int:user_id>", methods=["PUT"])
@require_admin
@strict_rate_limit()
def update_user(user_id: int) -> Response | tuple[Response, int]:
    """
    Update user details

    Args:
        user_id: User ID

    Expected JSON:
        {
            "email": str (optional),
            "is_active": bool (optional),
            "is_admin": bool (optional),
            "role": str (optional)
        }

    Returns:
        JSON success or error
    """
    from flask import session

    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    data = request.get_json() or {}
    changes = {}

    # Update email
    if "email" in data:
        new_email = data["email"].strip()
        if new_email != user.email:
            # Check if email already exists
            existing = UserService.get_by_email(new_email)
            if existing and existing.id != user_id:
                return jsonify({"error": "Email déjà utilisé"}), 400
            user.email = new_email
            changes["email"] = new_email

    # Update active status
    if "is_active" in data:
        user.is_active = bool(data["is_active"])
        changes["is_active"] = user.is_active

    # Update admin status
    if "is_admin" in data:
        user.is_admin = bool(data["is_admin"])
        changes["is_admin"] = user.is_admin

    # Update role
    if "role" in data:
        try:
            role = UserRole(data["role"])
            user.role = role.value
            changes["role"] = role.value
        except ValueError:
            return jsonify({"error": "Rôle invalide"}), 400

    db.session.commit()

    # Log admin action
    admin_id = session.get("user_id")
    log_admin_action(admin_id, "user_update", user_id, changes)
    db.session.commit()

    return jsonify(
        {"success": True, "message": "Utilisateur mis à jour", "changes": changes}
    )


@admin_users.route("/<int:user_id>", methods=["DELETE"])
@require_admin
@strict_rate_limit()
def delete_user(user_id: int) -> Response | tuple[Response, int]:
    """
    Delete user

    Args:
        user_id: User ID

    Returns:
        JSON success or error
    """
    from flask import session

    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Prevent self-deletion
    admin_id = session.get("user_id")
    if user_id == admin_id:
        return jsonify({"error": "Impossible de se supprimer soi-même"}), 400

    username = user.username
    db.session.delete(user)

    # Log admin action
    log_admin_action(admin_id, "user_delete", user_id, {"username": username})
    db.session.commit()

    return jsonify({"success": True, "message": f"Utilisateur {username} supprimé"})


@admin_users.route("/<int:user_id>/reset-2fa", methods=["POST"])
@require_admin
@strict_rate_limit()
def reset_2fa(user_id: int) -> Response | tuple[Response, int]:
    """
    Reset user 2FA (disable)

    Args:
        user_id: User ID

    Returns:
        JSON success or error
    """
    from flask import session

    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    if not user.totp_enabled:
        return jsonify({"error": "2FA non activé"}), 400

    # Disable 2FA
    user.disable_2fa()
    db.session.commit()

    # Log admin action
    admin_id = session.get("user_id")
    log_admin_action(admin_id, "user_reset_2fa", user_id, {"username": user.username})
    db.session.commit()

    return jsonify({"success": True, "message": "2FA réinitialisé"})


@admin_users.route("/<int:user_id>/unlock", methods=["POST"])
@require_admin
@strict_rate_limit()
def unlock_user(user_id: int) -> Response | tuple[Response, int]:
    """
    Unlock locked user account

    Args:
        user_id: User ID

    Returns:
        JSON success or error
    """
    from flask import session

    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    if not user.is_locked():
        return jsonify({"error": "Compte non verrouillé"}), 400

    # Reset login attempts
    user.reset_login_attempts()
    db.session.commit()

    # Log admin action
    admin_id = session.get("user_id")
    log_admin_action(admin_id, "user_unlock", user_id, {"username": user.username})
    db.session.commit()

    return jsonify({"success": True, "message": "Compte déverrouillé"})


@admin_users.route("/<int:user_id>/reset-password", methods=["POST"])
@require_admin
@strict_rate_limit()
def reset_password(user_id: int) -> Response | tuple[Response, int]:
    """
    Reset user password (admin action)

    Args:
        user_id: User ID

    Expected JSON:
        {
            "new_password": str
        }

    Returns:
        JSON success or error
    """
    from flask import session

    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    data = request.get_json() or {}
    new_password = data.get("new_password", "").strip()

    if not new_password or len(new_password) < 8:
        return jsonify(
            {"error": "Mot de passe doit contenir au moins 8 caractères"}
        ), 400

    # Set new password
    user.set_password(new_password)
    db.session.commit()

    # Log admin action (without password in logs)
    admin_id = session.get("user_id")
    log_admin_action(
        admin_id, "user_reset_password", user_id, {"username": user.username}
    )
    db.session.commit()

    return jsonify({"success": True, "message": "Mot de passe réinitialisé"})
