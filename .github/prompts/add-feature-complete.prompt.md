---
mode: "agent"
description: "Add a complete feature (backend + frontend + tests + documentation)"
---

# Add Complete Feature

**Task:** Add a complete feature from scratch, including backend routes, frontend templates, business logic, tests, and documentation.

---

## Input Required

### Feature Description
${input: feature: Describe the feature in detail (e.g., "User authentication with email/password")}

### User Stories
${input:stories:List user stories or acceptance criteria}

### Technical Requirements
${input:requirements: Specific technical requirements (database models, APIs, integrations, etc.)}

### Design Mockups/Wireframes (Optional)
${input:design:Paste links or describe UI layout}

---

## MANDATORY:  Pre-Implementation Process

### 1. Read Project Rules
- ✅ `.github/copilot-instructions.md` — General rules
- ✅ `.github/python.instructions.md` — Backend rules
- ✅ `.github/frontend.instructions.md` — Frontend rules
- ✅ `.github/workflow-rules.md` — Workflow process
- ✅ `.github/incidents-history.md` — Past issues

### 2. Kill All Servers

```powershell
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 3. Create Analysis Report

**Location:** `Analysis_reports/YYYY-MM-DD_HH-mm_feature-<name>-design.md`

**Content:**
- Feature overview
- User stories breakdown
- Technical approach
- Database schema changes (if any)
- API endpoints design
- UI/UX considerations
- Security considerations
- Testing strategy
- Risks and mitigations
- Implementation plan (step-by-step)

---

## Implementation Checklist

### 1. Database Layer (if needed)

**Models (`backend/src/models. py` or separate file):**
- [ ] Define SQLAlchemy models
- [ ] Add proper relationships (ForeignKey, backref)
- [ ] Add indexes for performance
- [ ] Add constraints (unique, nullable, defaults)
- [ ] Add `to_dict()` method for serialization
- [ ] Add docstrings

**Example:**
```python
from datetime import datetime
from backend.src import db

class Feature(db.Model):
    """Feature model description."""
    __tablename__ = "features"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime. utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = db.relationship("User", backref="features")
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self. created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id
        }
```

**Migration:**
```powershell
# Create migration
. \. venv\Scripts\flask. exe db migrate -m "Add Feature model"

# Review migration file in migrations/versions/

# Apply migration
.\.venv\Scripts\flask.exe db upgrade
```

---

### 2. Service Layer

**Location:** `backend/src/services/feature_service.py`

**Responsibilities:**
- [ ] Business logic (not in routes)
- [ ] Data validation
- [ ] Complex operations
- [ ] External API calls (if any)
- [ ] Error handling (raise custom exceptions)

**Example:**
```python
"""
Feature service layer. 

Purpose: Business logic for feature management
File: backend/src/services/feature_service.py | Repository:  X-Filamenta-Python
"""
import logging
from typing import List, Optional
from backend.src.models import Feature, db
from backend.src.exceptions import FeatureNotFoundError, ValidationError

logger = logging.getLogger(__name__)

def create_feature(user_id: int, data: dict) -> Feature:
    """
    Create a new feature. 
    
    Args:
        user_id: ID of user creating feature
        data: Feature data (name, description)
        
    Returns:
        Created Feature object
        
    Raises:
        ValidationError: If data invalid
    """
    # Validate
    if not data.get("name"):
        raise ValidationError("Feature name is required")
    
    if len(data["name"]) < 3:
        raise ValidationError("Feature name must be at least 3 characters")
    
    # Create
    feature = Feature(
        name=data["name"]. strip(),
        description=data. get("description", "").strip(),
        user_id=user_id
    )
    
    db.session.add(feature)
    db.session.commit()
    
    logger.info("Feature created:  ID=%s, User=%s", feature.id, user_id)
    return feature

def get_feature(feature_id: int) -> Feature:
    """Get feature by ID."""
    feature = Feature.query.get(feature_id)
    if not feature:
        raise FeatureNotFoundError(f"Feature {feature_id} not found")
    return feature

def list_features(user_id: Optional[int] = None) -> List[Feature]:
    """List all features, optionally filtered by user."""
    query = Feature.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(Feature.created_at.desc()).all()

def update_feature(feature_id: int, data: dict) -> Feature:
    """Update feature."""
    feature = get_feature(feature_id)
    
    if "name" in data:
        if len(data["name"]) < 3:
            raise ValidationError("Feature name must be at least 3 characters")
        feature.name = data["name"].strip()
    
    if "description" in data:
        feature.description = data["description"].strip()
    
    db.session.commit()
    logger.info("Feature updated: ID=%s", feature_id)
    return feature

def delete_feature(feature_id: int) -> None:
    """Delete feature."""
    feature = get_feature(feature_id)
    db.session.delete(feature)
    db.session.commit()
    logger.info("Feature deleted: ID=%s", feature_id)
```

---

### 3. Routes Layer

**Location:** `backend/src/routes/feature.py` (new Blueprint)

**Responsibilities:**
- [ ] HTTP request/response handling
- [ ] Input parsing (JSON, form data, query params)
- [ ] Call service layer
- [ ] Return proper status codes
- [ ] Error handling (catch service exceptions)

**Example:**
```python
"""
Feature routes.

Purpose: HTTP endpoints for feature management
File: backend/src/routes/feature.py | Repository: X-Filamenta-Python
"""
import logging
from flask import Blueprint, request, jsonify, render_template
from backend.src. services import feature_service
from backend.src.exceptions import FeatureNotFoundError, ValidationError

logger = logging.getLogger(__name__)

bp = Blueprint("feature", __name__, url_prefix="/features")

@bp.route("", methods=["GET"])
def list_features():
    """List all features (HTML or JSON)."""
    features = feature_service.list_features()
    
    if request.accept_mimetypes.best == "application/json":
        return jsonify([f.to_dict() for f in features]), 200
    
    return render_template("features/list.html", features=features)

@bp.route("", methods=["POST"])
def create_feature():
    """Create new feature (HTMX endpoint)."""
    data = request.form or request.json
    
    try:
        # TODO: Get user_id from session/auth
        user_id = 1  # Placeholder
        feature = feature_service.create_feature(user_id, data)
        
        # Return partial for HTMX
        if request.headers.get("HX-Request"):
            return render_template("partials/_feature_card.html", feature=feature), 201
        
        # Return JSON for API
        return jsonify(feature.to_dict()), 201
        
    except ValidationError as e: 
        logger.warning("Feature creation failed: %s", str(e))
        return jsonify({"error": "Validation Error", "message": str(e)}), 400

@bp.route("/<int:feature_id>", methods=["GET"])
def get_feature(feature_id:  int):
    """Get single feature."""
    try:
        feature = feature_service.get_feature(feature_id)
        
        if request.accept_mimetypes.best == "application/json":
            return jsonify(feature.to_dict()), 200
        
        return render_template("features/detail.html", feature=feature)
        
    except FeatureNotFoundError:
        return jsonify({"error": "Not Found", "message": "Feature not found"}), 404

@bp.route("/<int:feature_id>", methods=["PUT", "PATCH"])
def update_feature(feature_id: int):
    """Update feature."""
    data = request.json or request.form
    
    try:
        feature = feature_service.update_feature(feature_id, data)
        return jsonify(feature.to_dict()), 200
        
    except FeatureNotFoundError:
        return jsonify({"error": "Not Found"}), 404
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "message": str(e)}), 400

@bp.route("/<int:feature_id>", methods=["DELETE"])
def delete_feature(feature_id: int):
    """Delete feature (HTMX endpoint)."""
    try:
        feature_service.delete_feature(feature_id)
        return "", 200  # Empty response for HTMX
        
    except FeatureNotFoundError:
        return jsonify({"error": "Not Found"}), 404

# Register blueprint in app factory (backend/src/__init__.py)
# from backend.src.routes import feature
# app.register_blueprint(feature. bp)
```

---

### 4. Frontend Templates

**Create templates:**

**`backend/src/templates/features/list.html`:**
```html
{% extends "base.html" %}

{% block title %}{{ t('features.list. title') or 'Features' }}{% endblock %}

{% block content %}
<div class="container my-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h1>{{ t('features.list.title') or 'Features' }}</h1>
    <button 
      class="btn btn-primary" 
      data-bs-toggle="modal" 
      data-bs-target="#createFeatureModal"
    >
      {{ t('buttons.create') or 'Create Feature' }}
    </button>
  </div>
  
  <!-- Feature list -->
  <div id="feature-list" class="row g-3">
    {% for feature in features %}
      {% include 'partials/_feature_card.html' %}
    {% else %}
      <div class="col-12">
        <p class="text-muted text-center">
          {{ t('features.list.empty') or 'No features yet.' }}
        </p>
      </div>
    {% endfor %}
  </div>
  
  <!-- Create modal -->
  {% include 'features/_create_modal.html' %}
</div>
{% endblock %}
```

**`backend/src/templates/partials/_feature_card.html`:**
```html
<!-- Partial:  Feature Card
     Purpose: Display single feature in list
     Target: #feature-list
     Swap: afterbegin (when creating), outerHTML (when updating/deleting)
     Context: feature object
-->
<div class="col-md-6 col-lg-4" id="feature-{{ feature.id }}">
  <div class="card h-100 shadow-sm">
    <div class="card-body">
      <h5 class="card-title">{{ feature.name }}</h5>
      <p class="card-text text-muted">{{ feature.description or (t('common.no_description') or 'No description') }}</p>
      <small class="text-muted">
        {{ t('common.created') or 'Created' }}: {{ feature.created_at. strftime('%Y-%m-%d') }}
      </small>
    </div>
    <div class="card-footer bg-transparent border-top-0">
      <div class="btn-group btn-group-sm w-100" role="group">
        <a href="{{ url_for('feature. get_feature', feature_id=feature.id) }}" class="btn btn-outline-primary">
          {{ t('buttons.view') or 'View' }}
        </a>
        <button 
          class="btn btn-outline-danger" 
          hx-delete="{{ url_for('feature.delete_feature', feature_id=feature.id) }}" 
          hx-target="#feature-{{ feature.id }}" 
          hx-swap="outerHTML"
          hx-confirm="{{ t('features.delete. confirm') or 'Are you sure?' }}"
        >
          {{ t('buttons.delete') or 'Delete' }}
        </button>
      </div>
    </div>
  </div>
</div>
```

---

### 5. Translations (i18n)

**Add to `backend/src/i18n/fr.json`:**
```json
{
  "features. list.title": "Fonctionnalités",
  "features.list.empty": "Aucune fonctionnalité pour le moment.",
  "features.create.title": "Créer une fonctionnalité",
  "features.create.name. label": "Nom",
  "features.create.description.label": "Description",
  "features.delete.confirm": "Êtes-vous sûr de vouloir supprimer cette fonctionnalité ?",
  "buttons.create": "Créer",
  "buttons.view": "Voir",
  "buttons. delete": "Supprimer",
  "common.created": "Créé le",
  "common.no_description":  "Aucune description"
}
```

**Add to `backend/src/i18n/en.json`:**
```json
{
  "features. list.title": "Features",
  "features.list.empty":  "No features yet.",
  "features.create.title": "Create Feature",
  "features.create.name.label": "Name",
  "features.create.description.label": "Description",
  "features.delete.confirm": "Are you sure you want to delete this feature?",
  "buttons.create": "Create",
  "buttons.view":  "View",
  "buttons. delete": "Delete",
  "common.created": "Created",
  "common.no_description":  "No description"
}
```

---

### 6. Tests

**Create `tests/test_feature.py`:**

```python
"""
Tests for feature functionality.

File: tests/test_feature.py | Repository: X-Filamenta-Python
"""
import pytest
from backend.src import create_app, db
from backend. src.models import Feature, User
from backend.src.services import feature_service
from backend.src.exceptions import FeatureNotFoundError, ValidationError

@pytest.fixture
def app():
    """Create test app."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create sample user."""
    user = User(name="Test User", email="test@example.com")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def sample_feature(app, sample_user):
    """Create sample feature."""
    feature = Feature(
        name="Test Feature",
        description="Test description",
        user_id=sample_user.id
    )
    db.session.add(feature)
    db.session.commit()
    return feature

# Service layer tests
def test_create_feature_success(app, sample_user):
    """Test successful feature creation."""
    data = {"name": "New Feature", "description": "Description"}
    feature = feature_service.create_feature(sample_user.id, data)
    
    assert feature. id is not None
    assert feature. name == "New Feature"
    assert feature.description == "Description"
    assert feature.user_id == sample_user.id

def test_create_feature_validation_error(app, sample_user):
    """Test feature creation with invalid data."""
    data = {"name": "AB"}  # Too short
    
    with pytest.raises(ValidationError):
        feature_service.create_feature(sample_user.id, data)

def test_get_feature_success(app, sample_feature):
    """Test getting feature by ID."""
    feature = feature_service.get_feature(sample_feature.id)
    assert feature.id == sample_feature.id

def test_get_feature_not_found(app):
    """Test getting non-existent feature."""
    with pytest.raises(FeatureNotFoundError):
        feature_service.get_feature(99999)

# Route tests
def test_list_features_empty(client):
    """Test listing features when none exist."""
    response = client.get("/features")
    assert response.status_code == 200
    assert b"No features yet" in response.data or b"Aucune" in response.data

def test_list_features_with_data(client, sample_feature):
    """Test listing features."""
    response = client.get("/features")
    assert response.status_code == 200
    assert sample_feature.name. encode() in response.data

def test_create_feature_api_success(client, sample_user):
    """Test creating feature via API."""
    response = client.post("/features", json={
        "name": "API Feature",
        "description": "Created via API"
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "API Feature"

def test_create_feature_api_validation_error(client):
    """Test creating feature with invalid data."""
    response = client.post("/features", json={"name": "AB"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_delete_feature_success(client, sample_feature):
    """Test deleting feature."""
    response = client.delete(f"/features/{sample_feature.id}")
    assert response.status_code == 200
    
    # Verify deleted
    with pytest.raises(FeatureNotFoundError):
        feature_service.get_feature(sample_feature.id)

def test_delete_feature_not_found(client):
    """Test deleting non-existent feature."""
    response = client.delete("/features/99999")
    assert response.status_code == 404
```

---

### 7. Documentation

**Update `CHANGELOG.md`:**
```markdown
## [Unreleased]

### Added
- Feature management system (#issue)
  - CRUD operations for features
  - Database model with user relationships
  - Service layer with validation
  - REST API endpoints
  - HTMX-powered UI
  - Comprehensive test coverage (95%+)
```

**Create analysis report:** `Analysis_reports/YYYY-MM-DD_HH-mm_feature-<name>-implementation.md`

---

## Files Created/Modified

```
backend/src/models.py (or models/feature.py)     ← Add model
backend/src/services/feature_service.py          ← Create service
backend/src/routes/feature.py                    ← Create routes
backend/src/__init__.py                          ← Register blueprint
backend/src/templates/features/list.html         ← Create template
backend/src/templates/features/detail.html       ← Create template
backend/src/templates/features/_create_modal.html ← Create partial
backend/src/templates/partials/_feature_card.html ← Create partial
backend/src/i18n/fr.json                         ← Add translations
backend/src/i18n/en.json                         ← Add translations
tests/test_feature.py                            ← Create tests
migrations/versions/<timestamp>_add_feature. py   ← Migration
CHANGELOG.md                                     ← Update
Analysis_reports/<timestamp>_feature-design.md   ← Design doc
Analysis_reports/<timestamp>_feature-impl.md     ← Implementation notes
```

---

## Testing Workflow

### 1. Automated Tests

```powershell
# Run all tests
. \.venv\Scripts\pytest. exe -v

# Run only feature tests
.\.venv\Scripts\pytest.exe tests/test_feature.py -v

# Coverage report
.\.venv\Scripts\pytest.exe --cov=backend. src. services. feature_service --cov=backend.src.routes.feature
```

### 2. Manual Testing

**Dev mode:**
```powershell
# Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Clean DB (optional)
Remove-Item "instance\*. db" -Force -ErrorAction SilentlyContinue

# Run migrations
. \.venv\Scripts\flask. exe db upgrade

# Start dev server
.\.venv\Scripts\python.exe backend\src\app.py

# Test in browser: 
# - http://localhost:5000/features (list)
# - Create feature
# - View feature
# - Delete feature
# - Check all translations display
```

**Prod mode:**
```powershell
# Kill servers
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Start prod server
.\.venv\Scripts\python.exe run_prod. py

# Test same scenarios
```

---

## Validation Checklist

- [ ] Analysis report created (design phase)
- [ ] Database model defined with proper relationships
- [ ] Migration created and tested
- [ ] Service layer implements all business logic
- [ ] Routes are thin (delegate to service)
- [ ] Type hints on all functions
- [ ] Docstrings complete
- [ ] Error handling comprehensive
- [ ] Logging added (appropriate levels)
- [ ] Templates created (list, detail, partials)
- [ ] Bootstrap 5 classes used
- [ ] HTMX patterns followed
- [ ] Translations added to BOTH files
- [ ] All text uses `t()` with fallback
- [ ] Tests cover service layer (unit tests)
- [ ] Tests cover routes (integration tests)
- [ ] Test coverage ≥ 90%
- [ ] All tests pass
- [ ] Linters pass (Ruff, Mypy)
- [ ] Tested in dev mode (all features)
- [ ] Tested in prod mode (all features)
- [ ] No console errors
- [ ] No log warnings/errors
- [ ] CHANGELOG. md updated
- [ ] Implementation report created

---

## Don'ts

- ❌ Skip analysis/design phase
- ❌ Put business logic in routes
- ❌ Skip service layer for complex features
- ❌ Forget to register Blueprint
- ❌ Hardcode text (use i18n)
- ❌ Skip tests ("I'll add them later")
- ❌ Commit without running full test suite
- ❌ Test only happy path (test errors!)
- ❌ Forget to update CHANGELOG
- ❌ Leave commented-out code

---

## References

- `.github/copilot-instructions.md` — General rules
- `.github/python.instructions.md` — Backend rules
- `.github/frontend.instructions.md` — Frontend rules
- `.github/workflow-rules.md` — Workflow process

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved. 