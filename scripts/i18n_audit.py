import os
import re
import json
from typing import Any

def audit_i18n() -> None:
    project_root: str = "."
    backend_src: str = os.path.join(project_root, "backend", "src")
    frontend_templates: str = os.path.join(project_root, "frontend", "templates")
    i18n_dir: str = os.path.join(backend_src, "i18n")

    # Regex for finding t('key') or t("key") or t('key', default='...')
    # Matches t('key') and t("key")
    t_regex: re.Pattern = re.compile(r"t\(['\"]([^'\"]+)['\"]")
    # Matches {{ t('key') }} or {{ t('key', 'default') }} in Jinja
    jinja_t_regex: re.Pattern = re.compile(r"\{\{\s*t\(['\"]([^'\"]+)['\"]")

    found_keys: dict[str, list[str]] = {} # key -> list of files

    # Analyze Python files
    python_files: list[str] = []
    for root, _, files in os.walk(backend_src):
        for file in files:
            if file.endswith(".py"):
                p_path: str = os.path.join(root, file)
                python_files.append(p_path)
                with open(p_path, "r", encoding="utf-8") as f:
                    p_content: str = f.read()
                    p_matches: list[str] = t_regex.findall(p_content)
                    for key in p_matches:
                        if key not in found_keys:
                            found_keys[key] = []
                        found_keys[key].append(p_path)

    # Analyze HTML files
    html_files: list[str] = []
    for root, _, files in os.walk(frontend_templates):
        for file in files:
            if file.endswith(".html"):
                h_path: str = os.path.join(root, file)
                html_files.append(h_path)
                with open(h_path, "r", encoding="utf-8") as f:
                    h_content: str = f.read()
                    h_matches: list[str] = jinja_t_regex.findall(h_content)
                    for key in h_matches:
                        if key not in found_keys:
                            found_keys[key] = []
                        found_keys[key].append(h_path)

    # Load JSON translations
    json_translations: dict[str, dict[str, Any]] = {}
    for filename in os.listdir(i18n_dir):
        if filename.endswith(".json"):
            lang: str = filename.replace(".json", "")
            with open(os.path.join(i18n_dir, filename), "r", encoding="utf-8") as f:
                json_translations[lang] = json.load(f)

    def get_keys_from_dict(d: dict[str, Any], prefix: str = "") -> list[str]:
        keys: list[str] = []
        for k, v in d.items():
            new_key: str = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.extend(get_keys_from_dict(v, new_key))
            else:
                keys.append(new_key)
        return keys

    json_keys = {}
    for lang, trans in json_translations.items():
        json_keys[lang] = set(get_keys_from_dict(trans))

    # All keys used in code
    all_used_keys = set(found_keys.keys())

    # All keys present in any JSON
    all_json_keys = set()
    for keys in json_keys.values():
        all_json_keys.update(keys)

    # Missing keys (used in code but missing in at least one language)
    missing_in_lang = {}
    for lang in json_keys:
        missing_in_lang[lang] = all_used_keys - json_keys[lang]

    # Orphan keys (present in JSON but never used in code)
    orphan_keys = {}
    for lang in json_keys:
        orphan_keys[lang] = json_keys[lang] - all_used_keys

    # Report results
    print(f"Python files analyzed: {len(python_files)}")
    print(f"HTML files analyzed: {len(html_files)}")
    print(f"Total unique keys used in code: {len(all_used_keys)}")

    for lang in json_keys:
        print(f"\nLanguage: {lang.upper()}")
        print(f"  Total keys in JSON: {len(json_keys[lang])}")
        print(f"  Missing keys (used in code but not in JSON): {len(missing_in_lang[lang])}")
        print(f"  Orphan keys (in JSON but not in code): {len(orphan_keys[lang])}")

    # Detect hardcoded strings (simplified: strings in HTML not inside tags or attributes, or in Python flash/logs)
    # This is hard to do accurately with regex, but we can look for common patterns.
    # For now, let's just focus on the keys.

    # Detailed output for the report
    report = {
        "stats": {
            "python_files": len(python_files),
            "html_files": len(html_files),
            "used_keys_count": len(all_used_keys),
            "languages": list(json_keys.keys())
        },
        "missing": {lang: list(keys) for lang, keys in missing_in_lang.items()},
        "orphans": {lang: list(keys) for lang, keys in orphan_keys.items()},
        "used_keys_locations": {key: list(set(locations)) for key, locations in found_keys.items()}
    }

    with open("i18n_audit_data.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    audit_i18n()
