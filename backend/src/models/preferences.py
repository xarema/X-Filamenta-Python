"""
------------------------------------------------------------------------------
Purpose: User preferences model
Description: SQLAlchemy model for user preferences

File: backend/src/models/preferences.py | Repository: X-Filamenta-Python
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
------------------------------------------------------------------------------
"""

from typing import cast

from backend.src.extensions import db


class UserPreferences(db.Model):  # type: ignore[name-defined]
    """
    User preferences model

    Stores user-specific preferences (theme, language, notifications, etc.)
    One-to-one relationship with User.
    """

    __tablename__ = "user_preferences"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # Preferences
    theme = db.Column(
        db.String(20), default="light", nullable=False
    )  # light, dark, auto

    language = db.Column(db.String(10), default="fr", nullable=False)  # fr, en, es

    notifications = db.Column(db.Boolean, default=True, nullable=False)

    # Relationship
    user = db.relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        """String representation"""
        return f"<UserPreferences user_id={self.user_id}>"

    def to_dict(self) -> dict:
        """
        Convert preferences to dictionary

        Returns:
            Dictionary representation of preferences
        """
        return {
            "theme": self.theme,
            "language": self.language,
            "notifications": self.notifications,
        }

    @staticmethod
    def get_or_create(user_id: int) -> "UserPreferences":
        """
        Get preferences for user, or create default if not exists

        Args:
            user_id: User ID

        Returns:
            UserPreferences object
        """
        preferences = cast(
            "UserPreferences | None",
            UserPreferences.query.filter_by(user_id=user_id).first(),
        )

        if not preferences:
            preferences = UserPreferences(user_id=user_id)
            db.session.add(preferences)
            db.session.commit()

        assert preferences is not None
        return preferences
