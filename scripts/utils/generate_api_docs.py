"""
API Documentation Generator

Purpose: Generate API documentation from Python docstrings
Description: Extracts docstrings from modules, classes, and functions to create Markdown docs

File: scripts/utils/generate_api_docs.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier:  AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Usage: 
    # Generate API docs from backend/src/
    python scripts/utils/generate_api_docs.py

    # Specify custom app directory
    python scripts/utils/generate_api_docs.py --app-dir backend/src

    # Specify custom output file
    python scripts/utils/generate_api_docs.py --output docs/api/reference.md
"""

import argparse
import ast
import logging
from pathlib import Path
from typing import Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def extract_docstrings(file_path: Path) -> Dict:
    """
    Extract docstrings from Python file. 
    
    Args:
        file_path: Path to Python file
        
    Returns: 
        Dictionary containing module, classes, and functions docstrings
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
        return {}
    except Exception as e:
        logger. error(f"Error reading {file_path}: {e}")
        return {}
    
    docs = {
        'module': ast.get_docstring(tree) or '',
        'classes': {},
        'functions': {}
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docs['classes'][node.name] = ast.get_docstring(node) or ''
        elif isinstance(node, ast.FunctionDef):
            # Skip private functions
            if not node.name.startswith('_'):
                docs['functions'][node.name] = ast.get_docstring(node) or ''
    
    return docs


def generate_api_docs(app_dir: Path, output_file: Path) -> None:
    """
    Generate API documentation from Python files.
    
    Args:
        app_dir: Directory containing Python source files
        output_file: Path to output Markdown file
    """
    if not app_dir.exists():
        logger.error(f"App directory not found: {app_dir}")
        return
    
    content = ["# API Documentation\n\n"]
    content.append("Auto-generated from code docstrings.\n\n")
    content.append(f"**Generated from:** `{app_dir}`\n\n")
    content.append("---\n\n")
    
    # Find all Python files
    py_files = sorted(app_dir.rglob('*.py'))
    processed = 0
    
    for py_file in py_files:
        # Skip __pycache__, tests, and __init__ files without docstrings
        if '__pycache__' in str(py_file) or 'test' in str(py_file):
            continue
        
        rel_path = py_file.relative_to(app_dir. parent)
        docs = extract_docstrings(py_file)
        
        # Skip if no meaningful docstrings
        if not any([docs['module'], docs['classes'], docs['functions']]):
            continue
        
        processed += 1
        content.append(f"## `{rel_path}`\n\n")
        
        if docs['module']:
            content. append(f"{docs['module']}\n\n")
        
        if docs['classes']:
            content.append("### Classes\n\n")
            for class_name, docstring in sorted(docs['classes'].items()):
                content.append(f"#### `{class_name}`\n\n")
                if docstring:
                    content. append(f"{docstring}\n\n")
                else:
                    content. append("*No docstring provided.*\n\n")
        
        if docs['functions']:
            content.append("### Functions\n\n")
            for func_name, docstring in sorted(docs['functions'].items()):
                content.append(f"#### `{func_name}()`\n\n")
                if docstring:
                    content.append(f"{docstring}\n\n")
                else: 
                    content.append("*No docstring provided.*\n\n")
        
        content. append("---\n\n")
    
    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(''.join(content), encoding='utf-8')
    
    logger.info(f"Generated API documentation:  {output_file}")
    logger.info(f"Processed {processed} Python files")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate API documentation from Python docstrings',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--app-dir',
        type=Path,
        default=Path('backend/src'),
        help='Directory containing Python source files (default: backend/src)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('docs/api/README.md'),
        help='Output Markdown file (default: docs/api/README.md)'
    )
    
    args = parser.parse_args()
    
    generate_api_docs(args.app_dir, args.output)


if __name__ == '__main__':
    main()