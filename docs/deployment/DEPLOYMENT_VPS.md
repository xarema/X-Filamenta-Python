<!--
Purpose: VPS/Linux deployment configuration and setup guide
Description: Instructions for deploying X-Filamenta-Python on VPS or Linux servers

File: DEPLOYMENT_VPS.md | Repository: X-Filamenta-Python
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

# Déploiement sur VPS/Linux — X-Filamenta-Python

## 📋 Prérequis

- **OS** : Ubuntu 20.04 LTS+ / Debian 11+ / CentOS 8+ / Rocky Linux 8+
- **Python** : 3.12
- **Utilisateur** : Accès sudo ou root
- **Ports** : 8000+ disponibles (ou access via reverse proxy)
- **Dépendances système** : python3-dev, gcc, make

---

## 🚀 Installation étape par étape

### 1. Mise à jour du système

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3.12-dev \
  git curl nginx supervisor

# CentOS/Rocky
sudo yum update -y
sudo yum install -y python3.12 python3.12-devel git curl nginx supervisor
```

### 2. Créer un utilisateur dédié

```bash
# Créer l'utilisateur
sudo useradd -m -s /bin/bash filamenta

# Donner les permissions sudo (optionnel)
sudo usermod -aG sudo filamenta

# Basculer vers l'utilisateur
sudo su - filamenta
```

### 3. Cloner le dépôt et préparer l'application

```bash
# Depuis l'utilisateur filamenta
cd ~

# Cloner le dépôt
git clone https://github.com/xarema/X-Filamenta-Python.git
cd X-Filamenta-Python

# Créer l'environnement virtuel
python3.12 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .
pip install gunicorn
```

### 4. Configurer les variables d'environnement

```bash
# Créer le fichier .env
cp .env.example .env

# Éditer avec votre configuration
nano .env
```

**Exemple de `.env` pour VPS** :

```bash
FLASK_ENV=vps
FLASK_SECRET_KEY=your-very-long-random-secret-key-here
FLASK_DEBUG=False

# Database (MySQL recommandé)
DB_TYPE=mysql
DB_USER=filamenta_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_NAME=filamenta_db
DB_PORT=3306

# Security
SECURE_SSL_REDIRECT=True
PREFERRED_URL_SCHEME=https

# Application
APPLICATION_ROOT=/
```

### 5. Créer la base de données

#### Option A : MySQL

```bash
# Se connecter à MySQL
sudo mysql -u root -p

# Créer la base et l'utilisateur
CREATE DATABASE filamenta_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'filamenta_user'@'localhost' IDENTIFIED BY 'strong-password-here';
GRANT ALL PRIVILEGES ON filamenta_db.* TO 'filamenta_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Option B : PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base et l'utilisateur
CREATE DATABASE filamenta_db;
CREATE USER filamenta_user WITH PASSWORD 'strong-password-here';
ALTER ROLE filamenta_user SET client_encoding TO 'utf8';
ALTER ROLE filamenta_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE filamenta_db TO filamenta_user;
\q
```

### 6. Initialiser la base de données de l'application

```bash
# En tant qu'utilisateur filamenta
cd ~/X-Filamenta-Python
source venv/bin/activate

python -c "from backend.src.app import create_app, db; \
           from backend.src.config import get_config; \
           config = get_config('vps'); \
           app = create_app(config=config); \
           with app.app_context(): \
               db.create_all(); \
               print('Database initialized!')"
```

### 7. Configurer Gunicorn

```bash
# Créer le répertoire pour les logs
mkdir -p ~/logs

# Créer un service systemd pour Gunicorn
sudo tee /etc/systemd/system/filamenta.service > /dev/null << 'EOF'
[Unit]
Description=X-Filamenta-Python WSGI Server
After=network.target

[Service]
User=filamenta
WorkingDirectory=/home/filamenta/X-Filamenta-Python
ExecStart=/home/filamenta/X-Filamenta-Python/venv/bin/gunicorn \
    --workers 4 \
    --timeout 60 \
    --bind unix:/home/filamenta/X-Filamenta-Python/filamenta.sock \
    --access-logfile /home/filamenta/logs/access.log \
    --error-logfile /home/filamenta/logs/error.log \
    backend.wsgi:app

Environment="FLASK_ENV=vps"
Environment="PATH=/home/filamenta/X-Filamenta-Python/venv/bin"

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable filamenta
sudo systemctl start filamenta

# Vérifier le statut
sudo systemctl status filamenta
```

### 8. Configurer Nginx

```bash
# Créer la configuration Nginx
sudo tee /etc/nginx/sites-available/filamenta > /dev/null << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;

    # Redirection HTTP vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # Certificat SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Configuration SSL sécurisée
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Logs
    access_log /var/log/nginx/filamenta_access.log;
    error_log /var/log/nginx/filamenta_error.log;

    # Limite de taille des uploads
    client_max_body_size 10M;

    # Proxy vers Gunicorn
    location / {
        proxy_pass http://unix:/home/filamenta/X-Filamenta-Python/filamenta.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Servir les fichiers statiques
    location /static/ {
        alias /home/filamenta/X-Filamenta-Python/frontend/static/;
        expires 30d;
    }
}
EOF

# Activer le site
sudo ln -s /etc/nginx/sites-available/filamenta /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 9. Configurer Let's Encrypt (SSL gratuit)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Générer le certificat
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# Auto-renouvellement
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### 10. Configurer les logs et monitoring

```bash
# Créer la structure de logs
mkdir -p ~/logs
chmod 755 ~/logs

# Configuration de logrotate
sudo tee /etc/logrotate.d/filamenta > /dev/null << 'EOF'
/home/filamenta/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 filamenta filamenta
    sharedscripts
}
EOF
```

---

## 📊 Monitoring et maintenance

### Vérifier l'état de l'application

```bash
# Statut Gunicorn
sudo systemctl status filamenta

# Logs temps réel
sudo journalctl -u filamenta -f

# Logs Nginx
sudo tail -f /var/log/nginx/filamenta_access.log
sudo tail -f /var/log/nginx/filamenta_error.log
```

### Redémarrer l'application

```bash
sudo systemctl restart filamenta
sudo systemctl reload nginx
```

### Mettre à jour l'application

```bash
cd ~/X-Filamenta-Python
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
sudo systemctl restart filamenta
```

---

## 🆘 Troubleshooting

### Erreur de connexion socket

```bash
# Vérifier les permissions du socket
ls -la ~/X-Filamenta-Python/filamenta.sock

# Recréer le socket
sudo systemctl restart filamenta
```

### Erreur base de données

```bash
# Vérifier la connexion
mysql -u filamenta_user -p filamenta_db

# Recréer les tables
cd ~/X-Filamenta-Python
source venv/bin/activate
python -c "from backend.src.app import create_app, db; \
           app = create_app(); \
           with app.app_context(): \
               db.drop_all(); \
               db.create_all(); \
               print('Database reset!')"
```

### Nginx 502 Bad Gateway

```bash
# Vérifier Gunicorn
sudo systemctl status filamenta

# Redémarrer
sudo systemctl restart filamenta

# Vérifier les logs
sudo journalctl -u filamenta -n 50
```

---

## 📝 Checklist de déploiement

- [ ] Système mis à jour
- [ ] Python 3.12 installé
- [ ] Utilisateur `filamenta` créé
- [ ] Dépôt cloné
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] `.env` configuré avec SECRET_KEY
- [ ] Base de données créée
- [ ] Tables initialisées
- [ ] Service systemd créé et activé
- [ ] Nginx configuré
- [ ] Certificat SSL installé
- [ ] Application accessible via HTTPS
- [ ] Logs configurés
- [ ] Monitoring en place

---

## 🔗 Ressources

- [Gunicorn Deployment](https://docs.gunicorn.org/en/latest/deploy.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt/Certbot](https://certbot.eff.org/)
- [Flask Deployment Best Practices](https://flask.palletsprojects.com/en/latest/deploying/)
- [systemd User Services](https://freedesktop.org/wiki/Software/systemd/)

---

**Prêt pour le déploiement ? Commence par l'étape 1 !** 🚀
