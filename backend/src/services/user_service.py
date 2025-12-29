"""
------------------------------------------------------------------------------
Purpose: User service layer
Description: Handles user-related operations (CRUD, authentication, permissions)

File: backend/src/services/user_service.py | Repository: X-Filamenta-Python
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
- Real database integration with SQLAlchemy
- Handles user authentication and authorization
------------------------------------------------------------------------------
"""

from typing import Any, cast

from backend.src.extensions import db
from backend.src.models.preferences import UserPreferences
from backend.src.models.user import User


class UserService:
    """Service for user-related operations with database integration"""

    # ---- CRUD Operations ----

    @staticmethod
    def create(
        username: str,
        email: str,
        password: str,
        is_admin: bool = False,
        session: Any | None = None,
    ) -> User | None:
        """
        Create a new user

        Args:
            username: Username
            email: Email address
            password: Plain text password (will be hashed)
            is_admin: Whether user is admin
            session: Optional SQLAlchemy session to use

        Returns:
            User object if successful, None otherwise
        """
        try:
            db_session = session or db.session

            # Check if user already exists
            # Note: We must use the provided session for the query too if we want it to work
            existing_user = (
                db_session.query(User)
                .filter((User.username == username) | (User.email == email))
                .first()
            )
            if existing_user:
                return None

            user = User(
                username=username, email=email, is_admin=is_admin, is_active=True
            )
            user.set_password(password)

            db_session.add(user)
            db_session.commit()

            # Create default preferences
            prefs = UserPreferences(user_id=user.id)
            db_session.add(prefs)
            db_session.commit()

            return user
        except Exception:
            db_session.rollback()
            return None

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        """Get user by ID"""
        return cast(User | None, User.query.get(user_id))

    @staticmethod
    def get_by_username(username: str) -> User | None:
        """Get user by username"""
        return User.get_by_username(username)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        """Get user by email"""
        return User.get_by_email(email)

    @staticmethod
    def get_all(active_only: bool = True) -> list[User]:
        """
        Get all users

        Args:
            active_only: Only return active users

        Returns:
            List of User objects
        """
        query = User.query
        if active_only:
            query = query.filter_by(is_active=True)
        return cast(list[User], query.all())

    @staticmethod
    def update(user_id: int, **kwargs: Any) -> User | None:
        """
        Update user

        Args:
            user_id: User ID
            **kwargs: Fields to update

        Returns:
            Updated User object or None
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None

            for key, value in kwargs.items():
                if hasattr(user, key) and key != "password_hash":
                    setattr(user, key, value)

            db.session.commit()
            return cast(User | None, user)
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def delete(user_id: int) -> bool:
        """Delete user (soft delete by setting is_active=False)"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            user.is_active = False
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    # ---- Authentication & Authorization ----

    @staticmethod
    def authenticate(username: str, password: str) -> User | None:
        """
        Authenticate user

        Args:
            username: Username or email
            password: Plain text password

        Returns:
            User object if authenticated, None otherwise
        """
        user = User.get_by_username(username) or User.get_by_email(username)

        if user and user.is_active and user.check_password(password):
            return user
        return None

    @staticmethod
    def is_admin(user: User | None) -> bool:
        """Check if user is admin"""
        return user.is_admin if user else False

    @staticmethod
    def is_authenticated(user: User | None) -> bool:
        """Check if user is authenticated"""
        return user is not None and user.is_active

    @staticmethod
    def has_permission(user: User | None, action: str) -> bool:
        """
        Check if user has permission for action

        Args:
            user: User object
            action: Action to check

        Returns:
            True if user has permission
        """
        if not user or not user.is_active:
            return False

        # Admin has all permissions
        if user.is_admin:
            return True

        # Regular users can view public content
        return action in ["view_public", "post_comment"]

    # ---- Preferences ----

    @staticmethod
    def get_preferences(user_id: int) -> UserPreferences | None:
        """Get user preferences"""
        return UserPreferences.get_or_create(user_id)
