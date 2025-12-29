"""
------------------------------------------------------------------------------
Purpose: Content model
Description: SQLAlchemy model for content/posts

File: backend/src/models/content.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
------------------------------------------------------------------------------
"""

from datetime import datetime

from backend.src.extensions import db


class Content(db.Model):  # type: ignore[name-defined]
    """
    Content model

    Represents content/posts in the system (articles, pages, etc.)
    """

    __tablename__ = "content"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Content Data
    title = db.Column(db.String(200), nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)

    # Metadata
    type = db.Column(
        db.String(50), default="post", nullable=False, index=True
    )  # post, page, article

    status = db.Column(
        db.String(20), default="draft", nullable=False, index=True
    )  # draft, published, archived

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship
    author = db.relationship("User", back_populates="content")

    def __repr__(self) -> str:
        """String representation"""
        return f"<Content {self.title}>"

    def to_dict(self, include_body: bool = False) -> dict:
        """
        Convert content to dictionary

        Args:
            include_body: Whether to include full body text

        Returns:
            Dictionary representation of content
        """
        data = {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "status": self.status,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_body:
            data["body"] = self.body
        else:
            # Include excerpt (first 200 chars)
            excerpt = self.body[:200]
            data["excerpt"] = excerpt + "..." if len(self.body) > 200 else self.body

        if self.author:
            data["author"] = {"id": self.author.id, "username": self.author.username}

        return data
