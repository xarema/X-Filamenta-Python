"""
------------------------------------------------------------------------------
Purpose: Translation helper for Jinja templates
Description: Loads translations and provides t() function

File: backend/src/utils/i18n.py | Repository: X-Filamenta-Python
Created: 2025-12-28T17:50:00+01:00
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

from __future__ import annotations

import json
import os
from typing import Any

from flask import request, session


class Translations:
    """Simple translations manager"""

    def __init__(self, app_root: str) -> None:
        self.app_root = app_root
        self.translations: dict[str, dict[str, Any]] = {}
        self.supported_langs: set[str] = set()
        self.default_lang = "en"  # Fallback ultime si rien n'est détecté
        self.load_translations()

    def load_translations(self) -> None:
        """Load all translation files from i18n/translations directory"""
        # Priorité au nouveau dossier translations dans i18n
        trans_dir = os.path.join(self.app_root, "backend", "src", "i18n", "translations")

        # Fallback si le nouveau dossier n'existe pas
        if not os.path.exists(trans_dir):
            trans_dir = os.path.join(self.app_root, "backend", "src", "i18n")

        # Fallback ultime
        if not os.path.exists(trans_dir) or not any(
            f.endswith(".json") for f in os.listdir(trans_dir)
        ):
            trans_dir = os.path.join(self.app_root, "backend", "src", "translations")

        if not os.path.exists(trans_dir):
            return

        for filename in os.listdir(trans_dir):
            if filename.endswith(".json"):
                lang = filename.replace(".json", "")
                filepath = os.path.join(trans_dir, filename)

                try:
                    with open(filepath, encoding="utf-8") as f:
                        self.translations[lang] = json.load(f)
                        self.supported_langs.add(lang)
                except Exception as e:
                    # SEC-03: Log errors instead of silent pass
                    import logging

                    logging.warning(f"Failed to load i18n file {filepath}: {e}")

    def reload(self) -> None:
        """Clear and reload all translations"""
        self.translations.clear()
        self.supported_langs.clear()
        self.load_translations()

    def get_translations_for_lang(self, lang: str) -> dict[str, Any]:
        """Get all translations for a specific language"""
        return self.translations.get(lang, {})

    def get_available_languages(self) -> dict[str, str]:
        """Get list of available languages with display names"""
        # Map de codes langue → noms d'affichage
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

        return {
            lang: lang_names.get(lang, lang.upper()) for lang in self.supported_langs
        }

    def detect_browser_language(self) -> str:
        """
        Detect browser language from Accept-Language header.

        Returns:
            Language code (e.g. 'en', 'fr') or default language if not detected
        """
        if not request:
            return self.default_lang

        # Récupérer le header Accept-Language
        accept_languages = request.headers.get("Accept-Language", "")

        # Parser le header (format: "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7")
        for lang_entry in accept_languages.split(","):
            # Extraire le code langue (avant le '-' ou le ';')
            lang_code = lang_entry.split(";")[0].split("-")[0].strip().lower()

            # Si la langue est supportée, la retourner
            if lang_code in self.supported_langs:
                return lang_code

        # Fallback sur la langue par défaut
        return self.default_lang

    def get(self, key: str, lang: str | None = None, default: str = "") -> str:
        """
        Get translation by key (supports nested keys like 'wizard.title')

        Args:
            key: Translation key with dot notation
            lang: Language code (optional, auto-detected if None)
            default: Default value if key not found

        Returns:
            Translated string or default value
        """
        # Déterminer la langue à utiliser (ordre de priorité)
        if lang is None:
            # 1. Session (si l'utilisateur a choisi)
            # 2. Navigateur (détection automatique)
            # 3. Default (fallback)
            lang = session.get("lang") or self.detect_browser_language()

        if lang not in self.translations:
            lang = self.default_lang

        if lang not in self.translations:
            return default or key

        parts = key.split(".")
        value: Any = self.translations[lang]

        try:
            for part in parts:
                value = value[part]
            return str(value) if value else (default or key)
        except (KeyError, TypeError):
            return default or key


# Global instance
_translations: Translations | None = None


def init_translations(app_root: str) -> None:
    """Initialize translations"""
    global _translations
    _translations = Translations(app_root)


def get_translation(key: str, default: str = "") -> str:
    """Get translation for current session language (with browser detection)"""
    if _translations is None:
        return default or key

    # Récupère la langue ACTUELLEMENT en session/détectée
    lang: str | None = None
    try:
        # En contexte Flask: récupère depuis la session
        lang = session.get("lang")
    except (RuntimeError, AttributeError):
        # Hors contexte Flask (tests, etc.)
        pass

    # Si pas de langue en session, détecter du navigateur
    if not lang:
        lang = _translations.detect_browser_language()

    return _translations.get(key, lang, default)


def t(key: str, default: str = "") -> str:
    """Shortcut for get_translation - use CURRENT session language"""
    return get_translation(key, default)


def reload_translations() -> None:
    """Reload all translations"""
    if _translations:
        _translations.reload()


def get_all_translations(lang: str) -> dict[str, Any]:
    """Get all translations for a language"""
    if _translations:
        return _translations.get_translations_for_lang(lang)
    return {}


def get_available_languages() -> dict[str, str]:
    """Get list of available languages"""
    if _translations is None:
        return {"en": "English"}
    return _translations.get_available_languages()
