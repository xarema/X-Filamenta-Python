<!--
Purpose: RC Release Notes and Quick Start
Description: Overview of X-Filamenta-Python RC version with WSGI/multi-DB support

File: RC_RELEASE_NOTES.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Release Candidate
- Classification: Public

Notes:
- Git history is the source of truth for authorship and change tracking.
-->

# 🚀 X-Filamenta-Python — Release Candidate (RC)

**Version:** 0.0.1-Alpha RC  
**Date:** 2025-12-27  
**Status:** Ready for Testing

---

## ✨ Quoi de neuf dans cette RC ?

### 🎯 Support WSGI complet

- ✅ Compatible **Gunicorn** (recommandé)
- ✅ Compatible **uWSGI**
- ✅ Compatible **cPanel** Setup Python App
- ✅ Point d'entrée WSGI standard : `backend/wsgi.py`

### 📊 Support multi-bases de données

- ✅ **SQLite** (développement, défaut)
- ✅ **MySQL** (production recommandée)
- ✅ **PostgreSQL** (advanced, optionnel)
- ✅ Configuration automatique via `.env`

### 🌍 Déploiement multi-plateforme

- ✅ **cPanel** → [Guide complet](DEPLOYMENT_CPANEL.md)
- ✅ **VPS/Linux** → [Guide complet](DEPLOYMENT_VPS.md)
- ✅ **Docker** → [Guide complet](DEPLOYMENT_DOCKER.md)
- ✅ **Development local** → [Guide rapide](QUICKSTART.md)

### 📚 Documentation complète

- ✅ [DEPLOYMENT.md](DEPLOYMENT.md) — Comparaison des plateformes
- ✅ [WSGI_AND_MULTIDB_ADAPTATION.md](WSGI_AND_MULTIDB_ADAPTATION.md) — Architecture technique
- ✅ [DEPLOYMENT_CPANEL.md](DEPLOYMENT_CPANEL.md) — Guide cPanel étape par étape
- ✅ [DEPLOYMENT_VPS.md](DEPLOYMENT_VPS.md) — Guide VPS/Linux étape par étape
- ✅ [DEPLOYMENT_DOCKER.md](DEPLOYMENT_DOCKER.md) — Guide Docker étape par étape

---

## 🏃 Démarrage rapide

### Pour développement local

```bash
# 1. Clone et setup
git clone <repo>
cd X-Filamenta-Python
python -m venv venv
source venv/bin/activate  # ou .venv\Scripts\Activate.ps1 sur Windows

# 2. Installer
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# 3. Lancer
python -m backend.src
# Accès: http://localhost:5000
```

### Pour Docker

```bash
# 1. Préparer
git clone <repo>
cd X-Filamenta-Python
cp .env.example .env

# 2. Démarrer
docker-compose up -d

# 3. Initialiser BD
docker-compose exec web python scripts/init_db.py init

# Accès: https://localhost
```

### Pour cPanel

```bash
# 1. SSH
ssh user@domain.com

# 2. Setup (voir DEPLOYMENT_CPANEL.md pour détails)
cd ~/apps/filamenta
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# 3. Configurer via cPanel UI
# Setup Python App → backend/wsgi.py:app

# Accès: https://domain.com/filamenta
```

---

## 📋 Configuration requise

### Prérequis minimaux

- **Python:** 3.12
- **RAM:** 512 MB minimum
- **Disque:** 100 MB minimum

### Par plateforme

| Plateforme | Python        | BD               | WSGI      | Reverse Proxy |
| ---------- | ------------- | ---------------- | --------- | ------------- |
| **Local**  | 3.12          | SQLite           | Flask dev | None          |
| **cPanel** | 3.12 (cPanel) | MySQL            | Gunicorn  | Apache        |
| **VPS**    | 3.12          | MySQL/PostgreSQL | Gunicorn  | Nginx         |
| **Docker** | 3.12 (image)  | MySQL            | Gunicorn  | Nginx         |

---

## 🎯 Choisir votre plateforme

### 🏠 cPanel — Le plus simple

**Recommandé si :**

- Tu as un hébergement cPanel
- Tu veux zéro maintenance
- Tu ne besoin pas de scaling

**Avantages :** Setup graphique, SSL AutoSSL, facile  
**Temps de setup :** ~30 min  
→ [Voir le guide cPanel](DEPLOYMENT_CPANEL.md)

### 🖥️ VPS/Linux — Le plus flexible

**Recommandé si :**

- Tu veux full contrôle
- Tu vas scaler
- Tu as exp. Linux

**Avantages :** Pleine liberté, excellent perf, scaling  
**Temps de setup :** ~1h  
→ [Voir le guide VPS](DEPLOYMENT_VPS.md)

### 🐳 Docker — Le plus moderne

**Recommandé si :**

- Tu veux déployer partout
- Tu aimes containers
- Tu veux CI/CD

**Avantages :** Même image dev=prod, scaling facile  
**Temps de setup :** ~15 min  
→ [Voir le guide Docker](DEPLOYMENT_DOCKER.md)

---

## 🔧 Configuration `.env`

### Minimal (development avec SQLite)

```bash
FLASK_ENV=development
FLASK_SECRET_KEY=dev-key-change-in-production
FLASK_DEBUG=False
DB_TYPE=sqlite
```

### cPanel (MySQL)

```bash
FLASK_ENV=cpanel
FLASK_SECRET_KEY=votre-clé-secrète-longue
DB_TYPE=mysql
DB_USER=cpanel_user
DB_PASSWORD=votre-password
DB_HOST=localhost
DB_NAME=cpanel_db
APPLICATION_ROOT=/filamenta
SECURE_SSL_REDIRECT=True
```

### VPS (MySQL ou PostgreSQL)

```bash
FLASK_ENV=vps
FLASK_SECRET_KEY=votre-clé-secrète-longue
DB_TYPE=mysql  # ou postgresql
DB_USER=filamenta
DB_PASSWORD=votre-password
DB_HOST=localhost
DB_NAME=filamenta_db
SECURE_SSL_REDIRECT=True
PREFERRED_URL_SCHEME=https
```

### Docker

```bash
FLASK_ENV=docker
FLASK_SECRET_KEY=votre-clé-secrète-longue
DB_TYPE=mysql
DB_USER=filamenta
DB_PASSWORD=votre-password
DB_HOST=db
DB_NAME=filamenta_db
MYSQL_ROOT_PASSWORD=root-password
```

---

## 📊 Features principales

### Backend

- ✅ Flask 3.x + SQLAlchemy 3.x
- ✅ WSGI-ready (Gunicorn, uWSGI, cPanel)
- ✅ Multi-BD (SQLite, MySQL, PostgreSQL)
- ✅ Configuration multi-env
- ✅ Logging & monitoring prêt

### Frontend

- ✅ HTMX pour interactions
- ✅ Bootstrap 5 pour design
- ✅ CSS variables (tokens)
- ✅ Static files optimisés

### DevOps

- ✅ Docker Compose complet
- ✅ Nginx configuration incluse
- ✅ SSL support (Let's Encrypt)
- ✅ Scripts d'init BD

### Tests & Quality

- ✅ pytest pour tests
- ✅ Ruff pour linting
- ✅ mypy pour type checking
- ✅ Prettier pour formatage

---

## 🚀 Déploiement étape par étape

### 1. Choisir plateforme

- cPanel ? → [DEPLOYMENT_CPANEL.md](DEPLOYMENT_CPANEL.md)
- VPS ? → [DEPLOYMENT_VPS.md](DEPLOYMENT_VPS.md)
- Docker ? → [DEPLOYMENT_DOCKER.md](DEPLOYMENT_DOCKER.md)

### 2. Cloner et configurer

```bash
git clone <repo>
cp .env.example .env
nano .env  # Adapter selon plateforme
```

### 3. Installer dépendances

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Initialiser BD

```bash
python scripts/init_db.py init
```

### 5. Démarrer

- Local: `python -m backend.src`
- cPanel: Utiliser Setup Python App
- VPS: `systemctl start filamenta`
- Docker: `docker-compose up -d`

### 6. Accéder

- Local: http://localhost:5000
- cPanel: https://domain.com/filamenta
- VPS: https://domain.com
- Docker: https://localhost

---

## 🔒 Sécurité

### Avant TOUT déploiement

- [ ] Générer une FLASK_SECRET_KEY unique
- [ ] Utiliser HTTPS/SSL
- [ ] Ne pas commiter `.env`
- [ ] Utiliser une BD externe (MySQL/PostgreSQL, pas SQLite)
- [ ] Configurer un firewall

### Générer une clé secrète

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copier la sortie dans `.env` sous `FLASK_SECRET_KEY=...`

---

## 📈 Performance

### Recommandations

| Élément          | Recommandation                                  |
| ---------------- | ----------------------------------------------- |
| **BD**           | MySQL/PostgreSQL en prod (SQLite dev seulement) |
| **WSGI workers** | 2-4 (selon CPU cores)                           |
| **Timeout**      | 60s (par défaut)                                |
| **Cache**        | Redis (optionnel, futur)                        |
| **CDN**          | CloudFlare (optionnel, static files)            |

---

## 📝 Changelog

### Version 0.0.1-Alpha RC (2025-12-27)

#### Ajouté

- ✨ Support WSGI complet (Gunicorn, uWSGI, cPanel)
- ✨ Multi-base de données (SQLite, MySQL, PostgreSQL)
- ✨ Configuration multi-environnements
- ✨ Docker Compose complet
- ✨ Documentation de déploiement pour cPanel, VPS, Docker
- ✨ Script d'initialisation BD
- ✨ nginx.conf pour reverse proxy

#### Modifié

- 🔧 `backend/src/app.py` — Accepte config object
- 🔧 `backend/src/config.py` — Complet avec classes multi-env
- 🔧 `.env.example` — Support complet

#### Documentation

- 📚 `DEPLOYMENT.md` — Guide comparatif
- 📚 `DEPLOYMENT_CPANEL.md` — Guide cPanel
- 📚 `DEPLOYMENT_VPS.md` — Guide VPS
- 📚 `DEPLOYMENT_DOCKER.md` — Guide Docker
- 📚 `WSGI_AND_MULTIDB_ADAPTATION.md` — Architecture technique

---

## 🆘 Support & Aide

### Documentation

- [Guide de déploiement général](DEPLOYMENT.md)
- [Guide rapide development](QUICKSTART.md)
- [Guide cPanel](DEPLOYMENT_CPANEL.md)
- [Guide VPS](DEPLOYMENT_VPS.md)
- [Guide Docker](DEPLOYMENT_DOCKER.md)

### Problèmes courants

**Application ne démarre pas**
→ Vérifier les logs + FLASK_SECRET_KEY défini

**BD non accessible**
→ Vérifier DB_TYPE + credentials + création tables

**HTTPS ne marche pas**
→ Vérifier certificat SSL + redirects HTTP→HTTPS

**Port déjà utilisé**
→ Changer le port ou tuer le processus existant

→ Voir les guides spécifiques pour plus de détails

---

## 🎯 Prochaines étapes

### Phase RC (Cette version)

- [ ] Tester sur cPanel réel
- [ ] Tester sur VPS réel
- [ ] Tester Docker en production
- [ ] Collecte feedback

### Phase 1.0.0

- [ ] Corrections bugs
- [ ] Optimisations
- [ ] Sécurité audit
- [ ] Version stable

---

## 📊 Statistiques

- **Lignes de code Python:** ~500
- **Fichiers de configuration:** 5 (pyproject.toml, package.json, etc.)
- **Documentation:** 2000+ lignes
- **Tests:** 1 smoke test + suite test ready
- **Plateforme:** 4 (Local, cPanel, VPS, Docker)
- **BD supportées:** 3 (SQLite, MySQL, PostgreSQL)

---

## 📞 Contact & Feedback

- **Email:** filamenta@xarema.com
- **Problèmes:** Issues sur GitHub
- **Suggestions:** Discussions sur GitHub

---

## 📄 Licence

Voir [LICENSE.md](LICENSE.md) (TBD)

---

## 🙏 Remerciements

Merci d'avoir choisi X-Filamenta-Python !

Cette version RC représente des mois de développement pour rendre l'application flexible, deployable et maintenable sur plusieurs plateformes.

**Prêt à déployer ? Choisir votre plateforme et commencez !** 🚀

---

**Dernière mise à jour:** 2025-12-27  
**Version:** 0.0.1-Alpha RC  
**Statut:** ✅ Ready for Testing
