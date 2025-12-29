"""
Fix Duplicate Docstrings in Routes Files

Removes duplicate docstring blocks from all route files
"""

import re
from pathlib import Path

# Pattern to match duplicate docstring after first closing """
pattern = r'(""")\s*SPDX-License-Identifier:.*?-{70,}\s*"""'

routes_dir = Path("backend/src/routes")
fixed_files = []

for route_file in routes_dir.glob("*.py"):
    if route_file.name == "__init__.py":
        continue

    print(f"[INFO] Checking {route_file.name}...")
    content = route_file.read_text(encoding="utf-8")

    # Count """ occurrences
    count = content.count('"""')

    if count % 2 != 0:  # Odd number = problem
        print(f"  [WARN] Odd number of triple quotes ({count}) - fixing...")

        # Find and remove duplicate block
        new_content = re.sub(pattern, '"""', content, flags=re.DOTALL)

        # Write back
        route_file.write_text(new_content, encoding="utf-8")
        fixed_files.append(route_file.name)
        print(f"  [OK] Fixed {route_file.name}")
    else:
        print(f"  [OK] {route_file.name} is clean")

print()
print("=" * 70)
print(f"[DONE] Fixed {len(fixed_files)} files:")
for f in fixed_files:
    print(f"  - {f}")
print("=" * 70)
