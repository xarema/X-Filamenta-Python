"""
Purpose: Development guides

File: docs/guides/README.md | Repository: Template-Python
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
- Development and contribution guides here
- Git history is the source of truth for authorship and change tracking.
"""

# Development Guides

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Template-Python
   ```

2. **Setup Python environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # OR
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   npm install
   ```

4. **Run development server**
   ```bash
   make dev
   # OR
   python -m backend.src
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## Writing Code

- See [STRUCTURE.md](../../STRUCTURE.md) for folder organization
- See [copilot-instructions.md](.github/copilot-instructions.md) for coding conventions
- Add type hints to new Python code
- Comment non-obvious logic
- Keep functions small and testable

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest backend/tests/unit/test_validators.py -v

# With coverage
pytest --cov=backend/src backend/tests
```

## Code Quality

```bash
# Type checking
mypy backend/src

# Linting
ruff check backend/ frontend/

# Format code
ruff format backend/ frontend/
npm run format
```

## Database Migrations (if using SQLAlchemy)

```bash
# Create a migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade
```

## Deployment

(Configure as needed)

## Troubleshooting

### Port 5000 already in use
```bash
# Change port in .env or use:
FLASK_RUN_PORT=5001 python -m backend.src
```

### Module import errors
```bash
# Make sure you're in the correct venv and have installed deps:
pip install -e .
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) (create if needed)

