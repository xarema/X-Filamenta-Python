# Database Configuration

**Project:** X-Filamenta-Python  
**Version:** 0.0.1-Alpha

---

## 📋 Vue d'ensemble

Ce projet supporte plusieurs bases de données grâce à SQLAlchemy:

- **SQLite** - Développement local
- **PostgreSQL** - Production (recommandé)
- **MySQL** - Alternative production

---

## 🗄️ SQLite (Development)

### Configuration

Par défaut, l'application utilise SQLite en développement.

**Fichier `.env`:**

```bash
DATABASE_URL=sqlite:///instance/app.db
# ou laisser vide pour utiliser la configuration par défaut
```

### Emplacement

```
X-Filamenta-Python/
└── instance/
    └── app.db
```

### Avantages

- ✅ Aucune installation requise
- ✅ Fichier unique, portable
- ✅ Parfait pour développement

### Limitations

- ⚠️ Pas de concurrent writes
- ⚠️ Performances limitées
- ⚠️ Pas pour production

---

## 🐘 PostgreSQL (Production)

### Installation

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**

```bash
brew install postgresql
brew services start postgresql
```

**Windows:**

- Télécharger depuis https://www.postgresql.org/download/windows/
- Installer PostgreSQL 15+

### Créer la base de données

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer user
CREATE USER filamenta_user WITH PASSWORD 'your_secure_password';

# Créer database
CREATE DATABASE filamenta_db OWNER filamenta_user;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE filamenta_db TO filamenta_user;

# Quit
\q
```

### Configuration

**Fichier `.env` (Production):**

```bash
DATABASE_URL=postgresql://filamenta_user:your_secure_password@localhost:5432/filamenta_db
```

**Format général:**

```
postgresql://username:password@host:port/database
```

### Tester la connexion

```bash
# Via psql
psql -U filamenta_user -d filamenta_db -h localhost

# Via Python
python -c "from backend.src.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Connected')"
```

---

## 🗺️ Migrations avec Alembic

### Créer une migration

```bash
# Auto-générer depuis les models
alembic revision --autogenerate -m "Description of changes"

# Créer une migration vide
alembic revision -m "Description"
```

### Appliquer les migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision>
```

### Voir l'historique

```bash
# Current version
alembic current

# History
alembic history

# Show SQL (dry-run)
alembic upgrade head --sql
```

---

## 🔄 Migration SQLite → PostgreSQL

### Exporter les données (SQLite)

```python
# scripts/export_data.py
from backend.src.app import create_app, db
from backend.src.models import User, UserPreferences, Content
import json

app = create_app()
with app.app_context():
    users = [u.to_dict(include_email=True) for u in User.query.all()]

    with open('data_export.json', 'w') as f:
        json.dump({'users': users}, f, indent=2)
```

### Importer dans PostgreSQL

1. Changer DATABASE_URL dans `.env`
2. Créer les tables: `alembic upgrade head`
3. Importer les données avec script personnalisé

---

## 🚀 Déploiement

### cPanel (Shared Hosting)

**Configuration:**

```python
# app.ini (WSGI)
[uwsgi]
module = wsgi:app
master = true
processes = 4
threads = 2

env = DATABASE_URL=postgresql://...
```

**Remote PostgreSQL:**

- Utiliser l'IP publique de la DB
- Ouvrir le port 5432 dans firewall
- SSL recommandé

### VPS/Cloud

**Docker:**

```yaml
# docker-compose.yml
services:
  web:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/filamenta
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=filamenta
      - POSTGRES_PASSWORD=password
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 🔐 Sécurité

### Bonnes pratiques

✅ **DO:**

- Utiliser variables d'environnement pour credentials
- SSL/TLS pour connexions DB
- Limiter les privilèges utilisateur DB
- Backups réguliers
- Changer les mots de passe par défaut

❌ **DON'T:**

- Hardcoder credentials dans le code
- Utiliser 'postgres' user en production
- Exposer DB directement sur Internet
- Stocker mots de passe en clair

### Exemple sécurisé

```bash
# .env (NEVER commit this!)
DATABASE_URL=postgresql://filamenta_prod:$(openssl rand -base64 32)@db.internal:5432/filamenta_prod?sslmode=require
```

---

## 🧪 Testing

### Test Database

Utiliser une DB en mémoire pour tests:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

Ou une DB de test dédiée:

```bash
DATABASE_URL=postgresql://test_user:test_pass@localhost:5432/test_db
```

---

## 📊 Monitoring

### Queries lentes

```python
# Enable SQLAlchemy echo
app.config['SQLALCHEMY_ECHO'] = True
```

### Connection pool

```python
# config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

---

## 🆘 Troubleshooting

### "Could not connect to server"

```bash
# Vérifier que PostgreSQL tourne
sudo systemctl status postgresql

# Vérifier pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

### "password authentication failed"

```bash
# Reset password
sudo -u postgres psql
ALTER USER filamenta_user WITH PASSWORD 'new_password';
```

### "database does not exist"

```bash
# Créer la DB
sudo -u postgres createdb filamenta_db -O filamenta_user
```

---

## 📚 Références

- SQLAlchemy: https://docs.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/

---

**Last Updated:** 2025-12-27  
**Status:** ✅ Production Ready
