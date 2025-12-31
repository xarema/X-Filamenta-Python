"""
---
Purpose: Script de comparaison des fichiers de traduction EN et FR et ES
Description: Identifie les clés manquantes dans fr. json par rapport à en.json par rapport à es.json

File: scripts/compare_i18n.py | Repository: X-Filamenta-Python
Created: 2025-12-30T12:00:00-05:00
Last modified (Git): TBD | Commit: TBD

Distributed by:  XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License:  AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status:  Stable
- Classification: Internal

Notes:
- Utilisé pour identifier les traductions manquantes
---
"""

import json
from pathlib import Path
from typing import Any


def get_all_keys(d: dict[str, Any], parent_key: str = "") -> set[str]:
    """
    Extrait récursivement toutes les clés d'un dictionnaire imbriqué.

    Args:
        d:  Dictionnaire à parcourir
        parent_key:  Clé parente (pour la récursion)

    Returns:
        Set de toutes les clés au format "parent. child. grandchild"
    """
    keys = set()
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        keys.add(new_key)
        if isinstance(v, dict):
            keys.update(get_all_keys(v, new_key))
    return keys


def main() -> None:
    """Compare les fichiers de traduction EN, FR et ES."""
    base_path = Path(__file__).parent.parent
    en_path = base_path / "backend" / "src" / "i18n" / "translations" / "en.json"
    fr_path = base_path / "backend" / "src" / "i18n" / "translations" / "fr.json"
    es_path = base_path / "backend" / "src" / "i18n" / "translations" / "es.json"

    # Charger les fichiers
    with open(en_path, encoding="utf-8") as f:
        en_data = json.load(f)

    with open(fr_path, encoding="utf-8") as f:
        fr_data = json.load(f)

    with open(es_path, encoding="utf-8") as f:
        es_data = json.load(f)

    # Extraire toutes les clés
    en_keys = get_all_keys(en_data)
    fr_keys = get_all_keys(fr_data)
    es_keys = get_all_keys(es_data)

    # Trouver les différences
    missing_in_fr = en_keys - fr_keys
    missing_in_en = fr_keys - en_keys
    missing_in_es = en_keys - es_keys
    extra_in_fr = fr_keys - en_keys
    extra_in_es = es_keys - en_keys

    # Afficher les résultats
    print("=" * 80)
    print("Comparaison des fichiers de traduction")
    print("=" * 80)
    print(f"\nClés EN: {len(en_keys)}")
    print(f"Clés FR: {len(fr_keys)}")
    print(f"Clés ES: {len(es_keys)}")
    print(f"\n{'=' * 80}\n")

    if missing_in_fr:
        print(f"🔴 Clés manquantes dans FR ({len(missing_in_fr)}):")
        print("-" * 80)
        for key in sorted(missing_in_fr):
            print(f"  - {key}")
        print()
    else:
        print("✅ Aucune clé manquante dans FR\n")

    if extra_in_fr:
        print(f"⚠️  Clés en trop dans FR ({len(extra_in_fr)}):")
        print("-" * 80)
        for key in sorted(extra_in_fr):
            print(f"  - {key}")
        print()

    if missing_in_es:
        print(f"🔴 Clés manquantes dans ES ({len(missing_in_es)}):")
        print("-" * 80)
        for key in sorted(missing_in_es):
            print(f"  - {key}")
        print()
    else:
        print("✅ Aucune clé manquante dans ES\n")

    if extra_in_es:
        print(f"⚠️  Clés en trop dans ES ({len(extra_in_es)}):")
        print("-" * 80)
        for key in sorted(extra_in_es):
            print(f"  - {key}")
        print()

    print("=" * 80)

    # Sauvegarder le rapport
    report_path = base_path / ".github" / "i18n-comparison-report. md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Rapport de comparaison i18n\n\n")
        f.write(f"**Date:** 2025-12-30\n\n")
        f.write(f"**Clés EN:** {len(en_keys)}  \n")
        f.write(f"**Clés FR:** {len(fr_keys)}  \n")
        f.write(f"**Clés ES:** {len(es_keys)}  \n\n")
        f.write("---\n\n")

        if missing_in_fr:
            f.write(f"## 🔴 Clés manquantes dans FR ({len(missing_in_fr)})\n\n")
            for key in sorted(missing_in_fr):
                f.write(f"- `{key}`\n")
            f.write("\n")
        else:
            f.write("## ✅ Aucune clé manquante dans FR\n\n")

        if extra_in_fr:
            f.write(f"## ⚠️ Clés en trop dans FR ({len(extra_in_fr)})\n\n")
            for key in sorted(extra_in_fr):
                f.write(f"- `{key}`\n")
            f.write("\n")

        if missing_in_es:
            f.write(f"## 🔴 Clés manquantes dans ES ({len(missing_in_es)})\n\n")
            for key in sorted(missing_in_es):
                f.write(f"- `{key}`\n")
            f.write("\n")
        else:
            f.write("## ✅ Aucune clé manquante dans ES\n\n")

        if extra_in_es:
            f.write(f"## ⚠️ Clés en trop dans ES ({len(extra_in_es)})\n\n")
            for key in sorted(extra_in_es):
                f.write(f"- `{key}`\n")
            f.write("\n")

    print(f"\n✅ Rapport sauvegardé: {report_path}")


if __name__ == "__main__":
    main()
