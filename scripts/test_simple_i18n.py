import sys
import io
from pathlib import Path

# Force UTF-8 encoding for console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.src.utils.i18n import init_translations, _translations

print("Initialisation...")
init_translations(project_root)

if _translations:
    print(f"\nLangues disponibles: {list(_translations.translations.keys())}")

    test_keys = [
        "footer.legal",
        "pages.about.cta_source",
        "admin.users.table.name",
    ]

    for lang in ["fr", "en"]:
        print(f"\n[{lang.upper()}]")
        for key in test_keys:
            val = _translations.get(key, lang)
            print(f"  {key}: {val}")

