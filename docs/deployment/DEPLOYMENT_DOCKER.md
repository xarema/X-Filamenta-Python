<!--
Purpose: Docker deployment configuration and setup guide
Description: Instructions for deploying X-Filamenta-Python using Docker containers

File: DEPLOYMENT_DOCKER.md | Repository: X-Filamenta-Python
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

# Déploiement avec Docker — X-Filamenta-Python

## 📋 Prérequis

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Port 80 et 443** disponibles (ou NAT/reverse proxy)
- **10 GB d'espace disque** minimum

---

## 🚀 Installation rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/xarema/X-Filamenta-Python.git
cd X-Filamenta-Python
```

### 2. Configurer l'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer la configuration
nano .env
```

**Configuration minimale pour Docker** :

```bash
# Flask
FLASK_ENV=docker
FLASK_SECRET_KEY=your-very-long-random-secret-key-here-change-me

# Database (MySQL par défaut)
DB_TYPE=mysql
DB_USER=filamenta
DB_PASSWORD=your-strong-password
DB_HOST=db
DB_NAME=filamenta_db

# MySQL
MYSQL_ROOT_PASSWORD=root-password-change-me

# Security
SECURE_SSL_REDIRECT=True
PREFERRED_URL_SCHEME=https
```

### 3. Démarrer les conteneurs

```bash
# Démarrer en arrière-plan
docker-compose up -d

# Ou en mode foreground (pour voir les logs)
docker-compose up

# Vérifier le statut
docker-compose ps
```

### 4. Initialiser la base de données

```bash
# Exécuter les migrations (si disponibles)
docker-compose exec web python -c "from backend.src.app import create_app, db; \
                                    app = create_app(); \
                                    with app.app_context(): \
                                        db.create_all(); \
                                        print('Database initialized!')"
```

### 5. Accéder à l'application

```
https://your-domain.com
http://localhost:8000 (local, sans SSL)
```

---

## 🔧 Configuration avancée

### Utiliser PostgreSQL au lieu de MySQL

Modifier `docker-compose.yml` :

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: filamenta_db
      POSTGRES_USER: filamenta
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

Mettre à jour `.env` :

```bash
DB_TYPE=postgresql
DB_USER=filamenta
DB_PASSWORD=your-password
DB_HOST=db
DB_NAME=filamenta_db
DB_PORT=5432
```

### Ajouter Redis pour le caching

Décommenter dans `docker-compose.yml` :

```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - filamenta-network
```

Puis dans l'application Flask :

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis:6379/0'})
```

### Configurer HTTPS avec Let's Encrypt

```bash
# Créer les répertoires
mkdir -p certbot/conf certbot/www

# Générer le certificat
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d your-domain.com -d www.your-domain.com --email your-email@example.com

# Editer nginx.conf avec votre domaine
nano nginx.conf

# Redémarrer Nginx
docker-compose restart nginx

# Vérifier le certificat
docker-compose logs certbot
```

---

## 📊 Gestion des conteneurs

### Voir les logs

```bash
# Tous les logs
docker-compose logs -f

# Logs spécifiques
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### Exécuter des commandes dans un conteneur

```bash
# Shell interactif
docker-compose exec web bash

# Commande directe
docker-compose exec web python -c "print('Hello')"

# Accès à MySQL
docker-compose exec db mysql -u filamenta -p filamenta_db
```

### Redémarrer les services

```bash
# Tous les services
docker-compose restart

# Service spécifique
docker-compose restart web
docker-compose restart db

# Recharger la configuration
docker-compose restart nginx
```

### Arrêter les services

```bash
# Arrêt gracieux
docker-compose stop

# Arrêt forcé
docker-compose kill

# Arrêt et suppression des conteneurs
docker-compose down

# Arrêt avec suppression des volumes
docker-compose down -v
```

---

## 📦 Gestion des données

### Backup de la base de données

```bash
# MySQL
docker-compose exec db mysqldump -u filamenta -p filamenta_db > backup.sql

# PostgreSQL
docker-compose exec db pg_dump -U filamenta filamenta_db > backup.sql
```

### Restore d'une sauvegarde

```bash
# MySQL
docker-compose exec -T db mysql -u filamenta -p filamenta_db < backup.sql

# PostgreSQL
docker-compose exec -T db psql -U filamenta filamenta_db < backup.sql
```

### Volumes persistants

Les données sont sauvegardées dans :

- `mysql-data` volume (pour MySQL)
- `postgres-data` volume (pour PostgreSQL)

Pour voir les volumes :

```bash
docker volume ls
docker volume inspect filamenta_mysql-data
```

---

## 🚀 Déploiement en production

### 1. Utiliser un registre Docker privé

```bash
# Construire l'image
docker build -t registry.example.com/filamenta:latest .

# Pousser l'image
docker push registry.example.com/filamenta:latest

# Utiliser dans docker-compose.yml
services:
  web:
    image: registry.example.com/filamenta:latest
```

### 2. Configurer le reverse proxy (Nginx en dehors de Docker)

```nginx
upstream filamenta {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://filamenta;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Mettre à jour l'application

```bash
# Pousser les changements
git push

# Tirer la dernière version
git pull

# Reconstruire et redémarrer
docker-compose up -d --build
```

---

## 🔒 Sécurité

### Générer une clé secrète

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Limiter l'accès aux ports

```bash
# Ne pas exposer les ports de la BD au monde
# docker-compose.yml : Ne pas publier les ports de `db`

# Utiliser un firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Audit de sécurité

```bash
# Vérifier les images pour les CVE
docker scan filamenta:latest

# Vérifier les logs
docker-compose logs | grep -i error
docker-compose logs | grep -i warning
```

---

## 🆘 Troubleshooting

### Conteneur qui crash

```bash
# Voir les logs
docker-compose logs web

# Redémarrer
docker-compose restart web

# Reconstruire
docker-compose up -d --build
```

### Erreur de connexion à la base de données

```bash
# Vérifier que la BD est prête
docker-compose logs db

# Vérifier la connectivité
docker-compose exec web mysql -h db -u filamenta -p filamenta_db

# Réinitialiser la BD
docker-compose down -v
docker-compose up -d
docker-compose exec web python -c "from backend.src.app import create_app, db; \
                                    app = create_app(); \
                                    with app.app_context(): \
                                        db.create_all()"
```

### Port déjà utilisé

```bash
# Changer le port dans docker-compose.yml
# ports:
#   - "9000:8000"  # au lieu de 8000:8000

# Ou libérer le port
lsof -i :8000
kill -9 <PID>
```

### Problème de permissions

```bash
# Vérifier les permissions
docker-compose exec web ls -la

# Reconstruire (le Dockerfile crée un utilisateur `appuser`)
docker-compose up -d --build
```

---

## 📊 Performance et scaling

### Augmenter les workers Gunicorn

Modifier `Dockerfile` :

```dockerfile
CMD ["gunicorn", "--workers", "8", "--timeout", "60", "backend.wsgi:app"]
```

### Ajouter un load balancer

Utiliser Nginx ou HAProxy devant les conteneurs :

```yaml
services:
  web1:
    build: .
    networks:
      - filamenta-network

  web2:
    build: .
    networks:
      - filamenta-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    upstream: web1:8000
      web2:8000
```

---

## 📝 Checklist de déploiement Docker

- [ ] Docker et Docker Compose installés
- [ ] Dépôt cloné
- [ ] `.env` configuré avec SECRET_KEY
- [ ] Conteneurs démarrés (`docker-compose up -d`)
- [ ] Base de données initialisée
- [ ] Application accessible sur le port 8000
- [ ] Nginx configuré avec domaine
- [ ] Certificat SSL installé (Let's Encrypt)
- [ ] HTTPS fonctionnel
- [ ] Logs vérifiés pour les erreurs
- [ ] Backup de la BD configuré
- [ ] Monitoring en place

---

## 🔗 Ressources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gunicorn Docker Best Practices](https://docs.gunicorn.org/en/stable/deploy.html)
- [NGINX in Docker](https://hub.docker.com/_/nginx)
- [MySQL in Docker](https://hub.docker.com/_/mysql)
- [PostgreSQL in Docker](https://hub.docker.com/_/postgres)

---

**Docker simplifie le déploiement ! Commencez par les étapes rapides.** 🐳🚀
