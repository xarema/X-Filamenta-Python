---
Purpose: Database configuration and multi-database support
Description: SQLite, MySQL, and PostgreSQL setup and management

File: docs/features/database.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:10:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public

---

# 💾 Base de données

**Support multi-BD : SQLite, MySQL, PostgreSQL.**

---

## 🎯 Vue d'ensemble

L'application supporte **3 systèmes de bases de données** :

| BD | Cas d'usage | Performance | Maintenance |
|----|---|---|---|
| **SQLite** | Dev, tests, déploiement simple | Basse (mono-process) | Très faible |
| **MySQL** | Production, sites moyens | Bonne | Moyen |
| **PostgreSQL** | Production, sites complexes | Excellente | Moyen-haut |

---

## 📋 Configuration

### Via le wizard

L'assistant d'installation propose les 3 options :

**Onglet SQLite :**
```
Nom fichier : app.db
```
→ Crée/utilise `instance/app.db`

**Onglet MySQL :**
```
Host : localhost
Port : 3306
Nom : filamenta
User : root
Password : ***
```

**Onglet PostgreSQL :**
```
Host : localhost
Port : 5432
Nom : filamenta
User : postgres
Password : ***
```

### Via .env

```bash
# SQLite
SQLALCHEMY_DATABASE_URI=sqlite:///D:/path/to/instance/app.db

# MySQL
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:pass@host:3306/dbname

# PostgreSQL
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:pass@host:5432/dbname
```

---

## 🗄️ SQLite (Développement)

### Avantages
✅ Zéro configuration  
✅ Fichier unique  
✅ Sauvegarde facile  
✅ Parfait pour dev/tests  

### Limitations
❌ Un seul utilisateur à la fois  
❌ Pas de vraie authentification  
❌ Performance limitée  

### Utilisation

```bash
# Fichier créé à : instance/app.db
# Sauvegarde : cp instance/app.db instance/app.db.backup

# Restaurer :
cp instance/app.db.backup instance/app.db
```

---

## 🐬 MySQL (Production légère)

### Installation

```bash
# macOS
brew install mysql

# Ubuntu/Debian
sudo apt-get install mysql-server

# Windows
# Télécharger depuis mysql.com
```

### Création BD

```sql
CREATE DATABASE filamenta CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'filamenta'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON filamenta.* TO 'filamenta'@'localhost';
FLUSH PRIVILEGES;
```

### Connection string

```
mysql+pymysql://filamenta:strong_password@localhost:3306/filamenta
```

### Backup/Restore

```bash
# Backup
mysqldump -u filamenta -p filamenta > backup.sql

# Restore
mysql -u filamenta -p filamenta < backup.sql
```

---

## 🐘 PostgreSQL (Production robuste)

### Installation

```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Télécharger depuis postgresql.org
```

### Création BD

```sql
CREATE DATABASE filamenta ENCODING 'UTF8';
CREATE USER filamenta WITH PASSWORD 'strong_password';
ALTER ROLE filamenta SET client_encoding TO 'utf8';
ALTER ROLE filamenta SET default_transaction_isolation TO 'read committed';
ALTER ROLE filamenta SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE filamenta TO filamenta;
```

### Connection string

```
postgresql+psycopg2://filamenta:strong_password@localhost:5432/filamenta
```

### Backup/Restore

```bash
# Backup
pg_dump -U filamenta -d filamenta -f backup.sql

# Restore
psql -U filamenta -d filamenta -f backup.sql

# Backup bináire (plus rapide)
pg_dump -U filamenta -d filamenta -Fc -f backup.dump
pg_restore -U filamenta -d filamenta -Fc backup.dump
```

---

## 🔄 Migrations

Utilise **Alembic** pour les migrations de schéma :

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Add new table"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1

# Voir l'historique
alembic history
```

---

## 📊 Tables principales

```sql
-- Utilisateurs
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historique admin
CREATE TABLE admin_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT,
    action VARCHAR(255),
    target_type VARCHAR(50),
    target_id INT,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id)
);

-- Préférences utilisateur
CREATE TABLE user_preferences (
    user_id INT PRIMARY KEY,
    language VARCHAR(10),
    theme VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🔐 Sécurité

✅ **Credentials sécurisés** : Stockés dans `.env`, jamais en dur  
✅ **Connexions chiffrées** : SSL/TLS recommandé en prod  
✅ **Permissions restrictives** : Utilisateur dédié par BD  
✅ **Backups sécurisés** : Stockés hors du serveur web  

---

## 🧪 Tester la connexion

```python
from backend.src.extensions import db
from flask import current_app

with current_app.app_context():
    try:
        db.session.execute("SELECT 1")
        print("✓ Connexion OK")
    except Exception as e:
        print(f"✗ Erreur : {e}")
```

---

## 📚 Ressources

- **Guides de déploiement** → [../deployment/README.md](../deployment/README.md)
- **Architecture** → [../architecture/database.md](../architecture/database.md)
- **Troubleshooting** → [../troubleshooting/common-issues.md](../troubleshooting/common-issues.md)

---

**→ Choisir la BD appropriée selon vos besoins et infrastructure.**

