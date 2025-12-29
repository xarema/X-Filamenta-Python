#!/usr/bin/env python3
"""
Generate HTML documentation from Markdown files

Purpose: Convert all markdown documentation to navigable HTML with CSS
File: scripts/generate_html_docs.py
Created: 2025-12-28T23:35:00+01:00
License: AGPL-3.0-or-later
"""

import os
import markdown
import re
from pathlib import Path
from typing import Dict, List, Tuple

class HTMLDocumentationGenerator:
    def __init__(self, source_dir: str = ".", output_dir: str = "docs/html"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.md_files: Dict[str, List[Path]] = {}
        self.toc: List[Dict] = []

    def find_markdown_files(self):
        """Find all markdown files to convert"""
        # Docs
        for md_file in self.source_dir.glob("docs/**/*.md"):
            category = md_file.parent.name if md_file.parent.name != "docs" else "root"
            if category not in self.md_files:
                self.md_files[category] = []
            self.md_files[category].append(md_file)

        # Analysis reports
        for md_file in self.source_dir.glob("Analysis_reports/*.md"):
            if "Analysis_reports" not in self.md_files:
                self.md_files["Analysis_reports"] = []
            self.md_files["Analysis_reports"].append(md_file)

        print(f"Found {sum(len(v) for v in self.md_files.values())} markdown files")

    def markdown_to_html(self, md_content: str) -> str:
        """Convert markdown to HTML"""
        # Remove yaml frontmatter
        if md_content.startswith("---"):
            parts = md_content.split("---", 2)
            if len(parts) > 2:
                md_content = parts[2]

        md = markdown.Markdown(extensions=['tables', 'codehilite', 'fenced_code', 'toc'])
        html = md.convert(md_content)
        return html

    def create_css(self):
        """Create minimal CSS"""
        css = """/* X-Filamenta Documentation CSS */

:root {
    --primary: #0066cc;
    --secondary: #666;
    --success: #28a745;
    --warning: #ff9800;
    --danger: #dc3545;
    --light: #f8f9fa;
    --dark: #212529;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: var(--dark);
    background: white;
}

.container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 280px;
    background: var(--light);
    padding: 2rem;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    position: sticky;
    top: 0;
}

.sidebar h3 {
    font-size: 0.85rem;
    text-transform: uppercase;
    color: var(--secondary);
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 0.5rem;
}

.sidebar h3:first-child {
    margin-top: 0;
}

.sidebar ul {
    list-style: none;
}

.sidebar li {
    margin-bottom: 0.5rem;
}

.sidebar a {
    color: var(--secondary);
    text-decoration: none;
    font-size: 0.95rem;
    display: block;
    padding: 0.5rem 0.75rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.sidebar a:hover {
    background: rgba(0, 102, 204, 0.1);
    color: var(--primary);
    padding-left: 1rem;
}

.sidebar a.active {
    background: var(--primary);
    color: white;
    font-weight: 600;
}

.sidebar .section {
    margin-bottom: 1.5rem;
}

.sidebar .section-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #999;
    margin: 1.5rem 0 0.75rem 0;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Main Content */
.main {
    flex: 1;
    padding: 2rem;
    max-width: 900px;
}

.breadcrumb {
    font-size: 0.9rem;
    color: var(--secondary);
    margin-bottom: 2rem;
}

.breadcrumb a {
    color: var(--primary);
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

/* Typography */
h1 {
    font-size: 2rem;
    margin: 2rem 0 1rem 0;
    color: var(--dark);
    border-bottom: 3px solid var(--primary);
    padding-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    margin: 1.5rem 0 0.75rem 0;
    color: var(--dark);
}

h3 {
    font-size: 1.25rem;
    margin: 1.25rem 0 0.5rem 0;
    color: var(--secondary);
}

h4, h5, h6 {
    margin: 1rem 0 0.5rem 0;
}

p {
    margin-bottom: 1rem;
}

a {
    color: var(--primary);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.2s;
}

a:hover {
    border-bottom-color: var(--primary);
}

/* Code */
code {
    background: var(--light);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: "Monaco", "Courier New", monospace;
    font-size: 0.9rem;
}

pre {
    background: var(--dark);
    color: #fff;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1rem 0;
    line-height: 1.4;
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.95rem;
}

table th,
table td {
    padding: 0.75rem;
    border: 1px solid #ddd;
    text-align: left;
}

table th {
    background: var(--light);
    font-weight: 600;
}

table tr:hover {
    background: var(--light);
}

/* Lists */
ul, ol {
    margin: 1rem 0 1rem 2rem;
}

li {
    margin-bottom: 0.5rem;
}

blockquote {
    border-left: 4px solid var(--primary);
    padding-left: 1rem;
    margin: 1rem 0;
    color: var(--secondary);
    font-style: italic;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 0.5rem;
}

.badge-success { background: #d4edda; color: #155724; }
.badge-warning { background: #fff3cd; color: #856404; }
.badge-danger { background: #f8d7da; color: #721c24; }
.badge-info { background: #d1ecf1; color: #0c5460; }

/* Alerts */
.alert {
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    border-left: 4px solid;
}

.alert-info {
    background: #d1ecf1;
    border-color: #17a2b8;
    color: #0c5460;
}

.alert-success {
    background: #d4edda;
    border-color: #28a745;
    color: #155724;
}

.alert-warning {
    background: #fff3cd;
    border-color: #ff9800;
    color: #856404;
}

.alert-danger {
    background: #f8d7da;
    border-color: #dc3545;
    color: #721c24;
}

/* Header */
header {
    background: var(--dark);
    color: white;
    padding: 1rem 2rem;
    border-bottom: 3px solid var(--primary);
}

header h1 {
    border: none;
    color: white;
    margin: 0;
    font-size: 1.5rem;
}

/* Footer */
footer {
    background: var(--light);
    padding: 2rem;
    text-align: center;
    color: var(--secondary);
    font-size: 0.9rem;
    margin-top: 3rem;
    border-top: 1px solid #ddd;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        position: relative;
        padding: 1rem;
        border-right: none;
        border-bottom: 1px solid #ddd;
    }

    .main {
        padding: 1rem;
    }

    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.25rem; }
}

/* Utility */
.text-center { text-align: center; }
.mt-1 { margin-top: 1rem; }
.mb-1 { margin-bottom: 1rem; }
.text-muted { color: var(--secondary); }
.font-mono { font-family: "Monaco", "Courier New", monospace; }
"""
    return css

def main():
    generator = HTMLDocumentationGenerator()
    generator.find_markdown_files()

    # Create CSS
    css_content = generator.create_css()
    css_path = generator.output_dir / "style.css"
    css_path.write_text(css_content)
    print(f"✓ Created {css_path}")

    # Create base HTML files
    print(f"✓ Ready to generate HTML documentation")
    print(f"  Output directory: {generator.output_dir}")
    print(f"  Categories: {', '.join(sorted(generator.md_files.keys()))}")

if __name__ == "__main__":
    main()

