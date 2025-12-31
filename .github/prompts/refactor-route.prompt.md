---
mode: "agent"
description: "Refactor an existing route following best practices and workflow rules"
---

# Refactor Route

**Task:** Refactor an existing Flask route to improve code quality, maintainability, and follow project conventions.

---

## Input Required

### Route to Refactor
- **Endpoint:** ${input:endpoint:/example-route}
- **Current file:** ${input:file:backend/src/routes/example. py}

### Refactoring Goals
${input:goals:What needs improvement?  (e.g., "Extract business logic to service", "Add proper error handling", "Improve type hints")}

### Context
${input:context: Paste current code or describe current behavior}

---

## MANDATORY:  Pre-Refactoring Process

### 1. Read Workflow Rules
- ✅ Read `.github/workflow-rules.md` completely
- ✅ Read `.github/incidents-history.md` for this route
- ✅ Check if this route has failed before

### 2. Kill All Servers

**BEFORE making ANY changes:**

```powershell
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 3. Document Current Behavior
- Analyze current route
- Document inputs, outputs, side effects
- Identify all callers/dependencies
- List tests that cover this route

---

## Refactoring Requirements

### 1. Code Quality

**Route Handler (Thin):**
- Keep handler minimal (input parsing, output formatting)
- Extract business logic to service layer
- Extract data access to repository (if applicable)
- Use dependency injection when appropriate

**Example transformation:**

**Before (❌ Bad):**
```python
@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    
    if not validate_email(user.email):
        return jsonify({"error": "Invalid email"}), 400
    
    db.session.commit()
    return jsonify(user.to_dict()), 200
```

**After (✅ Good):**
```python
@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id:  int):
    """
    Update user by ID.
    
    Args:
        user_id: User ID to update
        
    Returns: 
        Updated user object (200) or error (400, 404)
    """
    data = request.json
    
    try:
        user = user_service.update_user(user_id, data)
        return jsonify(user.to_dict()), 200
    except UserNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
```

**Service layer (`backend/src/services/user_service.py`):**
```python
def update_user(user_id: int, data: dict) -> User:
    """
    Update user with provided data.
    
    Args:
        user_id: User ID
        data: Update data dictionary
        
    Returns:
        Updated User object
        
    Raises:
        UserNotFoundError: If user doesn't exist
        ValidationError: If data invalid
    """
    user = User.query.get(user_id)
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    
    # Validate
    if "email" in data and not validate_email(data["email"]):
        raise ValidationError("Invalid email format")
    
    # Update
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    
    db.session.commit()
    logger.info("User %s updated successfully", user_id)
    return user
```

### 2. Type Hints (Mandatory)

- ✅ Add to all function parameters
- ✅ Add to return types
- ✅ Use precise types (`int`, `str`, `dict[str, Any]`, etc.)
- ✅ Import from `typing` module when needed

### 3. Error Handling

**Comprehensive error handling:**
- ✅ Catch specific exceptions (not bare `except:`)
- ✅ Return appropriate HTTP status codes
- ✅ Consistent error response format
- ✅ Log errors with context
- ✅ Don't leak internal details in production

**Error response format:**
```python
{
    "error": "Short error type",
    "message": "Detailed error message",
    "status":  400
}
```

### 4. Logging

- ✅ Use `logging` module (not `print`)
- ✅ Log important events (INFO)
- ✅ Log errors with context (ERROR)
- ✅ Include relevant IDs/data (but not secrets!)
- ✅ Use appropriate log levels

### 5. Input Validation

- ✅ Validate ALL inputs (never trust client)
- ✅ Sanitize data (strip whitespace, normalize, etc.)
- ✅ Use schema validation (Pydantic, Marshmallow) if complex
- ✅ Return clear validation errors (400)

### 6. Security

- ✅ Use parameterized queries (no SQL injection)
- ✅ Validate permissions/authorization
- ✅ Don't log sensitive data
- ✅ Escape output (prevent XSS)
- ✅ Rate limiting (if applicable)

---

## Testing Requirements

### 1. Update Existing Tests

- Review all tests for this route
- Update assertions to match new behavior
- Ensure all edge cases still covered

### 2. Add New Tests (if needed)

**Test cases to cover:**
- ✅ Happy path (successful request)
- ✅ Invalid input (400)
- ✅ Not found (404)
- ✅ Authorization failure (403, if applicable)
- ✅ Server error (500, if applicable)

### 3. Test Service Layer (if extracted)

```python
def test_update_user_service_success():
    """Test user service update with valid data."""
    user = user_service.update_user(1, {"name": "New Name"})
    assert user.name == "New Name"

def test_update_user_service_not_found():
    """Test user service raises error for non-existent user."""
    with pytest.raises(UserNotFoundError):
        user_service.update_user(99999, {"name": "Test"})

def test_update_user_service_validation_error():
    """Test user service raises error for invalid email."""
    with pytest.raises(ValidationError):
        user_service.update_user(1, {"email": "not-an-email"})
```

---

## Workflow Compliance

### 1. Follow Workflow Rules

**Before refactoring:**
- [ ] All servers killed
- [ ] `.github/workflow-rules.md` read
- [ ] `.github/incidents-history.md` checked

**During refactoring:**
- [ ] Follow Flask conventions
- [ ] Add/update type hints
- [ ] Add/update docstrings
- [ ] Extract business logic to service
- [ ] Add/update tests
- [ ] Update translations (if UI text changed)

**After refactoring:**
- [ ] Kill servers again
- [ ] Run linters (Ruff, Mypy)
- [ ] Run tests (pytest)
- [ ] Test in dev mode
- [ ] Test in prod mode
- [ ] Update CHANGELOG.md

### 2. Testing Workflow

```powershell
# 1. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Run linters
. \.venv\Scripts\ruff. exe check .
.\.venv\Scripts\ruff.exe format --check . 
.\.venv\Scripts\mypy. exe backend/src

# 3. Run tests
.\.venv\Scripts\pytest.exe -v

# 4. Test in dev mode
.\.venv\Scripts\python.exe backend\src\app.py
# → Test route in browser/Postman

# 5. Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 6. Test in prod mode
.\.venv\Scripts\python.exe run_prod. py
# → Test route again
```

---

## Documentation Updates

### 1. CHANGELOG.md

**Format:**
```markdown
## [Unreleased]

### Changed
- Refactored `/example-route` endpoint (#issue)
  - Extracted business logic to service layer
  - Improved error handling
  - Added comprehensive type hints
```

### 2. Docstrings

**Update route docstring:**
```python
@bp.route("/example", methods=["POST"])
def example_route():
    """
    Short description of what route does. 
    
    Request Body:
        {
            "field1": "string",
            "field2": 123
        }
    
    Returns: 
        200: Success - { "result": "..." }
        400: Validation error - { "error": ".. .", "message": "..." }
        404: Not found - { "error": ".. .", "message": "..." }
    """
```

### 3. Analysis Report (if significant)

**Location:** `Analysis_reports/YYYY-MM-DD_HH-mm_refactor-route-name.md`

**Content:**
- Current state analysis
- Issues identified
- Refactoring decisions
- Trade-offs
- Performance impact (if any)
- Migration notes (if breaking change)

---

## Files to Create/Modify

```
backend/src/routes/<blueprint>. py         ← Refactor route handler
backend/src/services/<service>. py         ← Extract business logic
backend/src/models. py                     ← Update models (if needed)
tests/test_<feature>.py                   ← Update/add tests
tests/test_services.py                    ← Test service layer (if created)
CHANGELOG.md                              ← Document changes
Analysis_reports/<timestamp>_refactor.md  ← Analysis report (if significant)
```

---

## Breaking Changes

**If refactoring changes public API:**

### 1. Document in CHANGELOG

```markdown
### Changed
- **BREAKING:** `/api/users` endpoint now requires authentication
  Migration:  Add `Authorization` header to all requests
```

### 2. Version Bump

- Breaking change → MAJOR version bump
- See `.github/copilot-instructions.md` section 6 (Versioning)

### 3. Migration Guide

- Include clear migration instructions
- Provide code examples (before/after)
- Update API documentation

---

## Validation Checklist

Before completing: 

- [ ] Route handler is thin (business logic extracted)
- [ ] Type hints on all parameters and return
- [ ] Docstring complete and accurate
- [ ] Error handling comprehensive
- [ ] Logging added (appropriate levels)
- [ ] Input validation robust
- [ ] Security best practices followed
- [ ] Service layer created (if complex logic)
- [ ] Tests updated/added
- [ ] All tests pass
- [ ] Linters pass (Ruff, Mypy)
- [ ] Tested in dev mode
- [ ] Tested in prod mode
- [ ] CHANGELOG. md updated
- [ ] Analysis report created (if significant)
- [ ] No console errors
- [ ] No log warnings/errors

---

## Don'ts

- ❌ Refactor without killing servers first
- ❌ Change behavior without updating tests
- ❌ Skip testing in both dev and prod modes
- ❌ Commit without running linters
- ❌ Leave commented-out code
- ❌ Remove error handling
- ❌ Make breaking changes without documentation

---

## References

- `.github/workflow-rules.md` — Mandatory workflow
- `.github/python.instructions.md` — Python/Flask rules
- `.github/copilot-instructions.md` — General rules
- `.github/incidents-history.md` — Past issues to avoid

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.