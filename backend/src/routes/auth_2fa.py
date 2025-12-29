"""
------------------------------------------------------------------------------
Purpose: 2FA routes (setup, verify, disable)
Description: Flask Blueprint for two-factor authentication routes

File: backend/src/routes/auth_2fa.py | Repository: X-Filamenta-Python
Created: 2025-12-27T20:35:00+00:00
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
- TOTP setup, verification, and disable flows
- QR code generation for authenticator apps
- Backup codes management
- HTMX-enabled for smooth UX
------------------------------------------------------------------------------
"""

from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from backend.src.extensions import db
from backend.src.services.rate_limiter import strict_rate_limit, two_fa_rate_limit
from backend.src.services.totp_service import TOTPService
from backend.src.services.user_service import UserService

# ---- Blueprint Definition ----
auth_2fa = Blueprint("auth_2fa", __name__, url_prefix="/auth")


# ---- Helper Functions ----


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return "user_id" in session


def get_current_user_id() -> int | None:
    """Get current user ID from session"""
    return session.get("user_id")


def login_user(user_id: int) -> None:
    """Set user as logged in"""
    session["user_id"] = user_id
    session.permanent = True


# ---- Routes 2FA ----


@auth_2fa.route("/setup-2fa", methods=["GET"])
def setup_2fa_page() -> str:
    """
    Display 2FA setup page

    Returns:
        Rendered setup-2fa.html template with QR code
    """
    if not is_authenticated():
        return redirect(url_for("auth.login_page"))

    user_id = get_current_user_id()
    user = UserService.get_by_id(user_id)

    if not user:
        return redirect(url_for("auth.login_page"))

    # Check if 2FA already enabled
    if user.totp_enabled:
        return render_template("auth/setup-2fa.html", already_enabled=True)

    # Generate new TOTP secret
    secret = TOTPService.generate_secret()
    provisioning_uri = TOTPService.generate_provisioning_uri(user, secret)
    qr_code_data_uri = TOTPService.generate_qr_code(provisioning_uri)

    # Generate backup codes
    backup_codes, hashed_codes_json = TOTPService.generate_backup_codes()

    # Store temporarily in session (will be saved on successful verification)
    session["totp_setup_secret"] = secret
    session["totp_setup_backup_codes"] = hashed_codes_json

    return render_template(
        "auth/setup-2fa.html",
        qr_code=qr_code_data_uri,
        secret=secret,
        backup_codes=backup_codes,
    )


@auth_2fa.route("/setup-2fa", methods=["POST"])
@strict_rate_limit()
def setup_2fa() -> Response | tuple[Response, int]:
    """
    Complete 2FA setup (verify code and enable)

    Expected form data:
        code: str (6 digits)

    Returns:
        Redirect to dashboard or JSON error
        - 429: Rate limit exceeded
    """
    if not is_authenticated():
        return jsonify({"error": "Non authentifié"}), 401

    user_id = get_current_user_id()
    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Get setup data from session
    secret = session.get("totp_setup_secret")
    backup_codes_json = session.get("totp_setup_backup_codes")

    if not secret or not backup_codes_json:
        return jsonify({"error": "Session expirée, recommencez la configuration"}), 400

    # Get code from request
    code = request.form.get("code", "").strip()

    if not code:
        return jsonify({"error": "Code requis"}), 400

    # Verify code
    if not TOTPService.verify_code(secret, code):
        return jsonify({"error": "Code invalide, vérifiez votre application"}), 400

    # Code valid, enable 2FA
    user.enable_2fa(secret)
    user.backup_codes = backup_codes_json

    db.session.commit()

    # Clear session setup data
    session.pop("totp_setup_secret", None)
    session.pop("totp_setup_backup_codes", None)

    # HTMX redirect
    if request.headers.get("HX-Request"):
        response = Response()
        response.headers["HX-Redirect"] = url_for("pages.dashboard")
        return response

    return redirect(url_for("pages.dashboard"))


@auth_2fa.route("/verify-2fa", methods=["GET"])
def verify_2fa_page() -> str:
    """
    Display 2FA verification page (after login)

    Returns:
        Rendered verify-2fa.html template
    """
    # Check if user is in 2FA pending state
    if "pending_2fa_user_id" not in session:
        return redirect(url_for("auth.login_page"))

    return render_template("auth/verify-2fa.html")


@auth_2fa.route("/verify-2fa", methods=["POST"])
@two_fa_rate_limit()
def verify_2fa() -> Response | tuple[Response, int]:
    """
    Verify 2FA code after login

    Expected form data:
        code: str (6 digits or backup code)

    Returns:
        Redirect to dashboard or JSON error
        - 429: Rate limit exceeded
    """
    # Check if user is in 2FA pending state
    pending_user_id = session.get("pending_2fa_user_id")

    if not pending_user_id:
        return jsonify({"error": "Session invalide"}), 400

    user = UserService.get_by_id(pending_user_id)

    if not user or not user.totp_enabled:
        return jsonify({"error": "Configuration 2FA invalide"}), 400

    # Get code from request
    code = request.form.get("code", "").strip()

    if not code:
        return jsonify({"error": "Code requis"}), 400

    # Try to verify TOTP code
    code_valid = TOTPService.verify_code(user.totp_secret, code)

    # If TOTP fails, try backup code
    if not code_valid:
        code_valid = TOTPService.verify_backup_code(user, code)
        if code_valid:
            db.session.commit()  # Save consumed backup code

    if not code_valid:
        return jsonify({"error": "Code invalide"}), 400

    # Code valid, complete login
    login_user(pending_user_id)
    session.pop("pending_2fa_user_id", None)

    # Update last login
    user.update_last_login(request.remote_addr)
    db.session.commit()

    # HTMX redirect
    if request.headers.get("HX-Request"):
        response = Response()
        response.headers["HX-Redirect"] = url_for("pages.dashboard")
        return response

    return redirect(url_for("pages.dashboard"))


@auth_2fa.route("/disable-2fa", methods=["POST"])
@strict_rate_limit()
def disable_2fa() -> Response | tuple[Response, int]:
    """
    Disable 2FA for current user

    Returns:
        Redirect to profile or JSON response
        - 429: Rate limit exceeded
    """
    if not is_authenticated():
        return jsonify({"error": "Non authentifié"}), 401

    user_id = get_current_user_id()
    user = UserService.get_by_id(user_id)

    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Disable 2FA
    user.disable_2fa()
    db.session.commit()

    # HTMX response
    if request.headers.get("HX-Request"):
        return jsonify({"success": True, "message": "2FA désactivé"})

    return redirect(url_for("pages.dashboard"))
