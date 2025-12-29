# Backend - X-Filamenta-Python

**Version:** 0.0.1-Alpha  
**Language:** Python 3.12  
**Framework:** Flask 3.x  

---

## 📋 Vue d'ensemble

Backend Flask pour X-Filamenta-Python avec:
- ✅ App factory pattern
- ✅ Blueprints modulaires (main, api)
- ✅ SQLAlchemy ORM
- ✅ CSRF Protection (Flask-WTF)
- ✅ Error handling personnalisé
- ✅ Tests pytest

---

## 📁 Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── __main__.py          (Entry point)
│   ├── app.py               (App factory)
│   ├── config.py            (Configuration)
│   ├── models/              (Data models)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          (Public routes: /, /datagrid)
│   │   └── api.py           (API routes: /api/health)
│   ├── services/            (Business logic)
│   └── utils/               (Helper functions)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          (pytest fixtures)
│   ├── test_smoke.py        (Basic tests)
│   └── test_routes.py       (Routes tests)
│
└── wsgi.py                  (WSGI entry for production)
```

---

## 🚀 Démarrage

### Prérequis
- Python 3.12+
- pip (gestionnaire de paquets)

### Installation

```bash
# 1. Installer dépendances
pip install -r requirements.txt

# 2. Configurer .env
cp .env.example .env
# Éditer .env si nécessaire

# 3. Initialiser BD
python scripts/init_db.py init
```

### Démarrage Application

**Mode développement:**
```bash
cd backend
flask run
# Ou directement:
python -m flask --app src.app run --debug
```

**Mode production (WSGI):**
```bash
gunicorn -w 4 backend.wsgi:app
```

L'application sera disponible sur: **http://localhost:5000**

---

## 🛣️ Routes

### Routes Publiques (main.py)

| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET | Homepage (index.html) |
| `/datagrid` | GET | Exemple DataGrid (datagrid-example.html) |

### Routes API (api.py)

| Route | Méthode | Description | Response |
|-------|---------|-------------|----------|
| `/api/health` | GET | Health check | `{"status": "ok", "message": "API is running", "version": "0.0.1-Alpha"}` |

### Error Handlers

| Code | Template |
|------|----------|
| 404 | `errors/404.html` |
| 500 | `errors/500.html` |

---

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest -v

# Sans coverage
pytest -v --no-cov

# Test spécifique
pytest backend/tests/test_routes.py::test_api_health -v

# Avec coverage
pytest --cov=backend/src --cov-report=term-missing
```

### Statistiques (Phase 1)
- **Total tests:** 5
- **Passing:** 5/5 ✅
- **Coverage:** API health route: 100%

---

## 🔒 Sécurité

### Implémenté

✅ **CSRF Protection** (Flask-WTF)
- Tokens CSRF automatiques sur tous les formulaires
- Validation côté serveur

✅ **Template Security**
- Jinja2 auto-escaping (XSS protection)
- Pas de `|safe` sur contenu non validé

✅ **Input Validation**
- SQLAlchemy parameterized queries (SQL injection prevention)
- Pas de eval() ou exec()

✅ **Configuration**
- Secrets depuis variables d'environnement
- Session cookies sécurisés (HTTPS en prod)

### À Ajouter (PHASE 2+)

⏳ **Rate Limiting**
- Flask-Limiter pour limiter requêtes API

⏳ **Authentication & Authorization**
- Login/logout, JWT tokens (PHASE 4)
- Permissions par rôle

⏳ **Security Headers**
- Flask-Talisman (HSTS, CSP, etc.)

---

## 📊 Configuration

### Environnement (`.env`)

```bash
# Development / Production
FLASK_ENV=development
FLASK_DEBUG=True

# Secret key (CHANGE en production!)
SECRET_KEY=dev-secret-key-change-in-production

# Database
DATABASE_URL=sqlite:///instance/app.db
# ou: postgresql://user:password@localhost/db_name

# HTTPS (production)
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### Fichier Complet

Voir: `backend/src/config.py`

---

## 📝 Logging

### Configuration

Logging configuré en INFO par défaut:
```
Format: %(asctime)s [%(levelname)s] %(name)s: %(message)s
```

### Utilisation

```python
from flask import current_app

# Dans une route/fonction
current_app.logger.info("Message info")
current_app.logger.warning("Warning message")
current_app.logger.error("Error message")
```

---

## 🗄️ Base de Données

### Type

- **Dev:** SQLite (`instance/app.db`)
- **Prod:** PostgreSQL (recommandé)

### Initialisation

```bash
python scripts/init_db.py init
```

Crée les tables automatiquement via SQLAlchemy.

### Migrations (Future)

Alembic peut être intégré pour versionner le schéma.

---

## 🔧 Linting & Type Checking

### Linting (Ruff)

```bash
# Vérifier
py -m ruff check backend/src

# Formatter (auto-fix)
py -m ruff format backend/src
```

### Type Checking (mypy)

```bash
py -m mypy backend/src --explicit-package-bases --ignore-missing-imports
```

---

## 📚 Dépendances Principales

| Package | Version | Usage |
|---------|---------|-------|
| Flask | 3.x | Web framework |
| SQLAlchemy | 2.x | ORM |
| Flask-SQLAlchemy | Latest | Flask + SQLAlchemy |
| Flask-WTF | Latest | CSRF protection |
| python-dotenv | Latest | Env vars |
| Gunicorn | Latest | WSGI server (prod) |

Voir: `requirements.txt`

---

## 🚨 Troubleshooting

### Port déjà utilisé

```bash
# Changez le port
flask run --port 5001
```

### ImportError sur blueprints

Vérifiez que les blueprints sont enregistrés dans `app.py`:
```python
from backend.src.routes.main import main
from backend.src.routes.api import api

app.register_blueprint(main)
app.register_blueprint(api)
```

### Template not found

Vérifiez que `template_folder` est configuré dans `create_app()`:
```python
app = Flask(
    __name__,
    template_folder=template_folder,
    static_folder=static_folder
)
```

---

## 📖 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
- Projet: [README.md](../../README.md)
- Copilot Rules: [.github/copilot-instructions.md](../../.github/copilot-instructions.md)

---

## 📞 Questions?

Consultez:
1. `backend/src/app.py` - App factory
2. `backend/src/routes/` - Routes et blueprints
3. `backend/src/config.py` - Configuration
4. Tests: `backend/tests/`

---

**Last Updated:** 2025-12-27  
**Status:** ✅ PHASE 1 COMPLETE

