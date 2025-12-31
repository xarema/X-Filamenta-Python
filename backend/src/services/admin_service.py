"""
Purpose: Admin service for centralized admin operations
Description: CRUD operations for users and content with audit logging

File: backend/src/services/admin_service.py | Repository: X-Filamenta-Python
Created: 2025-12-30T00:40:00+01:00
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
- Centralizes all admin operations
- Includes audit logging via AdminHistory
"""

from typing import Any

from flask import current_app

from backend.src.extensions import db
from backend.src.models.admin_history import AdminHistory
from backend.src.models.content import Content
from backend.src.models.user import User
from backend.src.services.user_service import UserService


class AdminService:
    """Centralized service for admin operations with audit logging."""

    # ---- User CRUD ----

    @staticmethod
    def create_user(
        username: str,
        email: str,
        password: str,
        is_admin: bool = False,
        is_active: bool = True,
        send_email: bool = False,
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> User:
        """
        Create new user (admin action).

        Args:
            username: Username
            email: Email address
            password: Plain password (will be hashed)
            is_admin: Admin flag
            is_active: Active flag
            send_email: Send welcome email
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            Created user

        Raises:
            ValueError: If user already exists
        """
        # Create user via UserService
        user = UserService.create(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin,
        )

        if not user:
            raise ValueError(f"User {username} or {email} already exists")

        # Update is_active if needed
        if not is_active:
            user.is_active = False
            db.session.commit()

        # Log action
        if admin_user:
            AdminService._log_action(
                admin_user=admin_user,
                action="user_created",
                description=f"Created user: {username} ({email})",
                ip_address=ip_address,
            )

        # Send welcome email if requested
        if send_email:
            # TODO: Implement EmailService.send_welcome_email() in Sprint 2
            current_app.logger.info(f"Welcome email requested for {user.email} (not implemented yet)")
            # try:
            #     from backend.src.services.email_service import EmailService
            #     EmailService().send_welcome_email(user.email, username)
            # except Exception as e:
            #     current_app.logger.warning(f"Failed to send welcome email: {e}")

        return user

    @staticmethod
    def update_user(
        user_id: int,
        updates: dict[str, Any],
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> User:
        """
        Update user (admin action).

        Args:
            user_id: User ID to update
            updates: Dict of fields to update
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            Updated user

        Raises:
            ValueError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Track changes for audit
        changes = []

        # Update fields
        for field, value in updates.items():
            if hasattr(user, field):
                old_value = getattr(user, field)
                if old_value != value:
                    setattr(user, field, value)
                    changes.append(f"{field}: {old_value} → {value}")

        # Special: password update
        if "password" in updates:
            user.set_password(updates["password"])
            changes.append("password: [CHANGED]")

        db.session.commit()

        # Invalidate cache
        UserService.invalidate_cache(user)

        # Log action
        if admin_user and changes:
            AdminService._log_action(
                admin_user=admin_user,
                action="user_updated",
                description=f"Updated user {user.username}: {', '.join(changes)}",
                ip_address=ip_address,
            )

        return user

    @staticmethod
    def delete_user(
        user_id: int,
        hard_delete: bool = False,
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> bool:
        """
        Delete user (soft or hard).

        Args:
            user_id: User ID to delete
            hard_delete: True for hard delete, False for soft
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            True if deleted

        Raises:
            ValueError: If user not found or cannot delete self
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Prevent self-delete
        if admin_user and user.id == admin_user.id:
            raise ValueError("Cannot delete yourself")

        username = user.username

        if hard_delete:
            # Hard delete: remove from DB
            db.session.delete(user)
            action = "user_hard_deleted"
        else:
            # Soft delete: mark inactive
            user.is_active = False
            action = "user_soft_deleted"

        db.session.commit()

        # Invalidate cache
        UserService.invalidate_cache(user)

        # Log action
        if admin_user:
            AdminService._log_action(
                admin_user=admin_user,
                action=action,
                description=f"Deleted user: {username} (ID: {user_id})",
                ip_address=ip_address,
            )

        return True

    # ---- Content CRUD ----

    @staticmethod
    def create_content(
        key: str,
        value: str,
        language: str = "en",
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> Content:
        """
        Create content entry.

        Args:
            key: Content key
            value: Content value
            language: Language code
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            Created content
        """
        content = Content(key=key, value=value, language=language)
        db.session.add(content)
        db.session.commit()

        # Log action
        if admin_user:
            AdminService._log_action(
                admin_user=admin_user,
                action="content_created",
                description=f"Created content: {key} ({language})",
                ip_address=ip_address,
            )

        return content

    @staticmethod
    def update_content(
        content_id: int,
        updates: dict[str, Any],
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> Content:
        """
        Update content entry.

        Args:
            content_id: Content ID
            updates: Dict of fields to update
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            Updated content

        Raises:
            ValueError: If content not found
        """
        content = Content.query.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")

        changes = []
        for field, value in updates.items():
            if hasattr(content, field):
                old_value = getattr(content, field)
                if old_value != value:
                    setattr(content, field, value)
                    changes.append(f"{field}: {old_value} → {value}")

        db.session.commit()

        # Log action
        if admin_user and changes:
            AdminService._log_action(
                admin_user=admin_user,
                action="content_updated",
                description=f"Updated content {content.key}: {', '.join(changes)}",
                ip_address=ip_address,
            )

        return content

    @staticmethod
    def delete_content(
        content_id: int,
        admin_user: User | None = None,
        ip_address: str | None = None,
    ) -> bool:
        """
        Delete content entry.

        Args:
            content_id: Content ID
            admin_user: Admin performing action
            ip_address: Admin IP address

        Returns:
            True if deleted

        Raises:
            ValueError: If content not found
        """
        content = Content.query.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")

        key = content.key
        db.session.delete(content)
        db.session.commit()

        # Log action
        if admin_user:
            AdminService._log_action(
                admin_user=admin_user,
                action="content_deleted",
                description=f"Deleted content: {key} (ID: {content_id})",
                ip_address=ip_address,
            )

        return True

    # ---- Audit Logging ----

    @staticmethod
    def _log_action(
        admin_user: User,
        action: str,
        description: str,
        ip_address: str | None = None,
    ) -> None:
        """
        Log admin action to AdminHistory.

        Args:
            admin_user: Admin performing action
            action: Action type
            description: Action description
            ip_address: IP address
        """
        try:
            history = AdminHistory(
                admin_id=admin_user.id,
                action=action,
                description=description,
                ip_address=ip_address or "unknown",
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to log admin action: {e}")
            db.session.rollback()

