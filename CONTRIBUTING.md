---
Purpose: Contribution guidelines for X-Filamenta-Python
Description: Instructions for contributing to the project

File: CONTRIBUTING.md | Repository: X-Filamenta-Python
Created: 2025-12-29T16:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public

---

# Contributing to X-Filamenta-Python

Thank you for your interest in contributing to X-Filamenta-Python! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Workflow](#workflow)
5. [Code Style](#code-style)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)
8. [Testing](#testing)
9. [Documentation](#documentation)
10. [Questions & Support](#questions--support)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Getting Started

### Prerequisites

- **OS:** Windows 11, Linux, or macOS
- **Python:** 3.12+
- **Node.js:** 18+ (for frontend tools)
- **Git:** Latest version
- **IDE:** IntelliJ IDEA (recommended for Python + Web) or VS Code

### Fork & Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```powershell
   git clone https://github.com/YOUR_USERNAME/X-Filamenta-Python.git
   cd X-Filamenta-Python
   ```
3. Add upstream remote:
   ```powershell
   git remote add upstream https://github.com/XAREMA/X-Filamenta-Python.git
   ```

---

## Development Setup

### 1. Python Virtual Environment

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or use the provided setup script
.\.venv\Scripts\python.exe -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2. Frontend Setup

```powershell
npm install
npm run build
```

### 3. Database Setup

```powershell
# Create database and run migrations
.\.venv\Scripts\python.exe -m alembic upgrade head
```

### 4. Environment Configuration

Copy `.env.example` to `.env`:
```powershell
Copy-Item ".env.example" ".env"
```

Update `.env` with your local development settings.

---

## Workflow

### 1. Create a Feature Branch

```powershell
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

**Branch Naming Convention:**
- `feature/description-of-feature` — New features
- `fix/description-of-fix` — Bug fixes
- `docs/description` — Documentation updates
- `chore/description` — Maintenance tasks
- `test/description` — Test additions/fixes
- `refactor/description` — Code refactoring

### 2. Make Your Changes

- Make commits regularly (small, focused changes)
- Keep commits atomic (one logical change per commit)
- Reference issues in commit messages when applicable

### 3. Keep Your Branch Updated

```powershell
git fetch upstream
git rebase upstream/main
```

### 4. Push to Your Fork

```powershell
git push origin feature/your-feature-name
```

### 5. Open a Pull Request

Create a PR against `upstream/main` with:
- Clear title describing the change
- Description of what and why
- Reference to related issues
- Screenshots if UI changes

---

## Code Style

### Python

**Standards:**
- Black formatting (88 character line length)
- Ruff linting
- Type hints mandatory
- Docstrings for public functions/classes

**Run formatters:**
```powershell
.\.venv\Scripts\ruff.exe format .
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\mypy.exe backend/src
```

### Frontend (HTML/CSS/JS)

**Standards:**
- Prettier formatting
- ESLint rules
- Bootstrap 5 classes
- BEM naming for custom CSS

**Run formatters:**
```powershell
npm run fmt
npm run lint
```

### General Rules

- 88 character line length limit
- UTF-8 encoding
- LF line endings
- No trailing whitespace
- Comments explain *why*, not *what*

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that don't affect code meaning (formatting, etc.)
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `perf:` Code change that improves performance
- `test:` Adding or updating tests
- `chore:` Changes to build process, dependencies, tooling

### Examples

```
feat(auth): add two-factor authentication support

- Implement TOTP-based 2FA
- Add backup codes generation
- Update settings UI with 2FA controls

Closes #123
```

```
fix(wizard): correct database name generation

The database name was not respecting user input.
Now correctly uses the name provided in the form.

Fixes #456
```

---

## Pull Request Process

### Before Submitting

- [ ] All tests pass locally
- [ ] Code formatted with Black/Prettier
- [ ] Linters pass (Ruff, mypy, ESLint)
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No commented-out code
- [ ] No debug statements left in

### During Review

- Respond to feedback promptly
- Request changes if you disagree (with explanation)
- Keep discussions respectful
- Push additional commits as needed (don't force-push)

### Approval & Merge

Once approved:
- Maintainers will merge your PR
- Your branch will be deleted
- Your contribution will be in the next release

---

## Testing

### Running Tests

```powershell
# Run all tests
.\.venv\Scripts\pytest.exe -v

# Run specific test file
.\.venv\Scripts\pytest.exe backend/tests/unit/test_auth.py -v

# Run with coverage
.\.venv\Scripts\pytest.exe --cov=backend/src --cov-report=html
```

### Writing Tests

**Location:** `backend/tests/` or `frontend/tests/`

**Structure:**
- `unit/` — Unit tests (test individual functions)
- `integration/` — Integration tests (test across modules)
- `fixtures/` — Shared test data/fixtures

**Example:**
```python
import pytest
from backend.src.services.user_service import create_user

def test_create_user_success():
    user = create_user({"username": "test", "email": "test@example.com"})
    assert user.username == "test"
    assert user.email == "test@example.com"

def test_create_user_duplicate_email():
    create_user({"username": "user1", "email": "test@example.com"})
    with pytest.raises(ValueError):
        create_user({"username": "user2", "email": "test@example.com"})
```

---

## Documentation

### When to Document

- Public APIs (functions, classes, modules)
- Complex algorithms or business logic
- Configuration options
- User-facing features
- Breaking changes

### Documentation Standards

**Python Docstrings:**
```python
def create_user(user_data: dict) -> User:
    """
    Create a new user account.

    Args:
        user_data: Dictionary with 'username', 'email', 'password'

    Returns:
        User: The newly created user object

    Raises:
        ValueError: If email already exists or validation fails
    """
    ...
```

**Markdown Files:**
- Clear headings
- Code examples where applicable
- Links to related documentation
- Updated when code changes

---

## Questions & Support

- **GitHub Issues:** For bugs, features, questions → [Open an issue](../../issues)
- **Discussions:** For ideas and general questions → [GitHub Discussions](../../discussions)
- **Security Issues:** For security vulnerabilities → See [SECURITY.md](SECURITY.md)

---

## License

By contributing, you agree that your contributions will be licensed under the same AGPL-3.0-or-later license.

---

**Thank you for contributing to X-Filamenta-Python!** 🎉

