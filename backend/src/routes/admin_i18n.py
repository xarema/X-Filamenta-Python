"""
------------------------------------------------------------------------------
Purpose: i18n administration routes
Description: CRUD for translation files using Tabulator.js

File: backend/src/routes/admin_i18n.py | Repository: X-Filamenta-Python
Created: 2025-12-30T13:40:00+01:00
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

import json
import os
from typing import Any, Dict, List, Tuple

from flask import Blueprint, jsonify, render_template, request, current_app, Response
from backend.src.decorators import require_admin
from backend.src.utils import i18n

admin_i18n = Blueprint("admin_i18n", __name__, url_prefix="/admin/i18n")

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, str]:
    """Flatten a nested dictionary."""
    items: List[Tuple[str, str]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v)))
    return dict(items)

def set_nested_key(d: Dict[str, Any], key: str, value: str) -> None:
    """Set a value in a nested dictionary using dot notation."""
    keys = key.split('.')
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value

@admin_i18n.route("/translations", methods=["GET"])
@require_admin
def translations_page() -> str:
    """Render the translations management page."""
    languages = i18n.get_available_languages()
    return render_template("admin/translations.html", languages=languages)

@admin_i18n.route("/api/translations/<lang>", methods=["GET"])
@require_admin
def get_translations(lang: str) -> Any:
    """API endpoint to get flattened translations for a language."""
    translations = i18n.get_all_translations(lang)
    flat = flatten_dict(translations)

    # Format for Tabulator
    rows = [{"key": k, "value": v} for k, v in flat.items()]
    return jsonify(rows)

@admin_i18n.route("/api/translations/<lang>", methods=["POST"])
@require_admin
def update_translation(lang: str) -> Any:
    """API endpoint to update a single translation key."""
    data = request.get_json()
    if not data or "key" not in data or "value" not in data:
        return jsonify({"success": False, "error": "Invalid data"}), 400

    key = data["key"]
    value = data["value"]

    # Load original file to maintain structure
    # current_app.root_path points to backend/src usually if started via app.py
    # Let's use a more robust way to find the translations dir
    trans_dir = os.path.join(os.getcwd(), "backend", "src", "i18n", "translations")
    file_path = os.path.join(trans_dir, f"{lang}.json")

    if not os.path.exists(file_path):
        return jsonify({"success": False, "error": f"File not found at {file_path}"}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        set_nested_key(translations, key, value)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)

        # Reload memory cache
        i18n.reload_translations()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
