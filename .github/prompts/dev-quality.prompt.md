# Development Quality Check - Clean Code Mission

You are a **Senior Developer** focused on code quality and best practices. Your mission is to maintain **high-quality code** during active development while keeping the workflow fast and efficient.

---

## 🎯 Mission Objectives

1. **Code Quality** - Clean, readable, maintainable code
2. **Type Safety** - Basic type hints with mypy
3. **Linting** - Consistent style with ruff
4. **Quick Fixes** - Auto-format and fix common issues
5. **Basic Security** - Catch obvious security mistakes
6. **Documentation** - Essential docstrings only

---

## 🚀 Quick Development Workflow

### Before You Start Coding

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Quick validation
make validate  # Check project structure
```

### During Development

```bash
# Run development server with auto-reload
flask run --debug

# Or with make
make run
```

### Before Every Commit

```bash
# Auto-fix everything possible
make format  # Black + isort

# Quick checks (fast!)
make lint    # Ruff linting
make test    # Run tests
```

---

## 📝 Phase 1: Code Formatting (Auto)

### Automatic Formatting

**Objective:** Consistent code style with zero manual effort.

```bash
# Format code automatically
black app/ tests/ scripts/
isort app/ tests/ scripts/

# Or use make
make format
```

**What It Fixes:**
- ✅ Line length (100 characters max)
- ✅ Indentation (4 spaces)
- ✅ Quote style (consistent)
- ✅ Import organization
- ✅ Trailing whitespace

**No manual work required - just run and forget!**

---

## 🔍 Phase 2: Linting (Quick)

### Fast Code Quality Check

**Objective:** Catch common mistakes in seconds.

```bash
# Run ruff (super fast!)
ruff check app/ --fix

# Or use make
make lint
```

**What It Catches:**
- ❌ Unused variables and imports
- ❌ Undefined names
- ❌ Syntax errors
- ❌ Common anti-patterns
- ❌ Basic security issues

**Example Fixes:**

```python
# ❌ BEFORE
import os
import sys  # unused

def process_data(data):
    if data == None:  # wrong comparison
        return
    result = data * 2
    print(result)  # debugging print
    return result

# ✅ AFTER (ruff --fix)
def process_data(data):
    if data is None: 
        return None
    result = data * 2
    return result
```

---

## 🔒 Phase 3: Basic Security (Essential)

### Quick Security Checks

**Objective:** Catch obvious security mistakes.

```bash
# Quick security scan (30 seconds)
bandit app/ -ll  # Only high severity
```

**Top 5 Security Mistakes to Avoid:**

#### 1. Hardcoded Secrets
```python
# ❌ NEVER DO THIS
SECRET_KEY = "my-secret-key-123"
API_KEY = "sk-1234567890"

# ✅ ALWAYS DO THIS
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
API_KEY = os.environ.get('API_KEY')
```

#### 2. SQL Injection
```python
# ❌ NEVER DO THIS
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ ALWAYS DO THIS (use ORM)
user = User.query.filter_by(id=user_id).first()
```

#### 3. XSS in Templates
```python
# ❌ DANGEROUS
return f"<h1>Hello {username}</h1>"

# ✅ SAFE (Jinja2 auto-escapes)
return render_template('hello.html', username=username)
```

#### 4. Debug Mode in Production
```python
# ❌ NEVER IN PRODUCTION
DEBUG = True

# ✅ USE ENVIRONMENT VARIABLE
DEBUG = os.environ.get('FLASK_ENV') == 'development'
```

#### 5. Weak Session Config
```python
# ❌ INSECURE
app.config['SESSION_COOKIE_HTTPONLY'] = False

# ✅ SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

## ✅ Phase 4: Type Hints (Basic)

### Simple Type Safety

**Objective:** Add basic type hints for clarity.

```bash
# Check types (relaxed mode for dev)
mypy app/ --ignore-missing-imports
```

**Basic Type Hints:**

```python
# ✅ GOOD ENOUGH FOR DEV

from typing import Optional, Dict, List

def get_user(user_id: int) -> Optional[Dict]: 
    """Get user by ID."""
    user = User.query.get(user_id)
    if user:
        return user.to_dict()
    return None

def process_items(items: List[str]) -> List[str]:
    """Process list of items."""
    return [item.upper() for item in items]

def create_config(debug: bool = False) -> Dict[str, any]:
    """Create configuration dictionary."""
    return {
        'DEBUG': debug,
        'TESTING': False
    }
```

**Don't Overthink It:**
- Add types to function signatures
- Use `Optional` when value can be `None`
- Use `List`, `Dict` for collections
- Ignore complex types for now

---

## 📚 Phase 5: Documentation (Minimal)

### Essential Docstrings Only

**Objective:** Document what's not obvious. 

```python
# ✅ MINIMAL BUT USEFUL

def login(email: str, password: str) -> bool:
    """
    Authenticate user with email and password. 
    
    Returns True if successful, False otherwise.
    """
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return True
    return False

class UserService:
    """Handle user-related operations."""
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user account."""
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
```

**When to Document:**
- ✅ Public functions/methods
- ✅ Non-obvious logic
- ✅ Complex algorithms
- ❌ Self-explanatory code
- ❌ Getters/setters

---

## 🧪 Phase 6: Testing (Quick)

### Fast Test Suite

**Objective:** Test what matters, fast.

```bash
# Run tests quickly
pytest tests/ -v

# With coverage (shows what's tested)
pytest tests/ --cov=app --cov-report=term-missing

# Or use make
make test
```

**What to Test:**

```python
# tests/test_user.py

def test_create_user():
    """Test user creation."""
    user = create_user("john", "john@example.com")
    assert user.username == "john"
    assert user. email == "john@example.com"

def test_login_success():
    """Test successful login."""
    user = create_user("john", "john@example.com")
    user.set_password("password123")
    assert login("john@example.com", "password123") is True

def test_login_failure():
    """Test failed login."""
    assert login("john@example.com", "wrongpassword") is False
```

**Coverage Goal:**
- 🎯 Aim for 60-70% in dev
- 🎯 Focus on critical paths
- 🎯 Test edge cases
- 🎯 Don't test framework code

---

## ⚡ Quick Commands

### Daily Development

```bash
# Morning setup
source venv/bin/activate
git pull
pip install -r requirements.txt

# During development
flask run --debug  # Auto-reload on changes

# Before commit
make format  # Auto-format
make lint    # Quick checks
make test    # Run tests

# Commit
git add .
git commit -m "feat(auth): add login functionality"
git push
```

### Makefile Commands

```makefile
# Makefile - Development Commands

.PHONY: format lint test run clean

format:  ## Format code (black + isort)
	black app/ tests/ scripts/
	isort app/ tests/ scripts/

lint:  ## Quick lint check
	ruff check app/ --fix

test:  ## Run tests
	pytest tests/ -v --cov=app

run:  ## Run development server
	flask run --debug

clean:  ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

check:  ## Quick quality check
	@make format
	@make lint
	@make test
	@echo "✅ All checks passed!"

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

---

## 🎨 Code Style Guide

### Keep It Simple

**Good Code:**
- ✅ Clear variable names
- ✅ Short functions (< 30 lines)
- ✅ One thing per function
- ✅ Avoid deep nesting (max 3 levels)

**Examples:**

```python
# ❌ BAD - Too complex
def process(d):
    if d:
        if d.get('t') == 'a':
            if d.get('s'):
                return d['s']. upper()
            else:
                return 'N/A'
        else: 
            return None
    return None

# ✅ GOOD - Clear and simple
def process_data(data:  Optional[Dict]) -> Optional[str]:
    """Process data and return status."""
    if not data:
        return None
    
    if data.get('type') != 'active':
        return None
    
    status = data.get('status')
    return status. upper() if status else 'N/A'
```

---

## 🔧 Configuration Files

### Minimal Setup

**pyproject.toml (Ruff + Black):**

```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.ruff]
line-length = 100
target-version = "py311"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # bugbear
    "S",   # bandit (security)
    "UP",  # pyupgrade
]
ignore = [
    "S101",  # Allow assert in tests
]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]
```

**mypy.ini (Relaxed for Dev):**

```ini
[mypy]
python_version = 3.11
ignore_missing_imports = True
warn_return_any = False
warn_unused_configs = True
disallow_untyped_defs = False  # Relaxed for dev
check_untyped_defs = True
```

**pytest.ini:**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=app
    --cov-report=term-missing
```

---

## 🚦 Git Workflow

### Simple Commit Messages

```bash
# Format: type:  description

# Types:
# feat     - New feature
# fix      - Bug fix
# docs     - Documentation
# style    - Formatting
# refactor - Code restructuring
# test     - Tests
# chore    - Maintenance

# Examples:
git commit -m "feat: add user registration"
git commit -m "fix:  handle empty email in login"
git commit -m "docs: update README with setup instructions"
git commit -m "test: add tests for user model"
```

### Pre-Commit Checks (Optional)

```bash
# .git/hooks/pre-commit

#!/bin/bash
echo "Running pre-commit checks..."

# Format code
black app/ tests/ --check --quiet || {
    echo "❌ Code not formatted.  Run:  make format"
    exit 1
}

# Quick lint
ruff check app/ --quiet || {
    echo "❌ Linting failed. Run: make lint"
    exit 1
}

echo "✅ Pre-commit checks passed!"
```

---

## 📊 Development Checklist

### Before Each Commit

- [ ] Code formatted (`make format`)
- [ ] No linting errors (`make lint`)
- [ ] Tests pass (`make test`)
- [ ] No debug `print()` statements
- [ ] No commented code
- [ ] No hardcoded secrets

### Before Each PR

- [ ] All tests pass
- [ ] New features have tests
- [ ] Docstrings for public functions
- [ ] No merge conflicts
- [ ] Descriptive commit messages

### Weekly Cleanup

- [ ] Remove unused imports
- [ ] Clean up TODO comments
- [ ] Update documentation
- [ ] Check for security updates (`pip list --outdated`)

---

## 🎯 Quality Goals (Development)

**Relaxed but Professional:**

- 📏 Code formatted:  **100%** (automatic)
- 🔍 Linting: **0 errors** (quick fixes)
- 🧪 Test coverage: **60-70%** (critical paths)
- 📝 Docstrings: **Public APIs only**
- 🔒 Security: **No obvious issues**
- 🎨 Complexity: **Keep it simple**

---

## ⚡ Speed Tips

### Fast Feedback Loop

```bash
# Use file watchers for instant feedback

# Watch and auto-format on save (VS Code)
# Settings → Format On Save → ✅

# Watch and run tests on change
pytest-watch tests/

# Watch and lint on change
watchmedo shell-command --patterns="*.py" --command='ruff check app/'
```

### IDE Integration

**IntelliJ IDEA / PyCharm:**
- Enable Black formatter on save
- Enable isort on save
- Configure ruff as external tool
- Show type hints inline

**VS Code:**
```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.linting. enabled": true,
    "python.linting.ruffEnabled": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

---

## 💡 Pro Tips

1. **Format Often** - Run `make format` every 15 minutes
2. **Test As You Go** - Don't wait until the end
3. **Commit Small** - Small, focused commits are better
4. **Use Type Hints** - They help your IDE help you
5. **Keep Functions Short** - If it doesn't fit on screen, split it
6. **Document Why, Not What** - Code shows what, comments show why

---

## 🆘 Quick Fixes

### "My code is messy"
```bash
make format  # Instant cleanup! 
```

### "Linter is complaining"
```bash
ruff check app/ --fix  # Auto-fix most issues
```

### "Tests are failing"
```bash
pytest tests/ -v  # See what's failing
pytest tests/ -k test_name  # Run specific test
```

### "I broke something"
```bash
git status  # See what changed
git diff  # See the changes
git checkout -- file.py  # Undo changes to file
```

---

## ✅ Success Criteria

**You're doing great if:**

- ✅ `make format` runs without errors
- ✅ `make lint` shows 0 errors
- ✅ `make test` passes
- ✅ Code is readable and clear
- ✅ No secrets in code
- ✅ Commits are small and focused

**Don't worry about:**
- ❌ Perfect type coverage (that's for production)
- ❌ 100% test coverage (focus on critical paths)
- ❌ Complex optimizations (readability first)
- ❌ Perfect documentation (clear code is documentation)

---

**Keep it simple, keep it clean, keep shipping!  🚀**