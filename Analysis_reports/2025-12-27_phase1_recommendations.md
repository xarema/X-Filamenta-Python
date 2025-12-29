# Recommandations PHASE 1 - Actions Prioritaires

**Date:** 2025-12-27  
**Priority Level:** HAUTE  
**Timeline:** À faire avant PHASE 2  

---

## 🔴 CRITIQUES (0 jours - Avant tout déploiement)

### 1. Implémenter Flask-WTF pour CSRF Protection

**Sévérité:** CRITIQUE  
**Effort:** 30 min  
**Impact:** Sécurité

```bash
py -m pip install Flask-WTF
```

**Modifications app.py:**

```python
from flask_wtf.csrf import CSRFProtect

# Dans create_app()
csrf = CSRFProtect()

# Après db.init_app(app)
csrf.init_app(app)
```

**Tests:** 
```bash
py -m pytest backend/tests/test_routes.py::test_api_health -v
```

---

## 🟡 MAJEURS (Avant PHASE 2)

### 2. Corriger Line Length (Ruff Warning)

**Fichier:** `backend/src/config.py` ligne 118  
**Effort:** 5 min

```python
# Avant
PREFERRED_URL_SCHEME = "https" if os.getenv("PREFERRED_URL_SCHEME") == "https" else "http"

# Après
preferred_scheme_env = os.getenv("PREFERRED_URL_SCHEME")
PREFERRED_URL_SCHEME = "https" if preferred_scheme_env == "https" else "http"
```

**Validation:**
```bash
py -m ruff check backend/src --select=E501
```

---

### 3. Ajouter Logging dans Error Handlers

**Fichier:** `backend/src/app.py` (error handlers)  
**Effort:** 15 min

```python
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with logging"""
    app.logger.warning(f"404 Error: {request.path}")
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors with logging"""
    app.logger.error(f"500 Error: {error}", exc_info=True)
    return render_template('errors/500.html'), 500
```

**À ajouter à imports:**
```python
from flask import request
```

---

### 4. Corriger test_404_error

**Fichier:** `backend/tests/test_routes.py`  
**Issue:** Test échoue car template path mal résolu  
**Effort:** 15 min

**Fix:**
```python
def test_404_error(client):
    """Test 404 error handler"""
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404
    # Template doit être valide en test aussi
    assert b'404' in response.data or b'Introuvable' in response.data
```

---

### 5. Créer backend/README.md

**Contenu attendu:**
- Architecture du projet
- Structure des fichiers
- Dépendances principales
- Instructions de développement
- API endpoints

**Effort:** 30 min

---

## 🟢 RECOMMANDÉS (PHASE 2)

### 6. Créer Context Processors Module

**Créer:** `backend/src/context_processors.py`

```python
"""
Purpose: Jinja2 context processors
Description: Provides context variables to all templates
"""

from typing import Dict, Any, Callable

def inject_user() -> Dict[str, Any]:
    """Inject current_user into templates"""
    class MockUser:
        username = "Guest"
        is_authenticated = False
        is_admin = False
    
    return {'current_user': MockUser()}

def inject_csrf_token() -> Dict[str, Callable]:
    """Inject csrf_token function"""
    return {'csrf_token': lambda: 'mock-csrf-token'}

def register(app) -> None:
    """Register all context processors"""
    app.context_processor(inject_user)
    app.context_processor(inject_csrf_token)
```

**Utilisation dans app.py:**
```python
from backend.src.context_processors import register
# ...
register(app)
```

---

### 7. Ajouter Type Hints (mypy)

**Fichiers à mettre à jour:**
- `backend/src/routes/main.py`
- `backend/src/routes/api.py`
- `backend/src/app.py`

**Exemple:**
```python
from typing import Dict, Any, Tuple

def index() -> str:
    """Homepage route"""
    return render_template('pages/index.html')

def health() -> Tuple[Dict[str, Any], int]:
    """API health endpoint"""
    return jsonify({...}), 200
```

**Validation:**
```bash
py -m mypy backend/src --explicit-package-bases
```

---

### 8. Créer Constants Module

**Créer:** `backend/src/constants.py`

```python
"""Application constants"""

# Routes
TEMPLATE_INDEX = 'pages/index.html'
TEMPLATE_DATAGRID = 'pages/datagrid-example.html'
TEMPLATE_404 = 'errors/404.html'
TEMPLATE_500 = 'errors/500.html'

# API
API_PREFIX = '/api'
API_HEALTH_ROUTE = '/health'

# Messages
MSG_OK = 'OK'
MSG_API_RUNNING = 'API is running'
```

**Utilisation:**
```python
from backend.src.constants import TEMPLATE_INDEX

def index():
    return render_template(TEMPLATE_INDEX)
```

---

## 🔒 SÉCURITÉ AMÉLIORÉE (PHASE 2-3)

### 9. Rate Limiting

```bash
py -m pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@api.route('/health')
@limiter.limit("100 per hour")
def health():
    ...
```

---

### 10. Security Headers

```bash
py -m pip install Flask-Talisman
```

```python
from flask_talisman import Talisman

Talisman(app)
```

---

## ✅ CHECKLIST IMMÉDIATE

À faire maintenant (avant fin du jour):

- [ ] Installer Flask-WTF
- [ ] Modifier app.py pour CSRFProtect
- [ ] Corriger config.py line 118
- [ ] Ajouter logging dans error handlers
- [ ] Tester: `py -m pytest backend/tests/ --no-cov -v`

À faire demain (PHASE 2 kick-off):

- [ ] Corriger test_404_error
- [ ] Créer backend/README.md
- [ ] Créer context_processors.py
- [ ] Ajouter type hints (mypy)
- [ ] Créer constants.py

---

## 🚀 COMMANDE DE TEST COMPLET

```powershell
# 1. Installer dépendances de test
py -m pip install Flask-WTF --quiet

# 2. Linting
py -m ruff check backend/src

# 3. Type checking
py -m mypy backend/src --explicit-package-bases --ignore-missing-imports

# 4. Tests
py -m pytest backend/tests/ -v --no-cov

# 5. Démarrer l'app
py -m flask --app backend.src.app run --debug
```

---

## 📊 Matrice Effort/Impact

| Recommandation | Effort | Impact | Priorité |
|---|---|---|---|
| Flask-WTF | 30 min | CRITIQUE | 🔴 NOW |
| Fix line length | 5 min | Qualité | 🔴 NOW |
| Logging errors | 15 min | Observabilité | 🟡 Semaine |
| Fix test_404 | 15 min | Tests | 🟡 Semaine |
| backend/README | 30 min | Documentation | 🟡 Semaine |
| Context processors | 1h | Architecture | 🟢 Optionnel |
| Type hints | 2h | Qualité | 🟢 Optionnel |
| Constants module | 1h | Maintenance | 🟢 Optionnel |
| Rate limiting | 1h | Sécurité | 🟢 PHASE 3 |
| Security headers | 30 min | Sécurité | 🟢 PHASE 3 |

---

## 📞 Questions?

Pour chaque recommandation, consulter:
- `Analysis_reports/2025-12-27_phase1_code_audit.md` (détails)
- `docs/CHANGELOG_GUIDE.md` (format des changements)
- `.github/copilot-instructions.md` (conventions)

