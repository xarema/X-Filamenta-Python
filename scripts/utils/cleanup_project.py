"""
Automatic Project Cleanup Script

Purpose: Remove common junk files and organize the project structure
Description: Cleans Python cache, IDE files, temp files, and organizes static assets

File:  scripts/utils/cleanup_project. py | Repository: X-Filamenta-Python
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
    # Dry run (preview what will be deleted)
    python scripts/utils/cleanup_project.py

    # Execute cleanup
    python scripts/utils/cleanup_project.py --execute

    # Quiet mode (minimal output)
    python scripts/utils/cleanup_project.py --execute --quiet
"""

import argparse
import logging
import shutil
from pathlib import Path
from typing import List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class ProjectCleaner:
    """Clean up project files and directories."""
    
    def __init__(self, root_path: Path, dry_run: bool = True, quiet: bool = False):
        """
        Initialize project cleaner. 
        
        Args:
            root_path: Root directory of project
            dry_run: If True, don't actually delete files
            quiet:  If True, minimize output
        """
        self. root = root_path
        self.dry_run = dry_run
        self.quiet = quiet
        self.removed_files: List[str] = []
        self.removed_dirs: List[str] = []
        
    def _log(self, message: str, level: str = "info") -> None:
        """Log message if not in quiet mode."""
        if not self.quiet:
            if level == "info":
                logger.info(message)
            elif level == "warning":
                logger.warning(message)
            elif level == "error":
                logger.error(message)
    
    def remove_pycache(self) -> None:
        """Remove all __pycache__ directories."""
        for pycache in self.root.rglob('__pycache__'):
            if pycache.is_dir():
                if not self.dry_run:
                    shutil.rmtree(pycache)
                self. removed_dirs.append(str(pycache. relative_to(self.root)))
    
    def remove_pyc_files(self) -> None:
        """Remove all .pyc files."""
        for pyc in self.root.rglob('*.pyc'):
            if pyc.is_file():
                if not self.dry_run:
                    pyc.unlink()
                self.removed_files.append(str(pyc. relative_to(self.root)))
    
    def remove_ds_store(self) -> None:
        """Remove macOS .DS_Store files."""
        for ds in self.root.rglob('. DS_Store'):
            if ds.is_file():
                if not self.dry_run:
                    ds.unlink()
                self.removed_files.append(str(ds.relative_to(self.root)))
    
    def remove_ide_folders(self) -> None:
        """
        Remove IDE-specific folders that shouldn't be committed.
        
        Note:  Keeps .vscode and .idea if they contain workspace settings
        but removes build/cache folders. 
        """
        # Don't remove .idea and .vscode entirely (may have user settings)
        # Instead, remove cache/build subdirectories
        ide_cache_patterns = [
            '.idea/shelf',
            '.idea/workspace. xml',
            '.vscode/. ropeproject',
            '*.iml',
        ]
        
        for pattern in ide_cache_patterns:
            for path in self.root.rglob(pattern):
                if path. is_dir():
                    if not self.dry_run:
                        shutil.rmtree(path)
                    self. removed_dirs.append(str(path.relative_to(self. root)))
                elif path.is_file() and pattern. endswith('.iml'):
                    if not self.dry_run:
                        path.unlink()
                    self.removed_files.append(str(path.relative_to(self.root)))
    
    def remove_temp_files(self) -> None:
        """Remove temporary files."""
        temp_patterns = ['*. tmp', '*.temp', '*~', '*.swp', '*.swo', '*.bak']
        
        for pattern in temp_patterns: 
            for temp_file in self.root.rglob(pattern):
                if temp_file.is_file():
                    if not self.dry_run:
                        temp_file.unlink()
                    self.removed_files.append(str(temp_file.relative_to(self.root)))
    
    def remove_empty_dirs(self) -> None:
        """Remove empty directories (except . git)."""
        import os
        
        for dirpath, dirnames, filenames in os.walk(self.root, topdown=False):
            dir_path = Path(dirpath)
            
            # Skip .git directory
            if '. git' in dir_path.parts:
                continue
            
            # Skip if not empty
            if any(dir_path.iterdir()):
                continue
            
            if not self.dry_run:
                dir_path.rmdir()
            self.removed_dirs.append(str(dir_path.relative_to(self.root)))
    
    def organize_static_files(self) -> None:
        """Ensure static files are in correct directories."""
        static_dir = self.root / 'backend' / 'src' / 'static'
        
        if not static_dir. exists():
            self._log("Static directory not found, skipping organization", "warning")
            return
        
        # Create subdirectories if they don't exist
        (static_dir / 'css').mkdir(exist_ok=True)
        (static_dir / 'js').mkdir(exist_ok=True)
        (static_dir / 'img').mkdir(exist_ok=True)
        
        # Move misplaced CSS files
        for css_file in static_dir.glob('*.css'):
            target = static_dir / 'css' / css_file.name
            if css_file != target:
                if not self. dry_run:
                    css_file.rename(target)
                self._log(f"  Moved:  {css_file.name} -> static/css/")
        
        # Move misplaced JS files
        for js_file in static_dir.glob('*.js'):
            target = static_dir / 'js' / js_file.name
            if js_file != target:
                if not self.dry_run:
                    js_file.rename(target)
                self._log(f"  Moved: {js_file.name} -> static/js/")
        
        # Move misplaced image files
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico']
        for ext in image_extensions:
            for img_file in static_dir.glob(ext):
                target = static_dir / 'img' / img_file.name
                if img_file != target:
                    if not self.dry_run:
                        img_file.rename(target)
                    self._log(f"  Moved: {img_file.name} -> static/img/")
    
    def run_cleanup(self) -> None:
        """Run all cleanup operations."""
        mode = "DRY RUN" if self.dry_run else "EXECUTION"
        
        self._log("\n" + "=" * 60)
        self._log(f"Project Cleanup - {mode} Mode")
        self._log("=" * 60 + "\n")
        
        self._log("Removing Python cache files...")
        self.remove_pycache()
        self.remove_pyc_files()
        
        self._log("Removing system files...")
        self.remove_ds_store()
        
        self._log("Removing IDE cache folders...")
        self.remove_ide_folders()
        
        self._log("Removing temporary files...")
        self.remove_temp_files()
        
        self._log("Organizing static files...")
        self.organize_static_files()
        
        self._log("Removing empty directories...")
        self.remove_empty_dirs()
        
        # Summary
        self._log("\n" + "=" * 60)
        self._log(f"Cleanup Summary ({mode})")
        self._log("=" * 60)
        self._log(f"Files removed: {len(self.removed_files)}")
        self._log(f"Directories removed:  {len(self.removed_dirs)}")
        
        if self.removed_files and not self.quiet:
            self._log("\nFiles:")
            for f in self.removed_files[: 10]: 
                self._log(f"  - {f}")
            if len(self.removed_files) > 10:
                self._log(f"  ... and {len(self.removed_files) - 10} more")
        
        if self.removed_dirs and not self.quiet:
            self._log("\nDirectories:")
            for d in self.removed_dirs[:10]: 
                self._log(f"  - {d}")
            if len(self.removed_dirs) > 10:
                self._log(f"  ... and {len(self.removed_dirs) - 10} more")
        
        if self.dry_run:
            self._log("\n" + "!" * 60)
            self._log("This was a DRY RUN.  No files were actually deleted.")
            self._log("Run with --execute flag to perform cleanup.")
            self._log("!" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Clean up Flask project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/utils/cleanup_project.py                  # Dry run
  python scripts/utils/cleanup_project.py --execute        # Execute cleanup
  python scripts/utils/cleanup_project.py --execute --quiet # Execute quietly
        """
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually perform cleanup (default is dry-run)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimize output (only show summary)'
    )
    
    args = parser.parse_args()
    
    root = Path.cwd()
    cleaner = ProjectCleaner(root, dry_run=not args. execute, quiet=args.quiet)
    cleaner.run_cleanup()


if __name__ == '__main__':
    main()