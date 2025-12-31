"""
Test de diagnostic des traductions i18n

Purpose: Script de test pour vérifier le fonctionnement du système de traductions
File: scripts/test_i18n_translations.py | Repository: X-Filamenta-Python
Created: 2025-12-30T17:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.src.utils.i18n import init_translations, get_translation, get_available_languages


def test_translations():
    """Test le système de traductions"""

    print("=" * 80)
    print("TEST DU SYSTEME DE TRADUCTIONS i18n")
    print("=" * 80)

    # 1. Initialiser
    print("\n[1] Initialisation des traductions...")
    init_translations(project_root)
    print("OK Initialise")

    # 2. Langues disponibles
    print("\n[2] Langues disponibles:")
    langs = get_available_languages()
    for code, name in langs.items():
        print(f"   - {code}: {name}")

    # 3. Test des clés problématiques
    print("\n[3] Test des cles problematiques:")
    test_keys = [
        "footer.legal",
        "pages.about.features",
        "pages.about.cta_source",
        "pages.contact.send",
        "admin.dashboard.stats.errors",
        "admin.users.table.name",
        "admin.users.form.email",
    ]

    for lang in ["fr", "en"]:
        print(f"\n   Langue: {lang.upper()}")
        for key in test_keys:
            from backend.src.utils.i18n import _translations
            value = _translations.get(key, lang) if _translations else key
            status = "OK" if value and value != key else "FAIL"
            print(f"      {status} {key:40} = {value[:50] if len(value) > 50 else value}")

    # 4. Statistiques
    print("\n[4] Statistiques:")
    from backend.src.utils.i18n import _translations

    if _translations and hasattr(_translations, 'translations'):
        for lang, trans_dict in _translations.translations.items():
            def count_keys(d, prefix=""):
                count = 0
                for k, v in d.items():
                    if isinstance(v, dict):
                        count += count_keys(v, f"{prefix}{k}.")
                    else:
                        count += 1
                return count

            total = count_keys(trans_dict)
            print(f"   - {lang}: {total} cles")

    print("\n" + "=" * 80)
    print("FIN DU TEST")
    print("=" * 80)


if __name__ == "__main__":
    test_translations()

