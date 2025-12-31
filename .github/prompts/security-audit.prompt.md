# Complete Project Audit & Security Remediation - Lead Engineer Mission

You are a **Lead Engineer / Security Engineer** with 10+ years of experience in production systems, security auditing, and enterprise-grade code quality. Your mission is to perform a **COMPREHENSIVE AUDIT** and **COMPLETE REMEDIATION** of this Flask + HTMX project.

---

## 🎯 Mission Objectives

1. **Security Audit** - Identify and fix ALL security vulnerabilities
2. **Code Quality Audit** - Ensure production-grade code standards
3. **AI Configuration Audit** - Review and optimize `.github/` AI rules and workflows
4. **Automated Remediation** - Apply fixes automatically where safe
5. **Type Safety & Linting** - Full mypy + ruff compliance
6. **Penetration Testing** - Simulate attacks and patch weaknesses
7. **Performance Analysis** - Identify and fix bottlenecks
8. **Compliance Check** - Ensure OWASP, GDPR, and best practices

---

## 🔐 Phase 1: Security Audit

### 1.1 Dependency Security Scan

**Objective:** Find vulnerable dependencies and outdated packages. 

```bash
# Check for known vulnerabilities
pip-audit
safety check --json

# Analyze dependency tree
pipdeptree --warn

# Check for outdated packages
pip list --outdated
```

**What to Look For:**
- [ ] CVEs in dependencies (use `pip-audit` or `safety`)
- [ ] Outdated packages with security patches
- [ ] Unnecessary dependencies that increase attack surface
- [ ] Pinned versions vs.  version ranges (prefer exact pins)
- [ ] Transitive dependencies with vulnerabilities

**Remediation Actions:**
- Upgrade all packages to latest secure versions
- Remove unused dependencies
- Add `pip-audit` to CI/CD pipeline
- Create `requirements-security.txt` for security tools

### 1.2 Secrets & Credentials Scan

**Objective:** Ensure no secrets are committed to the repository.

```bash
# Scan for secrets in history
git secrets --scan-history
trufflehog git file://.  --only-verified

# Check current files
gitleaks detect --source .  --verbose
```

**What to Look For:**
- [ ] API keys, tokens, passwords in code
- [ ] Hardcoded credentials in config files
- [ ] `.env` files committed (should be in `.gitignore`)
- [ ] Database connection strings with passwords
- [ ] Private keys, certificates
- [ ] AWS/Cloud credentials

**Remediation Actions:**
- Remove secrets from Git history (use `git filter-branch` or BFG)
- Move all secrets to environment variables
- Use secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
- Add pre-commit hooks to prevent secret commits
- Rotate ALL exposed credentials immediately

### 1.3 Code Security Vulnerabilities

**Objective:** Find and fix code-level security issues.

```bash
# Static security analysis
bandit -r app/ -f json -o bandit-report.json
semgrep --config=auto app/

# SAST (Static Application Security Testing)
python -m flake8_bandit app/
```

**Critical Vulnerabilities to Check:**

#### SQL Injection
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ SECURE
query = "SELECT * FROM users WHERE id = ?"
db. execute(query, (user_id,))
```

#### XSS (Cross-Site Scripting)
```python
# ❌ VULNERABLE
return f"<div>{user_input}</div>"

# ✅ SECURE - Jinja2 auto-escapes
return render_template('page.html', data=user_input)
# Or explicitly escape
from markupsafe import escape
return f"<div>{escape(user_input)}</div>"
```

#### CSRF Protection
```python
# ✅ REQUIRED - Flask-WTF handles this
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
```

#### Path Traversal
```python
# ❌ VULNERABLE
file_path = os.path.join('/uploads', request.args.get('filename'))

# ✅ SECURE
from werkzeug.utils import secure_filename
filename = secure_filename(request.args.get('filename'))
file_path = os.path.join('/uploads', filename)
```

#### Command Injection
```python
# ❌ VULNERABLE
os.system(f"ping {user_input}")

# ✅ SECURE
import subprocess
subprocess.run(['ping', user_input], check=True, timeout=5)
```

#### Insecure Deserialization
```python
# ❌ VULNERABLE
import pickle
data = pickle.loads(user_data)

# ✅ SECURE
import json
data = json.loads(user_data)
```

**Remediation Checklist:**
- [ ] All user inputs are validated and sanitized
- [ ] All database queries use parameterized statements
- [ ] CSRF protection enabled on all forms
- [ ] Content Security Policy (CSP) headers configured
- [ ] Secure session configuration
- [ ] Password hashing with bcrypt/argon2 (never plain text)
- [ ] Rate limiting on authentication endpoints
- [ ] Secure file upload handling

### 1.4 Flask Security Configuration

**Objective:** Harden Flask application configuration.

```python
# config.py - SECURE CONFIGURATION

import os
from datetime import timedelta

class ProductionConfig: 
    # Secret Key - MUST be random and stored securely
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")
    
    # Security Headers
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Prevent clickjacking
    X_FRAME_OPTIONS = 'DENY'
    
    # XSS Protection
    X_CONTENT_TYPE_OPTIONS = 'nosniff'
    X_XSS_PROTECTION = '1; mode=block'
    
    # HSTS (HTTP Strict Transport Security)
    STRICT_TRANSPORT_SECURITY = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    CONTENT_SECURITY_POLICY = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"
    
    # Database - Use connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Disable debug in production
    DEBUG = False
    TESTING = False
    
    # File Upload Security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_EXTENSIONS = {'.jpg', '.png', '.gif', '.pdf'}
```

**Security Middleware:**

```python
# app/__init__.py

from flask import Flask
from flask_talisman import Talisman  # Force HTTPS
from flask_limiter import Limiter  # Rate limiting
from flask_limiter. util import get_remote_address

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Force HTTPS and security headers
    Talisman(app, 
             force_https=True,
             strict_transport_security=True,
             content_security_policy=app.config['CONTENT_SECURITY_POLICY'])
    
    # Rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    
    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return app
```

### 1.5 Authentication & Authorization Audit

**Objective:** Ensure secure user authentication. 

**Checklist:**
- [ ] Passwords hashed with bcrypt (min 12 rounds) or Argon2
- [ ] Password complexity requirements enforced
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow
- [ ] Multi-factor authentication (2FA) available
- [ ] Session timeout implemented
- [ ] Secure "Remember Me" functionality
- [ ] Role-Based Access Control (RBAC) implemented
- [ ] Privilege escalation prevented

**Example Secure Authentication:**

```python
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"

# Password hashing
hashed = bcrypt.generate_password_hash(password, rounds=12).decode('utf-8')

# Verification with timing attack protection
if bcrypt.check_password_hash(user. password_hash, password):
    # Login successful
    pass
```

### 1.6 API Security (if applicable)

**Checklist:**
- [ ] API authentication (OAuth2, JWT, API keys)
- [ ] Input validation on all endpoints
- [ ] Rate limiting per endpoint
- [ ] CORS properly configured
- [ ] API versioning implemented
- [ ] Sensitive data not exposed in responses
- [ ] Proper HTTP status codes
- [ ] Request size limits

---

## 📊 Phase 2: Code Quality Audit

### 2.1 Type Safety with mypy

**Objective:** Achieve 100% type coverage and zero mypy errors.

```bash
# Run mypy with strict settings
mypy app/ --strict --show-error-codes --pretty
```

**mypy Configuration:**

```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_unimported = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
check_untyped_defs = True
strict_equality = True
strict = True

# Per-module options
[mypy-flask_sqlalchemy.*]
ignore_missing_imports = True

[mypy-wtforms.*]
ignore_missing_imports = True
```

**Type Annotations Required:**

```python
# ✅ PROPERLY TYPED

from typing import Optional, Dict, List, Any
from flask import Flask, Response
from werkzeug.wrappers import Response as WerkzeugResponse

def create_user(
    username: str,
    email: str,
    password: str,
    age: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new user account. 
    
    Args:
        username: Unique username for the account
        email: Valid email address
        password: Plain text password (will be hashed)
        age: Optional user age
        
    Returns:
        Dictionary containing user data
        
    Raises:
        ValueError: If username or email already exists
    """
    # Implementation
    return {"id": 1, "username": username}

@app.route('/users/<int:user_id>')
def get_user(user_id: int) -> WerkzeugResponse:
    """Retrieve user by ID."""
    user:  Optional[User] = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user. to_dict())
```

**Remediation:**
- Add type hints to ALL functions and methods
- Use `typing` module for complex types
- Fix all mypy errors before proceeding
- Add mypy to CI/CD pipeline

### 2.2 Linting with Ruff

**Objective:** Zero ruff violations with aggressive settings.

```bash
# Run ruff with auto-fix
ruff check app/ --fix

# Check without fixing
ruff check app/ --output-format=github
```

**Ruff Configuration:**

```toml
# pyproject.toml

[tool.ruff]
target-version = "py311"
line-length = 100
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "C",      # flake8-comprehensions
    "B",      # flake8-bugbear
    "UP",     # pyupgrade
    "N",      # pep8-naming
    "YTT",    # flake8-2020
    "ANN",    # flake8-annotations
    "ASYNC",  # flake8-async
    "S",      # flake8-bandit (security)
    "BLE",    # flake8-blind-except
    "FBT",    # flake8-boolean-trap
    "A",      # flake8-builtins
    "COM",    # flake8-commas
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "DJ",     # flake8-django
    "EM",     # flake8-errmsg
    "EXE",    # flake8-executable
    "ISC",    # flake8-implicit-str-concat
    "ICN",    # flake8-import-conventions
    "G",      # flake8-logging-format
    "INP",    # flake8-no-pep420
    "PIE",    # flake8-pie
    "T20",    # flake8-print
    "PYI",    # flake8-pyi
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SLF",    # flake8-self
    "SLOT",   # flake8-slots
    "SIM",    # flake8-simplify
    "TID",    # flake8-tidy-imports
    "TCH",    # flake8-type-checking
    "INT",    # flake8-gettext
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "TD",     # flake8-todos
    "FIX",    # flake8-fixme
    "ERA",    # eradicate
    "PD",     # pandas-vet
    "PGH",    # pygrep-hooks
    "PL",     # pylint
    "TRY",    # tryceratops
    "FLY",    # flynt
    "NPY",    # NumPy-specific rules
    "PERF",   # Perflint
    "RUF",    # Ruff-specific rules
]

ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
    "COM812",  # Trailing comma missing (conflicts with formatter)
    "ISC001",  # Single line implicit string concatenation
]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101", "ANN"]  # Allow assert and missing annotations in tests
"__init__.py" = ["F401"]      # Allow unused imports

[tool.ruff.flake8-bugbear]
extend-immutable-calls = ["fastapi. Depends", "flask.current_app"]

[tool.ruff.isort]
known-first-party = ["app"]
```

**Common Issues to Fix:**

```python
# ❌ BEFORE RUFF

def process_data(data):
    if data == None:  # Use 'is None'
        return
    
    result = []
    for item in data: 
        result.append(item * 2)  # Use list comprehension
    
    print(result)  # Don't use print in production
    return result

# ✅ AFTER RUFF

from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def process_data(data:  Optional[List[int]]) -> Optional[List[int]]:
    """Process data by doubling each element."""
    if data is None:
        return None
    
    result = [item * 2 for item in data]
    logger.debug("Processed %d items", len(result))
    return result
```

### 2.3 Code Complexity Analysis

**Objective:** Reduce cyclomatic complexity and improve maintainability.

```bash
# Measure complexity
radon cc app/ -a -nb
radon mi app/ -nb

# Find code smells
vulture app/
```

**Metrics to Achieve:**
- Cyclomatic Complexity: < 10 per function
- Maintainability Index:  > 20 (A or B grade)
- Lines per function: < 50
- Function parameters: < 5

**Refactoring Example:**

```python
# ❌ HIGH COMPLEXITY (CC = 15)

def process_order(order_data):
    if not order_data:
        return {"error": "No data"}
    
    if order_data. get('type') == 'standard':
        if order_data.get('priority') == 'high':
            if order_data.get('customer_type') == 'premium':
                price = calculate_premium_high_priority(order_data)
            else:
                price = calculate_standard_high_priority(order_data)
        else:
            if order_data.get('customer_type') == 'premium':
                price = calculate_premium_standard(order_data)
            else:
                price = calculate_standard(order_data)
    elif order_data.get('type') == 'express':
        # More nested conditions... 
        pass
    
    return {"price": price}

# ✅ LOW COMPLEXITY (CC = 3)

from dataclasses import dataclass
from enum import Enum

class OrderType(Enum):
    STANDARD = "standard"
    EXPRESS = "express"

class Priority(Enum):
    HIGH = "high"
    NORMAL = "normal"

class CustomerType(Enum):
    PREMIUM = "premium"
    STANDARD = "standard"

@dataclass
class Order:
    order_type: OrderType
    priority: Priority
    customer_type: CustomerType
    amount: float

class PriceCalculator:
    """Calculate prices based on order configuration."""
    
    def __init__(self):
        self._strategies = {
            (OrderType.STANDARD, Priority. HIGH, CustomerType.PREMIUM): 
                self._premium_high_priority,
            (OrderType. STANDARD, Priority.HIGH, CustomerType.STANDARD): 
                self._standard_high_priority,
            # ...  other strategies
        }
    
    def calculate(self, order:  Order) -> float:
        """Calculate price using strategy pattern."""
        key = (order.order_type, order.priority, order.customer_type)
        strategy = self._strategies.get(key, self._default_strategy)
        return strategy(order)
    
    def _premium_high_priority(self, order: Order) -> float:
        return order.amount * 0.9
    
    # ... other strategy methods

def process_order(order_data:  dict) -> dict:
    """Process order and calculate price."""
    if not order_data:
        return {"error": "No data"}
    
    order = Order(
        order_type=OrderType(order_data.get('type')),
        priority=Priority(order_data.get('priority')),
        customer_type=CustomerType(order_data.get('customer_type')),
        amount=order_data.get('amount', 0.0)
    )
    
    calculator = PriceCalculator()
    price = calculator.calculate(order)
    
    return {"price": price}
```

### 2.4 Documentation Audit

**Objective:** Complete, accurate documentation for all public APIs.

```bash
# Check docstring coverage
interrogate app/ -v --fail-under=100

# Generate documentation
pydoc-markdown -p app > docs/api/auto-generated.md
```

**Documentation Standards:**

```python
"""Module-level docstring describing the module's purpose. 

This module handles user authentication and session management.
It provides utilities for password hashing, token generation,
and user verification.
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class UserAuthenticator:
    """Handle user authentication and session management.
    
    This class provides methods for user login, logout, and
    session validation. It uses bcrypt for password hashing
    and implements rate limiting to prevent brute force attacks. 
    
    Attributes:
        max_attempts:  Maximum login attempts before lockout
        lockout_duration: Duration of account lockout in seconds
        
    Example:
        >>> auth = UserAuthenticator(max_attempts=5)
        >>> result = auth.login("user@example.com", "password123")
        >>> if result['success']:
        ...     print(f"Welcome {result['user']['name']}")
    """
    
    def __init__(
        self, 
        max_attempts: int = 5,
        lockout_duration: int = 900
    ) -> None:
        """Initialize the authenticator. 
        
        Args:
            max_attempts: Maximum failed login attempts allowed
            lockout_duration: Account lockout duration in seconds
            
        Raises:
            ValueError: If max_attempts < 1 or lockout_duration < 60
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if lockout_duration < 60:
            raise ValueError("lockout_duration must be at least 60 seconds")
            
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        logger.info(
            "UserAuthenticator initialized with max_attempts=%d",
            max_attempts
        )
    
    def login(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """Authenticate a user with email and password.
        
        This method verifies the user's credentials and creates
        a new session if authentication is successful.  It implements
        rate limiting and account lockout for security.
        
        Args:
            email: User's email address (case-insensitive)
            password: User's plaintext password
            
        Returns: 
            Dictionary with keys:
                - success (bool): Whether authentication succeeded
                - user (dict): User data if successful
                - error (str): Error message if failed
                - locked_until (datetime): Lockout expiry if account locked
                
        Raises: 
            ValueError: If email or password is empty
            DatabaseError: If database connection fails
            
        Example:
            >>> result = auth.login("user@example.com", "SecurePass123!")
            >>> if result['success']:
            ...     session['user_id'] = result['user']['id']
            ...  else:
            ...     flash(result['error'])
            
        Security: 
            - Passwords are never logged or stored in plaintext
            - Uses timing-safe comparison to prevent timing attacks
            - Rate limited to prevent brute force attacks
            - Account locked after max_attempts failures
        """
        # Implementation
        pass
```

**Checklist:**
- [ ] All modules have docstrings
- [ ] All classes have docstrings with attributes
- [ ] All public functions/methods have docstrings
- [ ] Docstrings follow Google or NumPy style
- [ ] Type hints match docstring descriptions
- [ ] Examples provided for complex functions
- [ ] Security considerations documented
- [ ] Exceptions documented

---

## 🤖 Phase 3: AI Configuration Audit (. github/)

### 3.1 GitHub Actions Workflows

**Objective:** Optimize CI/CD workflows for security and efficiency.

**Audit Checklist:**

```yaml
# .github/workflows/ci.yml - SECURE & OPTIMIZED

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 0'  # Weekly dependency check

permissions:
  contents: read  # Minimal permissions

jobs:
  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    permissions:
      security-events: write  # For CodeQL
      
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning
      
      - name:  Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pip-audit safety bandit semgrep
      
      - name: Dependency vulnerability scan
        run: |
          pip-audit --desc --strict
          safety check --json
        continue-on-error: false  # Fail on vulnerabilities
      
      - name:  Secret scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
      
      - name:  SAST with Bandit
        run: bandit -r app/ -f json -o bandit-report.json
      
      - name: SAST with Semgrep
        run: semgrep --config=auto app/ --json -o semgrep-report.json
      
      - name: Upload security reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: security-reports
          path: |
            bandit-report.json
            semgrep-report.json
  
  code-quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install mypy ruff black isort radon
      
      - name:  Type checking with mypy
        run: mypy app/ --strict --junit-xml mypy-report.xml
      
      - name: Linting with ruff
        run:  ruff check app/ --output-format=github
      
      - name: Format check
        run: |
          black --check app/
          isort --check-only app/
      
      - name:  Complexity analysis
        run: |
          radon cc app/ -a -nb --total-average
          radon mi app/ -nb
      
      - name:  Documentation coverage
        run: interrogate app/ --fail-under=95 -v
  
  tests:
    name: Test Suite
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps: 
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run:  |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests with coverage
        run: pytest tests/ -v -n auto --cov=app --cov-report=xml --cov-report=html --cov-fail-under=80
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unittests
          name:  codecov-${{ matrix.python-version }}
  
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    
    steps:
      - uses:  actions/checkout@v4
      - uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
```

**Key Security Improvements:**
- [ ] Minimal permissions (RBAC)
- [ ] Pinned action versions (e.g., `@v4` not `@latest`)
- [ ] Secret scanning in every PR
- [ ] Dependency vulnerability checks
- [ ] SAST (Static Application Security Testing)
- [ ] No secrets in workflows
- [ ] Fail on security issues
- [ ] Matrix testing for multiple Python versions

### 3.2 Dependabot Configuration

```yaml
# .github/dependabot.yml - OPTIMIZED

version: 2
updates:
  # Python dependencies
  - package-ecosystem:  "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers: 
      - "security-team"
    assignees:
      - "lead-engineer"
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix:  "chore(deps)"
      include: "scope"
    # Group minor updates
    groups:
      development-dependencies:
        dependency-type: "development"
        update-types: 
          - "minor"
          - "patch"
    # Security updates separate
    target-branch: "develop"
    ignore:
      # Ignore major version updates for now
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
  
  # GitHub Actions
  - package-ecosystem:  "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "github-actions"
```

### 3.3 CodeQL Configuration

```yaml
# .github/workflows/codeql.yml - ADVANCED SECURITY

name: "CodeQL Advanced Security"

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron:  '0 6 * * 1'  # Monday at 6 AM

permissions: 
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    
    strategy:
      fail-fast: false
      matrix:
        language:  ['python']
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages:  ${{ matrix.language }}
          queries: +security-and-quality
          config-file: ./. github/codeql/codeql-config.yml
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with: 
          category: "/language:${{matrix. language}}"
```

```yaml
# .github/codeql/codeql-config.yml

name: "Custom CodeQL Configuration"

queries:
  - uses: security-and-quality
  - uses: security-extended

query-filters:
  - exclude:
      id: py/unused-import

paths-ignore:
  - tests/
  - docs/
  - migrations/
```

### 3.4 GitHub Copilot Instructions

**Audit `.github/copilot-instructions.md`:**

```markdown
# GitHub Copilot Instructions - Project Standards

## Code Style & Quality

- Always use type hints (PEP 484)
- Follow PEP 8 and PEP 257 (docstrings)
- Maximum line length: 100 characters
- Use Google-style docstrings
- All functions must have docstrings
- Use `pathlib` instead of `os.path`
- Use f-strings for formatting (not `%` or `.format()`)
- Prefer list/dict comprehensions over loops when clear
- Use context managers (`with`) for resource handling

## Security Requirements

- NEVER hardcode secrets or credentials
- ALWAYS validate and sanitize user input
- Use parameterized SQL queries (SQLAlchemy ORM)
- Escape output in templates (Jinja2 auto-escapes)
- Implement CSRF protection on all forms
- Use bcrypt for password hashing (12 rounds minimum)
- Implement rate limiting on authentication endpoints
- Use HTTPS-only cookies with `httponly` and `samesite`

## Flask-Specific

- Use application factory pattern (`create_app()`)
- Use Blueprints for route organization
- Store secrets in environment variables
- Use Flask-WTF for forms with CSRF
- Use Flask-Login for authentication
- Use Flask-SQLAlchemy for database
- Implement proper error handlers (404, 500, etc.)
- Use `current_app` instead of global `app`

## Testing

- Write tests for all new features
- Minimum 80% code coverage
- Use pytest fixtures for setup
- Mock external dependencies
- Test both success and failure cases
- Include integration tests for workflows

## Git Commit Messages

- Format: `<type>(<scope>): <subject>`
- Types:  feat, fix, docs, style, refactor, test, chore
- Subject:  imperative mood, lowercase, no period
- Body: explain what and why, not how

Example:  `feat(auth): add two-factor authentication support`

## When Suggesting Code

1. Check for security vulnerabilities first
2. Ensure type safety (mypy compatible)
3. Follow existing patterns in the codebase
4. Include docstrings and comments
5. Consider error handling
6. Think about edge cases
```

---

## 🔧 Phase 4: Automated Remediation

### 4.1 Auto-Fix Script

```python
# scripts/auto_remediate.py

#!/usr/bin/env python3
"""
Automated Code Remediation Script
Applies safe fixes for common issues
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

class AutoRemediator:
    def __init__(self, project_root: Path):
        self.root = project_root
        self. fixes_applied:  List[str] = []
        self.manual_review:  List[str] = []
    
    def run_black(self) -> bool:
        """Auto-format code with Black"""
        print("🎨 Formatting code with Black...")
        try:
            subprocess. run(
                ["black", "app/", "tests/", "scripts/"],
                check=True,
                cwd=self.root
            )
            self.fixes_applied. append("✓ Code formatted with Black")
            return True
        except subprocess.CalledProcessError:
            self.manual_review.append("✗ Black formatting failed")
            return False
    
    def run_isort(self) -> bool:
        """Sort imports with isort"""
        print("📦 Sorting imports with isort...")
        try:
            subprocess. run(
                ["isort", "app/", "tests/", "scripts/"],
                check=True,
                cwd=self.root
            )
            self.fixes_applied.append("✓ Imports sorted with isort")
            return True
        except subprocess.CalledProcessError:
            self.manual_review.append("✗ isort failed")
            return False
    
    def run_ruff_fix(self) -> bool:
        """Auto-fix with Ruff"""
        print("🔧 Applying Ruff auto-fixes...")
        try:
            subprocess.run(
                ["ruff", "check", "app/", "--fix"],
                check=True,
                cwd=self.root
            )
            self.fixes_applied.append("✓ Ruff auto-fixes applied")
            return True
        except subprocess.CalledProcessError:
            self.manual_review. append("⚠ Some Ruff issues require manual fix")
            return False
    
    def upgrade_syntax(self) -> bool:
        """Upgrade Python syntax with pyupgrade"""
        print("⬆️  Upgrading syntax with pyupgrade...")
        py_files = list(self.root.rglob("*.py"))
        try:
            subprocess.run(
                ["pyupgrade", "--py311-plus"] + [str(f) for f in py_files],
                check=True,
                cwd=self. root
            )
            self.fixes_applied.append("✓ Syntax upgraded to Python 3.11+")
            return True
        except subprocess. CalledProcessError:
            self.manual_review.append("✗ pyupgrade failed")
            return False
    
    def remove_unused_imports(self) -> bool:
        """Remove unused imports with autoflake"""
        print("🧹 Removing unused imports...")
        try:
            subprocess. run(
                [
                    "autoflake",
                    "--in-place",
                    "--remove-all-unused-imports",
                    "--remove-unused-variables",
                    "--recursive",
                    "app/",
                    "tests/"
                ],
                check=True,
                cwd=self. root
            )
            self.fixes_applied.append("✓ Unused imports removed")
            return True
        except subprocess.CalledProcessError:
            self. manual_review.append("✗ autoflake failed")
            return False
    
    def fix_common_security_issues(self) -> None:
        """Fix common security issues in Flask config"""
        print("🔐 Checking Flask security configuration...")
        
        config_file = self.root / "config.py"
        if not config_file.exists():
            self.manual_review.append("⚠ config.py not found - create secure config")
            return
        
        content = config_file.read_text()
        
        issues = []
        if "SECRET_KEY = " in content and "dev-secret-key" in content. lower():
            issues.append("Hardcoded SECRET_KEY found")
        
        if "SESSION_COOKIE_SECURE" not in content:
            issues.append("Missing SESSION_COOKIE_SECURE")
        
        if "SESSION_COOKIE_HTTPONLY" not in content:
            issues.append("Missing SESSION_COOKIE_HTTPONLY")
        
        if issues:
            self.manual_review.append(
                f"⚠ Security issues in config. py: {', '.join(issues)}"
            )
        else:
            self.fixes_applied.append("✓ Flask security config looks good")
    
    def run_all(self) -> Tuple[int, int]:
        """Run all automated fixes"""
        print("\n" + "="*60)
        print("🤖 AUTOMATED REMEDIATION")
        print("="*60 + "\n")
        
        # Run formatters and fixers
        self.run_black()
        self.run_isort()
        self.upgrade_syntax()
        self.remove_unused_imports()
        self.run_ruff_fix()
        
        # Security checks
        self.fix_common_security_issues()
        
        # Summary
        print("\n" + "="*60)
        print("📊 REMEDIATION SUMMARY")
        print("="*60)
        
        if self.fixes_applied:
            print(f"\n✅ Fixes Applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"  {fix}")
        
        if self.manual_review:
            print(f"\n⚠️  Manual Review Required ({len(self.manual_review)}):")
            for issue in self.manual_review:
                print(f"  {issue}")
        
        return len(self.fixes_applied), len(self.manual_review)

def main():
    root = Path. cwd()
    remediator = AutoRemediator(root)
    fixes, reviews = remediator.run_all()
    
    sys.exit(0 if reviews == 0 else 1)

if __name__ == '__main__':
    main()
```

### 4.2 Security Patcher

```python
# scripts/security_patcher.py

#!/usr/bin/env python3
"""
Automated Security Patcher
Fixes common security vulnerabilities
"""

import re
from pathlib import Path
from typing import List, Dict

class SecurityPatcher:
    def __init__(self, project_root: Path):
        self.root = project_root
        self. patches_applied: List[Dict] = []
    
    def patch_sql_injection(self, file_path: Path) -> None:
        """Find and suggest fixes for potential SQL injection"""
        content = file_path.read_text()
        
        # Pattern:  f"SELECT ...  {variable}"
        pattern = r'f"SELECT.*?\{.*?\}"'
        matches = re.findall(pattern, content)
        
        if matches: 
            self.patches_applied.append({
                'file': str(file_path. relative_to(self.root)),
                'type': 'SQL Injection Risk',
                'count': len(matches),
                'suggestion': 'Use parameterized queries with SQLAlchemy'
            })
    
    def patch_hardcoded_secrets(self, file_path: Path) -> None:
        """Find hardcoded secrets"""
        content = file_path. read_text()
        
        patterns = [
            (r'SECRET_KEY\s*=\s*["\'](?! os\.environ).*?["\']', 'SECRET_KEY'),
            (r'PASSWORD\s*=\s*["\'].*?["\']', 'PASSWORD'),
            (r'API_KEY\s*=\s*["\'].*?["\']', 'API_KEY'),
            (r'aws_access_key.*?=.*?["\'].*?["\']', 'AWS_KEY'),
        ]
        
        for pattern, secret_type in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.patches_applied.append({
                    'file': str(file_path.relative_to(self.root)),
                    'type': f'Hardcoded {secret_type}',
                    'suggestion': f'Move {secret_type} to environment variable'
                })
    
    def patch_unsafe_deserialization(self, file_path: Path) -> None:
        """Find unsafe pickle usage"""
        content = file_path.read_text()
        
        if 'pickle. loads' in content:
            self.patches_applied.append({
                'file': str(file_path.relative_to(self. root)),
                'type': 'Unsafe Deserialization',
                'suggestion': 'Replace pickle with json or use safe alternatives'
            })
    
    def scan_all_files(self) -> None:
        """Scan all Python files for security issues"""
        print("🔍 Scanning for security vulnerabilities.. .\n")
        
        for py_file in self.root.rglob("*.py"):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            self.patch_sql_injection(py_file)
            self.patch_hardcoded_secrets(py_file)
            self.patch_unsafe_deserialization(py_file)
    
    def report(self) -> None:
        """Generate security report"""
        if not self.patches_applied:
            print("✅ No security issues found!\n")
            return
        
        print(f"⚠️  Found {len(self.patches_applied)} security issues:\n")
        
        for i, patch in enumerate(self.patches_applied, 1):
            print(f"{i}. {patch['type']}")
            print(f"   File: {patch['file']}")
            print(f"   Fix: {patch['suggestion']}\n")

def main():
    root = Path.cwd()
    patcher = SecurityPatcher(root)
    patcher.scan_all_files()
    patcher.report()

if __name__ == '__main__':
    main()
```

---

## ✅ Phase 5: Testing & Validation

### 5.1 Run Complete Audit

```bash
# scripts/run_full_audit.sh

#!/bin/bash
set -e

echo "🚀 COMPLETE PROJECT AUDIT"
echo "================================================"

# 1. Security Scanning
echo -e "\n📍 Phase 1: Security Audit"
echo "---------------------------------------"

echo "Checking for vulnerabilities in dependencies..."
pip-audit || echo "⚠️  Vulnerabilities found!"

echo "Scanning for secrets..."
gitleaks detect --source .  || echo "⚠️  Potential secrets found!"

echo "Running Bandit security scanner..."
bandit -r app/ -f screen

echo "Running Semgrep..."
semgrep --config=auto app/

# 2. Type Checking
echo -e "\n📍 Phase 2: Type Safety"
echo "---------------------------------------"
mypy app/ --strict || echo "⚠️  Type errors found!"

# 3. Linting
echo -e "\n📍 Phase 3: Code Quality"
echo "---------------------------------------"
ruff check app/ || echo "⚠️  Linting issues found!"

# 4. Formatting
echo -e "\n📍 Phase 4: Code Formatting"
echo "---------------------------------------"
black --check app/ || echo "⚠️  Formatting issues found!"
isort --check-only app/ || echo "⚠️  Import sorting issues found!"

# 5. Complexity
echo -e "\n📍 Phase 5: Complexity Analysis"
echo "---------------------------------------"
radon cc app/ -a -nb
radon mi app/ -nb

# 6. Documentation
echo -e "\n📍 Phase 6: Documentation Coverage"
echo "---------------------------------------"
interrogate app/ -v

# 7. Tests
echo -e "\n📍 Phase 7: Test Suite"
echo "---------------------------------------"
pytest tests/ -v --cov=app --cov-report=term --cov-fail-under=80

# 8. Structure Validation
echo -e "\n📍 Phase 8: Project Structure"
echo "---------------------------------------"
python scripts/validate_structure.py

echo -e "\n✅ AUDIT COMPLETE"
echo "================================================"
```

### 5.2 Pre-Production Checklist

```markdown
# Pre-Production Security Checklist

## Security
- [ ] All dependencies scanned (pip-audit, safety)
- [ ] No secrets in code or git history
- [ ] HTTPS enforced (Flask-Talisman)
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] SQL injection prevented (ORM only)
- [ ] XSS prevented (auto-escaping)
- [ ] Rate limiting implemented
- [ ] Session security configured
- [ ] Password hashing with bcrypt (12+ rounds)
- [ ] Input validation on all endpoints
- [ ] File upload security implemented
- [ ] Error messages don't leak info
- [ ] Logging doesn't expose sensitive data

## Code Quality
- [ ] mypy --strict passes (100%)
- [ ] ruff check passes (0 errors)
- [ ] black formatting applied
- [ ] isort import sorting applied
- [ ] Cyclomatic complexity < 10
- [ ] Test coverage ≥ 80%
- [ ] All functions documented
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No TODO comments (convert to issues)

## Configuration
- [ ] DEBUG = False in production
- [ ] SECRET_KEY from environment
- [ ] Database credentials from environment
- [ ] ALLOWED_HOSTS configured
- [ ] CORS properly configured
- [ ] Logging configured
- [ ] Error monitoring (Sentry, etc.)
- [ ] Performance monitoring

## Infrastructure
- [ ] Database backups automated
- [ ] SSL certificates valid
- [ ] Firewall rules configured
- [ ] DDoS protection enabled
- [ ] CDN configured for static files
- [ ] Load balancing configured

## Compliance
- [ ] GDPR compliance (if applicable)
- [ ] Data encryption at rest
- [ ] Data encryption in transit
- [ ] Privacy policy updated
- [ ] Terms of service updated
- [ ] Cookie consent implemented
```

---

## 📦 Required Dependencies

```text
# requirements-audit.txt

# Security Scanning
pip-audit==2.6.1
safety==2.3.5
bandit[toml]==1.7.5
semgrep==1.45.0
gitleaks==8.18.0

# Type Checking
mypy==1.7.1
types-Flask==1.1.6
types-requests==2.31.0

# Linting & Formatting
ruff==0.1.8
black==23.12.1
isort==5.13.2
autoflake==2.2.1
pyupgrade==3.15.0

# Complexity Analysis
radon==6.0.1
vulture==2.10
xenon==0.9.1

# Documentation
interrogate==1.5.0
pydoc-markdown==4.8.2

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-xdist==3.5.0
pytest-mock==3.12.0

# Flask Security
Flask-Talisman==1.1.0
Flask-Limiter==3.5.0
Flask-SeaSurf==1.1.1

# Production Server
gunicorn[gthread]==21.2.0
```

---

## 🎯 Success Criteria

Your audit is complete when: 

✅ **Security**:  
- 0 vulnerabilities in `pip-audit`
- 0 secrets detected by `gitleaks`
- 0 critical issues in `bandit`
- A+ rating on securityheaders.com

✅ **Code Quality**: 
- `mypy --strict` passes 100%
- `ruff check` shows 0 errors
- Code coverage ≥ 80%
- Cyclomatic complexity < 10
- Documentation coverage ≥ 95%

✅ **AI Configuration**:
- All GitHub Actions use pinned versions
- Dependabot configured and running
- CodeQL enabled
- Copilot instructions comprehensive

✅ **Performance**:
- Page load < 2 seconds
- API response < 200ms (p95)
- Database queries optimized

---

## 💼 Deliverables

After completing the audit, provide:

1. **Security Report** - Vulnerabilities found and fixed
2. **Code Quality Report** - Metrics before/after
3. **Remediation Log** - All changes made
4. **Risk Assessment** - Remaining risks and mitigation plan
5. **Recommendations** - Future improvements

---

**You are the last line of defense before production.  Leave no stone unturned.  🛡️**