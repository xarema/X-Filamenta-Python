"""
Purpose: Email service for sending application emails
Description: Multi-provider email service with template support, encryption, and logging

File: backend/src/services/email_service.py | Repository: X-Filamenta-Python
Created: 2025-12-29T02:45:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Supports Mailtrap (dev) and SendGrid (prod)
- HTML + plaintext email formats
- Jinja2 template rendering
"""

import logging
import secrets
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from flask import current_app, render_template

from backend.src.models.settings import Settings

logger = logging.getLogger(__name__)


class EmailToken:
    """Generate and validate time-expiring email tokens."""

    TOKEN_LENGTH = 32

    @staticmethod
    def generate() -> str:
        """Generate secure email token."""
        return secrets.token_urlsafe(EmailToken.TOKEN_LENGTH)

    @staticmethod
    def validate(token: str, expiry_datetime: datetime) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() < expiry_datetime


class EmailService:
    """
    Email service handling verification and reset emails.

    Supports:
    - Email verification workflow
    - Password reset workflow
    - HTML and plaintext formats
    - Multiple SMTP providers (Mailtrap, SendGrid)
    - Template rendering with Jinja2
    """

    # Email format options
    FORMAT_HTML_ONLY = "html_only"
    FORMAT_TXT_ONLY = "txt_only"
    FORMAT_HTML_WITH_FALLBACK = "html_with_fallback"

    def __init__(self):
        """Initialize email service with configuration from Settings."""
        self.host = Settings.get("smtp_host", "smtp.mailtrap.io")
        self.port = int(Settings.get("smtp_port", 465))
        self.username = Settings.get("smtp_user", "")
        self.password = Settings.get("smtp_password", "")
        self.use_tls = bool(Settings.get("smtp_tls_enabled", True))
        self.from_email = Settings.get("smtp_from_email", "noreply@example.com")
        self.from_name = Settings.get("smtp_from_name", "X-Filamenta")
        self.email_format = Settings.get("email_format", self.FORMAT_HTML_WITH_FALLBACK)

    def send_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: dict[str, Any],
        reply_to: str | None = None,
    ) -> bool:
        """
        Send email using template.

        Args:
            to_email: Recipient email address
            subject: Email subject
            template_name: Template name (without .html/.txt extension)
            context: Template context variables
            reply_to: Reply-to email address (optional)

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Prepare message
            msg = MIMEMultipart("alternative")
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            if reply_to:
                msg["Reply-To"] = reply_to

            # Render templates based on format setting
            text_body = None
            html_body = None

            if self.email_format in [
                self.FORMAT_TXT_ONLY,
                self.FORMAT_HTML_WITH_FALLBACK,
            ]:
                try:
                    text_body = render_template(
                        f"emails/{template_name}.txt",
                        **context,
                    )
                except Exception as e:
                    logger.warning(f"Failed to render text template: {e}")

            if self.email_format in [
                self.FORMAT_HTML_ONLY,
                self.FORMAT_HTML_WITH_FALLBACK,
            ]:
                try:
                    html_body = render_template(
                        f"emails/{template_name}.html",
                        **context,
                    )
                except Exception as e:
                    logger.warning(f"Failed to render HTML template: {e}")

            # Attach text part
            if text_body:
                msg.attach(MIMEText(text_body, "plain", "utf-8"))

            # Attach HTML part
            if html_body:
                msg.attach(MIMEText(html_body, "html", "utf-8"))

            # Send email
            self._send_smtp(msg, to_email)

            logger.info(f"Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def _send_smtp(self, msg: MIMEMultipart, to_email: str) -> None:
        """Send email via SMTP."""
        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()

            if self.username and self.password:
                server.login(self.username, self.password)

            server.send_message(msg, to_addrs=[to_email])

    def send_verification_email(
        self,
        user_email: str,
        user_name: str,
        verification_token: str,
    ) -> bool:
        """
        Send email verification link.

        Args:
            user_email: User email address
            user_name: User display name
            verification_token: Token for verification

        Returns:
            True if sent successfully
        """
        site_url = Settings.get(
            "site_url", current_app.config.get("SERVER_NAME", "http://localhost:5000")
        )
        verification_link = f"{site_url}/auth/verify-email/{verification_token}"

        context = {
            "user_name": user_name,
            "verification_link": verification_link,
            "expiry_hours": Settings.get("email_verification_token_expiry_hours", 24),
            "site_name": Settings.get("site_name", "X-Filamenta"),
        }
        site_name = Settings.get("site_name", "X-Filamenta")
        subject_key = "auth.email_verification_subject"
        subject_text = context.get(subject_key, "Email Verification")
        subject = f"{site_name} — {subject_text}"

        return self.send_email(
            to_email=user_email,
            subject=subject,
            template_name="verification",
            context=context,
        )

    def send_password_reset_email(
        self,
        user_email: str,
        user_name: str,
        reset_token: str,
    ) -> bool:
        """
        Send password reset link.

        Args:
            user_email: User email address
            user_name: User display name
            reset_token: Token for password reset

        Returns:
            True if sent successfully
        """
        site_url = Settings.get(
            "site_url", current_app.config.get("SERVER_NAME", "http://localhost:5000")
        )
        reset_link = f"{site_url}/auth/reset-password/{reset_token}"

        context = {
            "user_name": user_name,
            "reset_link": reset_link,
            "expiry_minutes": Settings.get("password_reset_token_expiry_minutes", 60),
            "site_name": Settings.get("site_name", "X-Filamenta"),
        }

        site_name = Settings.get("site_name", "X-Filamenta")
        subject_key = "auth.password_reset_subject"
        subject_text = context.get(subject_key, "Password Reset")
        subject = f"{site_name} — {subject_text}"

        return self.send_email(
            to_email=user_email,
            subject=subject,
            template_name="password_reset",
            context=context,
        )

    def test_smtp_connection(self) -> tuple[bool, str]:
        """
        Test SMTP connection with current settings.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()

                if self.username and self.password:
                    server.login(self.username, self.password)

            message = f"Successfully connected to {self.host}:{self.port}"
            logger.info(f"SMTP test: {message}")
            return True, message

        except smtplib.SMTPAuthenticationError:
            message = "SMTP authentication failed. Check username/password."
            logger.error(f"SMTP test: {message}")
            return False, message
        except smtplib.SMTPException as e:
            message = f"SMTP error: {str(e)}"
            logger.error(f"SMTP test: {message}")
            return False, message
        except Exception as e:
            message = f"Connection error: {str(e)}"
            logger.error(f"SMTP test: {message}")
            return False, message

    def generate_verification_token(self) -> str:
        """
        Generate a secure verification token.

        Returns:
            A secure token string.
        """
        return EmailToken.generate()


def send_verification_email_task(
    user_id: int,
    user_email: str,
    user_name: str,
) -> bool:
    """
    Send email verification (async-ready task).

    Args:
        user_id: User database ID
        user_email: User email address
        user_name: User display name

    Returns:
        True if sent successfully
    """
    from backend.src.models.user import User

    try:
        user = User.query.get(user_id)
        if not user:
            logger.error(f"User {user_id} not found for email verification")
            return False

        service = EmailService()
        return service.send_verification_email(
            user_email=user_email,
            user_name=user_name,
            verification_token=user.email_verification_token,
        )

    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        return False


def send_password_reset_email_task(
    user_email: str,
    user_name: str,
    reset_token: str,
) -> bool:
    """
    Send password reset email (async-ready task).

    Args:
        user_email: User email address
        user_name: User display name
        reset_token: Password reset token

    Returns:
        True if sent successfully
    """
    try:
        service = EmailService()
        return service.send_password_reset_email(
            user_email=user_email,
            user_name=user_name,
            reset_token=reset_token,
        )

    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return False
