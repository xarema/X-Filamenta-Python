"""
------------------------------------------------------------------------------
Purpose: i18n service
Description: Load translations and provide lookup with fallback (EN default).

File: backend/src/services/i18n_service.py | Repository: X-Filamenta-Python
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
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

DEFAULT_LANG = "en"
SUPPORTED_LANGS = {"en", "fr"}


def _load_lang(path: str) -> dict[str, Any]:
    """
    Load language JSON file from disk (private helper).

    Args:
        path: Full file path to language JSON file

    Returns:
        dict with translation keys and values

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    with open(path, encoding="utf-8") as fp:
        return cast(dict[str, Any], json.load(fp))


@lru_cache(maxsize=4)
def load_translations(lang: str, base_path: str) -> dict[str, Any]:
    """
    Load translations for specified language with fallback to default.

    Caches up to 4 language files for performance. Falls back to English
    if requested language not available.

    Args:
        lang: Language code (e.g. 'en', 'fr')
        base_path: Base directory containing language files

    Returns:
        dict with all translation keys and values for language

    Example:
        >>> trans = load_translations('fr', '/app/i18n')
        >>> assert 'auth.login' in trans
    """
    lang_key = lang if lang in SUPPORTED_LANGS else DEFAULT_LANG
    target = os.path.join(base_path, f"{lang_key}.json")
    if not os.path.exists(target):
        target = os.path.join(base_path, f"{DEFAULT_LANG}.json")
    return _load_lang(target)


def t(lang: str, key: str, base_path: str) -> str:
    """
    Translate key to specified language with dot-notation support.

    Supports nested keys using dot notation (e.g. 'auth.login.title').
    Returns the original key if translation not found.

    Args:
        lang: Language code (e.g. 'en', 'fr')
        key: Translation key using dot notation (e.g. 'auth.login.title')
        base_path: Base directory containing language files

    Returns:
        Translated string, or original key if not found

    Example:
        >>> result = t('fr', 'auth.login', '/app/i18n')
        >>> assert isinstance(result, str)
    """
    data = load_translations(lang, base_path)
    node: Any = data
    for part in key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return key
    if isinstance(node, str):
        return node
    return key


def available_languages(base_path: str | None = None) -> dict[str, str]:
    """
    Get list of supported languages with display names.

    Auto-detects available languages from JSON files in i18n directory.

    Args:
        base_path: Base directory containing language files (optional)

    Returns:
        dict mapping language codes to display names

    Example:
        >>> langs = available_languages()
        >>> assert 'en' in langs
        >>> assert 'fr' in langs
    """
    # Map of language codes to display names
    lang_names = {
        "en": "English",
        "fr": "Français",
        "es": "Español",
        "de": "Deutsch",
        "it": "Italiano",
        "pt": "Português",
        "ru": "Русский",
        "zh": "中文",
        "ja": "日本語",
        "ar": "العربية",
    }

    # If no base_path provided, use default i18n directory
    if base_path is None:
        try:
            current_dir = Path(__file__).resolve().parent.parent
            base_path = str(current_dir / "i18n")
        except Exception:
            return {"en": "English", "fr": "Français"}

    # Get supported languages from JSON files in base_path
    supported = [f.stem for f in Path(base_path).glob("*.json")]

    return {lang: lang_names.get(lang, lang.upper()) for lang in supported}
