"""
------------------------------------------------------------------------------
Purpose: Authentication helper functions
Description: Centralized auth helpers to avoid duplication

File: backend/src/utils/auth_helpers.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:40:00+00:00
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
- Centralized auth helpers
- Avoids duplication across routes
- Session management utilities
------------------------------------------------------------------------------
"""

from flask import session


def is_authenticated() -> bool:
    """
    Check if user is authenticated

    Returns:
        True if user_id exists in session
    """
    return "user_id" in session


def get_current_user_id() -> int | None:
    """
    Get current user ID from session

    Returns:
        User ID if authenticated, None otherwise
    """
    return session.get("user_id")


def login_user(user_id: int) -> None:
    """
    Log in user by setting session

    Args:
        user_id: User ID to log in
    """
    session["user_id"] = user_id
    session.permanent = True  # Use permanent session (configurable timeout)


def logout_user() -> None:
    """
    Log out user by clearing session
    """
    session.pop("user_id", None)
    session.clear()
