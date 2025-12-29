#!/usr/bin/env python3
"""
Convert all markdown files to HTML with navigation

Purpose: Complete HTML documentation generator
File: scripts/build_full_html_docs.py
Created: 2025-12-28T23:35:00+01:00
License: AGPL-3.0-or-later
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("⚠️  markdown module not found. Install with: pip install markdown")

class HTMLDocBuilder:
    def __init__(self, source_root: str = ".", output_dir: str = "docs/html"):
        self.root = Path(source_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create assets directory
        (self.output_dir / "assets").mkdir(exist_ok=True)

        self.file_map: Dict[str, Tuple[str, str]] = {}  # {output_path: (title, category)}

    def find_markdown_files(self) -> Dict[str, List[Path]]:
        """Find all markdown files and organize by category"""
        files_by_category = {}

        # Docs
        if (self.root / "docs").exists():
            for md_file in sorted((self.root / "docs").glob("**/*.md")):
                # Skip archives and certain files
                if "archives" in str(md_file):
                    continue

                category = md_file.parent.name if md_file.parent.name != "docs" else "docs"
                if category not in files_by_category:
                    files_by_category[category] = []
                files_by_category[category].append(md_file)

        # Analysis reports
        if (self.root / "Analysis_reports").exists():
            for md_file in sorted((self.root / "Analysis_reports").glob("*.md")):
                category = "analysis"
                if category not in files_by_category:
                    files_by_category[category] = []
                files_by_category[category].append(md_file)

        return files_by_category

    def extract_title(self, content: str, filename: str) -> str:
        """Extract title from markdown content or filename"""
        # Look for H1
        for line in content.split('\n'):
            if line.startswith('# '):
                return line.replace('# ', '').strip()

        # Fallback to filename
        return filename.replace('_', ' ').replace('-', ' ').title()

    def markdown_to_html(self, content: str) -> str:
        """Convert markdown to HTML"""
        if not HAS_MARKDOWN:
            return f"<pre>{content}</pre>"

        # Remove YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) > 2:
                content = parts[2].strip()

        try:
            md = markdown.Markdown(extensions=['tables', 'fenced_code'])
            html = md.convert(content)
            return html
        except Exception as e:
            return f"<pre>{content}\n\nError: {e}</pre>"

    def create_css(self) -> str:
        """Generate CSS"""
        return r"""/* X-Filamenta Documentation - Minimal CSS */

:root {
    --primary: #0066cc;
    --secondary: #666;
    --success: #28a745;
    --warning: #ff9800;
    --danger: #dc3545;
    --light: #f8f9fa;
    --dark: #212529;
    --border: #ddd;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: var(--dark);
    background: white;
}

/* Header */
header {
    background: linear-gradient(135deg, var(--dark) 0%, #1a1a2e 100%);
    color: white;
    padding: 1rem 2rem;
    border-bottom: 3px solid var(--primary);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
}

/* Layout */
.container {
    display: flex;
    min-height: calc(100vh - 140px);
}

/* Sidebar */
.sidebar {
    width: 280px;
    background: var(--light);
    padding: 2rem 1.5rem;
    border-right: 1px solid var(--border);
    overflow-y: auto;
    position: sticky;
    top: 0;
    height: calc(100vh - 140px);
}

.sidebar::-webkit-scrollbar {
    width: 6px;
}

.sidebar::-webkit-scrollbar-track {
    background: var(--light);
}

.sidebar::-webkit-scrollbar-thumb {
    background: #bbb;
    border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
    background: #999;
}

.sidebar-section {
    margin-bottom: 2rem;
}

.sidebar-section:first-child {
    margin-top: 0;
}

.sidebar-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 0.5rem;
}

.sidebar ul {
    list-style: none;
}

.sidebar li {
    margin-bottom: 0.25rem;
}

.sidebar a {
    color: var(--secondary);
    text-decoration: none;
    display: block;
    padding: 0.5rem 0.75rem;
    border-radius: 4px;
    font-size: 0.95rem;
    transition: all 0.2s ease;
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

/* Main Content */
.main {
    flex: 1;
    padding: 2rem;
    max-width: 900px;
    overflow-y: auto;
}

.main::-webkit-scrollbar {
    width: 8px;
}

.main::-webkit-scrollbar-track {
    background: white;
}

.main::-webkit-scrollbar-thumb {
    background: #bbb;
    border-radius: 4px;
}

.main::-webkit-scrollbar-thumb:hover {
    background: #999;
}

.breadcrumb {
    font-size: 0.9rem;
    color: var(--secondary);
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.breadcrumb a {
    color: var(--primary);
}

.breadcrumb a:hover {
    text-decoration: underline;
}

/* Typography */
h1 {
    font-size: 2rem;
    margin: 0 0 1.5rem 0;
    color: var(--dark);
    border-bottom: 3px solid var(--primary);
    padding-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    margin: 2rem 0 1rem 0;
    color: var(--dark);
}

h3 {
    font-size: 1.25rem;
    margin: 1.5rem 0 0.75rem 0;
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
    background: #f5f5f5;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: "Monaco", "Courier New", "Courier", monospace;
    font-size: 0.9rem;
    color: #d73a49;
}

pre {
    background: #282c34;
    color: #abb2bf;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1rem 0;
    line-height: 1.4;
    font-family: "Monaco", "Courier New", "Courier", monospace;
    font-size: 0.9rem;
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
    margin: 1.5rem 0;
    font-size: 0.95rem;
}

table th,
table td {
    padding: 0.75rem;
    border: 1px solid var(--border);
    text-align: left;
}

table th {
    background: var(--light);
    font-weight: 600;
    color: var(--dark);
}

table tbody tr:hover {
    background: #fafafa;
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

/* Badges */
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

/* Cards */
.card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.card-header {
    background: var(--light);
    padding: 1rem 1.5rem;
    margin: -1.5rem -1.5rem 1rem -1.5rem;
    border-bottom: 1px solid var(--border);
    font-weight: 600;
    border-radius: 4px 4px 0 0;
}

/* Footer */
footer {
    background: var(--light);
    padding: 2rem;
    text-align: center;
    color: var(--secondary);
    font-size: 0.9rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}

/* Utilities */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-muted { color: var(--secondary); }
.mt-1 { margin-top: 1rem; }
.mb-1 { margin-bottom: 1rem; }
.p-1 { padding: 1rem; }

/* Responsive */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
        position: relative;
        padding: 1rem;
        border-right: none;
        border-bottom: 1px solid var(--border);
    }

    .main {
        padding: 1rem;
        max-width: 100%;
    }

    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.25rem; }

    header h1 { font-size: 1.25rem; }
}

@media (max-width: 480px) {
    body { font-size: 14px; }
    .sidebar { padding: 1rem 0.75rem; }
    .main { padding: 0.75rem; }
    h1 { font-size: 1.25rem; }
    h2 { font-size: 1.1rem; }
}
"""

    def create_html_page(self, title: str, content_html: str, category: str = "",
                         sidebar_html: str = "") -> str:
        """Create complete HTML page"""
        breadcrumb = f'<a href="index.html">HOME</a> / <span>{category.upper()}</span>' if category else ''

        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="X-Filamenta Documentation">
    <title>{title} - X-Filamenta Docs</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>📚 X-Filamenta Documentation</h1>
    </header>

    <div class="container">
        <aside class="sidebar">
            {sidebar_html}
        </aside>

        <main class="main">
            {'<div class="breadcrumb">' + breadcrumb + '</div>' if breadcrumb else ''}
            <article class="content">
                {content_html}
            </article>
        </main>
    </div>

    <footer>
        <p>&copy; 2025 XAREMA. Licensed under AGPL-3.0-or-later.</p>
        <p><small>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
    </footer>
</body>
</html>"""

    def generate_sidebar(self, files_by_category: Dict[str, List[Path]]) -> str:
        """Generate sidebar navigation"""
        sidebar = ""

        # Priority sections
        priority_order = ["docs", "guides", "features", "deployment", "architecture",
                         "security", "api", "contributing", "troubleshooting", "analysis"]

        for category in priority_order:
            if category not in files_by_category:
                continue

            sidebar += f'<div class="sidebar-section">\n'
            sidebar += f'<div class="sidebar-title">{category.upper()}</div>\n'
            sidebar += '<ul>\n'

            for md_file in sorted(files_by_category[category]):
                # Create output filename
                title = self.extract_title(md_file.read_text(), md_file.stem)
                output_name = md_file.stem.lower().replace(' ', '-') + '.html'

                sidebar += f'<li><a href="{output_name}">{title}</a></li>\n'

            sidebar += '</ul>\n</div>\n'

        return sidebar

    def build(self):
        """Build complete HTML documentation"""
        print("🔨 Building HTML documentation...")

        files_by_category = self.find_markdown_files()
        print(f"📁 Found {sum(len(v) for v in files_by_category.values())} markdown files")

        # Create CSS
        (self.output_dir / "style.css").write_text(self.create_css())
        print("✓ CSS created")

        # Generate sidebar once
        sidebar_html = self.generate_sidebar(files_by_category)

        # Create index page
        index_html = self.create_index_page()
        (self.output_dir / "index.html").write_text(index_html)
        print("✓ Index page created")

        # Convert all markdown files
        total_files = sum(len(v) for v in files_by_category.values())
        current = 0

        for category, files in files_by_category.items():
            for md_file in sorted(files):
                current += 1

                # Read content
                content = md_file.read_text(encoding='utf-8')
                title = self.extract_title(content, md_file.stem)

                # Convert to HTML
                html_content = self.markdown_to_html(content)

                # Create output file
                output_name = md_file.stem.lower().replace(' ', '-') + '.html'
                output_path = self.output_dir / output_name

                # Create full page
                full_html = self.create_html_page(title, html_content, category, sidebar_html)
                output_path.write_text(full_html, encoding='utf-8')

                print(f"✓ [{current}/{total_files}] {title}")

        print(f"\n✅ Documentation generated in: {self.output_dir.absolute()}")
        print(f"📖 Open in browser: {(self.output_dir / 'index.html').absolute()}")

    def create_index_page(self) -> str:
        """Create index/home page"""
        return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X-Filamenta Documentation</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>📚 X-Filamenta Documentation</h1>
    </header>

    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-section">
                <div class="sidebar-title">QUICK ACCESS</div>
                <ul>
                    <li><a href="00-start-here.html">START HERE</a></li>
                    <li><a href="reference.html">REFERENCE</a></li>
                    <li><a href="00-plan-documentation.html">PLAN</a></li>
                </ul>
            </div>
        </aside>

        <main class="main">
            <h1>Welcome to X-Filamenta</h1>

            <div class="alert alert-info">
                <strong>👋 New here?</strong> Read <a href="00-start-here.html">START HERE</a> first!
            </div>

            <h2>Documentation Overview</h2>

            <p style="font-size: 1.1rem; color: #666; margin: 1.5rem 0;">
                <strong>Version:</strong> 0.0.1-Alpha |
                <strong>License:</strong> AGPL-3.0-or-later
            </p>

            <h3>🚀 Getting Started</h3>
            <ul>
                <li><a href="00-start-here.html">Start Here</a> - Navigation guide</li>
                <li><a href="quickstart.html">Quick Start</a> - 5-minute setup</li>
                <li><a href="guides.html">Guides</a> - Detailed tutorials</li>
            </ul>

            <h3>✨ Features</h3>
            <ul>
                <li><a href="authentication.html">Authentication & 2FA</a></li>
                <li><a href="wizard-installation.html">Installation Wizard</a></li>
                <li><a href="internationalization.html">Multi-language Support</a></li>
                <li><a href="database.html">Database Configuration</a></li>
            </ul>

            <h3>🚀 Deployment</h3>
            <ul>
                <li><a href="01-cpanel.html">cPanel</a></li>
                <li><a href="02-vps-linux.html">VPS/Linux</a></li>
                <li><a href="03-docker.html">Docker</a></li>
            </ul>

            <h3>🏗️ Architecture</h3>
            <ul>
                <li><a href="overview.html">Architecture Overview</a></li>
                <li><a href="backend.html">Backend (Flask)</a></li>
                <li><a href="frontend.html">Frontend (HTMX + Bootstrap)</a></li>
            </ul>

            <h3>🔒 Security</h3>
            <ul>
                <li><a href="best-practices.html">Best Practices</a></li>
                <li><a href="2fa.html">2FA TOTP</a></li>
                <li><a href="csrf-protection.html">CSRF Protection</a></li>
            </ul>

            <h3>❓ Help</h3>
            <ul>
                <li><a href="faq.html">Frequently Asked Questions</a></li>
                <li><a href="common-issues.html">Common Issues & Solutions</a></li>
                <li><a href="reference.html">Complete Reference</a></li>
            </ul>

            <h2>Key Features</h2>
            <ul>
                <li>✅ Multi-language support (EN, FR)</li>
                <li>✅ 2FA TOTP authentication</li>
                <li>✅ Installation wizard</li>
                <li>✅ Support SQLite, MySQL, PostgreSQL</li>
                <li>✅ HTMX for dynamic updates</li>
                <li>✅ Bootstrap 5 responsive design</li>
                <li>✅ CSRF protection</li>
                <li>✅ Rate limiting</li>
            </ul>
        </main>
    </div>

    <footer>
        <p>&copy; 2025 XAREMA. Licensed under AGPL-3.0-or-later.</p>
        <p><small>Distributed by XAREMA | Coder: AleGabMar</small></p>
    </footer>
</body>
</html>"""

def main():
    builder = HTMLDocBuilder()
    builder.build()

if __name__ == "__main__":
    main()

