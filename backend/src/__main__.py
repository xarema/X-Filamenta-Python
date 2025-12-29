"""
------------------------------------------------------------------------------
Purpose: Main entry point for running the Flask application
Description: Provides a CLI entry point for development server execution.

File: backend/src/__main__.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Git history is the source of truth for authorship and change tracking.
- Run with: python -m backend.src
------------------------------------------------------------------------------
"""

from backend.src.app import create_app


def main() -> None:
    """
    Start the Flask development server.

    Configuration:
        - Host: 127.0.0.1 (localhost only)
        - Port: 5000
        - Debug: True (auto-reload enabled)

    Notes:
        - For production, use a WSGI server like Gunicorn or uWSGI
        - Never use debug=True in production
    """
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
