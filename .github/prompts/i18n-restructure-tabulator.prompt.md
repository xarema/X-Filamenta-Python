---
Purpose: Implémentation de la nouvelle stack i18n avec gestion admin Tabulator
Description: Ce prompt implémente la nouvelle architecture i18n (JSON hiérarchique + lazy load + cache) et crée l'interface d'administration avec Tabulator.js pour la gestion des traductions.

File: .github/prompts/i18n-restructure-tabulator.prompt.md | Repository: X-Filamenta-Python
Created: 2025-12-30T09:00:00-05:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Notes:
- Exécuter APRÈS l'audit i18n (i18n-audit-restructure.prompt.md)
- Nécessite le rapport d'audit pour planifier les migrations
- Crée interface admin avec Tabulator.js pour édition des traductions
---

# 🔧 Implémentation Nouvelle Stack i18n + Admin Tabulator

## 📋 Objectifs

1. **Migrer** vers JSON hiérarchique par langue (structure optimale)
2. **Implémenter** lazy loading + cache local (performance)
3. **Créer** interface admin avec Tabulator.js (gestion traductions)
4. **Ajouter** upload de nouvelles langues (extensibilité)
5. **Tester** complètement (validation)

---

## 🎯 Architecture Cible

### Décisions Confirmées

| Question | Réponse Choisie |
|----------|-----------------|
| **Q1: Structure de stockage** | **Option B:** JSON hiérarchique par langue |
| **Q2: Mécanisme de chargement** | **Option C:** Lazy load + cache local |
| **Q3: Interface admin** | **Option B:** Table éditable (Tabulator.js) |
| **Q4: Babel** | **Option C:** Non, trop complexe pour cette phase |

### Structure des Fichiers

```
backend/src/i18n/
├── loader.py              # Service de chargement des traductions
├── cache_manager.py       # Gestion du cache local
└── translations/          # Fichiers JSON par langue
    ├── en.json           # Langue par défaut
    ├── fr.json           # Français
    └── ...               # Langues futures

frontend/templates/admin/
└── translations.html      # Interface admin Tabulator

backend/src/routes/
└── admin_i18n.py         # Routes CRUD traductions
```

---

## 🏗️ Phase 1 : Backend — Nouvelle Stack

### 1.1 Service de Chargement (`backend/src/i18n/loader.py`)

**Fonctionnalités:**
- Lazy loading des fichiers JSON
- Cache en mémoire (dict Python)
- Fallback EN si clé manquante
- Validation de structure

**Exemple d'implémentation:**

```python
"""
Purpose: Service de chargement et gestion des traductions i18n
Description: Lazy loading, cache local, fallback automatique

File: backend/src/i18n/loader.py | Repository: X-Filamenta-Python
Created: 2025-12-30T09:00:00-05:00

License: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from flask import current_app

class TranslationLoader:
    """Gestionnaire de chargement des traductions avec cache."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._translations_dir = Path(__file__).parent / "translations"
    
    def load_language(self, lang_code: str) -> Dict[str, Any]:
        """Charge un fichier de langue avec cache."""
        if lang_code in self._cache:
            return self._cache[lang_code]
        
        file_path = self._translations_dir / f"{lang_code}.json"
        
        if not file_path.exists():
            current_app.logger.warning(f"Language file not found: {lang_code}")
            return self.load_language('en')  # Fallback
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                self._cache[lang_code] = translations
                return translations
        except Exception as e:
            current_app.logger.error(f"Error loading {lang_code}: {e}")
            return {}
    
    def get_translation(self, lang_code: str, key: str, **kwargs) -> str:
        """Récupère une traduction avec fallback."""
        translations = self.load_language(lang_code)
        
        # Navigation hiérarchique (ex: "auth.login.title")
        keys = key.split('.')
        value = translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Fallback EN si clé manquante
                if lang_code != 'en':
                    return self.get_translation('en', key, **kwargs)
                return f"[MISSING: {key}]"
        
        # Interpolation de variables
        if isinstance(value, str) and kwargs:
            return value.format(**kwargs)
        
        return value
    
    def clear_cache(self):
        """Vide le cache (utile après modification)."""
        self._cache.clear()
    
    def get_available_languages(self) -> list:
        """Liste toutes les langues disponibles."""
        return [f.stem for f in self._translations_dir.glob("*.json")]

# Instance globale
translation_loader = TranslationLoader()
```

### 1.2 Helper Template (`backend/src/utils/template_helpers.py`)

```python
"""Helper pour templates Jinja."""

from flask import session
from backend.src.i18n.loader import translation_loader

def get_translation(key: str, **kwargs) -> str:
    """Fonction t() pour templates."""
    lang = session.get('language', 'en')
    return translation_loader.get_translation(lang, key, **kwargs)

def init_template_helpers(app):
    """Enregistre helpers dans Jinja."""
    app.jinja_env.globals['t'] = get_translation
```

### 1.3 Routes Admin (`backend/src/routes/admin_i18n.py`)

**Endpoints:**
- `GET /admin/translations` → Interface Tabulator
- `GET /api/translations/<lang>` → Récupère toutes les traductions d'une langue
- `POST /api/translations/<lang>` → Met à jour une clé
- `POST /api/translations/upload` → Upload nouvelle langue (fichier JSON)
- `DELETE /api/translations/<lang>/<key>` → Supprime une clé

**Exemple:**

```python
"""
Purpose: Routes API pour gestion des traductions (Admin)
"""

from flask import Blueprint, jsonify, request, render_template
from backend.src.decorators import admin_required
from backend.src.i18n.loader import translation_loader
import json

bp = Blueprint('admin_i18n', __name__, url_prefix='/admin')

@bp.route('/translations')
@admin_required
def translations_page():
    """Interface admin Tabulator."""
    languages = translation_loader.get_available_languages()
    return render_template('admin/translations.html', languages=languages)

@bp.route('/api/translations/<lang>')
@admin_required
def get_translations(lang):
    """Récupère toutes les traductions d'une langue."""
    translations = translation_loader.load_language(lang)
    # Aplatir structure hiérarchique pour Tabulator
    flat = flatten_dict(translations)
    return jsonify(flat)

@bp.route('/api/translations/<lang>', methods=['POST'])
@admin_required
def update_translation(lang):
    """Met à jour une traduction."""
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    
    # Charger JSON
    file_path = translation_loader._translations_dir / f"{lang}.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # Mettre à jour clé (navigation hiérarchique)
    set_nested_key(translations, key, value)
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
    
    # Clear cache
    translation_loader.clear_cache()
    
    return jsonify({'success': True})

def flatten_dict(d, parent_key='', sep='.'):
    """Aplatir dict hiérarchique."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def set_nested_key(d, key, value):
    """Définir clé dans dict hiérarchique."""
    keys = key.split('.')
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value
```

---

## 🎨 Phase 2 : Frontend — Interface Admin Tabulator

### 2.1 Template (`frontend/templates/admin/translations.html`)

**Fonctionnalités:**
- Table Tabulator éditable
- Filtrage par langue
- Recherche de clés
- Édition inline
- Upload fichier JSON

**Exemple:**

```html
{% extends "layouts/admin.html" %}

{% block title %}{{ t('admin.translations.title') }}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row mb-3">
        <div class="col-md-6">
            <h2>{{ t('admin.translations.title') }}</h2>
        </div>
        <div class="col-md-6 text-end">
            <select id="languageSelector" class="form-select d-inline-block w-auto">
                {% for lang in languages %}
                <option value="{{ lang }}">{{ lang.upper() }}</option>
                {% endfor %}
            </select>
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#uploadModal">
                {{ t('admin.translations.upload') }}
            </button>
        </div>
    </div>
    
    <div id="translations-table"></div>
</div>

<!-- Modal Upload -->
<div class="modal fade" id="uploadModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5>{{ t('admin.translations.upload_new_language') }}</h5>
            </div>
            <div class="modal-body">
                <input type="file" id="jsonFileInput" accept=".json" class="form-control">
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">{{ t('common.cancel') }}</button>
                <button class="btn btn-primary" onclick="uploadLanguage()">{{ t('common.upload') }}</button>
            </div>
        </div>
    </div>
</div>

<script>
// Tabulator initialization
let table;

document.addEventListener('DOMContentLoaded', function() {
    loadTranslations('en');
    
    document.getElementById('languageSelector').addEventListener('change', function(e) {
        loadTranslations(e.target.value);
    });
});

function loadTranslations(lang) {
    fetch(`/admin/api/translations/${lang}`)
        .then(r => r.json())
        .then(data => {
            const rows = Object.entries(data).map(([key, value]) => ({
                key: key,
                value: value,
                lang: lang
            }));
            
            if (table) {
                table.destroy();
            }
            
            table = new Tabulator("#translations-table", {
                data: rows,
                layout: "fitColumns",
                pagination: "local",
                paginationSize: 50,
                columns: [
                    {title: "{{ t('admin.translations.key') }}", field: "key", width: 400},
                    {
                        title: "{{ t('admin.translations.value') }}", 
                        field: "value", 
                        editor: "input",
                        cellEdited: function(cell) {
                            updateTranslation(cell.getData());
                        }
                    }
                ],
                placeholder: "{{ t('admin.translations.no_data') }}"
            });
        });
}

function updateTranslation(row) {
    fetch(`/admin/api/translations/${row.lang}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            key: row.key,
            value: row.value
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast('{{ t("admin.translations.save_success") }}', 'success');
        }
    });
}

function uploadLanguage() {
    const fileInput = document.getElementById('jsonFileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('{{ t("admin.translations.select_file") }}');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/admin/api/translations/upload', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}
</script>
{% endblock %}
```

---

## 🧪 Phase 3 : Tests

### 3.1 Tests Backend

**Fichier:** `backend/tests/test_i18n_loader.py`

```python
import pytest
from backend.src.i18n.loader import translation_loader

def test_load_english():
    """Test chargement EN."""
    trans = translation_loader.load_language('en')
    assert isinstance(trans, dict)
    assert len(trans) > 0

def test_get_translation_simple():
    """Test récupération simple."""
    result = translation_loader.get_translation('en', 'auth.login.title')
    assert result != '[MISSING: auth.login.title]'

def test_fallback_to_en():
    """Test fallback si clé manquante en FR."""
    result = translation_loader.get_translation('fr', 'nonexistent.key')
    # Doit retourner la valeur EN ou [MISSING]
    assert isinstance(result, str)

def test_interpolation():
    """Test interpolation variables."""
    result = translation_loader.get_translation('en', 'welcome.message', username='John')
    assert 'John' in result
```

### 3.2 Tests Frontend

**Fichier:** `frontend/tests/test_translations_admin.html`

- Test chargement table Tabulator
- Test édition inline
- Test upload fichier JSON
- Test filtrage par langue

---

## 📦 Phase 4 : Migration des Données

### 4.1 Script de Migration

**Fichier:** `scripts/migrate_i18n.py`

```python
"""
Script de migration de l'ancienne stack vers la nouvelle.
Usage: .venv\Scripts\python.exe scripts\migrate_i18n.py
"""

import json
from pathlib import Path

OLD_DIR = Path("backend/src/translations_old")  # Anciens fichiers
NEW_DIR = Path("backend/src/i18n/translations")  # Nouvelle structure

def migrate():
    """Migre les fichiers JSON vers nouvelle structure."""
    NEW_DIR.mkdir(parents=True, exist_ok=True)
    
    for old_file in OLD_DIR.glob("*.json"):
        lang = old_file.stem
        
        with open(old_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        # Convertir structure plate vers hiérarchique
        new_data = unflatten_dict(old_data)
        
        # Sauvegarder
        new_file = NEW_DIR / f"{lang}.json"
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated {lang}.json")

def unflatten_dict(flat_dict):
    """Convertit dict plat vers hiérarchique."""
    result = {}
    for key, value in flat_dict.items():
        keys = key.split('.')
        d = result
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
    return result

if __name__ == '__main__':
    migrate()
```

---

## ✅ Checklist d'Implémentation

### Backend
- [ ] Créer `backend/src/i18n/loader.py`
- [ ] Créer `backend/src/i18n/cache_manager.py` (optionnel)
- [ ] Créer `backend/src/routes/admin_i18n.py`
- [ ] Enregistrer Blueprint dans `app.py`
- [ ] Créer helper `t()` pour templates
- [ ] Migrer fichiers JSON (script)

### Frontend
- [ ] Créer `frontend/templates/admin/translations.html`
- [ ] Intégrer Tabulator.js (CDN ou local)
- [ ] Ajouter styles CSS personnalisés
- [ ] Implémenter upload fichier JSON
- [ ] Tester édition inline

### Tests
- [ ] Écrire tests unitaires loader
- [ ] Écrire tests API routes
- [ ] Tester fallback EN
- [ ] Tester interpolation variables
- [ ] Tester upload langue

### Documentation
- [ ] Mettre à jour `docs/i18n/README.md`
- [ ] Documenter conventions de nommage
- [ ] Ajouter guide admin (gestion traductions)
- [ ] Mettre à jour CHANGELOG

---

## 🔗 Références

- **Audit préalable:** `.github/prompts/i18n-audit-restructure.prompt.md`
- **Règles projet:** `.github/copilot-instructions.md`
- **Tabulator.js:** https://tabulator.info/
- **Exemple JSON hiérarchique:** `backend/src/i18n/translations/en.json`

---

**Exécution:**
```
AI: Exécute ce prompt en implémentant TOUTE la nouvelle stack.
Suis l'ordre des phases 1 → 2 → 3 → 4.
Valide avec tests à chaque étape.
```

