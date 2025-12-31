"""
i18n Translation Checker

Purpose:  Detect missing translations, inconsistencies, and hardcoded text in templates
Description: Validates translation files and scans templates for untranslated text

File:  scripts/utils/check_i18n.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified (Git): TBD | Commit: TBD

Distributed by:  XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License:  AGPL-3.0-or-later
SPDX-License-Identifier:  AGPL-3.0-or-later

Copyright (c) 2025 XAREMA.  All rights reserved. 

Metadata:
- Status:  Stable
- Classification: Internal

Usage:
    # Check all (JSON validation + missing keys + hardcoded text)
    python scripts/utils/check_i18n.py

    # Check only JSON validation
    python scripts/utils/check_i18n.py --validate-only

    # Check only missing keys
    python scripts/utils/check_i18n.py --missing-keys-only

    # Check only hardcoded text in templates
    python scripts/utils/check_i18n.py --hardcoded-only

    # Exit with error code if issues found (for CI/CD)
    python scripts/utils/check_i18n.py --strict
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# ---- Configuration ----

# Paths
I18N_DIR = Path("backend/src/i18n")
TEMPLATES_DIR = Path("backend/src/templates")

# Translation files
TRANSLATION_FILES = {
    "fr": I18N_DIR / "fr. json",
    "en": I18N_DIR / "en. json",
}

# Patterns to detect hardcoded text in templates
# Matches text NOT using {{ t('... ') or '...' }}
HARDCODED_TEXT_PATTERNS = [
    # Text directly in HTML tags (excluding {{ t(... ) }})
    r'>\s*[A-Z][a-zA-Z\s]{3,}\s*<',  # e.g., >Hello World<
    
    # Button text without translation
    r'<button[^>]*>\s*[A-Z][a-zA-Z\s]{2,}\s*</button>',
    
    # Placeholder without translation
    r'placeholder\s*=\s*"[A-Z][^"]{3,}"',
    
    # Title without translation
    r'<h[1-6][^>]*>\s*[A-Z][a-zA-Z\s]{3,}\s*</h[1-6]>',
]

# Exceptions (allowed hardcoded text)
ALLOWED_HARDCODED = [
    "XAREMA",  # Brand name
    "X-Filamenta",  # App name
    "Python",  # Technology names
    "Flask",
    "HTMX",
    "Bootstrap",
    "OK",  # Common short codes
    "ID",
]


# ---- Helper Functions ----

def load_json(file_path: Path) -> Tuple[Dict, List[str]]:
    """
    Load and validate JSON file. 
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Tuple of (parsed_data, errors)
    """
    errors = []
    
    if not file_path.exists():
        errors.append(f"File not found: {file_path}")
        return {}, errors
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, errors
    except json. JSONDecodeError as e: 
        errors.append(f"Invalid JSON in {file_path}: {e}")
        return {}, errors
    except Exception as e: 
        errors.append(f"Error reading {file_path}: {e}")
        return {}, errors


def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict[str, str]:
    """
    Flatten nested dictionary into dot-notation keys.
    
    Example:
        {"wizard":  {"step1": {"title": "Title"}}}
        -> {"wizard.step1.title": "Title"}
    """
    items = []
    for k, v in d. items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_all_keys(data: Dict) -> Set[str]:
    """Get all keys from flattened dictionary."""
    return set(flatten_dict(data).keys())


def compare_keys(reference_data: Dict, target_data: Dict, reference_lang: str, target_lang: str) -> List[str]:
    """
    Compare two translation dictionaries and find missing keys.
    
    Args:
        reference_data:  Reference translation dict (e.g., French)
        target_data: Target translation dict (e.g., English)
        reference_lang: Reference language code
        target_lang:  Target language code
        
    Returns:
        List of error messages
    """
    errors = []
    
    reference_keys = get_all_keys(reference_data)
    target_keys = get_all_keys(target_data)
    
    # Keys in reference but not in target
    missing_in_target = reference_keys - target_keys
    if missing_in_target:
        errors.append(f"\n❌ Missing in {target_lang}. json ({len(missing_in_target)} keys):")
        for key in sorted(missing_in_target):
            errors.append(f"   - {key}")
    
    # Keys in target but not in reference
    extra_in_target = target_keys - reference_keys
    if extra_in_target:
        errors.append(f"\n⚠️  Extra keys in {target_lang}.json (not in {reference_lang}. json) ({len(extra_in_target)} keys):")
        for key in sorted(extra_in_target):
            errors.append(f"   - {key}")
    
    return errors


def find_hardcoded_text(templates_dir: Path) -> List[str]:
    """
    Scan templates for hardcoded text (not using {{ t(...) }}).
    
    Args:
        templates_dir: Path to templates directory
        
    Returns:
        List of findings (file: line - text)
    """
    findings = []
    
    if not templates_dir.exists():
        return [f"❌ Templates directory not found: {templates_dir}"]
    
    # Find all HTML files
    html_files = list(templates_dir.rglob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, start=1):
                # Skip lines with {{ t('...') }} (already translated)
                if re.search(r'{{\s*t\(', line):
                    continue
                
                # Skip comments
                if re.search(r'<!--.*-->', line):
                    continue
                
                # Check for hardcoded text patterns
                for pattern in HARDCODED_TEXT_PATTERNS: 
                    matches = re.findall(pattern, line)
                    for match in matches:
                        # Extract text content
                        text = re.sub(r'<[^>]+>', '', match).strip()
                        
                        # Skip if in allowed list
                        if any(allowed in text for allowed in ALLOWED_HARDCODED):
                            continue
                        
                        # Skip very short text (likely not user-facing)
                        if len(text) < 3:
                            continue
                        
                        # Skip if it looks like a variable
                        if re.match(r'^{[{%].*[}%]}$', text):
                            continue
                        
                        relative_path = file_path.relative_to(Path.cwd())
                        findings.append(f"{relative_path}:{line_num} - '{text}'")
        
        except Exception as e: 
            findings.append(f"❌ Error reading {file_path}: {e}")
    
    return findings


def find_used_translation_keys(templates_dir: Path) -> Set[str]:
    """
    Find all translation keys used in templates via {{ t('key') }}.
    
    Args:
        templates_dir: Path to templates directory
        
    Returns: 
        Set of translation keys found
    """
    used_keys = set()
    
    if not templates_dir.exists():
        return used_keys
    
    # Pattern to match {{ t('key. path') }}
    pattern = r"{{\s*t\(['\"]([^'\"]+)['\"]\)"
    
    html_files = list(templates_dir.rglob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            matches = re.findall(pattern, content)
            used_keys.update(matches)
        
        except Exception: 
            pass  # Skip files with errors
    
    return used_keys


def find_unused_keys(translation_data: Dict, used_keys: Set[str]) -> Set[str]:
    """
    Find translation keys defined but never used in templates.
    
    Args:
        translation_data: Translation dictionary
        used_keys: Set of keys used in templates
        
    Returns: 
        Set of unused keys
    """
    defined_keys = get_all_keys(translation_data)
    unused = defined_keys - used_keys
    return unused


# ---- Main Checks ----

def check_json_validity() -> Tuple[bool, List[str]]:
    """
    Validate JSON syntax for all translation files.
    
    Returns:
        Tuple of (success, errors)
    """
    print("🔍 Checking JSON validity...")
    all_errors = []
    
    for lang, file_path in TRANSLATION_FILES.items():
        _, errors = load_json(file_path)
        if errors:
            all_errors.extend([f"[{lang}. json] {err}" for err in errors])
        else:
            print(f"   ✅ {lang}.json - Valid JSON")
    
    success = len(all_errors) == 0
    return success, all_errors


def check_missing_keys() -> Tuple[bool, List[str]]:
    """
    Check for missing translation keys between languages.
    
    Returns:
        Tuple of (success, errors)
    """
    print("\n🔍 Checking for missing translation keys...")
    
    # Load all translation files
    translations = {}
    for lang, file_path in TRANSLATION_FILES. items():
        data, errors = load_json(file_path)
        if errors:
            return False, [f"Cannot check missing keys due to JSON errors in {lang}.json"]
        translations[lang] = data
    
    # Compare FR (reference) with EN
    errors = compare_keys(
        translations["fr"], 
        translations["en"], 
        "fr", 
        "en"
    )
    
    if not errors:
        print("   ✅ All translation keys consistent")
    
    success = len(errors) == 0
    return success, errors


def check_hardcoded_text() -> Tuple[bool, List[str]]:
    """
    Check templates for hardcoded text (not using {{ t(...) }}).
    
    Returns:
        Tuple of (success, findings)
    """
    print("\n🔍 Checking for hardcoded text in templates...")
    
    findings = find_hardcoded_text(TEMPLATES_DIR)
    
    if not findings:
        print("   ✅ No hardcoded text detected")
        return True, []
    
    errors = ["\n❌ Potential hardcoded text found: "]
    errors.extend([f"   {finding}" for finding in findings])
    
    return False, errors


def check_unused_keys() -> Tuple[bool, List[str]]:
    """
    Check for translation keys defined but never used.
    
    Returns:
        Tuple of (success, findings)
    """
    print("\n🔍 Checking for unused translation keys...")
    
    # Load French translations (reference)
    fr_data, errors = load_json(TRANSLATION_FILES["fr"])
    if errors:
        return False, ["Cannot check unused keys due to JSON errors"]
    
    # Find keys used in templates
    used_keys = find_used_translation_keys(TEMPLATES_DIR)
    
    # Find unused keys
    unused = find_unused_keys(fr_data, used_keys)
    
    if not unused:
        print("   ✅ All translation keys are used")
        return True, []
    
    warnings = [f"\n⚠️  Unused translation keys ({len(unused)}):"]
    warnings.extend([f"   - {key}" for key in sorted(unused)])
    warnings.append("\n   Note: These keys are defined but never used in templates.")
    warnings.append("   Consider removing them or verify they're used in Python code.")
    
    # Unused keys are warnings, not errors (don't fail check)
    return True, warnings


# ---- Main Function ----

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check i18n translation files for issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/utils/check_i18n.py                    # Run all checks
  python scripts/utils/check_i18n.py --validate-only    # Only JSON validation
  python scripts/utils/check_i18n.py --strict           # Exit with error code if issues found
        """
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate JSON syntax (skip other checks)"
    )
    
    parser.add_argument(
        "--missing-keys-only",
        action="store_true",
        help="Only check for missing translation keys"
    )
    
    parser.add_argument(
        "--hardcoded-only",
        action="store_true",
        help="Only check for hardcoded text in templates"
    )
    
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code 1 if any issues found (for CI/CD)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("i18n Translation Checker")
    print("=" * 60)
    
    all_success = True
    all_messages = []
    
    # Run checks based on arguments
    if args.validate_only:
        success, messages = check_json_validity()
        all_success &= success
        all_messages. extend(messages)
    
    elif args.missing_keys_only:
        success, messages = check_missing_keys()
        all_success &= success
        all_messages.extend(messages)
    
    elif args.hardcoded_only:
        success, messages = check_hardcoded_text()
        all_success &= success
        all_messages.extend(messages)
    
    else:
        # Run all checks
        success, messages = check_json_validity()
        all_success &= success
        all_messages.extend(messages)
        
        if success:  # Only check keys if JSON is valid
            success, messages = check_missing_keys()
            all_success &= success
            all_messages.extend(messages)
        
        success, messages = check_hardcoded_text()
        all_success &= success
        all_messages.extend(messages)
        
        # Unused keys (warnings only)
        success, messages = check_unused_keys()
        all_messages.extend(messages)
    
    # Print all messages
    if all_messages:
        print("\n" + "\n".join(all_messages))
    
    # Summary
    print("\n" + "=" * 60)
    if all_success:
        print("✅ All checks passed!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ Some checks failed.  Please fix the issues above.")
        print("=" * 60)
        
        if args.strict:
            sys. exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()