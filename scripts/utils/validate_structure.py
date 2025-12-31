"""
Repository Structure Validator

Purpose: Validate that the project follows the expected Flask structure
Description: Checks required files, directories, dependencies, and configuration

File: scripts/utils/validate_structure.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Usage:
    # Validate project structure
    python scripts/utils/validate_structure.py

    # Use in CI/CD (exits with code 1 if errors found)
    python scripts/utils/validate_structure.py
"""

import sys
from pathlib import Path
from typing import List


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class StructureValidator:
    """Validate Flask project structure."""
    
    def __init__(self, root_path: Path):
        """
        Initialize validator.
        
        Args:
            root_path: Root directory of project
        """
        self.root = root_path
        self.errors:  List[str] = []
        self.warnings: List[str] = []
        self.passed:  List[str] = []
        
    def check_required_files(self) -> None:
        """Check for required files in Flask project."""
        required_files = [
            'requirements.txt',
            'README.md',
            '. gitignore',
            '. env. example',
        ]
        
        # Check for entry point (multiple options)
        entry_points = ['app. py', 'wsgi.py', 'run.py', 'run_prod.py']
        entry_found = any((self.root / ep).exists() for ep in entry_points)
        
        for file in required_files:
            if (self.root / file).exists():
                self.passed.append(f"✓ Required file exists: {file}")
            else:
                self.errors.append(f"✗ Missing required file: {file}")
        
        if entry_found:
            self.passed.append("✓ Application entry point found")
        else:
            self.errors.append(f"✗ No entry point found (expected one of: {', '.join(entry_points)})")
    
    def check_flask_structure(self) -> None:
        """Check Flask application structure."""
        expected_dirs = {
            'backend/src':  'Application package directory',
            'backend/src/templates': 'Jinja2 templates directory',
            'backend/src/static': 'Static files directory',
            'backend/src/static/css':  'CSS files',
            'backend/src/static/js': 'JavaScript files',
            'backend/src/static/img': 'Images',
            'tests':  'Test directory',
        }
        
        optional_dirs = {
            'migrations': 'Database migrations (Flask-Migrate)',
            'docs': 'Documentation',
            'scripts': 'Utility scripts',
        }
        
        for dir_path, description in expected_dirs.items():
            full_path = self.root / dir_path
            if full_path.exists():
                self.passed.append(f"✓ {description}:  {dir_path}")
            else:
                self.errors.append(f"✗ Missing directory: {dir_path} ({description})")
        
        for dir_path, description in optional_dirs.items():
            full_path = self.root / dir_path
            if full_path.exists():
                self.passed.append(f"✓ {description}: {dir_path}")
            else:
                self.warnings.append(f"⚠ Optional directory missing: {dir_path} ({description})")
    
    def check_python_files(self) -> None:
        """Check Python file organization."""
        app_dir = self.root / 'backend' / 'src'
        if not app_dir.exists():
            return
            
        required_files = ['__init__.py']
        recommended_files = ['models.py', 'routes.py', 'config.py']
        
        for file in required_files:
            if (app_dir / file).exists():
                self.passed. append(f"✓ Required module exists: backend/src/{file}")
            else:
                self.errors.append(f"✗ Missing required module: backend/src/{file}")
        
        for file in recommended_files:
            if (app_dir / file).exists():
                self.passed.append(f"✓ Recommended module exists:  backend/src/{file}")
            else:
                self.warnings. append(f"⚠ Recommended file missing: backend/src/{file}")
    
    def check_documentation(self) -> None:
        """Check documentation completeness."""
        docs = {
            'README.md': True,
            'CONTRIBUTING.md': False,
            'CHANGELOG.md': False,
            'LICENSE':  False,
            'docs/':  False,
        }
        
        for doc, required in docs.items():
            path = self.root / doc
            if path.exists():
                self.passed.append(f"✓ Documentation exists: {doc}")
            else:
                if required:
                    self.errors.append(f"✗ Missing required documentation: {doc}")
                else:
                    self.warnings. append(f"⚠ Missing recommended documentation: {doc}")
    
    def check_config_files(self) -> None:
        """Check configuration files."""
        config_files = {
            '.env. example': 'Environment variables template',
            '. editorconfig': 'Editor configuration',
            '.flaskenv': 'Flask environment variables',
        }
        
        for file, description in config_files.items():
            if (self.root / file).exists():
                self.passed.append(f"✓ {description}: {file}")
            else:
                self.warnings.append(f"⚠ Missing {description}: {file}")
    
    def check_gitignore(self) -> None:
        """Check .gitignore completeness."""
        gitignore = self.root / '.gitignore'
        if not gitignore.exists():
            self.errors.append("✗ .gitignore is missing!")
            return
        
        content = gitignore.read_text()
        required_patterns = [
            '__pycache__',
            '*.pyc',
            '. env',
            'venv/',
            '. venv/',
            'instance/',
            '*.db',
            '*.sqlite',
        ]
        
        for pattern in required_patterns:
            if pattern in content:
                self.passed.append(f"✓ .gitignore includes: {pattern}")
            else:
                self.warnings.append(f"⚠ .gitignore missing pattern: {pattern}")
    
    def check_dependencies(self) -> None:
        """Check requirements.txt for essential Flask dependencies."""
        req_file = self.root / 'requirements.txt'
        if not req_file.exists():
            return
        
        content = req_file.read_text().lower()
        essential_deps = ['flask']
        recommended_deps = ['python-dotenv', 'flask-sqlalchemy', 'waitress']
        
        for dep in essential_deps:
            if dep in content:
                self. passed.append(f"✓ Essential dependency found: {dep}")
            else:
                self.errors.append(f"✗ Missing essential dependency: {dep}")
        
        for dep in recommended_deps:
            if dep in content: 
                self.passed.append(f"✓ Recommended dependency found: {dep}")
            else:
                self.warnings.append(f"⚠ Missing recommended dependency: {dep}")
    
    def check_github_instructions(self) -> None:
        """Check . github/ instruction files."""
        github_dir = self.root / '.github'
        
        if not github_dir.exists():
            self.warnings.append("⚠ . github/ directory missing (no Copilot instructions)")
            return
        
        required_instructions = [
            'copilot-instructions.md',
            'read-before-any-change.md',
        ]
        
        for file in required_instructions:
            if (github_dir / file).exists():
                self.passed.append(f"✓ GitHub instruction file exists: . github/{file}")
            else:
                self.warnings.append(f"⚠ Missing GitHub instruction:  .github/{file}")
    
    def run_all_checks(self) -> bool:
        """
        Run all validation checks.
        
        Returns:
            True if no errors found, False otherwise
        """
        print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 Flask Project Structure Validator{Colors.RESET}\n")
        print(f"Validating:  {self.root}\n")
        
        self. check_required_files()
        self.check_flask_structure()
        self.check_python_files()
        self.check_documentation()
        self.check_config_files()
        self.check_gitignore()
        self.check_dependencies()
        self.check_github_instructions()
        
        # Print results
        if self.passed:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ PASSED ({len(self.passed)}){Colors.RESET}")
            for msg in self.passed:
                print(f"  {Colors.GREEN}{msg}{Colors.RESET}")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ WARNINGS ({len(self.warnings)}){Colors.RESET}")
            for msg in self.warnings:
                print(f"  {Colors.YELLOW}{msg}{Colors.RESET}")
        
        if self.errors:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ ERRORS ({len(self. errors)}){Colors.RESET}")
            for msg in self.errors:
                print(f"  {Colors.RED}{msg}{Colors.RESET}")
        
        # Summary
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
        print(f"  Total checks: {total}")
        print(f"  {Colors.GREEN}Passed: {len(self.passed)}{Colors.RESET}")
        print(f"  {Colors. YELLOW}Warnings: {len(self.warnings)}{Colors.RESET}")
        print(f"  {Colors.RED}Errors: {len(self.errors)}{Colors.RESET}")
        
        return len(self.errors) == 0


def main():
    """Main entry point."""
    root = Path.cwd()
    validator = StructureValidator(root)
    success = validator.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()