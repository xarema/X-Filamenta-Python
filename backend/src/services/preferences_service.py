"""
------------------------------------------------------------------------------
Purpose: Preferences service layer
Description: Handles user preferences operations

File: backend/src/services/preferences_service.py | Repository: X-Filamenta-Python
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

from typing import Any

from backend.src.app import db
from backend.src.models.preferences import UserPreferences


class PreferencesService:
    """Service for user preferences management"""

    @staticmethod
    def get(user_id: int) -> UserPreferences | None:
        """Get or create preferences for a user"""
        return UserPreferences.get_or_create(user_id)

    @staticmethod
    def update(user_id: int, **kwargs: Any) -> UserPreferences | None:
        """Update preferences fields (theme, language, notifications)"""
        try:
            prefs = UserPreferences.get_or_create(user_id)
            allowed = {"theme", "language", "notifications"}
            for k, v in kwargs.items():
                if k in allowed and hasattr(prefs, k):
                    setattr(prefs, k, v)
            db.session.commit()
            return prefs
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def update_theme(user_id: int, theme: str) -> bool:
        if theme not in ["light", "dark", "auto"]:
            return False
        return PreferencesService.update(user_id, theme=theme) is not None

    @staticmethod
    def update_language(user_id: int, language: str) -> bool:
        if language not in ["fr", "en", "es"]:
            return False
        return PreferencesService.update(user_id, language=language) is not None

    @staticmethod
    def update_notifications(user_id: int, enabled: bool) -> bool:
        return PreferencesService.update(user_id, notifications=enabled) is not None

    @staticmethod
    def get_theme(user_id: int) -> str:
        prefs = PreferencesService.get(user_id)
        return prefs.theme if prefs else "light"

    @staticmethod
    def get_language(user_id: int) -> str:
        prefs = PreferencesService.get(user_id)
        return prefs.language if prefs else "fr"

    @staticmethod
    def to_dict(user_id: int) -> dict[str, Any]:
        prefs = PreferencesService.get(user_id)
        return (
            prefs.to_dict()
            if prefs
            else {
                "theme": "light",
                "language": "fr",
                "notifications": True,
            }
        )
