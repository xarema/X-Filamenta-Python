"""
------------------------------------------------------------------------------
Purpose: Content service layer
Description: Handles content/posts CRUD operations

File: backend/src/services/content_service.py | Repository: X-Filamenta-Python
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

from typing import Any, cast

from backend.src.app import db
from backend.src.models.content import Content


class ContentService:
    """Service for content management (posts, pages, articles)"""

    # ---- CRUD Operations ----

    @staticmethod
    def create(
        title: str,
        body: str,
        author_id: int,
        content_type: str = "post",
        status: str = "draft",
    ) -> Content | None:
        """
        Create new content

        Args:
            title: Content title
            body: Content body
            author_id: Author user ID
            content_type: Type (post, page, article)
            status: Status (draft, published, archived)

        Returns:
            Content object or None
        """
        try:
            content = Content(
                title=title,
                body=body,
                author_id=author_id,
                type=content_type,
                status=status,
            )

            db.session.add(content)
            db.session.commit()
            return content
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def get_by_id(content_id: int) -> Content | None:
        """
        Get content by ID with caching.

        Cache TTL: 120 seconds (2 minutes)
        """
        from backend.src.services.cache_service import cache_service

        # Try cache first
        cache_key = f"content:id:{content_id}"
        cached = cache_service.get(cache_key)
        if cached:
            return cached

        # Query database
        content = cast(Content | None, Content.query.get(content_id))

        # Cache result if found
        if content:
            cache_service.set(cache_key, content, ttl=120)

        return content

    @staticmethod
    def get_all(
        content_type: str | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Content], int]:
        """
        Get all content with filters and pagination with caching.

        Cache TTL: 120 seconds (2 minutes)

        Args:
            content_type: Filter by type (post, page, article)
            status: Filter by status (draft, published, archived)
            page: Page number (1-indexed)
            per_page: Items per page

        Returns:
            Tuple of (content list, total count)
        """
        from backend.src.services.cache_service import cache_service

        # Build cache key based on filters
        cache_key = (
            f"content:all:{content_type or 'all'}:{status or 'all'}:{page}:{per_page}"
        )
        cached = cache_service.get(cache_key)
        if cached:
            return cached

        query = Content.query

        if content_type:
            query = query.filter_by(type=content_type)

        if status:
            query = query.filter_by(status=status)

        # Eager load author relationship to avoid N+1 queries
        from sqlalchemy.orm import joinedload

        query = query.options(joinedload(Content.author))

        # Order by created_at desc
        query = query.order_by(Content.created_at.desc())

        # Get total count
        total = query.count()

        # Paginate
        offset = (page - 1) * per_page
        items = query.limit(per_page).offset(offset).all()

        result = (cast(list[Content], items), total)

        # Cache result
        cache_service.set(cache_key, result, ttl=120)

        return result

    @staticmethod
    def invalidate_cache(content_id: int | None = None) -> None:
        """
        Invalidate cache for content.

        Args:
            content_id: Specific content ID to invalidate, or None for all
        """
        from backend.src.services.cache_service import cache_service

        if content_id:
            cache_service.delete(f"content:id:{content_id}")

        # Note: For get_all cache, we'd need to track all possible keys
        # or use a more sophisticated cache invalidation strategy.
        # For now, we rely on TTL expiration (120 seconds).

    @staticmethod
    def get_published(
        content_type: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Content], int]:
        """Get published content only"""
        return ContentService.get_all(
            content_type=content_type, status="published", page=page, per_page=per_page
        )

    @staticmethod
    def get_by_author(
        author_id: int, page: int = 1, per_page: int = 20
    ) -> tuple[list[Content], int]:
        """
        Get content by author with eager loading.

        Args:
            author_id: Author user ID
            page: Page number
            per_page: Items per page

        Returns:
            Tuple of (content list, total count)
        """
        from sqlalchemy.orm import joinedload

        query = Content.query.filter_by(author_id=author_id)

        # Eager load author relationship
        query = query.options(joinedload(Content.author))

        query = query.order_by(Content.created_at.desc())

        total = query.count()
        offset = (page - 1) * per_page
        items = query.limit(per_page).offset(offset).all()
        return cast(list[Content], items), total

    @staticmethod
    def update(content_id: int, **kwargs: Any) -> Content | None:
        """
        Update content

        Args:
            content_id: Content ID
            **kwargs: Fields to update

        Returns:
            Updated Content object or None
        """
        try:
            content = Content.query.get(content_id)
            if not content:
                return None

            # Update allowed fields
            allowed_fields = ["title", "body", "type", "status"]
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(content, key):
                    setattr(content, key, value)

            db.session.commit()
            return cast(Content | None, content)
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def delete(content_id: int) -> bool:
        """
        Delete content

        Args:
            content_id: Content ID

        Returns:
            True if successful
        """
        try:
            content = Content.query.get(content_id)
            if not content:
                return False

            db.session.delete(content)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def publish(content_id: int) -> Content | None:
        """Publish content (set status to published)"""
        return ContentService.update(content_id, status="published")

    @staticmethod
    def archive(content_id: int) -> Content | None:
        """Archive content (set status to archived)"""
        return ContentService.update(content_id, status="archived")

    # ---- Search ----

    @staticmethod
    def search(
        query: str, content_type: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Content], int]:
        """
        Search content by title

        Args:
            query: Search query
            content_type: Filter by type
            page: Page number
            per_page: Items per page

        Returns:
            Tuple of (content list, total count)
        """
        search_query = Content.query.filter(Content.title.ilike(f"%{query}%"))

        if content_type:
            search_query = search_query.filter_by(type=content_type)

        search_query = search_query.order_by(Content.created_at.desc())

        total = search_query.count()
        offset = (page - 1) * per_page
        items = search_query.limit(per_page).offset(offset).all()
        return cast(list[Content], items), total
