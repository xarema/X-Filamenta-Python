# Python & Flask Rules

**Purpose:** Python and Flask-specific coding rules (auto-loaded for *.py files)  
**File:** `.github/python.instructions.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

**Metadata:**
- Status:  Stable
- Classification: Internal
- Auto-loaded: Yes (for *.py files)

---

## 1) Project Structure

### 1.1 Flask Application Factory

- Use an **app factory pattern** (`create_app()`)
- Register **Blueprints** for route organization
- Keep configuration in `backend/src/config.py`

**Example:**

```python
def create_app(config_name:  str = "development") -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Register blueprints
    from . routes import main_bp, wizard_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(wizard_bp, url_prefix="/wizard")
    
    return app
```

### 1.2 Route Organization

- Keep route handlers **thin**: 
  - Input parsing/validation at the edge
  - Business logic in services (`backend/src/services/`)
  - Data access in repositories (`backend/src/repositories/`) if applicable
- Prefer pure functions for domain logic when possible

**Example:**

```python
# ❌ BAD:  Business logic in route
@bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# ✅ GOOD:  Thin route, logic in service
@bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = user_service.create_user(data)
    return jsonify(user.to_dict()), 201
```

---

## 2) Types & Style

### 2.1 Python Version

- Target: **Python 3.12**
- Use modern Python features (structural pattern matching, type unions with `|`, etc.)

### 2.2 Type Hints (Mandatory)

**Add type hints to:**
- Function parameters
- Function return values
- Class attributes
- Complex variables

**Examples:**

```python
from typing import Optional, Dict, List, Any

def calculate_total(items: List[Dict[str, Any]], tax_rate: float = 0.2) -> float:
    """Calculate total price with tax."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    return subtotal * (1 + tax_rate)

def get_user_by_id(user_id: int) -> Optional[User]:
    """Retrieve user by ID, or None if not found."""
    return User.query.get(user_id)
```

### 2.3 Code Formatting

- **Formatter:** Black
- **Line length:** 88 characters
- **Indentation:** 4 spaces (no tabs)

**Run before commit:**

```powershell
. \.venv\Scripts\ruff. exe format . 
```

### 2.4 Linting

- **Linter:** Ruff
- Fix issues before committing

**Run:**

```powershell
.\.venv\Scripts\ruff. exe check .
. \.venv\Scripts\ruff.exe check .  --fix  # Auto-fix safe issues
```

### 2.5 Type Checking

- **Tool:** Mypy
- Target: `backend/src/`

**Run:**

```powershell
.\.venv\Scripts\mypy. exe backend/src
```

---

## 3) Logging

### 3.1 Use `logging`, NOT `print`

**Always use Python's logging module:**

```python
import logging

logger = logging.getLogger(__name__)

# Examples
logger.debug("Debug info:  %s", data)
logger.info("User %s logged in", user_id)
logger.warning("Config missing, using default:  %s", default_value)
logger.error("Failed to connect to database:  %s", error)
logger.exception("Unhandled exception in view")  # Includes traceback
```

### 3.2 Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed diagnostic info (dev only) |
| `INFO` | General informational messages (important events) |
| `WARNING` | Warning about potential issues |
| `ERROR` | Error occurred but app continues |
| `CRITICAL` | Critical error, app may stop |

### 3.3 Sensitive Data

**NEVER log:**
- Passwords
- API keys/tokens
- PII (personal identifiable information)
- Full credit card numbers

**If needed, mask:**

```python
logger.info("Processing payment for card ending in %s", card_number[-4:])
```

---

## 4) Error Handling

### 4.1 HTTP Status Codes

**Use correct status codes:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input/validation error |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 500 | Internal Server Error | Unexpected server error |

### 4.2 Error Response Format

**Use consistent JSON structure:**

```python
from flask import jsonify

@bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": str(error),
        "status": 400
    }), 400

@bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "Resource not found",
        "status": 404
    }), 404
```

### 4.3 Don't Leak Internal Errors in Production

```python
import os
from flask import current_app

@bp.errorhandler(500)
def internal_error(error):
    logger.exception("Internal error occurred")
    
    # In production, hide details
    if current_app.config.get("ENV") == "production":
        message = "An unexpected error occurred.  Please try again later."
    else:
        message = str(error)
    
    return jsonify({
        "error":  "Internal Server Error",
        "message": message,
        "status": 500
    }), 500
```

---

## 5) API Design

### 5.1 Input Validation

**Always validate and sanitize inputs:**

```python
from flask import request, abort

@bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    
    # Validate required fields
    if not data or "email" not in data or "name" not in data: 
        abort(400, description="Missing required fields:  email, name")
    
    # Validate format
    if not is_valid_email(data["email"]):
        abort(400, description="Invalid email format")
    
    # Sanitize
    clean_data = {
        "email": data["email"]. strip().lower(),
        "name": data["name"].strip()
    }
    
    user = user_service.create_user(clean_data)
    return jsonify(user.to_dict()), 201
```

### 5.2 Use Parameterized Queries (Security)

**NEVER use string formatting for SQL:**

```python
# ❌ NEVER DO THIS (SQL injection risk)
query = f"SELECT * FROM users WHERE email = '{email}'"
result = db.engine.execute(query)

# ✅ ALWAYS use parameterized queries
from sqlalchemy import text

query = text("SELECT * FROM users WHERE email = :email")
result = db.session.execute(query, {"email":  email})

# ✅ BETTER:  Use ORM
user = User.query.filter_by(email=email).first()
```

### 5.3 Idempotency

**GET requests must NOT have side effects:**

```python
# ❌ BAD:  GET request modifies data
@bp.route("/users/<int:user_id>/activate", methods=["GET"])
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active = True
    db.session. commit()
    return "OK"

# ✅ GOOD: Use POST/PUT/PATCH for modifications
@bp.route("/users/<int:user_id>/activate", methods=["POST"])
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active = True
    db.session.commit()
    return jsonify(user.to_dict()), 200
```

---

## 6) Testing (pytest)

### 6.1 Test Structure

**Location:** `tests/`

**Naming:**
- Test files: `test_*.py`
- Test functions: `test_*`

### 6.2 What to Test

**Every behavior change should include tests:**
- ✅ Happy path (normal flow)
- ✅ Edge cases (boundary conditions)
- ✅ Error cases (invalid input, failures)

**Example:**

```python
import pytest
from backend.src import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def test_create_user_success(client):
    """Test successful user creation."""
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example. com"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_create_user_missing_email(client):
    """Test user creation fails without email."""
    response = client. post("/users", json={"name": "John Doe"})
    assert response.status_code == 400
    data = response.get_json()
    assert "email" in data["message"]. lower()

def test_create_user_invalid_email(client):
    """Test user creation fails with invalid email."""
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "not-an-email"
    })
    assert response.status_code == 400
```

### 6.3 Deterministic Tests

**Tests must be fast and deterministic:**
- ❌ No real network calls (mock external APIs)
- ❌ No real database calls (use in-memory SQLite or fixtures)
- ❌ No reliance on current time (freeze/patch `datetime.now()`)

**Example (mocking):**

```python
from unittest.mock import patch

@patch("backend.src.services.user_service.send_welcome_email")
def test_create_user_sends_email(mock_send_email, client):
    """Test that creating user sends welcome email."""
    response = client.post("/users", json={
        "name": "Jane",
        "email": "jane@example.com"
    })
    assert response.status_code == 201
    mock_send_email.assert_called_once_with("jane@example.com")
```

### 6.4 Fixtures

**Use pytest fixtures for setup:**

```python
import pytest
from backend.src.models import User

@pytest.fixture
def sample_user(db):
    """Create a sample user for testing."""
    user = User(name="Test User", email="test@example.com")
    db.session.add(user)
    db.session.commit()
    return user

def test_get_user(client, sample_user):
    """Test retrieving a user by ID."""
    response = client.get(f"/users/{sample_user.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "test@example.com"
```

### 6.5 Running Tests

```powershell
# Run all tests
. \.venv\Scripts\pytest. exe

# Run with verbose output
.\.venv\Scripts\pytest.exe -v

# Run specific test file
.\.venv\Scripts\pytest.exe tests/test_users.py

# Run specific test
.\.venv\Scripts\pytest.exe tests/test_users. py::test_create_user_success
```

---

## 7) Database (SQLAlchemy)

### 7.1 Model Definition

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self. name,
            "created_at": self.created_at.isoformat(),
            "active":  self.active
        }
```

### 7.2 Migrations (Flask-Migrate)

**After model changes:**

```powershell
# Create migration
. \.venv\Scripts\flask. exe db migrate -m "Add user active field"

# Review migration file (in migrations/versions/)

# Apply migration
.\.venv\Scripts\flask.exe db upgrade
```

---

## 8) Environment & Configuration

### 8.1 Configuration Files

**Location:** `backend/src/config.py`

**Structure:**

```python
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-prod"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config = {
    "development":  DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
```

### 8.2 Environment Variables

**NEVER commit secrets to Git.**

**Use `.env` file (local only, in `.gitignore`):**

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

**Load with `python-dotenv`:**

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 9) PowerShell Integration

**For command execution, see:** `.github/powershell.instructions.md`

**Python-specific commands:**

```powershell
# Activate venv
. \.venv\Scripts\Activate.ps1

# Run Flask app
.\.venv\Scripts\python.exe backend\src\app.py

# Run tests
.\.venv\Scripts\pytest.exe

# Install dependencies
.\.venv\Scripts\pip.exe install -r requirements. txt
```

---

## 10) Don'ts

- ❌ Use `print()` for logging
- ❌ Hardcode secrets/credentials
- ❌ Use string formatting for SQL queries
- ❌ Forget type hints
- ❌ Skip tests for behavior changes
- ❌ Use `python` directly (always use `.venv\Scripts\python.exe`)
- ❌ Commit without running linters (Ruff, Mypy)

---

**See Also:**
- `.github/copilot-instructions.md` — General project rules
- `.github/frontend.instructions.md` — HTMX/Bootstrap/i18n rules
- `.github/powershell.instructions.md` — PowerShell commands
- `.github/workflow-rules.md` — Workflow process