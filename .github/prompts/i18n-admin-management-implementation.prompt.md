---
name: "i18n-admin-management-implementation.prompt"
version: "1.0.0"
description: "Implement language management system in admin panel with Tabulator.js"
tags: ["i18n", "admin", "tabulator", "implementation"]

---

# 🌐 i18n Admin Management Implementation

## 📋 Objective

Implement a complete language management system in the admin panel allowing:
- View available languages
- Upload/add new language translations
- Edit existing translations
- Test translations in real-time
- Manage translation file versions

## 🎯 Architecture Decision (From Previous Analysis)

- **Storage:** JSON files (hierarchical by language) ✅ Option B
- **Loading:** Lazy load + local cache ✅ Option C  
- **UI:** Table-based editable interface ✅ Tabulator.js (Option B)
- **Plurals:** Not required (Option C - too complex for Phase 1)

---

## 📐 Implementation Plan

### Phase 1: Backend API Endpoints

#### Endpoint 1: List Languages

```python
@admin_i18n.route("/api/languages", methods=["GET"])
@admin_only
def get_languages():
    """List all available languages with metadata"""
    return jsonify({
        "languages": [
            {
                "code": "en",
                "name": "English",
                "native_name": "English",
                "total_keys": 524,
                "translated": 524,
                "percent": 100
            },
            {
                "code": "fr",
                "name": "Français",
                "native_name": "Français",
                "total_keys": 524,
                "translated": 520,
                "percent": 99.2
            }
        ]
    })
```

#### Endpoint 2: Get Language Translations

```python
@admin_i18n.route("/api/languages/<lang>/keys", methods=["GET"])
@admin_only
def get_language_keys(lang: str):
    """Get all translation keys for a language (with flattened structure)"""
    # Flatten nested JSON: admin.users.table.name → admin|users|table|name
    all_trans = get_all_translations(lang)
    
    flattened = []
    def flatten_keys(obj, prefix=""):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                flatten_keys(v, full_key)
            else:
                flattened.append({
                    "key": full_key,
                    "value": v,
                    "category": full_key.split(".")[0]
                })
    
    flatten_keys(all_trans)
    return jsonify({"translations": flattened})
```

#### Endpoint 3: Save Language Translation

```python
@admin_i18n.route("/api/languages/<lang>/keys/<path:key>", methods=["PUT"])
@admin_only
def update_translation(lang: str, key: str):
    """Update a single translation key"""
    data = request.json
    new_value = data.get("value", "")
    
    # Load language file
    filepath = get_translation_filepath(lang)
    with open(filepath) as f:
        trans = json.load(f)
    
    # Navigate and set nested key
    parts = key.split(".")
    target = trans
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = new_value
    
    # Save back
    with open(filepath, "w") as f:
        json.dump(trans, f, indent=2, ensure_ascii=False)
    
    # Reload translations in app
    reload_translations()
    
    return jsonify({"success": True})
```

#### Endpoint 4: Upload New Language

```python
@admin_i18n.route("/api/languages/upload", methods=["POST"])
@admin_only
def upload_language():
    """Upload new language translation file"""
    file = request.files.get("file")
    lang = request.form.get("lang", "").lower()
    
    if not file or not lang:
        return jsonify({"error": "Missing file or language code"}), 400
    
    # Validate JSON
    try:
        trans_data = json.load(file)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 400
    
    # Validate structure (must have same keys as EN)
    en_trans = get_all_translations("en")
    def get_all_keys(obj):
        keys = set()
        for k, v in obj.items():
            if isinstance(v, dict):
                keys.update(f"{k}.{sub}" for sub in get_all_keys(v))
            else:
                keys.add(k)
        return keys
    
    en_keys = get_all_keys(en_trans)
    new_keys = get_all_keys(trans_data)
    
    missing = en_keys - new_keys
    if missing:
        return jsonify({
            "error": "Missing translation keys",
            "missing": list(missing)[:10]
        }), 400
    
    # Save file
    filepath = get_translation_filepath(lang)
    with open(filepath, "w") as f:
        json.dump(trans_data, f, indent=2, ensure_ascii=False)
    
    reload_translations()
    
    return jsonify({"success": True, "message": f"Language '{lang}' uploaded"})
```

---

### Phase 2: Frontend Admin Interface

#### Template: `frontend/templates/admin/i18n.html`

```html
{% extends "layouts/admin.html" %}

{% block title %}{{ t('admin.languages.title') }} - Admin{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
  <div class="row">
    <div class="col-12">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ t('admin.languages.title') }}</h1>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#uploadModal">
          + {{ t('admin.languages.upload_new') }}
        </button>
      </div>

      <!-- Language List Table -->
      <div class="card shadow-sm">
        <div class="card-header">
          <h5 class="mb-0">{{ t('admin.languages.available') }}</h5>
        </div>
        <div class="card-body">
          <div id="languages-table"></div>
        </div>
      </div>

      <!-- Translation Keys Editor (shown when language selected) -->
      <div class="card shadow-sm mt-4" id="keys-editor" style="display: none;">
        <div class="card-header d-flex justify-content-between">
          <h5 class="mb-0">
            {{ t('admin.languages.editing') }}: <strong id="editing-lang-name"></strong>
          </h5>
          <small class="text-muted" id="progress"></small>
        </div>
        <div class="card-body">
          <!-- Tabulator table for keys -->
          <div id="translations-table"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Upload Modal -->
<div class="modal fade" id="uploadModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5>{{ t('admin.languages.upload_new') }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <form id="upload-form" enctype="multipart/form-data">
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">{{ t('admin.languages.lang_code') }}</label>
            <input type="text" class="form-control" id="lang-code" 
                   placeholder="e.g., es, de, it" required maxlength="2">
          </div>
          <div class="mb-3">
            <label class="form-label">{{ t('admin.languages.upload_file') }}</label>
            <input type="file" class="form-control" id="lang-file" 
                   accept=".json" required>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" class="btn btn-primary">
            {{ t('common.upload') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/tabulator-tables@5.4.0/dist/js.tabulator.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/tabulator-tables@5.4.0/dist/css/tabulator.min.css" rel="stylesheet">

<script>
// Language List Table
const languagesTable = new Tabulator("#languages-table", {
  layout: "fitColumns",
  responsiveLayout: "collapse",
  ajaxURL: "/admin/i18n/api/languages",
  ajaxContentType: "json",
  columns: [
    {title: "Code", field: "code", width: 80},
    {title: "Name", field: "name", width: 150},
    {title: "Keys Translated", field: "percent", width: 150, 
     formatter: "progress", formatterParams: {min: 0, max: 100}},
    {title: "Actions", width: 150, 
     formatter: (cell) => {
      const data = cell.getRow().getData();
      return `<button class="btn btn-sm btn-primary" onclick="editLanguage('${data.code}')">
                Edit
              </button>`;
    }}
  ]
});

// Translation Keys Editor (Tabulator)
let translationsTable;

function editLanguage(lang) {
  document.getElementById("keys-editor").style.display = "block";
  document.getElementById("editing-lang-name").textContent = lang;
  
  if (translationsTable) translationsTable.destroy();
  
  translationsTable = new Tabulator("#translations-table", {
    layout: "fitColumns",
    responsiveLayout: "collapse",
    ajaxURL: `/admin/i18n/api/languages/${lang}/keys`,
    columns: [
      {title: "Key", field: "key", width: 250},
      {title: "Value", field: "value", editor: "textarea", 
       headerFilter: "input"},
      {title: "Category", field: "category", width: 120}
    ],
    cellEdited: async (cell) => {
      const row = cell.getRow().getData();
      const lang = document.getElementById("editing-lang-name").textContent;
      
      try {
        const response = await fetch(
          `/admin/i18n/api/languages/${lang}/keys/${row.key}`,
          {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({value: row.value})
          }
        );
        
        if (!response.ok) throw new Error("Save failed");
        
        showAlert("✅ Saved", "success");
      } catch (err) {
        showAlert("❌ Error saving: " + err.message, "danger");
        cell.restoreValue();
      }
    }
  });
}

// Upload handler
document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const formData = new FormData();
  formData.append("lang", document.getElementById("lang-code").value);
  formData.append("file", document.getElementById("lang-file").files[0]);
  
  try {
    const response = await fetch("/admin/i18n/api/languages/upload", {
      method: "POST",
      body: formData
    });
    
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "Upload failed");
    }
    
    showAlert("✅ Language uploaded successfully", "success");
    bootstrap.Modal.getInstance(document.getElementById("uploadModal")).hide();
    languagesTable.setData();
  } catch (err) {
    showAlert("❌ " + err.message, "danger");
  }
});

function showAlert(msg, type) {
  const alert = document.createElement("div");
  alert.className = `alert alert-${type} alert-dismissible fade show`;
  alert.innerHTML = `${msg}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
  document.querySelector(".container-fluid").prepend(alert);
  setTimeout(() => alert.remove(), 5000);
}
</script>
{% endblock %}
```

---

### Phase 3: Admin Route Registration

#### Update: `backend/src/routes/admin_i18n.py`

```python
"""
Admin i18n management routes
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required
from functools import wraps
from backend.src.utils.i18n import get_all_translations, reload_translations
import json
import os

admin_i18n = Blueprint("admin_i18n", __name__, url_prefix="/admin/i18n")

def admin_only(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        from flask_login import current_user
        if not current_user.is_admin:
            return {"error": "Unauthorized"}, 403
        return f(*args, **kwargs)
    return decorated

# ... implement all API endpoints ...
```

---

### Phase 4: Add Navigation Menu Item

#### Update: `frontend/templates/components/nav.html`

Add to admin menu:
```html
<li><a href="/admin/i18n" class="dropdown-item">{{ t('admin.languages.title') }}</a></li>
```

---

## 🧪 Testing Plan

### Test 1: List Languages
```bash
curl http://localhost:5000/admin/i18n/api/languages
```

Expected:
```json
{
  "languages": [
    {"code": "en", "name": "English", ...},
    {"code": "fr", "name": "Français", ...}
  ]
}
```

### Test 2: Get Translations
```bash
curl http://localhost:5000/admin/i18n/api/languages/en/keys | head -20
```

### Test 3: Update Translation
```bash
curl -X PUT http://localhost:5000/admin/i18n/api/languages/fr/keys/auth.login.title \
  -H "Content-Type: application/json" \
  -d '{"value": "Nouvelle valeur"}'
```

### Test 4: Upload Language
```bash
curl -X POST http://localhost:5000/admin/i18n/api/languages/upload \
  -F "lang=es" \
  -F "file=@es.json"
```

---

## ✅ Success Criteria

- [ ] Admin can view all languages with stats
- [ ] Admin can edit any translation key directly in table
- [ ] Admin can upload new language file with validation
- [ ] Translations update live without page reload  
- [ ] All AJAX calls return proper JSON responses
- [ ] Error handling for invalid JSON files
- [ ] Untranslated keys highlighted/tracked

---

## 📦 Dependencies

```python
# Already installed:
- tabulator-tables (CDN)
- flask-login
- jsonify

# Might need:
# None - all dependencies already present
```

---


