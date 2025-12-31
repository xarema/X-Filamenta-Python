"""
------------------------------------------------------------------------------
Purpose: Authentication routes (login, logout, 2FA)
Description: Flask Blueprint for user authentication with HTMX support

File: backend/src/routes/auth.py | Repository: X-Filamenta-Python
Created: 2025-12-27T14:30:00+00:00
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
- Authentication routes with HTMX partials
- Login/logout with session management
- 2FA TOTP support (to be implemented)
------------------------------------------------------------------------------
"""

from typing import Any

from flask import (
    Blueprint,
    Response,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from backend.src.decorators import require_admin
from backend.src.extensions import db
from backend.src.models.user import User
from backend.src.services.email_service import EmailService
from backend.src.services.rate_limiter import login_rate_limit
from backend.src.services.user_service import UserService
from backend.src.utils.i18n import t

# ---- Blueprint Definition ----
auth = Blueprint("auth", __name__, url_prefix="/auth")


# ---- Helper Functions ----


def is_authenticated() -> Any:
    """
    Check if user is authenticated (Flask-Login)

    Returns:
        True if user is authenticated via Flask-Login
    """
    return current_user.is_authenticated


def get_current_user_id() -> Any:
    """
    Get current user ID from Flask-Login

    Returns:
        User ID if authenticated, None otherwise
    """
    return current_user.id if current_user.is_authenticated else None


# Note: login_user() and logout_user() are now provided by flask_login
# They are imported at the top of this file


# ---- Routes ----


@auth.route("/login", methods=["GET"])
def login_page() -> Any:
    """
    Display login page

    Returns:
        Rendered login.html template
    """
    # If already authenticated, redirect to dashboard
    if is_authenticated():
        return redirect(url_for("pages.dashboard"))

    # Otherwise, show login form (don't redirect if not authenticated)
    return render_template("auth/login.html")


@auth.route("/register", methods=["GET"])
def register_page() -> Any:
    """
    Display registration page

    Returns:
        Rendered register.html template
    """
    # If already authenticated, redirect to dashboard
    if is_authenticated():
        return redirect(url_for("pages.dashboard"))

    # Otherwise, show registration form
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
@login_rate_limit()
def register() -> Any:
    """
    Process user registration (HTMX/JSON)

    Expected JSON:
        {
            "username": str,
            "email": str,
            "password": str,
            "password_confirm": str
        }

    Returns:
        JSON response with success/error
        - 201: Registration successful, redirect to login
        - 400: Invalid input or user exists
        - 429: Rate limit exceeded
    """
    data = request.get_json() or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    password_confirm = data.get("password_confirm", "")

    # Validation
    if not username or not email or not password:
        return jsonify({"error": "Tous les champs sont requis"}), 400

    if len(username) < 3:
        return jsonify({"error": "Le nom d'utilisateur doit contenir au moins 3 caractères"}), 400

    if len(password) < 8:
        return jsonify({"error": "Le mot de passe doit contenir au least 8 caractères"}), 400

    if password != password_confirm:
        return jsonify({"error": "Les mots de passe ne correspondent pas"}), 400

    # Check if user already exists
    user_service = UserService()
    if user_service.get_by_username(username):
        return jsonify({"error": "Ce nom d'utilisateur est déjà utilisé"}), 400

    if user_service.get_by_email(email):
        return jsonify({"error": "Cet email est déjà utilisé"}), 400

    # Create new user
    try:
        user = User(
            username=username,
            email=email,
            is_active=True,
            role="user"
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Send verification email if required
        settings_service = current_app.config.get("SETTINGS_SERVICE")
        if settings_service and settings_service.get_setting("email_verification_required"):
            token = user.generate_email_verification_token()
            db.session.commit()

            email_service = EmailService()
            email_service.send_verification_email(
                user_email=user.email,
                user_name=user.username,
                verification_token=token,
            )

        return jsonify(
            {
                "success": True,
                "message": "Inscription réussie. Veuillez vous connecter.",
                "redirect": url_for("auth.login_page"),
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Erreur lors de l'inscription"}), 500


@auth.route("/login", methods=["POST"])
@login_rate_limit()
def login() -> Any:
    """
    Process login form (HTMX)

    Expected JSON:
        {
            "username": str,
            "password": str
        }

    Returns:
        JSON response with success/error
        - 200: Login successful, redirect to dashboard
        - 400: Invalid input
        - 401: Invalid credentials
        - 403: Account locked or inactive
        - 429: Rate limit exceeded
    """
    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    # Validation
    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe requis"}), 400

    # Get user first to check existence
    user_service = UserService()
    user = user_service.get_by_username(username) or user_service.get_by_email(username)

    if not user:
        return jsonify({"error": "Identifiants invalides"}), 401

    # Check if user is active
    if not user.is_active:
        return jsonify({"error": "Compte désactivé"}), 401

    # Check password
    if not user.check_password(password):
        return jsonify({"error": "Identifiants invalides"}), 401

    # Login user with Flask-Login (pass User object, not ID)
    login_user(user, remember=True)

    # TODO: Check if 2FA is enabled, redirect to 2FA verification if needed

    # Return success with redirect URL
    return jsonify(
        {
            "success": True,
            "message": "Connexion réussie",
            "redirect": url_for("pages.dashboard"),
        }
    )


@auth.route("/logout", methods=["GET", "POST"])
def logout() -> Any:
    """
    Log out current user

    Returns:
        Redirect to login page or JSON for AJAX requests
    """
    logout_user()

    # If AJAX request, return JSON
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "success": True,
                "message": "Déconnexion réussie",
                "redirect": url_for("auth.login_page"),
            }
        )

    # Otherwise, redirect directly
    return redirect(url_for("auth.login_page"))


@auth.route("/status", methods=["GET"])
def status() -> Any:
    """
    Check authentication status (API endpoint)

    Returns:
        JSON with authentication status
    """
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({"authenticated": False})

    # Get user info
    user_service = UserService()
    user = user_service.get_by_id(user_id)

    if not user:
        # User deleted, clear session
        logout_user()
        return jsonify({"authenticated": False})

    return jsonify(
        {
            "authenticated": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            },
        }
    )


# ---- Email Verification Routes ----


@auth.route("/send-verification", methods=["POST"])
@login_rate_limit()
def send_verification() -> Any:
    """
    Send email verification to current logged-in user.

    Returns:
        Redirect to email-sent page or error
    """
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({"error": "Non authentifié"}), 401

    user = User.query.get(user_id)
    if not user:
        logout_user()
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Generate token
    token = user.generate_email_verification_token()
    db.session.commit()

    # Send email
    email_service = EmailService()
    success = email_service.send_verification_email(
        user_email=user.email,
        user_name=user.username,
        verification_token=token,
    )

    if not success:
        return jsonify({"error": "Erreur lors de l'envoi de l'email"}), 500

    return render_template("auth/email-sent.html", email=user.email)


@auth.route("/verify-email/<token>", methods=["GET"])
def verify_email(token: str) -> Any:
    """
    Verify email using token.

    Args:
        token: Email verification token

    Returns:
        Rendered email-verified page or redirect to login
    """
    # Find user by token
    user = User.query.filter_by(email_verification_token=token).first()

    if not user:
        flash(t("auth.verify_email.error"), "error")
        return redirect(url_for("auth.login_page"))

    # Verify token
    if not user.verify_email_token(token):
        flash(t("auth.verify_email.expired"), "error")
        return redirect(url_for("auth.login_page"))

    # Mark email as verified
    user.mark_email_verified()
    db.session.commit()

    return render_template("auth/email-verified.html")


# ---- Password Reset Routes ----


@auth.route("/forgot-password", methods=["GET"])
def forgot_password_page() -> Any:
    """
    Display forgot password form.

    Returns:
        Rendered forgot-password.html template
    """
    return render_template("auth/forgot-password.html")


@auth.route("/forgot-password", methods=["POST"])
@login_rate_limit()
def forgot_password() -> Any:
    """
    Send password reset email.

    Expected form data:
        {
            "email": str
        }

    Returns:
        Rendered password-reset-sent page or error
    """
    email = request.form.get("email", "").strip()

    if not email:
        flash(t("auth.forgot.error.email_required"), "error")
        return render_template("auth/forgot-password.html")

    user = User.get_by_email(email)

    if user:
        # Generate reset token
        token = user.generate_password_reset_token()
        db.session.commit()

        # Send reset email
        email_service = EmailService()
        email_service.send_password_reset_email(
            user_email=user.email,
            user_name=user.username,
            reset_token=token,
        )

    # Always show success message for security (don't reveal if user exists)
    return render_template("auth/password-reset-sent.html", email=email)


@auth.route("/reset-password/<token>", methods=["GET"])
def reset_password_page(token: str) -> Any:
    """
    Display password reset form.

    Args:
        token: Password reset token

    Returns:
        Rendered reset-password.html or redirect to login if token invalid
    """
    user = User.query.filter_by(password_reset_token=token).first()

    if not user or not user.verify_password_reset_token(token):
        flash(t("auth.reset.error.invalid"), "error")
        return redirect(url_for("auth.login_page"))

    return render_template("auth/reset-password.html", token=token)


@auth.route("/reset-password/<token>", methods=["POST"])
def reset_password(token: str) -> Any:
    """
    Process password reset.

    Expected form data:
        {
            "password": str,
            "password_confirm": str
        }

    Returns:
        Redirect to login on success, form on error
    """
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")

    if not password or not password_confirm:
        flash(t("auth.reset.error.all_required"), "error")
        return render_template("auth/reset-password.html", token=token)

    if password != password_confirm:
        flash(t("auth.reset.error.mismatch"), "error")
        return render_template("auth/reset-password.html", token=token)

    if len(password) < 8:
        flash(t("auth.reset.error.password_short"), "error")
        return render_template("auth/reset-password.html", token=token)

    # Find user and reset password
    user = User.query.filter_by(password_reset_token=token).first()

    if not user or not user.reset_password_with_token(token, password):
        flash(t("auth.reset.error.generic"), "error")
        return redirect(url_for("auth.login_page"))

    db.session.commit()

    flash(t("auth.reset.success_connect"), "success")
    return redirect(url_for("auth.login_page"))


# ---- 2FA Routes (to be implemented) ----


@auth.route("/setup-2fa", methods=["GET"])
def setup_2fa_page() -> Any:
    """
    Display 2FA setup page

    Returns:
        Rendered setup-2fa.html template
    """
    # TODO: Implement 2FA setup with PyOTP
    return render_template("auth/setup-2fa.html")


@auth.route("/verify-2fa", methods=["POST"])
def verify_2fa() -> Any:
    """
    Verify 2FA code (HTMX)

    Expected JSON:
        {
            "code": str (6 digits)
        }

    Returns:
        JSON response with success/error
    """
    # TODO: Implement 2FA verification with PyOTP
    return jsonify({"error": "2FA non implémenté"}), 501
