---
mode: "agent"
description:  "Add a new step to the installation wizard (routes, templates, breadcrumb, translations, tests)"
---

# Add Wizard Step

**Task:** Add a new step to the X-Filamenta installation wizard.

---

## Input Required

### Step Details
- **Step Number:** ${input:step_number: 6}
- **Step Name:** ${input:step_name: Example: "Database Configuration"}
- **Step Description:** ${input:description:What does this step configure?}

### Form Fields (if applicable)
${input:fields:List form fields with types (text, checkbox, select, etc.)}

### Validation Rules
${input:validation: Describe validation requirements}

---

## Requirements

### 1. Update Routes (`backend/src/routes/wizard.py`)

**Add route handler:**
- Endpoint: `/wizard/step<N>`
- Methods: `GET` (display form), `POST` (process form)
- Type hints on all parameters
- Docstring explaining purpose
- Input validation
- Session management (save step data to session)
- Redirect to next step on success
- Return to same step on validation error

**Example structure:**

```python
@wizard_bp.route("/step<N>", methods=["GET", "POST"])
def step_N():
    """
    Wizard Step <N>:  <Name>
    
    <Description of what this step does>
    """
    if request.method == "POST": 
        # Validate input
        data = request.form
        errors = validate_step_N(data)
        
        if not errors:
            # Save to session
            session["wizard_step_N"] = {
                "field1": data["field1"],
                # ... 
            }
            session.modified = True
            
            logger.info("Wizard step <N> completed")
            return redirect(url_for("wizard.step_<N+1>"))
        else:
            # Show errors
            return render_template(
                "wizard/step<N>.html",
                errors=errors,
                data=data
            )
    
    # GET:  Display form
    return render_template("wizard/step<N>.html")
```

---

### 2. Create Template (`backend/src/templates/wizard/step<N>.html`)

**Extend base wizard layout:**

```html
{% extends "wizard/_wizard_content.html" %}

{% block wizard_step_content %}
<div class="wizard-step" id="step-<N>">
  <!-- Step title -->
  <h2 class="mb-4">{{ t('wizard. step<N>.title') or '<Title>' }}</h2>
  
  <!-- Step description -->
  <p class="text-muted mb-4">
    {{ t('wizard.step<N>.description') or '<Description>' }}
  </p>
  
  <!-- Form -->
  <form method="POST" action="{{ url_for('wizard. step_<N>') }}">
    {{ csrf_token() if csrf_token }}
    
    <!-- Form fields (example) -->
    <div class="mb-3">
      <label for="field1" class="form-label">
        {{ t('wizard.step<N>.field1.label') or 'Field 1' }}
      </label>
      <input 
        type="text" 
        class="form-control {% if errors and errors. field1 %}is-invalid{% endif %}" 
        id="field1" 
        name="field1" 
        value="{{ data.field1 if data else '' }}"
        required
      >
      {% if errors and errors.field1 %}
        <div class="invalid-feedback">{{ errors.field1 }}</div>
      {% endif %}
      <div class="form-text">
        {{ t('wizard.step<N>.field1.hint') or 'Help text' }}
      </div>
    </div>
    
    <!-- Buttons (included in partial) -->
    {% include 'wizard/partials/_step_buttons.html' %}
  </form>
</div>
{% endblock %}
```

---

### 3. Update Breadcrumb Configuration

**Modify breadcrumb data structure** (wherever it's defined):

**If 2-line layout (current):**
- Line 1: Steps 1, 2, 3
- Line 2: Steps 4, 5, **<N>**

**Update:**
- Add step to appropriate line
- Maintain fixed 2-line layout
- Update active state logic

---

### 4. Add Translations

**`backend/src/i18n/fr.json`:**
```json
{
  "wizard.step<N>.title": "<Titre FR>",
  "wizard.step<N>.description": "<Description FR>",
  "wizard.step<N>.field1.label":  "<Label FR>",
  "wizard. step<N>.field1.hint": "<Hint FR>",
  "wizard.step<N>. errors.required": "Ce champ est requis",
  "wizard.step<N>.errors.invalid": "Valeur invalide"
}
```

**`backend/src/i18n/en.json`:**
```json
{
  "wizard.step<N>.title": "<Title EN>",
  "wizard.step<N>.description": "<Description EN>",
  "wizard.step<N>.field1.label": "<Label EN>",
  "wizard.step<N>.field1.hint": "<Hint EN>",
  "wizard.step<N>.errors.required": "This field is required",
  "wizard. step<N>.errors.invalid":  "Invalid value"
}
```

---

### 5. Add Validation Function (if complex)

**Location:** `backend/src/services/wizard_service.py` or similar

```python
def validate_step_N(data:  dict) -> dict:
    """
    Validate wizard step <N> form data.
    
    Args:
        data: Form data dictionary
        
    Returns:
        Dictionary of errors (empty if valid)
    """
    errors = {}
    
    # Required fields
    if not data.get("field1"):
        errors["field1"] = "This field is required"
    
    # Custom validation
    if data.get("field1") and len(data["field1"]) < 3:
        errors["field1"] = "Must be at least 3 characters"
    
    return errors
```

---

### 6. Create Tests (`tests/test_wizard. py`)

```python
def test_wizard_step_N_get(client):
    """Test displaying step <N> form."""
    response = client.get("/wizard/step<N>")
    assert response.status_code == 200
    assert b"<Title>" in response. data  # Or translation key

def test_wizard_step_N_post_success(client):
    """Test successful step <N> submission."""
    response = client.post("/wizard/step<N>", data={
        "field1": "valid value"
    }, follow_redirects=False)
    
    assert response.status_code == 302  # Redirect
    assert response.location. endswith("/wizard/step<N+1>")

def test_wizard_step_N_post_validation_error(client):
    """Test step <N> with invalid data."""
    response = client. post("/wizard/step<N>", data={
        "field1": ""  # Invalid
    })
    
    assert response.status_code == 200  # Stay on page
    assert b"required" in response.data. lower()  # Error message

def test_wizard_step_N_session_storage(client):
    """Test step <N> data saved to session."""
    with client.session_transaction() as sess:
        sess["wizard_step_1"] = {"some": "data"}  # Previous step
    
    response = client.post("/wizard/step<N>", data={
        "field1":  "test value"
    })
    
    with client.session_transaction() as sess:
        assert "wizard_step_<N>" in sess
        assert sess["wizard_step_<N>"]["field1"] == "test value"
```

---

### 7. Update Documentation

**`CHANGELOG.md`:**
```markdown
## [Unreleased]

### Added
- Wizard step <N>: <Name> (#issue)
  - Form fields:  <list>
  - Validation:  <description>
  - Session storage for step data
```

**Analysis Report (if complex):**
- Location: `Analysis_reports/YYYY-MM-DD_HH-mm_wizard-step-N-design.md`
- Include: design decisions, trade-offs, implementation notes

---

## Files to Create/Modify

```
backend/src/routes/wizard.py                     ← Add route handler
backend/src/templates/wizard/step<N>.html        ← Create template
backend/src/services/wizard_service.py           ← Add validation (if complex)
backend/src/i18n/fr.json                         ← Add translations
backend/src/i18n/en.json                         ← Add translations
backend/src/templates/wizard/_breadcrumb.html    ← Update breadcrumb (if separate file)
tests/test_wizard.py                             ← Add tests
CHANGELOG. md                                     ← Update
```

---

## Wizard-Specific Rules

### Breadcrumb
- ✅ Maintain **2-line layout** (see `.github/workflow-rules.md`)
- ✅ Update active state for current step
- ✅ Make completed steps clickable (if logic allows)

### Buttons
- ✅ **Include in partial** (`wizard/partials/_step_buttons.html`)
- ✅ "Précédent" button:  Goes to step N-1
- ✅ "Suivant" button:  Submits form (type="submit")
- ❌ **DO NOT duplicate buttons** in wrapper template

### Session Management
- ✅ Save step data to `session["wizard_step_<N>"]`
- ✅ Mark session modified:  `session.modified = True`
- ✅ Clear session on wizard completion
- ✅ Handle session expiration gracefully

### Translations
- ✅ **NO hardcoded text** anywhere
- ✅ All text in `t()` function with fallback
- ✅ Add to BOTH `fr.json` AND `en.json`

---

## Validation Checklist

Before completing: 

- [ ] Route handler added with proper methods (GET, POST)
- [ ] Type hints and docstring
- [ ] Input validation implemented
- [ ] Session storage working
- [ ] Template created extending base
- [ ] Form fields match requirements
- [ ] Bootstrap 5 classes used
- [ ] Breadcrumb updated (2-line layout maintained)
- [ ] Buttons in partial (not duplicated)
- [ ] Translations added to BOTH files
- [ ] All text uses `t()` with fallback
- [ ] Tests cover GET, POST success, POST validation error, session
- [ ] CHANGELOG. md updated
- [ ] File headers added

**Testing:**
- [ ] Clean database
- [ ] Test in dev mode (all steps)
- [ ] Test in prod mode (all steps)
- [ ] Verify breadcrumb navigation
- [ ] Verify session persistence
- [ ] Verify translations display

---

## References

- `.github/workflow-rules.md` — Wizard-specific rules
- `.github/python.instructions.md` — Flask routes
- `.github/frontend.instructions.md` — Templates & i18n
- `.github/copilot-instructions.md` — General rules

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.