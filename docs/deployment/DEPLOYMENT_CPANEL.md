<!--
**Besoin d'aide ?** Consulte les logs ou ouvre une issue ! 🚀

---

- [SQLAlchemy Database URIs](https://docs.sqlalchemy.org/en/20/core/engines.html)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [cPanel Setup Python App Documentation](https://docs.cpanel.net/cPanel/Web-Services/Setup-Python-App/)

## 🔗 Ressources

---

- [ ] Domaine accessible via `/filamenta`
- [ ] Logs vérifiés pour les erreurs
- [ ] SSL/HTTPS activé
- [ ] cPanel Setup Python App configuré OU .htaccess mis à jour
- [ ] Application testée localement
- [ ] Script de démarrage `.sh` créé et exécutable
- [ ] Répertoires `run` et `logs` créés
- [ ] Gunicorn installé
- [ ] Tables de BD créées
- [ ] Base de données créée (MySQL/SQLite/PostgreSQL)
- [ ] Fichier `.env` configuré avec SECRET_KEY
- [ ] Dépendances installées
- [ ] Environnement virtuel créé et activé
- [ ] Python 3.12 installé et accessible

## 📝 Checklist de déploiement

---

```
# Dans .env : SECURE_SSL_REDIRECT=False
# Désactiver temporairement pour tester

curl -v https://your-domain.com/filamenta
# Vérifier le certificat SSL
```bash

### Erreur SSL/Certificate

```
               print('Database initialized!')"
               db.create_all(); \
           with app.app_context(): \
           app = create_app(); \
python -c "from backend.src.app import create_app, db; \
# Recréer les tables

mysql -h localhost -u your_db_user -p your_db_name
# Vérifier la connexion MySQL
```bash

### Erreur de base de données

```
chmod 777 ~/apps/filamenta/run
# Ajuster les permissions
```bash

### Erreur : "Permission denied" sur le socket

```
pip install -e .
source venv/bin/activate
# Vérifier que le package est installé
```bash

### Erreur : "Module not found"

## 🆘 Troubleshooting

---

```
netstat -tulpn | grep 5000
# Vérifier le port

ps aux | grep gunicorn
# Vérifier si Gunicorn tourne
```bash

### Vérifier l'état du processus

```
tail -f ~/apps/filamenta/logs/app.log
# Logs application

tail -f ~/apps/filamenta/logs/error.log
tail -f ~/apps/filamenta/logs/access.log
# Logs Gunicorn
```bash

### Voir les logs

## 📊 Monitoring

---

```
PREFERRED_URL_SCHEME=https
SECURE_SSL_REDIRECT=True
# Forcer HTTPS dans .env
```bash

### SSL/HTTPS

```
chmod 755 ~/apps/filamenta/backend
chmod 755 ~/apps/filamenta/venv
chmod 600 ~/apps/filamenta/.env
chmod 700 ~/apps/filamenta
# Restreindre les permissions
```bash

### Permissions des fichiers

Copier la clé générée dans `.env` sous `FLASK_SECRET_KEY`.

```
python -c "import secrets; print(secrets.token_hex(32))"
```bash

### Générer une clé secrète sûre

## 🔒 Sécurité

---

```
# https://your-domain.com/filamenta
# Accéder via votre domaine

curl -s http://localhost:5000 | head
# Tester localement avec curl

ls -la ~/apps/filamenta/run/app.sock
# Vérifier que le socket existe
```bash

### 13. Tester l'application

```
supervisord -c ~/apps/filamenta/supervisor.conf
# Démarrer avec supervisor

EOF
environment=PATH="/home/user/apps/filamenta/venv/bin",FLASK_ENV="cpanel"
stderr_logfile=/home/user/apps/filamenta/logs/supervisor_error.log
stdout_logfile=/home/user/apps/filamenta/logs/supervisor.log
autorestart=true
autostart=true
command=/home/user/apps/filamenta/venv/bin/gunicorn --workers 2 --timeout 60 --bind unix:run/app.sock backend.wsgi:app
directory=/home/user/apps/filamenta
[program:filamenta]
cat > ~/apps/filamenta/supervisor.conf << 'EOF'
# Créer la configuration

pip install supervisor
# Installer supervisor
```bash

### 12. Configurer le démarrage automatique (Option : Supervisor)

```
~/apps/filamenta/start.sh
# Lancer le script

chmod +x ~/apps/filamenta/start.sh
# Rendre exécutable

EOF
  backend.wsgi:app
  --pid run/app.pid \
  --error-logfile logs/error.log \
  --access-logfile logs/access.log \
  --bind unix:run/app.sock \
gunicorn --workers 2 --timeout 60 \
source venv/bin/activate
cd ~/apps/filamenta
#!/bin/bash
cat > ~/apps/filamenta/start.sh << 'EOF'
# Créer le script
```bash

### 11. Créer un script de démarrage (daemon)

```
# (voir section 12 ci-dessous)
# Option B : Via un script de démarrage

  backend.wsgi:app
  --error-logfile /home/user/apps/filamenta/logs/error.log \
  --access-logfile /home/user/apps/filamenta/logs/access.log \
  --bind unix:/home/user/apps/filamenta/run/app.sock \
gunicorn --workers 2 --timeout 60 \
# Option A : Lancer directement (pour tester)

source venv/bin/activate
# Activation de l'environnement
```bash

### 10. Démarrer l'application avec Gunicorn

```
ProxyPassReverse / unix:/home/user/apps/filamenta/run/app.sock|http://localhost/
# Proxy vers l'application WSGI

</IfModule>
    RewriteRule . index.html [L]
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^index\.html$ - [L]
    RewriteBase /filamenta/
    RewriteEngine On
<IfModule mod_rewrite.c>
# Fichier : public_html/filamenta/.htaccess
```apache

#### Option B : Configuration manuelle avec `.htaccess`

   - Une configuration pour le WSGI
   - Un fichier `.htaccess`
4. cPanel générera automatiquement :

   - **Application entry point** : `app`
   - **Application startup file** : `backend/wsgi.py`
   - **Application URL** : `/filamenta`
   - **Application root** : `/home/user/apps/filamenta`
   - **Python version** : 3.12
3. Configurer :
2. Cliquer sur **Create Application**
1. Accéder à **cPanel → Setup Python App**

#### Option A : Via cPanel Setup Python App

### 9. Configurer l'application WSGI dans cPanel

```
chmod 755 ~/apps/filamenta/logs
chmod 755 ~/apps/filamenta/run
mkdir -p ~/apps/filamenta/logs
mkdir -p ~/apps/filamenta/run
# cPanel utilise généralement des sockets Unix
```bash

### 8. Créer le répertoire pour les sockets WSGI

```
           with app.app_context(): db.create_all(); print('Database initialized!')"
python -c "from backend.src.app import create_app, db; app = create_app(); \
# Créer les tables

source venv/bin/activate
# Activer l'environnement
```bash

### 7. Initialiser la base de données

5. Copier les identifiants dans le `.env`
4. Assigner l'utilisateur à la base de données avec tous les privilèges
3. Créer un utilisateur : `your_user_db_user`
2. Créer une nouvelle base de données : `your_user_filamenta`
1. Accéder à **cPanel → Databases → MySQL Databases**

Via **cPanel phpMyAdmin** :

### 6. Créer la base de données (MySQL)

```
SQLALCHEMY_ECHO=False
# Logging

# DB_PORT=5432
# DB_NAME=your-db-name
# DB_HOST=localhost
# DB_PASSWORD=your-db-password
# DB_USER=your-db-user
# DB_TYPE=postgresql
# Option 3 : PostgreSQL (si disponible)

DB_PORT=3306
DB_NAME=your-cpanel-user_db_name
DB_HOST=localhost
DB_PASSWORD=your-database-password
DB_USER=your-cpanel-user_db_user
DB_TYPE=mysql
# Option 2 : MySQL (recommandé sur cPanel)

DB_TYPE=sqlite
# Option 1 : SQLite (simple mais moins performant en production)
# Database Configuration (choisis une option)

APPLICATION_ROOT=/filamenta
# Application path (pour cPanel)

SECURE_SSL_REDIRECT=True
FLASK_DEBUG=False
FLASK_SECRET_KEY=your-very-long-random-secret-key-here-change-me
FLASK_ENV=cpanel
# Flask Configuration
```bash

**Contenu du `.env` pour cPanel** :

```
nano .env
# Éditer le fichier .env avec ton éditeur préféré

cp .env.example .env
# Copier le fichier d'exemple
```bash

### 5. Configurer les variables d'environnement

```
# pip install uwsgi
# OU pour uWSGI
pip install gunicorn
# Installer les dépendances pour le serveur WSGI

pip install -e .
# Installer le package en mode éditable

pip install -r requirements.txt
# Installer les dépendances de base

pip install --upgrade pip setuptools wheel
# Mettre à jour pip
```bash

### 4. Installer les dépendances

```
which python
# Vérifier l'activation

source venv/bin/activate
# Activer l'environnement

python3.12 -m venv venv
# Créer l'environnement virtuel

python3.12 --version
# Vérifier la version de Python disponible
```bash

### 3. Créer l'environnement virtuel Python

```
# tar -xzf X-Filamenta-Python.tar.gz
# wget https://your-repo/X-Filamenta-Python.tar.gz
# Option B : Télécharger et extraire l'archive

git clone https://github.com/xarema/X-Filamenta-Python.git .
# Option A : Cloner depuis Git
```bash

### 2. Cloner le dépôt ou extraire les fichiers

```
cd apps/filamenta
mkdir -p apps/filamenta
# Créer un répertoire pour l'application

cd ~
# Accéder au répertoire home

ssh user@your-domain.com
# Connexion SSH
```bash

### 1. Connexion SSH et préparation

## 🚀 Installation étape par étape

---

- Domaine pointant vers le répertoire public_html
- Accès SSH ou Terminal dans cPanel
- cPanel avec **Python 3.12** disponible

## 📋 Prérequis

# Déploiement sur cPanel — X-Filamenta-Python

-->

- Git history is the source of truth for authorship and change tracking.
  Notes:

- Classification: Public
- Status: Draft
  Metadata:

Copyright (c) 2025 XAREMA. All rights reserved.

SPDX-License-Identifier: NOASSERTION
License: TBD

App version: 0.0.1-Alpha | File version: 0.0.1-Alpha
Distributed by: XAREMA | Coder: AleGabMar

Last modified (Git): TBD | Commit: TBD
Created: 2025-12-27T00:00:00+00:00
File: DEPLOYMENT_CPANEL.md | Repository: X-Filamenta-Python

Description: Instructions and configuration files for deploying X-Filamenta-Python on cPanel
Purpose: cPanel deployment configuration and setup guide
