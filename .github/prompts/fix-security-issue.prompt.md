---
mode: "agent"
description: "Analyze and fix security vulnerabilities with proper testing and documentation"
---

# Fix Security Issue

**Task:** Identify, analyze, and fix a security vulnerability following security best practices.

---

## Input Required

### Vulnerability Description
${input: vulnerability: Describe the security issue (e.g., "SQL injection in search endpoint", "XSS in user profile")}

### Severity
${input:severity:Critical|High|Medium|Low}

### Affected Components
${input:components:List affected files, routes, or modules}

### CVE (if applicable)
${input:cve:CVE-YYYY-XXXXX (if assigned)}

### Discovery Method
${input:discovery:How was this discovered? (security scan, audit, bug report, etc.)}

---

## CRITICAL:  Security Issue Workflow

### 1. Immediate Actions

**DO NOT commit fix to public repository until:**
- [ ] Severity assessed
- [ ] Impact analyzed
- [ ] Fix developed and tested
- [ ] Security advisory prepared (if needed)

**For Critical/High severity:**
- Create private branch
- Limit access to security team
- Prepare coordinated disclosure

### 2. Analysis Phase

**Create confidential analysis report:**
- Location: `Analysis_reports/YYYY-MM-DD_HH-mm_security-<issue>-CONFIDENTIAL.md`
- Mark as:  **CONFIDENTIAL - DO NOT COMMIT TO PUBLIC REPO**

**Report content:**
- Vulnerability description
- Affected versions
- Attack vector (how to exploit)
- Impact assessment (data loss, privilege escalation, etc.)
- Affected users/systems
- Immediate mitigations (if any)
- Proposed fix
- Testing strategy

---

## Common Vulnerability Types & Fixes

### 1. SQL Injection

**Vulnerable code:**
```python
# ❌ NEVER DO THIS
@bp.route("/search")
def search():
    query = request.args.get("q")
    results = db.engine.execute(f"SELECT * FROM users WHERE name LIKE '%{query}%'")
    return jsonify([dict(r) for r in results])
```

**Fixed code:**
```python
# ✅ ALWAYS USE PARAMETERIZED QUERIES
from sqlalchemy import text

@bp.route("/search")
def search():
    query = request.args.get("q", "")
    
    # Input validation
    if len(query) > 100:
        return jsonify({"error": "Query too long"}), 400
    
    # Parameterized query
    sql = text("SELECT * FROM users WHERE name LIKE : query")
    results = db.session.execute(sql, {"query":  f"%{query}%"})
    
    return jsonify([dict(r) for r in results])

# ✅ BETTER: Use ORM
@bp.route("/search")
def search():
    query = request. args.get("q", "").strip()
    
    if len(query) > 100:
        return jsonify({"error":  "Query too long"}), 400
    
    users = User.query.filter(User.name.like(f"%{query}%")).all()
    return jsonify([u.to_dict() for u in users])
```

---

### 2. Cross-Site Scripting (XSS)

**Vulnerable code:**
```python
# ❌ BAD:  Directly embedding user input
@bp.route("/profile/<username>")
def profile(username):
    user = User.query. filter_by(username=username).first_or_404()
    # Template directly outputs user.bio (could contain <script>)
    return render_template("profile.html", user=user)
```

**Template (vulnerable):**
```html
<!-- ❌ BAD: No escaping -->
<div class="bio">{{ user.bio | safe }}</div>
```

**Fixed code:**
```python
# ✅ GOOD: Sanitize HTML input
import bleach

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'a']
ALLOWED_ATTRS = {'a': ['href', 'title']}

@bp.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Sanitize bio HTML
    user.bio_safe = bleach.clean(
        user.bio or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )
    
    return render_template("profile. html", user=user)
```

**Template (fixed):**
```html
<!-- ✅ GOOD:  Auto-escaped (default in Jinja2) -->
<div class="bio">{{ user. bio_safe }}</div>

<!-- Or without HTML:  -->
<div class="bio">{{ user.bio }}</div>  <!-- Auto-escaped -->
```

---

### 3. Insecure Direct Object Reference (IDOR)

**Vulnerable code:**
```python
# ❌ BAD: No authorization check
@bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
```

**Fixed code:**
```python
# ✅ GOOD: Check authorization
from flask_login import current_user, login_required

@bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id:  int):
    user = User.query.get_or_404(user_id)
    
    # Authorization check
    if user.id != current_user.id and not current_user.is_admin:
        logger.warning(
            "Unauthorized delete attempt:  user %s tried to delete user %s",
            current_user.id, user_id
        )
        return jsonify({"error": "Forbidden"}), 403
    
    db.session.delete(user)
    db.session.commit()
    
    logger.info("User %s deleted by %s", user_id, current_user.id)
    return "", 204
```

---

### 4. Sensitive Data Exposure

**Vulnerable code:**
```python
# ❌ BAD:  Logging sensitive data
logger.info("User login:  email=%s, password=%s", email, password)

# ❌ BAD: Returning sensitive data in API
@bp.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())  # Includes password_hash! 
```

**Fixed code:**
```python
# ✅ GOOD: Never log passwords
logger.info("User login attempt: email=%s", email)

# ✅ GOOD: Filter sensitive fields
@bp.route("/users/<int:user_id>")
def get_user(user_id:  int):
    user = User.query.get_or_404(user_id)
    
    # Public-safe serialization
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat()
        # NO password_hash, NO session_token, etc.
    })
```

---

### 5. Missing Authentication/Authorization

**Vulnerable code:**
```python
# ❌ BAD: No authentication required
@bp.route("/admin/users")
def admin_users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)
```

**Fixed code:**
```python
# ✅ GOOD:  Require authentication + authorization
from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            logger.warning(
                "Unauthorized admin access attempt by user %s",
                current_user.id
            )
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query. all()
    return render_template("admin/users.html", users=users)
```

---

## Testing Security Fixes

### 1. Unit Tests

**Test that vulnerability is fixed:**

```python
def test_search_sql_injection_prevented(client):
    """Test that SQL injection is prevented in search."""
    # Attempt SQL injection
    malicious_query = "admin' OR '1'='1"
    response = client.get(f"/search?q={malicious_query}")
    
    # Should NOT return all users
    assert response.status_code == 200
    data = response.get_json()
    # Verify safe behavior (empty results or escaped query)
    assert len(data) == 0 or all("admin" not in u["name"]. lower() for u in data)

def test_xss_sanitized(client, sample_user):
    """Test that XSS payloads are sanitized."""
    # Update bio with XSS payload
    sample_user.bio = '<script>alert("XSS")</script><p>Safe text</p>'
    db.session.commit()
    
    response = client.get(f"/profile/{sample_user.username}")
    
    # <script> should be stripped
    assert b'<script>' not in response. data
    assert b'alert' not in response.data
    # Safe HTML should remain
    assert b'<p>Safe text</p>' in response.data

def test_idor_prevented(client, sample_user, other_user):
    """Test that users can't delete other users."""
    # Login as sample_user
    login(client, sample_user)
    
    # Try to delete other_user
    response = client.post(f"/users/{other_user.id}/delete")
    
    assert response.status_code == 403  # Forbidden
    
    # Verify other_user still exists
    assert User.query.get(other_user.id) is not None
```

### 2. Security Scan

**Run automated security tools:**

```powershell
# pip-audit (check dependencies)
.\.venv\Scripts\pip-audit.exe

# Bandit (Python security linter)
.\.venv\Scripts\bandit. exe -r backend/src

# Safety (check known vulnerabilities)
.\.venv\Scripts\safety.exe check
```

### 3. Manual Security Testing

**Checklist:**
- [ ] Attempt exploit before fix (confirm vulnerability)
- [ ] Apply fix
- [ ] Attempt exploit after fix (confirm patched)
- [ ] Test edge cases
- [ ] Test with different user roles
- [ ] Test with malicious input
- [ ] Verify logs don't leak sensitive data

---

## Documentation

### 1. CHANGELOG.md

**Format (use Security section):**

```markdown
## [Unreleased]

### Security
- **[CRITICAL]** Fix SQL injection vulnerability in search endpoint (CVE-2025-XXXXX)
  - Affects: v0.1.0 to v0.3.2
  - Impact:  Potential unauthorized data access
  - Fix: Migrated to parameterized queries and ORM
  - Credit: Security researcher @username
```

### 2. Security Advisory (if public disclosure)

**Create:** `SECURITY. md` or GitHub Security Advisory

**Content:**
- Vulnerability description
- Affected versions
- Severity (CVSS score if available)
- Exploitation difficulty
- Recommended action (upgrade to version X.Y.Z)
- Workarounds (if any)
- Timeline (discovery → fix → disclosure)
- Credits

### 3. Incident Report

**Location:** `.github/incidents-history.md`

**Add entry:**
```markdown
## [YYYY-MM-DD] Security — <Vulnerability Type>

**Severity:** Critical  
**Component:** Backend / Routes  
**Discovered by:** <Name or method>  
**CVE:** CVE-2025-XXXXX (if assigned)

### Symptoms
- SQL injection possible in search endpoint via query parameter

### Root Cause
- Direct string interpolation in SQL query
- No input validation or parameterization

### Solution Applied
- Migrated to SQLAlchemy ORM
- Added input validation (length limits)
- Implemented parameterized queries as fallback
- Files modified: `backend/src/routes/search.py`
- Commit: abc123def

### Prevention Future
- ✅ Added Bandit to CI/CD pipeline
- ✅ Mandatory code review for database queries
- ✅ Security training for developers
- ✅ Regular security audits

### References
- CVE-2025-XXXXX
- Security advisory:  GHSA-XXXX-XXXX-XXXX
- Analysis report: `Analysis_reports/2025-12-30_security-sql-injection.md`
```

---

## Version Bump & Release

### 1. Security Fix Version

**Determine version bump:**
- **Critical/High severity** → PATCH bump (x.y.Z)
- **If backporting to old versions** → Patch each affected version

**Example:**
- Current: v1.2.3
- Security fix → v1.2.4
- Backport to v1.1.x → v1.1.8

### 2. Release Process

```powershell
# 1. Update version in all files
# pyproject.toml, package.json, file headers

# 2. Update CHANGELOG.md
# Move from [Unreleased] to [X.Y.Z] - YYYY-MM-DD

# 3. Commit
git add .
git commit -m "fix(security): patch SQL injection (CVE-2025-XXXXX)"

# 4. Tag
git tag -a vX.Y.Z -m "Security release:  Fix CVE-2025-XXXXX"

# 5. Push
git push origin main --tags

# 6. Publish security advisory (if applicable)
```

---

## Files Created/Modified

```
backend/src/routes/<affected>. py              ← Fix vulnerability
backend/src/services/<affected>.py            ← Fix business logic (if needed)
tests/test_security_<issue>.py                ← Add security tests
CHANGELOG.md                                  ← Document fix (Security section)
.github/incidents-history.md                  ← Add incident record
Analysis_reports/<timestamp>_security-<issue>-CONFIDENTIAL.md  ← Analysis (DO NOT COMMIT if sensitive)
SECURITY.md                                   ← Public advisory (if applicable)
```

---

## Validation Checklist

- [ ] Vulnerability analyzed and documented
- [ ] Severity assessed (CVSS score if available)
- [ ] Affected versions identified
- [ ] Fix developed using security best practices
- [ ] Fix tested (unit tests + manual exploit attempts)
- [ ] Security tests added to prevent regression
- [ ] All tests pass
- [ ] Security scan tools run (pip-audit, Bandit)
- [ ] No new vulnerabilities introduced
- [ ] CHANGELOG. md updated (Security section)
- [ ] Incident history updated
- [ ] Version bumped appropriately
- [ ] Security advisory prepared (if public)
- [ ] Coordinated disclosure timeline followed
- [ ] Backports created (if needed for old versions)

---

## Don'ts

- ❌ Commit fix to public repo before coordinated disclosure
- ❌ Include exploit details in public commits
- ❌ Skip security testing
- ❌ Forget to update CHANGELOG (Security section)
- ❌ Leave vulnerability unfixed in old versions
- ❌ Ignore similar patterns elsewhere in codebase
- ❌ Skip updating dependencies with known vulnerabilities
- ❌ Log sensitive data (even in debug mode)

---

## References

- `.github/copilot-instructions.md` — Security rules (Section 2)
- `.github/python.instructions.md` — Secure coding practices
- `.github/workflow-rules.md` — Testing workflow
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Database](https://cwe.mitre.org/)

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 