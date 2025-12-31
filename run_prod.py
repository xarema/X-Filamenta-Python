#!/usr/bin/env python
"""
---
Purpose: Production server entry point
Description: Starts the Flask application using Waitress WSGI server for production deployment

File: run_prod.py | Repository: X-Filamenta-Python
Created: 2025-12-30T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Notes:
- Uses Waitress (pure Python WSGI server, no native extensions required)
- Production-ready: DEBUG=False, proper error handling
- Usage:
  - Development: FLASK_ENV=development python run_prod.py
  - Production: FLASK_ENV=production python run_prod.py
---
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from waitress import serve

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env or .env.production
env_path = project_root / ".env.production"
if not env_path.exists():
    env_path = project_root / ".env"

if env_path.exists():
    load_dotenv(env_path)

# Create Flask application
from backend.src.app import create_app

app = create_app()

# Configuration
HOST = os.getenv("WAITRESS_HOST", "127.0.0.1")
PORT = int(os.getenv("WAITRESS_PORT", 5000))
THREADS = int(os.getenv("WAITRESS_THREADS", 4))

if __name__ == "__main__":
    # Only run in development (for testing)
    # For production, use: gunicorn -w 4 -b 0.0.0.0:5000 backend.wsgi:app

    env = os.getenv("FLASK_ENV", "development").lower()
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    print(f"Starting Flask application")
    print(f"  Environment: {env}")
    print(f"  Debug: {debug}")
    print(f"  Host: {HOST}")
    print(f"  Port: {PORT}")
    print(f"  Threads: {THREADS}")
    print("")
    print(f"Serving on http://{HOST}:{PORT}")
    print(f"Press CTRL+C to quit")
    print("")

    try:
        # Use Waitress WSGI server (production-ready)
        serve(app, host=HOST, port=PORT, threads=THREADS, _quiet=False)
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

