#!/usr/bin/env python3
"""
Generate complete HTML documentation from Markdown files with navigation

Purpose: Convert all markdown docs to navigable HTML with CSS
File: scripts/build_html_docs.py
Created: 2025-12-28T23:35:00+01:00
License: AGPL-3.0-or-later
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List
import markdown
from datetime import datetime

class DocGenerator:
    def __init__(self, source_root: str = ".", output_dir: str = "docs/html"):
        self.root = Path(source_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.docs: Dict = {}
        self.md = markdown.Markdown(
            extensions=['tables', 'fenced_code', 'codehilite', 'toc']
        )

    def find_all_docs(self):
        """Find all markdown files"""
        # Docs directory
        docs_files = list((self.root / "docs").glob("**/*.md"))

        # Analysis reports
        reports_files = list((self.root / "Analysis_reports").glob("*.md"))

        all_files = sorted(docs_files + reports_files)
        print(f"Found {len(all_files)} markdown files")
        return all_files

    def read_md_file(self, filepath: Path) -> tuple:
        """Read markdown file and extract metadata"""
        content = filepath.read_text(encoding='utf-8')

        # Extract title from first H1
        title = filepath.stem.replace('_', ' ').title()
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break

        return title, content

    def md_to_html(self, content: str) -> str:
        """Convert markdown to HTML"""
        # Remove yaml frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) > 2:
                content = parts[2].strip()

        # Convert
        html = self.md.convert(content)
        self.md.reset()

        return html

    def create_page_html(self, title: str, content_html: str, breadcrumb: str = "") -> str:
        """Create full HTML page"""
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - X-Filamenta Documentation</title>
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
</head>
<body>
    <header>
        <h1>📚 X-Filamenta Documentation</h1>
    </header>

    <div class="container">
        <aside class="sidebar">
            {self.generate_sidebar()}
        </aside>

        <main class="main">
            {f'<div class="breadcrumb">{breadcrumb}</div>' if breadcrumb else ''}
            <article class="content">
                {content_html}
            </article>
        </main>
    </div>

    <footer>
        <p>&copy; 2025 XAREMA. Licensed under AGPL-3.0-or-later.</p>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</body>
</html>"""

    def generate_sidebar(self) -> str:
        """Generate sidebar navigation"""
        sidebar = """
        <div class="section">
            <div class="section-title">START</div>
            <ul>
                <li><a href="index.html">HOME</a></li>
                <li><a href="start-here.html">START HERE</a></li>
                <li><a href="reference.html">REFERENCE</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">GUIDES</div>
            <ul>
                <li><a href="guides.html">Overview</a></li>
                <li><a href="quickstart.html">Quick Start</a></li>
                <li><a href="installation.html">Installation</a></li>
                <li><a href="development.html">Development</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">FEATURES</div>
            <ul>
                <li><a href="features.html">Overview</a></li>
                <li><a href="authentication.html">Authentication</a></li>
                <li><a href="wizard.html">Wizard</a></li>
                <li><a href="i18n.html">i18n</a></li>
                <li><a href="database.html">Database</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">DEPLOYMENT</div>
            <ul>
                <li><a href="deployment.html">Overview</a></li>
                <li><a href="cpanel.html">cPanel</a></li>
                <li><a href="vps.html">VPS/Linux</a></li>
                <li><a href="docker.html">Docker</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">ARCHITECTURE</div>
            <ul>
                <li><a href="architecture.html">Overview</a></li>
                <li><a href="backend.html">Backend</a></li>
                <li><a href="frontend.html">Frontend</a></li>
                <li><a href="wsgi.html">WSGI</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">SECURITY</div>
            <ul>
                <li><a href="security.html">Overview</a></li>
                <li><a href="best-practices.html">Best Practices</a></li>
                <li><a href="csrf.html">CSRF</a></li>
                <li><a href="2fa.html">2FA</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">TROUBLESHOOTING</div>
            <ul>
                <li><a href="issues.html">Common Issues</a></li>
                <li><a href="faq.html">FAQ</a></li>
            </ul>
        </div>

        <div class="section">
            <div class="section-title">ANALYSIS</div>
            <ul>
                <li><a href="analysis.html">Reports</a></li>
            </ul>
        </div>
        """
        return sidebar

    def create_index(self) -> str:
        """Create index page"""
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
            <div class="section">
                <div class="section-title">NAVIGATION</div>
                <ul>
                    <li><a href="start-here.html">START HERE</a></li>
                    <li><a href="reference.html">REFERENCE</a></li>
                </ul>
            </div>
        </aside>

        <main class="main">
            <article class="content">
                <h1>Welcome to X-Filamenta Documentation</h1>

                <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
                    <strong>Version:</strong> 0.0.1-Alpha |
                    <strong>License:</strong> AGPL-3.0-or-later
                </p>

                <div class="alert alert-info">
                    <strong>👋 Start here:</strong> Read <a href="start-here.html">START HERE</a> to find what you need.
                </div>

                <h2>Documentation Sections</h2>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
                    <div class="card">
                        <h3>🚀 Getting Started</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="start-here.html">Start Here</a></li>
                            <li><a href="quickstart.html">Quick Start</a></li>
                            <li><a href="guides.html">Guides</a></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>✨ Features</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="authentication.html">Authentication</a></li>
                            <li><a href="wizard.html">Installation Wizard</a></li>
                            <li><a href="features.html">All Features</a></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>🚀 Deployment</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="cpanel.html">cPanel</a></li>
                            <li><a href="vps.html">VPS/Linux</a></li>
                            <li><a href="docker.html">Docker</a></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>🏗️ Architecture</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="architecture.html">Overview</a></li>
                            <li><a href="backend.html">Backend</a></li>
                            <li><a href="frontend.html">Frontend</a></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>🔒 Security</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="best-practices.html">Best Practices</a></li>
                            <li><a href="2fa.html">2FA</a></li>
                            <li><a href="security.html">All Security</a></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>❓ Help</h3>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                            <li><a href="faq.html">FAQ</a></li>
                            <li><a href="issues.html">Common Issues</a></li>
                            <li><a href="reference.html">Reference</a></li>
                        </ul>
                    </div>
                </div>

                <h2>About X-Filamenta</h2>
                <p>
                    X-Filamenta is a web application built with Flask, HTMX, and Bootstrap 5.
                    It features multi-language support, 2FA authentication, and flexible database configuration.
                </p>

                <h2>Key Features</h2>
                <ul>
                    <li>✅ Multi-language support (EN, FR)</li>
                    <li>✅ 2FA TOTP authentication</li>
                    <li>✅ Installation wizard</li>
                    <li>✅ Support for SQLite, MySQL, PostgreSQL</li>
                    <li>✅ HTMX for dynamic UI</li>
                    <li>✅ Bootstrap 5 responsive design</li>
                </ul>
            </article>
        </main>
    </div>

    <footer>
        <p>&copy; 2025 XAREMA. Licensed under AGPL-3.0-or-later.</p>
    </footer>

    <style>
        .card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #ddd;
        }

        .card h3 {
            margin-top: 0;
            color: #0066cc;
        }

        .card a {
            color: #0066cc;
        }
    </style>
</body>
</html>"""

def main():
    print("Generating HTML documentation...")
    generator = DocGenerator()

    # Create CSS
    css_content = """/* X-Filamenta Documentation */

:root {
    --primary: #0066cc;
    --secondary: #666;
    --light: #f8f9fa;
    --dark: #212529;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: var(--dark); }

header {
    background: var(--dark);
    color: white;
    padding: 1.5rem 2rem;
    border-bottom: 3px solid var(--primary);
}

header h1 { margin: 0; font-size: 1.5rem; }

.container { display: flex; min-height: calc(100vh - 80px); }

.sidebar {
    width: 280px;
    background: var(--light);
    padding: 2rem;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    position: sticky;
    top: 0;
    height: calc(100vh - 80px);
}

.sidebar .section-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #999;
    margin: 1.5rem 0 0.75rem 0;
    font-weight: 700;
    letter-spacing: 1px;
}

.sidebar ul { list-style: none; }
.sidebar li { margin-bottom: 0.5rem; }
.sidebar a {
    color: var(--secondary);
    text-decoration: none;
    display: block;
    padding: 0.5rem 0.75rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.sidebar a:hover { background: rgba(0, 102, 204, 0.1); color: var(--primary); padding-left: 1rem; }

.main {
    flex: 1;
    padding: 2rem;
    max-width: 900px;
    overflow-y: auto;
}

.content h1 {
    font-size: 2rem;
    margin: 0 0 1rem 0;
    border-bottom: 3px solid var(--primary);
    padding-bottom: 0.5rem;
}

.content h2 { font-size: 1.5rem; margin: 1.5rem 0 0.75rem 0; }
.content h3 { font-size: 1.25rem; margin: 1.25rem 0 0.5rem 0; }

a { color: var(--primary); text-decoration: none; border-bottom: 1px solid transparent; }
a:hover { border-bottom-color: var(--primary); }

code {
    background: var(--light);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: monospace;
    font-size: 0.9rem;
}

pre {
    background: var(--dark);
    color: #fff;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1rem 0;
}

table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
table th, table td { padding: 0.75rem; border: 1px solid #ddd; text-align: left; }
table th { background: var(--light); font-weight: 600; }

.alert {
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    border-left: 4px solid;
}

.alert-info { background: #d1ecf1; border-color: #17a2b8; color: #0c5460; }
.alert-warning { background: #fff3cd; border-color: #ff9800; color: #856404; }
.alert-danger { background: #f8d7da; border-color: #dc3545; color: #721c24; }
.alert-success { background: #d4edda; border-color: #28a745; color: #155724; }

footer {
    background: var(--light);
    padding: 2rem;
    text-align: center;
    color: var(--secondary);
    font-size: 0.9rem;
    border-top: 1px solid #ddd;
}

@media (max-width: 768px) {
    .container { flex-direction: column; }
    .sidebar { width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid #ddd; }
    .main { padding: 1rem; }
}
"""

    (generator.output_dir / "style.css").write_text(css_content)
    (generator.output_dir / "index.html").write_text(generator.create_index())

    print(f"✓ Created CSS and index")
    print(f"✓ Output: {generator.output_dir.absolute()}")
    print(f"\nNext: Run 'python scripts/convert_md_to_html.py' to convert all markdown files")

if __name__ == "__main__":
    main()

