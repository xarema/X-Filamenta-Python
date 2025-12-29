"""
------------------------------------------------------------------------------
Purpose: WSGI application entry point
Description: WSGI entry point for production servers (cPanel, VPS, Docker).
             This file is used by WSGI servers like Gunicorn, uWSGI, etc.

File: backend/wsgi.py | Repository: X-Filamenta-Python
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
- Usage:
  - gunicorn backend.wsgi:app
  - uwsgi --http :5000 --wsgi-file backend/wsgi.py --callable app
  - cPanel: Add this file path to application startup
------------------------------------------------------------------------------
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from backend.src.app import create_app
from backend.src.config import get_config

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file if it exists
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Create Flask application
env = os.getenv("FLASK_ENV", "production")
config = get_config(env)

app = create_app(config=config)

# Application is ready for WSGI servers
if __name__ == "__main__":
    app.run()
