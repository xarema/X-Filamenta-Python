"""
------------------------------------------------------------------------------
Purpose: API routes
Description: Flask Blueprint for API endpoints (health, data endpoints)

File: backend/src/routes/api.py | Repository: X-Filamenta-Python
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

Notes:
- RESTful API endpoints for data access
- Returns JSON responses
- Used by datagrid and other frontend components
- Support for pagination and filtering
------------------------------------------------------------------------------
"""

from typing import Any

from flask import Blueprint, current_app, jsonify, request

# ---- Blueprint Definition ----
api = Blueprint("api", __name__, url_prefix="/api")


# ---- Routes ----


@api.route("/health", methods=["GET"])
def health() -> Any:
    """
    Health check endpoint

    Returns JSON with application status

    Returns:
        JSON: {'status': 'ok', 'message': 'API is running'}
        HTTP 200
    """
    return jsonify(
        {"status": "ok", "message": "API is running", "version": "0.0.1-Alpha"}
    ), 200


@api.route("/config", methods=["GET"])
def config() -> Any:
    """
    Get application configuration

    Returns:
        JSON: Application configuration settings
        HTTP 200
    """
    return jsonify(
        {
            "app_name": "X-Filamenta-Python",
            "version": "0.0.1-Alpha",
            "api_version": "1.0",
            "environment": "development",
        }
    ), 200


@api.route("/version", methods=["GET"])
def version() -> Any:
    """
    Get application version

    Returns:
        JSON: Version information
        HTTP 200
    """
    return jsonify(
        {"app_version": "0.0.1-Alpha", "api_version": "1.0", "status": "stable"}
    ), 200


@api.route("/contact", methods=["POST"])
def contact() -> Any:
    """
    Process contact form submission

    Expected JSON body:
    {
        'name': 'string',
        'email': 'string',
        'message': 'string'
    }

    Returns:
        JSON: Success/error response
        HTTP 200 or 400
    """
    data = request.get_json()

    # Validate data is provided
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Validate required fields exist
    required_fields = ["name", "email", "message"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate name (1-100 chars)
    name = str(data.get("name", "")).strip()
    if not (1 <= len(name) <= 100):
        return jsonify({"error": "Name must be 1-100 characters"}), 400

    # Validate email format
    email = str(data.get("email", "")).strip()
    if not email or "@" not in email or len(email) > 254:
        return jsonify({"error": "Invalid email format"}), 400

    # Validate message (1-5000 chars)
    message = str(data.get("message", "")).strip()
    if not (1 <= len(message) <= 5000):
        return jsonify({"error": "Message must be 1-5000 characters"}), 400

    # TODO: Send email or save to database
    # For now, just acknowledge receipt
    current_app.logger.info(f"Contact form received from {email}")

    return jsonify(
        {
            "status": "success",
            "message": "Message received",
            "data": {"name": name, "email": email},
        }
    ), 200


@api.route("/data/stats", methods=["GET"])
def stats() -> Any:
    """
    Get application statistics

    Returns:
        JSON: Statistics data
        HTTP 200
    """
    # Placeholder stats - to be replaced with real data
    return jsonify(
        {
            "stats": {
                "users_total": 0,
                "content_items": 0,
                "errors_24h": 0,
                "visits_24h": 0,
            },
            "period": "24h",
        }
    ), 200


@api.route("/preferences", methods=["POST"])
def update_preferences() -> Any:
    """
    Update user preferences (HTMX endpoint)

    Expected JSON/Form body:
    {
        'theme': 'light|dark|auto',
        'language': 'fr|en|es',
        'notifications': true|false
    }

    Requires: User authentication (currently mock, will be real in PHASE 4)

    Returns:
        JSON: Success/error response
        HTTP 200 or 401
    """
    from backend.src.services.preferences_service import PreferencesService

    # For now, use admin user (mock)
    # TODO: Replace with real current_user in PHASE 4
    user_id = 1  # Assuming admin user ID is 1

    data = request.get_json() or request.form

    # Update preferences using service
    updated = PreferencesService.update(user_id, **data)

    if not updated:
        return jsonify({"error": "Failed to update preferences"}), 400

    current_app.logger.info(f"User {user_id} preferences updated")

    return jsonify(
        {
            "status": "success",
            "message": "Préférences mises à jour",
            "preferences": updated.to_dict(),
        }
    ), 200
