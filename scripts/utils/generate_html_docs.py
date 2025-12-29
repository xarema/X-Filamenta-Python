"""
Purpose: Generate complete HTML documentation from Markdown files
Description: Converts all project Markdown docs to navigable HTML with proper formatting

File: scripts/utils/generate_html_docs.py | Repository: X-Filamenta-Python
Created: 2025-12-28T21:45:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Force UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("WARNING: 'markdown' package not installed. Using basic conversion.")
    print("   Install with: pip install Markdown")


PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_ROOT = PROJECT_ROOT / "docs"
HTML_OUTPUT = DOCS_ROOT / "HTML"
ANALYSIS_REPORTS = PROJECT_ROOT / "Analysis_reports"

# Navigation structure
NAV_SECTIONS = {
    "Getting Started": [
        ("index.html", "Home"),
        ("00_START_HERE.html", "Start Here"),
        ("guides-QUICKSTART.html", "Quick Start"),
        ("REFERENCE.html", "Reference"),
    ],
    "Features": [
        ("features-README.html", "Overview"),
        ("features-authentication.html", "Authentication"),
        ("features-wizard-installation.html", "Installation Wizard"),
        ("features-internationalization.html", "Internationalization"),
        ("features-database.html", "Database Support"),
    ],
    "Deployment": [
        ("deployment-DEPLOYMENT.html", "Overview"),
        ("deployment-DEPLOYMENT_CPANEL.html", "cPanel"),
        ("deployment-DEPLOYMENT_VPS.html", "VPS/Linux"),
        ("deployment-DEPLOYMENT_DOCKER.html", "Docker"),
    ],
    "Architecture": [
        ("architecture-README.html", "Overview"),
        ("DATABASE.html", "Database"),
        ("technical-WSGI_AND_MULTIDB_ADAPTATION.html", "WSGI & Multi-DB"),
    ],
    "Security": [
        ("security-README.html", "Overview"),
    ],
    "Contributing": [
        ("contributing-README.html", "Guidelines"),
    ],
    "Help": [
        ("troubleshooting-README.html", "Troubleshooting"),
        ("troubleshooting-faq.html", "FAQ"),
        ("troubleshooting-common-issues.html", "Common Issues"),
        ("analysis-reports.html", "Analysis Reports"),
    ],
}


def get_html_filename(md_path: Path) -> str:
    """Convert markdown path to HTML filename."""
    relative = md_path.relative_to(DOCS_ROOT)
    parts = list(relative.parts)

    # Remove .md extension
    parts[-1] = parts[-1].replace(".md", "")

    # Join with hyphens
    html_name = "-".join(parts) + ".html"

    return html_name


def extract_title(md_path: Path) -> str:
    """Extract title from markdown file."""
    try:
        content = md_path.read_text(encoding="utf-8")

        # Try to find first # heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fallback to filename
        return md_path.stem.replace("-", " ").replace("_", " ").title()
    except Exception:
        return md_path.stem


def convert_markdown_to_html(content: str) -> str:
    """Convert markdown content to HTML."""
    if HAS_MARKDOWN:
        # Use markdown library with extensions
        md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'tables',
                'toc',
                'codehilite',
                'nl2br',
                'sane_lists',
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False,
                }
            }
        )
        return md.convert(content)
    else:
        # Basic fallback conversion
        html = content

        # Headers
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

        # Code blocks
        html = re.sub(
            r"```(\w+)?\s*\n(.*?)\n```",
            r'<pre><code class="language-\1">\2</code></pre>',
            html,
            flags=re.DOTALL
        )

        # Inline code
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

        # Bold and italic
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

        # Links
        html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)

        # Lists
        html = re.sub(r"^- (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)

        # Paragraphs
        lines = html.split("\n")
        new_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith("<"):
                new_lines.append(f"<p>{line}</p>")
            else:
                new_lines.append(line)
        html = "\n".join(new_lines)

        return html


def generate_sidebar() -> str:
    """Generate sidebar HTML."""
    html = ""

    for section, links in NAV_SECTIONS.items():
        html += f'<div class="sidebar-section">\n'
        html += f'  <div class="sidebar-title">{section}</div>\n'
        html += '  <ul>\n'

        for href, label in links:
            html += f'    <li><a href="{href}">{label}</a></li>\n'

        html += '  </ul>\n'
        html += '</div>\n'

    return html


def generate_html_page(title: str, content: str, is_index: bool = False) -> str:
    """Generate complete HTML page."""
    sidebar = generate_sidebar()

    template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="X-Filamenta Documentation - {title}">
    <title>{title} - X-Filamenta Documentation</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>📚 X-Filamenta Documentation</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="all-pages.html">All Pages</a>
            <a href="analysis-reports.html">Analysis Reports</a>
        </nav>
    </header>

    <div class="container">
        <aside class="sidebar">
            {sidebar}
        </aside>

        <main class="main">
            {content}

            <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e0e0e0;">
                <p style="color: #666; font-size: 0.9rem;">
                    © 2025 XAREMA. Licensed under <strong>AGPL-3.0-or-later</strong>.
                    <a href="https://github.com/XAREMA" target="_blank">View source</a>
                </p>
            </footer>
        </main>
    </div>
</body>
</html>
"""
    return template


def process_markdown_file(md_path: Path) -> Tuple[str, str, str]:
    """Process single markdown file and return (filename, title, html)."""
    title = extract_title(md_path)
    html_filename = get_html_filename(md_path)

    # Read and convert content
    content = md_path.read_text(encoding="utf-8")

    # Remove YAML frontmatter if present
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

    # Remove HTML comments
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

    html_content = convert_markdown_to_html(content)
    full_html = generate_html_page(title, html_content)

    return html_filename, title, full_html


def generate_all_pages_index(pages: List[Tuple[str, str]]) -> str:
    """Generate index page with all documentation pages."""
    pages_by_category: Dict[str, List[Tuple[str, str]]] = {}

    for filename, title in sorted(pages, key=lambda x: x[1]):
        # Determine category from filename prefix
        if "-" in filename:
            category = filename.split("-")[0].title()
        else:
            category = "General"

        if category not in pages_by_category:
            pages_by_category[category] = []

        pages_by_category[category].append((filename, title))

    content = "<h1>All Documentation Pages</h1>\n"
    content += '<p class="alert alert-info">Complete index of all documentation files.</p>\n'

    for category, items in sorted(pages_by_category.items()):
        content += f"<h2>{category}</h2>\n<ul>\n"
        for filename, title in sorted(items, key=lambda x: x[1]):
            content += f'  <li><a href="{filename}">{title}</a></li>\n'
        content += "</ul>\n"

    return generate_html_page("All Pages", content)


def generate_analysis_reports_index() -> str:
    """Generate index page for analysis reports."""
    if not ANALYSIS_REPORTS.exists():
        content = "<h1>Analysis Reports</h1>\n"
        content += '<p class="alert alert-warning">No analysis reports found.</p>\n'
        return generate_html_page("Analysis Reports", content)

    reports = sorted(ANALYSIS_REPORTS.glob("*.md"), reverse=True)

    content = "<h1>Analysis Reports</h1>\n"
    content += f'<p class="alert alert-info">Found {len(reports)} analysis reports.</p>\n'

    # Group by date
    by_date: Dict[str, List[Path]] = {}
    for report in reports:
        # Extract date from filename (YYYY-MM-DD_...)
        match = re.match(r"(\d{4}-\d{2}-\d{2})_", report.name)
        if match:
            date = match.group(1)
            if date not in by_date:
                by_date[date] = []
            by_date[date].append(report)
        else:
            if "Other" not in by_date:
                by_date["Other"] = []
            by_date["Other"].append(report)

    for date in sorted(by_date.keys(), reverse=True):
        content += f"<h2>{date}</h2>\n<ul>\n"
        for report in sorted(by_date[date]):
            title = extract_title(report)
            html_name = "reports-" + report.name.replace(".md", ".html")
            content += f'  <li><a href="{html_name}">{title}</a></li>\n'
        content += "</ul>\n"

    return generate_html_page("Analysis Reports", content)


def main():
    """Main function to generate all HTML documentation."""
    print("=== Generating HTML Documentation ===")
    print(f"Project: {PROJECT_ROOT}")
    print(f"Docs: {DOCS_ROOT}")
    print(f"Output: {HTML_OUTPUT}")
    print()

    # Create output directory
    HTML_OUTPUT.mkdir(parents=True, exist_ok=True)

    # Find all markdown files
    md_files = list(DOCS_ROOT.rglob("*.md"))
    md_files = [f for f in md_files if "HTML" not in str(f) and ".git" not in str(f)]

    print(f"Found {len(md_files)} markdown files in docs/")

    # Process analysis reports
    if ANALYSIS_REPORTS.exists():
        report_files = list(ANALYSIS_REPORTS.glob("*.md"))
        print(f"Found {len(report_files)} analysis reports")
        md_files.extend(report_files)

    print()

    # Convert all files
    all_pages: List[Tuple[str, str]] = []
    converted = 0

    for md_file in md_files:
        try:
            # Determine if it's a report
            is_report = "Analysis_reports" in str(md_file)

            if is_report:
                # Process report
                title = extract_title(md_file)
                html_filename = "reports-" + md_file.name.replace(".md", ".html")
                content = md_file.read_text(encoding="utf-8")
                content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
                content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
                html_content = convert_markdown_to_html(content)
                full_html = generate_html_page(title, html_content)
            else:
                # Process regular doc
                html_filename, title, full_html = process_markdown_file(md_file)

            # Save HTML file
            output_path = HTML_OUTPUT / html_filename
            output_path.write_text(full_html, encoding="utf-8")

            all_pages.append((html_filename, title))
            converted += 1

            print(f"OK {md_file.name} -> {html_filename}")

        except Exception as e:
            print(f"ERROR processing {md_file.name}: {e}")

    print()
    print(f"Converted {converted} files")
    print()

    # Generate index pages
    print("Generating index pages...")

    # All pages index
    all_pages_html = generate_all_pages_index(all_pages)
    (HTML_OUTPUT / "all-pages.html").write_text(all_pages_html, encoding="utf-8")
    print("OK all-pages.html")

    # Analysis reports index
    reports_html = generate_analysis_reports_index()
    (HTML_OUTPUT / "analysis-reports.html").write_text(reports_html, encoding="utf-8")
    print("OK analysis-reports.html")

    print()
    print("=== Generation Complete ===")
    print(f"Output: {HTML_OUTPUT}")
    print()
    print("To view documentation:")
    print(f"  Start-Process '{HTML_OUTPUT}\\index.html'")


if __name__ == "__main__":
    main()

