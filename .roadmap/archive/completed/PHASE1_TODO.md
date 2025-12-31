<!--
Purpose: Immediate action items and quick tasks
Description: Todo list for Phase 1 - Infrastructure setup

File: TODO_PHASE1.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
-->

# TODO — PHASE 1 (Maintenant)

**Statut :** À faire  
**Durée estimée :** 2-3 jours  
**Priorité :** CRITIQUE

---

## ⭐ À faire AUJOURD'HUI

### Task 1: Vérifier que l'app démarre

**Durée :** 10 min

```bash
cd D:\xarema\X-Filamenta-Python
python -m backend.src
```

**Résultat attendu :**

```
Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**✓ Task 1 complétée ?** [ ]

---

### Task 2: Installer les dépendances

**Durée :** 5-10 min

```bash
pip install -r requirements.txt
npm install
```

**Vérification :**

```bash
python -c "import flask, sqlalchemy; print('✓ OK')"
npm --version
```

**✓ Task 2 complétée ?** [ ]

---

### Task 3: Configurer .env

**Durée :** 5 min

```bash
cd D:\xarema\X-Filamenta-Python
copy .env.example .env
```

**Fichier `.env` créé ?** [ ]

**Contenu à vérifier :**

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

**✓ Task 3 complétée ?** [ ]

---

### Task 4: Initialiser la base de données

**Durée :** 5 min

```bash
python scripts/init_db.py init
```

**Résultat attendu :**

```
✓ Database initialized successfully
✓ Tables created
```

**BD créée ?** [ ]

---

### Task 5: Tester les imports Python

**Durée :** 5 min

```bash
python -c "from backend.src.app import create_app; app = create_app(); print('✓ App créée')"
python -c "from backend.src.config import get_config; print(get_config('development'))"
```

**✓ Task 5 complétée ?** [ ]

---

## ⭐ À faire DEMAIN

### Task 6: Vérifier les chemins frontend

**Durée :** 10 min

```bash
# Vérifier CSS
ls frontend\css\tokens\variables.css
ls frontend\css\main.css

# Vérifier JS
ls frontend\js\plugins\tabulator.js
ls frontend\js\plugins\alpine-utils.js
ls frontend\js\plugins\htmx-utils.js

# Vérifier templates
ls frontend\templates\layouts\base.html
ls frontend\templates\components\navbar.html
ls frontend\templates\components\footer.html
ls frontend\templates\pages\index.html
```

**✓ Task 6 complétée ?** [ ]

---

### Task 7: Créer route GET /

**Durée :** 15 min

**Fichier :** `backend/src/routes/main.py`

```python
"""
Purpose: Main routes for public pages
Description: Flask Blueprint with main routes

File: backend/src/routes/main.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
"""

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage route"""
    return render_template('pages/index.html')

@main.route('/datagrid')
def datagrid():
    """DataGrid example route"""
    return render_template('pages/datagrid-example.html')
```

**Fichier créé ?** [ ]

---

### Task 8: Enregistrer le blueprint

**Durée :** 10 min

**Fichier :** `backend/src/app.py`

Ajouter après `app = Flask(...)` :

```python
# Enregistrer les blueprints
from backend.src.routes.main import main
app.register_blueprint(main)
```

**✓ Task 8 complétée ?** [ ]

---

### Task 9: Tester la route /

**Durée :** 10 min

```bash
# Dans un terminal
cd backend
flask run

# Dans un autre terminal
curl http://localhost:5000/
```

**Résultat attendu :** HTML de la page d'accueil

**✓ Task 9 complétée ?** [ ]

---

### Task 10: Créer route API /api/health

**Durée :** 15 min

**Fichier :** `backend/src/routes/api.py`

```python
"""
Purpose: API routes
Description: Flask Blueprint for API endpoints

File: backend/src/routes/api.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
"""

from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200
```

**Fichier créé ?** [ ]

---

### Task 11: Enregistrer blueprint API

**Durée :** 5 min

**Fichier :** `backend/src/app.py`

Ajouter :

```python
from backend.src.routes.api import api
app.register_blueprint(api)
```

**✓ Task 11 complétée ?** [ ]

---

### Task 12: Tester /api/health

**Durée :** 5 min

```bash
curl http://localhost:5000/api/health
```

**Résultat attendu :**

```json
{ "status": "ok", "message": "API is running" }
```

**✓ Task 12 complétée ?** [ ]

---

## ⭐ À faire JOUR 3

### Task 13: Créer templates d'erreur

**Durée :** 15 min

**Fichier :** `frontend/templates/errors/404.html`

```html
{% extends "layouts/base.html" %} {% block title %}404 - Introuvable{% endblock %} {%
block content %}
<div class="container py-5 text-center">
  <h1 class="display-1">404</h1>
  <p class="lead">Page introuvable</p>
  <a href="/" class="btn btn-primary">Retour à l'accueil</a>
</div>
{% endblock %}
```

**Fichier créé ?** [ ]

---

**Fichier :** `frontend/templates/errors/500.html`

```html
{% extends "layouts/base.html" %} {% block title %}500 - Erreur serveur{% endblock %} {%
block content %}
<div class="container py-5 text-center">
  <h1 class="display-1">500</h1>
  <p class="lead">Erreur serveur</p>
  <p class="text-muted">Contactez l'administrateur</p>
  <a href="/" class="btn btn-primary">Retour à l'accueil</a>
</div>
{% endblock %}
```

**Fichier créé ?** [ ]

---

### Task 14: Enregistrer error handlers

**Durée :** 10 min

**Fichier :** `backend/src/app.py`

```python
@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500
```

**✓ Task 14 complétée ?** [ ]

---

### Task 15: Tester les erreurs

**Durée :** 5 min

```bash
# Test 404
curl http://localhost:5000/notfound

# Test 500 (provoque intentionnellement une erreur)
# Ajouter une route de test temporaire
```

**✓ Task 15 complétée ?** [ ]

---

### Task 16: Vérifier le linting

**Durée :** 10 min

```bash
ruff check backend/
ruff format --check backend/
```

**Pas d'erreurs ?** [ ]

---

### Task 17: Vérifier les tests

**Durée :** 10 min

```bash
pytest backend/tests/ -v
```

**Tests passent ?** [ ]

---

### Task 18: Créer un test pour la route /

**Durée :** 15 min

**Fichier :** `backend/tests/test_routes.py`

```python
"""
Purpose: Test routes
Description: Tests for Flask routes

File: backend/tests/test_routes.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
"""

def test_index_route(client):
    """Test GET /"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'X-Filamenta' in response.data

def test_datagrid_route(client):
    """Test GET /datagrid"""
    response = client.get('/datagrid')
    assert response.status_code == 200
    assert b'table' in response.data.lower()

def test_api_health(client):
    """Test GET /api/health"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_404_error(client):
    """Test 404 error"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
```

**Fichier créé ?** [ ]

---

### Task 19: Lancer les tests

**Durée :** 5 min

```bash
pytest backend/tests/test_routes.py -v
```

**Tests passent ?** [ ]

---

### Task 20: Documenter la fin de PHASE 1

**Durée :** 5 min

Créer `PHASE1_COMPLETED.txt` :

```
✅ PHASE 1 — COMPLÉTÉE

Date: 2025-12-27
Durée totale: 2-3 jours

✓ App Flask démarre
✓ Routes principales / et /datagrid
✓ API /api/health
✓ Templates intégrés
✓ BD SQLite créée
✓ Tests passent
✓ Code clean (ruff OK)

Prêt pour PHASE 2 !
```

**✓ Task 20 complétée ?** [ ]

---

## 📋 Checklist rapide PHASE 1

Copie-colle et coche au fur et à mesure :

```
PHASE 1 — Infrastructure & Setup
==================================

Jour 1:
  [ ] Task 1 - App démarre
  [ ] Task 2 - Dépendances installées
  [ ] Task 3 - .env configuré
  [ ] Task 4 - BD initialisée
  [ ] Task 5 - Imports OK

Jour 2:
  [ ] Task 6 - Chemins frontend vérifiés
  [ ] Task 7 - Route / créée
  [ ] Task 8 - Blueprint enregistré
  [ ] Task 9 - Route / testée
  [ ] Task 10 - Route /api/health créée
  [ ] Task 11 - Blueprint API enregistré
  [ ] Task 12 - /api/health testée

Jour 3:
  [ ] Task 13 - Templates d'erreur créés
  [ ] Task 14 - Error handlers enregistrés
  [ ] Task 15 - Erreurs testées
  [ ] Task 16 - Linting OK
  [ ] Task 17 - Tests passent
  [ ] Task 18 - Nouveaux tests créés
  [ ] Task 19 - Tous les tests passent
  [ ] Task 20 - PHASE 1 documentée

PHASE 1 COMPLÉTÉE ✅
```

---

## 🎯 Commande de démarrage

**Tu peux toujours revenir à cette commande :**

```bash
cd D:\xarema\X-Filamenta-Python
pip install -r requirements.txt
python scripts/init_db.py init
cd backend
flask run
```

Puis ouvrir : http://localhost:5000

---

## 🚀 Prêt ?

**C'est parti pour la PHASE 1 !** 🎉

Coche les tasks au fur et à mesure et partage ta progression !
