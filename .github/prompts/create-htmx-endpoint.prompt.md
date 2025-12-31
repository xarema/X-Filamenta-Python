---
mode: "agent"
description: "Create a complete HTMX endpoint with Flask route, partial template, and tests"
---

# Create HTMX Endpoint

**Task:** Create a new HTMX-powered endpoint with Flask backend and Bootstrap 5 frontend. 

---

## Input Required

### User Story
${input: story: Describe the user interaction (e.g., "User can delete items from list with AJAX")}

### Route Details
- **Endpoint URL:** ${input:url:/example-route}
- **HTTP Method:** ${input:method:GET|POST|PUT|DELETE}
- **Target Element:** ${input:target:#element-id}
- **Swap Strategy:** ${input:swap:innerHTML|outerHTML|afterbegin|beforeend}

### Existing Context (Optional)
${input:context: Paste relevant existing code if modifying existing feature}

---

## Requirements

### Backend (Flask)

1. **Create route in appropriate Blueprint:**
   - Location:   `backend/src/routes/<blueprint>. py`
   - Add proper type hints
   - Add docstring explaining purpose
   - Validate all inputs (query params, form data, JSON)
   - Return appropriate HTTP status codes (200, 201, 400, 404, etc.)
   - Use proper error handling

2. **Business logic in service layer (if complex):**
   - Location:  `backend/src/services/<service>.py`
   - Keep route handler thin
   - Use pure functions when possible

3. **Add logging:**
   - Use `logging` module (not `print`)
   - Log important events (INFO level)
   - Log errors/warnings appropriately

### Frontend (Template)

1. **Create partial template:**
   - Location: `backend/src/templates/partials/_<name>.html`
   - Add comment header explaining:  
     - Purpose
     - Expected target
     - Swap strategy
     - Required context variables
   - Use Bootstrap 5 classes
   - NO custom CSS unless absolutely necessary

2. **HTMX attributes:**
   - `hx-<method>`: Correct HTTP verb
   - `hx-target`: Stable, predictable selector
   - `hx-swap`: Appropriate strategy
   - `hx-indicator`: Loading state (if applicable)
   - `hx-confirm`: For destructive actions

3. **Accessibility:**
   - Semantic HTML
   - Proper labels (`<label for="... ">`)
   - ARIA attributes only when needed
   - Keyboard accessible

### Translations (i18n)

1. **Add to BOTH translation files:**
   - `backend/src/i18n/fr.json`
   - `backend/src/i18n/en.json`

2. **Use in template:**
   - `{{ t('key. path') or 'Fallback' }}`
   - Fallback is MANDATORY

3. **Key naming convention:**
   - Format:   `<context>.<sub-context>.<element>`
   - Example: `user_list.delete.confirm`

### Testing

1. **Create pytest test:**
   - Location: `tests/test_<feature>.py`
   - Test happy path (successful request)
   - Test edge cases (invalid input, missing data)
   - Test error cases (404, 400, 500)
   - Assert status codes AND minimal response content

2. **Test must be deterministic:**
   - No real network calls
   - No real database (use fixtures or in-memory SQLite)
   - Mock external dependencies

### Documentation

1. **Update CHANGELOG. md:**
   - Add to `[Unreleased]` section
   - Category: `Added`
   - Format: `- HTMX endpoint for <feature> (#issue)`

2. **Add file headers:**
   - Follow template in `.github/copilot-instructions.md` section 4
   - Include purpose, license, copyright

---

## Output Structure

### Files to Create/Modify

```
backend/src/routes/<blueprint>. py         ← Add route handler
backend/src/services/<service>.py         ← Business logic (if needed)
backend/src/templates/partials/_<name>. html  ← HTMX partial
backend/src/i18n/fr.json                  ← French translations
backend/src/i18n/en.json                  ← English translations
tests/test_<feature>.py                   ← Tests
CHANGELOG.md                              ← Update
```

---

## Example Output

### Route (`backend/src/routes/users.py`)

```python
@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id:  int):
    """
    Delete a user by ID (HTMX endpoint).
    
    Returns empty 200 response on success, allowing client to remove element.
    """
    logger.info("Deleting user ID: %s", user_id)
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    logger.info("User ID %s deleted successfully", user_id)
    return "", 200  # Empty response, HTMX will remove element
```

### Partial Template (`backend/src/templates/partials/_user_card.html`)

```html
<!-- Partial:  User Card
     Purpose: Display single user in list with delete button
     Target: #user-list (or individual card)
     Swap: outerHTML (when deleting), afterbegin (when adding)
     Context: user object (id, name, email)
-->
<div class="card mb-2" id="user-{{ user.id }}">
  <div class="card-body d-flex justify-content-between align-items-center">
    <div>
      <h5 class="card-title mb-1">{{ user.name }}</h5>
      <p class="card-text text-muted small mb-0">{{ user.email }}</p>
    </div>
    <button 
      class="btn btn-sm btn-danger" 
      hx-delete="/users/{{ user.id }}" 
      hx-target="#user-{{ user.id }}" 
      hx-swap="outerHTML"
      hx-confirm="{{ t('user_list.delete.confirm') or 'Are you sure you want to delete this user?' }}"
      aria-label="{{ t('user_list.delete.aria') or 'Delete user' }}"
    >
      {{ t('buttons.delete') or 'Delete' }}
    </button>
  </div>
</div>
```

### Translations

**`backend/src/i18n/fr.json`:**
```json
{
  "user_list.delete.confirm": "Êtes-vous sûr de vouloir supprimer cet utilisateur ?",
  "user_list.delete.aria": "Supprimer l'utilisateur",
  "buttons.delete": "Supprimer"
}
```

**`backend/src/i18n/en.json`:**
```json
{
  "user_list.delete.confirm": "Are you sure you want to delete this user? ",
  "user_list. delete.aria": "Delete user",
  "buttons.delete": "Delete"
}
```

### Test (`tests/test_users.py`)

```python
def test_delete_user_success(client, sample_user):
    """Test successful user deletion."""
    response = client.delete(f"/users/{sample_user.id}")
    assert response.status_code == 200
    assert response.data == b""  # Empty response
    
    # Verify user deleted
    assert User.query.get(sample_user.id) is None

def test_delete_user_not_found(client):
    """Test deleting non-existent user returns 404."""
    response = client.delete("/users/99999")
    assert response.status_code == 404
```

---

## Validation Checklist

Before completing, verify:

- [ ] Route handler is thin (business logic in service if complex)
- [ ] Type hints on all parameters
- [ ] Docstring explains purpose
- [ ] Input validation (no trusting client data)
- [ ] Proper HTTP status codes
- [ ] Partial template has comment header
- [ ] Bootstrap 5 classes used
- [ ] HTMX attributes correct
- [ ] Translations added to BOTH files
- [ ] Fallback in template (`or 'Fallback'`)
- [ ] Tests cover happy path + edge cases + errors
- [ ] Tests are deterministic (no real network/DB)
- [ ] CHANGELOG. md updated
- [ ] File headers added

---

## References

- `.github/copilot-instructions. md` — General rules
- `.github/python. instructions.md` — Python/Flask rules
- `.github/frontend. instructions.md` — HTMX/Bootstrap/i18n rules
- `.github/workflow-rules.md` — Testing workflow

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved. 