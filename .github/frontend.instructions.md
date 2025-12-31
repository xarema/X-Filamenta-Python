# Frontend Rules — HTMX + Bootstrap 5 + i18n

**Purpose:** Frontend-specific rules (auto-loaded for *.html, *.css, *.js files)  
**File:** `.github/frontend.instructions.md` | Repository:  X-Filamenta-Python  
**Created:** 2025-12-30  
**Last modified:** 2025-12-30

**Distributed by:** XAREMA | Coder: AleGabMar  
**App version:** 0.0.1-Alpha | File version:  1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

**Metadata:**
- Status: Stable
- Classification: Internal
- Auto-loaded: Yes (for *. html, *.css, *. js files)

---

## 1) HTMX-First Architecture

### 1.1 Prefer HTMX Over Custom JS

**Use HTMX for:**
- ✅ Form submissions (AJAX)
- ✅ Partial page updates
- ✅ Dynamic content loading
- ✅ Search/filter interactions
- ✅ Infinite scroll
- ✅ Modal/dialog updates

**Example:**

```html
<!-- HTMX form submission -->
<form hx-post="/users" hx-target="#user-list" hx-swap="afterbegin">
  <input type="text" name="name" required>
  <input type="email" name="email" required>
  <button type="submit">Add User</button>
</form>

<!-- Target container -->
<div id="user-list">
  <!-- Partial user cards inserted here -->
</div>
```

### 1.2 HTMX Response Patterns

**Flask route returns partial HTML:**

```python
@bp.route("/users", methods=["POST"])
def create_user():
    data = request.form
    user = user_service.create_user(data)
    # Return partial template (just the new user card)
    return render_template("partials/_user_card.html", user=user), 201
```

**Partial template (`partials/_user_card.html`):**

```html
<div class="card mb-2">
  <div class="card-body">
    <h5>{{ user.name }}</h5>
    <p>{{ user. email }}</p>
  </div>
</div>
```

### 1.3 HTMX Attributes Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `hx-get` | GET request | `hx-get="/users/1"` |
| `hx-post` | POST request | `hx-post="/users"` |
| `hx-put` | PUT request | `hx-put="/users/1"` |
| `hx-delete` | DELETE request | `hx-delete="/users/1"` |
| `hx-target` | Where to put response | `hx-target="#result"` |
| `hx-swap` | How to insert | `hx-swap="innerHTML"` (default) |
| `hx-trigger` | What triggers request | `hx-trigger="click"` (default for buttons) |
| `hx-indicator` | Loading indicator | `hx-indicator="#spinner"` |

**Swap strategies:**

| Strategy | Description |
|----------|-------------|
| `innerHTML` | Replace inner content (default) |
| `outerHTML` | Replace entire element |
| `afterbegin` | Insert at start of target |
| `beforebegin` | Insert before target |
| `afterend` | Insert after target |
| `beforeend` | Insert at end of target |
| `delete` | Delete target element |
| `none` | Don't swap (useful for side effects) |

### 1.4 Loading States

**Show spinner during requests:**

```html
<button hx-post="/process" hx-indicator="#spinner">
  Process
</button>

<div id="spinner" class="htmx-indicator">
  <div class="spinner-border" role="status">
    <span class="visually-hidden">{{ t('common.loading') or 'Loading...' }}</span>
  </div>
</div>
```

**CSS for indicator:**

```css
.htmx-indicator {
  display: none;
}

.htmx-request . htmx-indicator,
.htmx-request. htmx-indicator {
  display: inline-block;
}
```

---

## 2) Bootstrap 5

### 2.1 Use Utility Classes First

**Prefer Bootstrap utilities over custom CSS:**

```html
<!-- ✅ GOOD: Bootstrap utilities -->
<div class="container mt-4">
  <div class="row g-3">
    <div class="col-md-6 col-lg-4">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title mb-3">Title</h5>
          <p class="text-muted">Description</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ❌ BAD:  Custom CSS for everything -->
<div class="my-container">
  <div class="my-row">
    <div class="my-col">
      <div class="my-card">... </div>
    </div>
  </div>
</div>
```

### 2.2 Common Bootstrap Patterns

**Grid:**

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">Column 1</div>
    <div class="col-12 col-md-6 col-lg-4">Column 2</div>
    <div class="col-12 col-md-12 col-lg-4">Column 3</div>
  </div>
</div>
```

**Forms:**

```html
<form>
  <div class="mb-3">
    <label for="email" class="form-label">{{ t('forms.email') or 'Email' }}</label>
    <input type="email" class="form-control" id="email" name="email" required>
    <div class="form-text">{{ t('forms.email.hint') or 'We will never share your email.' }}</div>
  </div>
  
  <div class="mb-3">
    <label for="password" class="form-label">{{ t('forms.password') or 'Password' }}</label>
    <input type="password" class="form-control" id="password" name="password" required>
  </div>
  
  <button type="submit" class="btn btn-primary">{{ t('buttons.submit') or 'Submit' }}</button>
</form>
```

**Alerts:**

```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
  {{ t('messages.success') or 'Success!' }}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
```

---

## 3) CSS Tokens (Custom Properties)

### 3.1 Use CSS Variables for Design Constants

**Define in `:root`:**

```css
:root {
  /* Colors */
  --color-primary: #0d6efd;
  --color-secondary: #6c757d;
  --color-success: #198754;
  --color-danger: #dc3545;
  --color-warning: #ffc107;
  --color-info: #0dcaf0;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 3rem;
  
  /* Typography */
  --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-size-base: 1rem;
  --font-size-sm: 0.875rem;
  --font-size-lg: 1.25rem;
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md:  0.375rem;
  --radius-lg: 0.5rem;
  
  /* Shadows */
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

**Use in CSS:**

```css
.custom-button {
  background-color: var(--color-primary);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
```

### 3.2 Avoid Magic Numbers

```css
/* ❌ BAD: Magic numbers everywhere */
.card {
  padding: 16px;
  margin-bottom: 24px;
  border-radius: 8px;
}

/* ✅ GOOD: Use tokens */
.card {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  border-radius: var(--radius-md);
}
```

---

## 4) Accessibility

### 4.1 Semantic HTML

**Use semantic elements:**

```html
<!-- ✅ GOOD: Semantic HTML -->
<header>
  <nav>... </nav>
</header>

<main>
  <article>
    <h1>Title</h1>
    <section>... </section>
  </article>
</main>

<footer>... </footer>

<!-- ❌ BAD:  Generic divs everywhere -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="main">
  <div class="article">...</div>
</div>
```

### 4.2 Form Labels (Mandatory)

**Always label inputs:**

```html
<!-- ✅ GOOD: Proper label -->
<label for="username">{{ t('forms.username') or 'Username' }}</label>
<input type="text" id="username" name="username">

<!-- ❌ BAD: No label -->
<input type="text" placeholder="Username">
```

### 4.3 ARIA Attributes (When Needed)

**Use when semantic HTML isn't enough:**

```html
<!-- Loading button -->
<button aria-busy="true" aria-live="polite">
  {{ t('buttons.loading') or 'Loading...' }}
</button>

<!-- Expandable section -->
<button aria-expanded="false" aria-controls="details">
  {{ t('buttons. show_details') or 'Show Details' }}
</button>
<div id="details" hidden>... </div>
```

### 4.4 Focus States

**Ensure keyboard usability:**
- All interactive elements must be focusable
- Visible focus indicator (don't use `outline:  none` without replacement)
- Logical tab order

```css
/* Custom focus style */
button:focus-visible,
a:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## 5) Custom JavaScript (Minimal)

### 5.1 When to Use Custom JS

**Only when HTMX can't handle it:**
- Complex client-side validation
- Local state management
- Canvas/WebGL interactions
- Third-party library integration (charts, maps)

### 5.2 ES Modules

**Use modern JS modules:**

```html
<!-- In HTML -->
<script type="module" src="{{ url_for('static', filename='js/app.js') }}" defer></script>
```

```javascript
// static/js/app.js
import { initializeChart } from './chart.js';
import { setupValidation } from './validation.js';

document.addEventListener('DOMContentLoaded', () => {
  initializeChart();
  setupValidation();
});
```

### 5.3 Avoid Global Variables

```javascript
// ❌ BAD: Global pollution
var userData = {};
function processUser() { ...  }

// ✅ GOOD: Module scope
const app = (() => {
  let userData = {};
  
  function processUser() { ... }
  
  return { processUser };
})();
```

### 5.4 No Inline Scripts

```html
<!-- ❌ BAD: Inline script -->
<button onclick="alert('Clicked')">Click</button>

<!-- ✅ GOOD: Event listener in module -->
<button id="clickBtn">Click</button>

<script type="module">
  document.getElementById('clickBtn').addEventListener('click', () => {
    alert('Clicked');
  });
</script>
```

---

## 6) Internationalization (i18n) — MANDATORY

### 6.1 File Structure

```
backend/src/i18n/
├── fr. json       ← French translations
└── en.json       ← English translations
```

### 6.2 Key Naming Convention

**Format:** `<context>. <sub-context>.<element>`

**Examples:**

```json
{
  "wizard.step1.title": "Configuration de base",
  "wizard.step1.description": "Configurez les paramètres.. .",
  "errors.validation.required": "Ce champ est requis",
  "buttons.next": "Suivant",
  "buttons.previous": "Précédent",
  "common.loading": "Chargement..."
}
```

**Rules:**
- Use **lowercase** with **dots** as separators
- Be **specific** (avoid generic keys like `title` alone)
- Group by **feature/page**:  `wizard.*`, `settings.*`, `dashboard.*`
- Common elements in root: `buttons.*`, `errors.*`, `common.*`

### 6.3 Adding Translations (CRITICAL)

**ALWAYS add to BOTH `fr.json` AND `en.json` simultaneously.**

**Process:**
1. Identify the text to translate
2. Choose appropriate key name (follow convention)
3. Add key+value in `fr.json`
4. Add key+value in `en.json`
5. Use in template with fallback

**Example:**

`backend/src/i18n/fr.json`:
```json
{
  "wizard.database.title": "Configuration Base de Données"
}
```

`backend/src/i18n/en. json`:
```json
{
  "wizard.database.title":  "Database Configuration"
}
```

**Template usage:**
```html
<h2>{{ t('wizard.database.title') or 'Database Configuration' }}</h2>
```

### 6.4 Template Usage (MANDATORY)

**NEVER hardcode text** — Always use translation function `t()`.

**Syntax:**
```jinja
{{ t('key. path') or 'Fallback Text' }}
```

**Fallback is MANDATORY:**
- If translation key missing → fallback displayed
- Prevents blank text in UI
- Use English as fallback language

**Examples:**

```html
<!-- Button -->
<button>{{ t('buttons.save') or 'Save' }}</button>

<!-- Title -->
<h1>{{ t('dashboard.title') or 'Dashboard' }}</h1>

<!-- Placeholder -->
<input placeholder="{{ t('forms.email. placeholder') or 'Enter your email' }}">

<!-- Error message -->
<div class="alert alert-danger">
  {{ t('errors.network.timeout') or 'Request timeout' }}
</div>

<!-- With variable -->
<p>{{ t('messages.welcome_user') or 'Welcome' }}, {{ user.name }}!</p>
```

### 6.5 Validation

**Before committing translations:**

✅ **Validate JSON syntax:**

```powershell
. \.venv\Scripts\python. exe -c "import json; json.load(open('backend/src/i18n/fr.json'))"
.\.venv\Scripts\python. exe -c "import json; json.load(open('backend/src/i18n/en.json'))"
```

✅ **Check both files have same keys** (no missing translations)

✅ **Test in browser** (switch language, verify all texts display)

### 6.6 Adding a New Language

**To add a new language (e.g., Spanish):**

1. Create `backend/src/i18n/es.json`
2. Copy structure from `en.json`
3. Translate all values
4. Update `backend/src/config.py` (add `es` to `AVAILABLE_LANGUAGES`)
5. Update language selector in UI
6. Test all pages with new language

### 6.7 Don'ts

- ❌ **NEVER** hardcode text directly in templates
- ❌ **NEVER** commit incomplete translations (missing keys)
- ❌ **NEVER** forget fallback in templates
- ❌ **NEVER** use machine translation without human review
- ❌ **NEVER** add translations outside `backend/src/i18n/*. json`

### 6.8 Automated Validation

**Before committing templates:**

✅ **Run i18n checker:**
```powershell
.\.venv\Scripts\python.exe scripts\utils\check_i18n.py
```

**This checks:**
- JSON syntax validity
- Missing translation keys (FR ↔ EN)
- Hardcoded text in templates
- Unused translation keys

**Fix all issues before committing.**

**In CI/CD:**
```powershell
.\.venv\Scripts\python.exe scripts\utils\check_i18n.py --strict
```

This will fail the build if issues detected. 

---

## 7) Template Organization (Jinja2)

### 7.1 Template Structure

```
backend/src/templates/
├── base. html              ← Base layout
├── layouts/
│   ├── _header.html
│   ├── _footer.html
│   └── _sidebar.html
├── partials/              ← HTMX fragments
│   ├── _user_card.html
│   ├── _search_results.html
│   └── _wizard_step.html
├── wizard/
│   ├── index.html
│   ├── step1.html
│   └── step2.html
└── errors/
    ├── 404.html
    └── 500.html
```

### 7.2 Base Template

```html
<!DOCTYPE html>
<html lang="{{ current_language or 'en' }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ t('common.app_name') or 'X-Filamenta' }}{% endblock %}</title>
  
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <!-- Custom CSS -->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  
  <!-- HTMX -->
  <script src="https://unpkg.com/htmx. org@1.9.10"></script>
  
  {% block head %}{% endblock %}
</head>
<body>
  {% include 'layouts/_header.html' %}
  
  <main class="container my-4">
    {% block content %}{% endblock %}
  </main>
  
  {% include 'layouts/_footer.html' %}
  
  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  
  {% block scripts %}{% endblock %}
</body>
</html>
```

### 7.3 Partial Templates (for HTMX)

**Comment required at top:**

```html
<!-- Partial: User Card
     Purpose: Display single user in list
     Target: #user-list
     Swap: afterbegin or innerHTML
     Context: user object
-->
<div class="card mb-2" id="user-{{ user.id }}">
  <div class="card-body">
    <h5 class="card-title">{{ user.name }}</h5>
    <p class="card-text text-muted">{{ user.email }}</p>
    <button 
      class="btn btn-sm btn-danger" 
      hx-delete="/users/{{ user.id }}" 
      hx-target="#user-{{ user.id }}" 
      hx-swap="outerHTML"
      hx-confirm="{{ t('messages.confirm_delete') or 'Are you sure?' }}"
    >
      {{ t('buttons.delete') or 'Delete' }}
    </button>
  </div>
</div>
```

---

## 8) Don'ts

- ❌ Use custom JS when HTMX can handle it
- ❌ Hardcode text (use i18n)
- ❌ Forget fallback in `t()` function
- ❌ Use inline styles (prefer Bootstrap utilities or CSS tokens)
- ❌ Inline scripts (use modules with `defer`)
- ❌ Skip accessibility (labels, ARIA, focus states)
- ❌ Use magic numbers in CSS (use tokens)

---

**See Also:**
- `.github/copilot-instructions.md` — General project rules
- `.github/python. instructions.md` — Python/Flask rules
- `.github/powershell.instructions.md` — PowerShell commands
- `.github/workflow-rules.md` — Workflow process