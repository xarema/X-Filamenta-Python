"""
------------------------------------------------------------------------------
Purpose: Admin History model
Description: Track admin actions for audit trail

File: backend/src/models/admin_history.py | Repository: X-Filamenta-Python
Created: 2025-12-27T21:10:00+00:00
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
- Audit trail for admin actions
- JSON details for flexibility
- Indexed for performance
------------------------------------------------------------------------------
"""

from datetime import datetime

from backend.src.extensions import db


class AdminHistory(db.Model):
    """
    Admin History model

    Tracks actions performed by administrators for audit purposes.
    """

    __tablename__ = "admin_history"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    admin_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Action Details
    action = db.Column(
        db.String(100), nullable=False, index=True
    )  # e.g., "user_create"
    target_type = db.Column(
        db.String(50), nullable=True
    )  # e.g., "user", "content", "settings"
    target_id = db.Column(db.Integer, nullable=True)  # ID of affected entity
    details = db.Column(db.Text, nullable=True)  # JSON with additional info

    # Metadata
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    user_agent = db.Column(db.String(255), nullable=True)

    # Timestamp
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Relationships
    admin = db.relationship("User", foreign_keys=[admin_id], backref="admin_actions")

    def __repr__(self) -> str:
        """String representation"""
        return f"<AdminHistory {self.action} by admin_id={self.admin_id}>"

    def to_dict(self) -> dict:
        """
        Convert to dictionary

        Returns:
            Dictionary representation
        """
        import json

        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "details": json.loads(self.details) if self.details else None,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    @staticmethod
    def log_action(
        admin_id: int,
        action: str,
        target_type: str | None = None,
        target_id: int | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> "AdminHistory":
        """
        Log an admin action

        Args:
            admin_id: ID of admin performing action
            action: Action name (e.g., "user_create", "user_delete")
            target_type: Type of target entity (optional)
            target_id: ID of target entity (optional)
            details: Additional details as dict (optional)
            ip_address: IP address of request (optional)
            user_agent: User agent string (optional)

        Returns:
            Created AdminHistory instance
        """
        import json

        entry = AdminHistory(
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.session.add(entry)
        return entry
