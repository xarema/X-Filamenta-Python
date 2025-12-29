<!--
Purpose: Summary of WSGI and multi-database adaptations
Description: Documents all changes made for cPanel/WSGI compatibility

File: WSGI_AND_MULTIDB_ADAPTATION.md | Repository: X-Filamenta-Python
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

Notes:
- Git history is the source of truth for authorship and change tracking.
-->

# Adaptation WSGI et Multi-BD — X-Filamenta-Python

Ce document résume les adaptations effectuées pour rendre X-Filamenta-Python compatible avec :

- ✅ **WSGI servers** (Gunicorn, uWSGI) pour cPanel, VPS, Docker
- ✅ **Plusieurs bases de données** (SQLite, MySQL, PostgreSQL)
- ✅ **Multiples environnements de déploiement** (dev, cPanel, VPS, Docker, production)

---

## 📋 Modifications principales

### 1. Configuration multi-BD (`backend/src/config.py`)

**Avant :**

- Seul SQLite supporté en développement
- Pas de configuration pour production
- Configuration fixe, non flexible

**Après :**

- Support complet de SQLite, MySQL et PostgreSQL
- Classe `Config` de base avec configuration commune
- Classes spécialisées pour chaque environnement :
  - `DevelopmentConfig` — SQLite, debug activé
  - `TestingConfig` — SQLite en mémoire
  - `ProductionConfig` — Configuration générique
  - `CPanelConfig` — Configuration cPanel-spécifique
  - `VPSConfig` — Configuration VPS-spécifique
  - `DockerConfig` — Configuration Docker-spécifique

**Fonction `_build_database_uri()` :**

```python
# Construit automatiquement l'URI de BD basé sur les variables d'env:
# 1. SQLALCHEMY_DATABASE_URI si défini (override)
# 2. DB_TYPE + DB_USER/PASSWORD/HOST/NAME si défini
# 3. SQLite par défaut

# Exemples supportés:
# SQLite:      sqlite:///./app.db
# MySQL:       mysql+pymysql://user:pass@host:3306/dbname
# PostgreSQL:  postgresql://user:pass@host:5432/dbname
```

**Configuration améliorée :**

```python
# Pool de connexion pour production
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,      # Vérifier connexions avant utilisation
    'pool_recycle': 3600,       # Recycler connexions après 1h
}

# Headers de sécurité
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True (en production)

# Déploiement
DEPLOYMENT_TARGET = 'cpanel'|'vps'|'docker'|'production'
```

---

### 2. Fichier WSGI (`backend/wsgi.py`)

**Nouveau fichier créé spécialement pour WSGI.**

**Caractéristiques :**

- Point d'entrée standard WSGI pour tous les serveurs
- Compatible avec Gunicorn, uWSGI, cPanel
- Charge automatiquement le fichier `.env`
- Initialise Flask avec la configuration appropriée

**Usage :**

```bash
# Gunicorn
gunicorn backend.wsgi:app

# uWSGI
uwsgi --http :5000 --wsgi-file backend/wsgi.py --callable app

# cPanel Setup Python App
# -> Application startup file: backend/wsgi.py
# -> Application entry point: app
```

---

### 3. Application Factory améliorée (`backend/src/app.py`)

**Avant :**

```python
def create_app() -> Flask:
    # Charge depuis os.getenv()
    # Config fixe
```

**Après :**

```python
def create_app(config=None) -> Flask:
    """
    Args:
        config: Configuration object (optionnel)
    """
    if config is None:
        config = get_config()  # Charge depuis FLASK_ENV

    app.config.from_object(config)  # Utilise le config object
    # ...
```

**Avantages :**

- Flexibilité complète pour WSGI servers
- Configuration par objet Python (meilleure pratique Flask)
- Testable et reproductible

---

### 4. Dépendances BD (`requirements.txt`)

**Ajoutées :**

```
PyMySQL>=1.1,<2.0        # MySQL driver
psycopg2-binary>=2.9,<3.0  # PostgreSQL driver
gunicorn>=21.0,<22.0     # WSGI server
```

**SQLAlchemy supporte automatiquement :**

- `sqlite://` — SQLite (natif)
- `mysql+pymysql://` — MySQL via PyMySQL
- `postgresql://` — PostgreSQL via psycopg2

---

### 5. Variables d'environnement `.env.example`

**Avant :**

- Minimal, SQLite seulement
- Pas de commentaires détaillés

**Après :**

- ✅ Support complet de tous les types de BD
- ✅ Exemples pour cPanel, VPS, Docker
- ✅ Commentaires détaillés
- ✅ Guide rapide de configuration
- ✅ Explications pour chaque variable

**Nouvelles variables :**

```bash
DB_TYPE=mysql|postgresql|sqlite
DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
SQLALCHEMY_DATABASE_URI  # Override explicite
DEPLOYMENT_TARGET=cpanel|vps|docker|production
APPLICATION_ROOT=/filamenta  # Pour cPanel
SECURE_SSL_REDIRECT=True|False
PREFERRED_URL_SCHEME=http|https
```

---

### 6. Documentation de déploiement

**Fichiers créés :**

| Fichier                          | Contenu                                        |
| -------------------------------- | ---------------------------------------------- |
| `DEPLOYMENT.md`                  | Guide général, comparaison des plateformes     |
| `DEPLOYMENT_CPANEL.md`           | Instructions complètes pour cPanel + WSGI      |
| `DEPLOYMENT_VPS.md`              | Instructions pour VPS Linux (Gunicorn + Nginx) |
| `DEPLOYMENT_DOCKER.md`           | Instructions Docker Compose                    |
| `WSGI_AND_MULTIDB_ADAPTATION.md` | Ce fichier                                     |

---

### 7. Configuration Docker

**Fichiers créés :**

| Fichier              | Contenu                                     |
| -------------------- | ------------------------------------------- |
| `Dockerfile`         | Image Python 3.12 + Gunicorn                |
| `docker-compose.yml` | Services : web, MySQL, Nginx, Certbot       |
| `nginx.conf`         | Configuration Nginx avec SSL, rate limiting |
| `.dockerignore`      | Fichiers à ignorer lors du build            |

**Avantages Docker :**

- Même image = dev, test, production (reproductibilité)
- Facile de changer de BD (MySQL/PostgreSQL)
- Support multi-base de données natif
- Scaling horizontal simple
- CI/CD automatisé

---

### 8. Scripts de déploiement

**Fichier créé :**

- `scripts/init_db.py` — Initialisation de BD pour tous les environnements

**Commandes disponibles :**

```bash
python scripts/init_db.py init      # Initialiser BD
python scripts/init_db.py reset     # Réinitialiser BD
python scripts/init_db.py drop      # Supprimer tables
python scripts/init_db.py create    # Créer tables seulement
python scripts/init_db.py seed      # Seed data (à implémenter)
```

---

## 🔄 Architecture WSGI

### Flux d'exécution

```
┌─────────────────────────────────────────────────────────────┐
│  Serveur web (nginx / Apache)                               │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP reverse proxy
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  WSGI Server (Gunicorn / uWSGI / cPanel)                    │
│  ├─ Charge backend/wsgi.py                                  │
│  ├─ Crée app = Flask instance                               │
│  └─ Transmet requêtes HTTP                                  │
└────────────────────┬────────────────────────────────────────┘
                     │ Interface WSGI standard
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Application Flask (backend/src/app.py)                     │
│  ├─ create_app(config) initialise                           │
│  ├─ Routes, modèles, logique métier                         │
│  └─ SQLAlchemy ORM                                          │
└────────────────────┬────────────────────────────────────────┘
                     │ Requêtes SQL
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Base de données (SQLite / MySQL / PostgreSQL)              │
│  ├─ Données utilisateur                                     │
│  ├─ Configuration de l'app                                  │
│  └─ Logs et métriques (optionnel)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Support des bases de données

### SQLite (Développement)

```bash
# Configuration
DB_TYPE=sqlite

# URI générée automatiquement
sqlite:///./instance/app.db

# Avantages
✅ Zéro configuration
✅ Pas de serveur externe
✅ Fichier unique

# Inconvénients
❌ Pas multi-utilisateur en production
❌ Performance limitée
❌ Pas de scaling
```

### MySQL (Recommandé pour production)

```bash
# Configuration
DB_TYPE=mysql
DB_USER=filamenta
DB_PASSWORD=secret
DB_HOST=localhost
DB_NAME=filamenta_db
DB_PORT=3306

# URI générée automatiquement
mysql+pymysql://filamenta:secret@localhost:3306/filamenta_db

# Avantages
✅ Compatible cPanel
✅ Multi-utilisateur
✅ Bonne performance
✅ Scaling possible

# Inconvénients
⚠️ Installation supplémentaire
⚠️ Maintenance requise
```

### PostgreSQL (Advanced)

```bash
# Configuration
DB_TYPE=postgresql
DB_USER=filamenta
DB_PASSWORD=secret
DB_HOST=localhost
DB_NAME=filamenta_db
DB_PORT=5432

# URI générée automatiquement
postgresql://filamenta:secret@localhost:5432/filamenta_db

# Avantages
✅ Plus robuste que MySQL
✅ Meilleures fonctionnalités
✅ Performance très bonne
✅ JSON natif

# Inconvénients
⚠️ Pas disponible sur tous les cPanel
⚠️ Plus complexe
```

---

## 🎯 Flux de déploiement par plateforme

### cPanel (WSGI via cPanel Setup Python App)

```
1. SSH vers cPanel
2. Cloner le dépôt
3. Créer venv + installer dépendances
4. Copier .env et configurer MySQL
5. Créer tables : python scripts/init_db.py init
6. cPanel Setup Python App :
   ├─ Python version: 3.12
   ├─ Application root: /home/user/apps/filamenta
   ├─ Application URL: /filamenta
   ├─ Startup file: backend/wsgi.py
   ├─ Entry point: app
7. cPanel démarre automatiquement avec Gunicorn
```

### VPS (WSGI via systemd + Nginx)

```
1. SSH vers VPS
2. Cloner le dépôt
3. Créer venv + installer dépendances
4. Copier .env et configurer MySQL/PostgreSQL
5. Créer tables : python scripts/init_db.py init
6. Créer service systemd
7. systemctl start filamenta
8. Configurer Nginx reverse proxy
9. SSL Let's Encrypt
```

### Docker (WSGI via Dockerfile)

```
1. Cloner le dépôt
2. Copier .env
3. docker-compose up -d
4. docker-compose exec web python scripts/init_db.py init
5. Accès via https://your-domain.com
```

---

## ✅ Checklist d'adaptation WSGI

- [x] Créer fichier WSGI (`backend/wsgi.py`)
- [x] Adapter `create_app()` pour accepter config
- [x] Créer `backend/src/config.py` avec classes multi-env
- [x] Implémenter `_build_database_uri()` pour multi-BD
- [x] Ajouter drivers BD (`PyMySQL`, `psycopg2`)
- [x] Ajouter `gunicorn` aux dépendances
- [x] Créer `.env.example` complet
- [x] Créer Dockerfile
- [x] Créer docker-compose.yml
- [x] Créer nginx.conf
- [x] Créer guide cPanel
- [x] Créer guide VPS
- [x] Créer guide Docker
- [x] Créer script d'initialisation BD
- [x] Tester chaque plateforme

---

## 🧪 Tests de validation

### Test local (development)

```bash
# SQLite
python -m backend.src

# Vérifier port 5000
curl http://localhost:5000
```

### Test WSGI

```bash
# Gunicorn
gunicorn --bind 127.0.0.1:8000 backend.wsgi:app

# Vérifier port 8000
curl http://localhost:8000
```

### Test Docker

```bash
# Build et run
docker-compose up -d

# Vérifier port 8000
curl http://localhost:8000
```

### Test multi-BD

```bash
# Change DB_TYPE dans .env
export DB_TYPE=mysql
python scripts/init_db.py init

# Ou PostgreSQL
export DB_TYPE=postgresql
python scripts/init_db.py init
```

---

## 📚 Ressources

- [WSGI PEP-3333](https://peps.python.org/pep-3333/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask WSGI Guide](https://flask.palletsprojects.com/en/latest/deploying/wsgi/)
- [SQLAlchemy Database Engines](https://docs.sqlalchemy.org/en/20/core/engines.html)
- [cPanel Python Applications](https://docs.cpanel.net/cPanel/Web-Services/Setup-Python-App/)

---

## 🎉 Résumé

X-Filamenta-Python est maintenant **prêt pour la RC (Release Candidate)** avec support complet pour :

✅ cPanel (WSGI + MySQL)
✅ VPS Linux (Gunicorn + Nginx + MySQL/PostgreSQL)
✅ Docker (Containerization complète)
✅ SQLite, MySQL, PostgreSQL

L'application peut être déployée sur n'importe quelle plateforme sans modification du code, juste en configurant les variables d'environnement !

🚀 **Prêt pour la production !**
