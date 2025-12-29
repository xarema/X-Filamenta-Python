"""
Purpose: Architecture documentation

File: docs/architecture/README.md | Repository: Template-Python
Created: 2025-12-26
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: TBD
SPDX-License-Identifier: NOASSERTION

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Document architecture decisions and patterns here
- Git history is the source of truth for authorship and change tracking.
"""

# Architecture

## Overview

This is a **monorepo** project using:
- **Backend:** Flask (Python 3.12)
- **Frontend:** HTMX + Bootstrap 5 + Jinja2 templates
- **Database:** (TBD — SQLite for dev, PostgreSQL for prod)
- **Deployment:** (TBD — Docker, Heroku, AWS, etc.)

## Key Patterns

### App Factory Pattern

Flask app is created via `create_app()` function in `backend/src/app.py`.
This allows multiple configurations (dev, test, prod).

### Blueprints

Routes are organized by domain in `backend/src/routes/`.
Each blueprint is a separate module (e.g., `api.py`, `auth.py`).

### Service Layer

Business logic is isolated in `backend/src/services/`.
Routes call services; services call models/database.

### HTMX-First Frontend

- Server renders **complete pages** on full requests
- Server returns **fragments** for HTMX requests
- Minimal custom JavaScript
- Bootstrap 5 for styling

## Data Flow

```
User Browser
    ↓ HTTP Request
Flask Routes (routes/*.py)
    ↓
Services (services/*.py)
    ↓
Models (models/*.py)
    ↓
Database / External APIs
    ↓
Response (JSON or HTML)
    ↓
Browser renders / HTMX updates
```

## Files to Create

- Architecture decision records (ADRs)
- Deployment diagrams
- Database schema

