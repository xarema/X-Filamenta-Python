---
Purpose: Complete documentation reference
Description: Exhaustive documentation of all features, APIs, and modules

File: docs/REFERENCE.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:20:00+01:00
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

# 📚 Documentation complète — X-Filamenta-Python

**Référence exhaustive de toutes les fonctionnalités, APIs et modules.**

---

## 🗺️ Sections

### 🚀 Pour démarrer rapidement
- **[00_START_HERE.md](00_START_HERE.md)** — Entry point principal (lire d'abord !)
- **[guides/01_QUICKSTART.md](guides/01_QUICKSTART.md)** — Installation en 5 minutes
- **[guides/README.md](guides/README.md)** — Index des guides

### 📋 Fonctionnalités
- **[features/README.md](features/README.md)** — Inventaire complet
- **[features/authentication.md](features/authentication.md)** — Login & 2FA
- **[features/wizard-installation.md](features/wizard-installation.md)** — Wizard
- **[features/internationalization.md](features/internationalization.md)** — i18n
- **[features/database.md](features/database.md)** — Support multi-BD

### 🚀 Déploiement
- **[deployment/README.md](deployment/README.md)** — Comparaison des approches
- **[deployment/01_CPANEL.md](deployment/01_CPANEL.md)** — cPanel
- **[deployment/02_VPS_LINUX.md](deployment/02_VPS_LINUX.md)** — VPS/Linux
- **[deployment/03_DOCKER.md](deployment/03_DOCKER.md)** — Docker
- **[deployment/04_LOCAL_DEVELOPMENT.md](deployment/04_LOCAL_DEVELOPMENT.md)** — Dev local

### 🏗️ Architecture
- **[architecture/README.md](architecture/README.md)** — Index architecture
- **[architecture/overview.md](architecture/overview.md)** — Vue d'ensemble
- **[architecture/backend.md](architecture/backend.md)** — Backend (Flask)
- **[architecture/frontend.md](architecture/frontend.md)** — Frontend (HTMX + Bootstrap)
- **[architecture/database.md](architecture/database.md)** — BD & ORM
- **[architecture/wsgi_multidb.md](architecture/wsgi_multidb.md)** — WSGI & multi-BD

### 🔒 Sécurité
- **[security/README.md](security/README.md)** — Index sécurité
- **[security/best-practices.md](security/best-practices.md)** — Bonnes pratiques
- **[security/csrf-protection.md](security/csrf-protection.md)** — CSRF
- **[security/2fa.md](security/2fa.md)** — 2FA TOTP
- **[security/secrets-management.md](security/secrets-management.md)** — Secrets

### 🤝 Contribution
- **[contributing/README.md](contributing/README.md)** — Commencer à contribuer
- **[contributing/code-standards.md](contributing/code-standards.md)** — Standards de code
- **[contributing/testing.md](contributing/testing.md)** — Tests
- **[contributing/release-process.md](contributing/release-process.md)** — Release

### ❓ Troubleshooting
- **[troubleshooting/README.md](troubleshooting/README.md)** — Index dépannage
- **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)** — Problèmes courants
- **[troubleshooting/faq.md](troubleshooting/faq.md)** — FAQ

### 📦 API
- **[api/README.md](api/README.md)** — Index API
- **[api/endpoints.md](api/endpoints.md)** — Endpoints disponibles
- **[api/authentication.md](api/authentication.md)** — API Auth
- **[api/errors.md](api/errors.md)** — Codes d'erreur

---

## 📁 Structure des fichiers

```
X-Filamenta-Python/
├── backend/
│   ├── src/
│   │   ├── routes/        # Blueprints Flask
│   │   ├── services/      # Logique métier
│   │   ├── models/        # ORM SQLAlchemy
│   │   ├── i18n/          # Traductions
│   │   ├── utils/         # Utilitaires
│   │   ├── app.py         # Factory app
│   │   ├── config.py      # Configuration
│   │   └── extensions.py  # Extensions
│   └── tests/             # Tests
│
├── frontend/
│   ├── templates/         # Jinja2 templates
│   │   ├── layouts/       # Base layouts
│   │   ├── pages/         # Page templates
│   │   └── components/    # Reusable components
│   └── static/            # CSS, JS, images
│       ├── css/
│       ├── js/
│       └── images/
│
├── docs/                  # Documentation (ce dossier)
│   ├── guides/
│   ├── features/
│   ├── deployment/
│   ├── architecture/
│   ├── security/
│   ├── contributing/
│   ├── troubleshooting/
│   ├── api/
│   ├── screenshots/
│   └── archives/
│
├── migrations/            # Alembic migrations
├── scripts/               # Scripts utilitaires
├── config/                # Configuration serveur
└── instance/              # Runtime data (BD, logs)
```

---

## 🎯 Guides rapides

### Je veux...

#### ...installer & tester localement
→ [guides/01_QUICKSTART.md](guides/01_QUICKSTART.md)

#### ...déployer en production
→ [deployment/README.md](deployment/README.md) → choisir plateforme

#### ...comprendre l'architecture
→ [architecture/overview.md](architecture/overview.md)

#### ...ajouter une fonctionnalité
→ [guides/04_DEVELOPMENT.md](guides/04_DEVELOPMENT.md) + [contributing/README.md](contributing/README.md)

#### ...sécuriser l'appli
→ [security/best-practices.md](security/best-practices.md)

#### ...résoudre un problème
→ [troubleshooting/common-issues.md](troubleshooting/common-issues.md)

#### ...contribuer au projet
→ [contributing/README.md](contributing/README.md)

---

## 🔧 Commandes utiles

### Développement
```bash
# Installation
pip install -r requirements.txt && npm install

# Linter
ruff check .

# Formater
ruff format . && npm run fmt

# Type checking
mypy backend/src/

# Tests
pytest backend/tests/ -v

# Serveur
python run_prod.py
```

### Déploiement
```bash
# Docker
docker-compose up -d

# Alembic (migrations)
alembic upgrade head

# Sauvegarde BD
mysqldump -u user -p database > backup.sql
```

---

## 📞 Support & Contact

- **Bugs** : Créer une issue GitHub
- **Questions** : Consultez la FAQ
- **Contributions** : Voir guide de contribution

---

## 📜 License & Copyright

**License :** AGPL-3.0-or-later  
**Copyright :** © 2025 XAREMA. All rights reserved.  
**Maintainers :** AleGabMar

Voir [../LICENSE](../LICENSE) pour plus de détails.

---

**→ Utilisez [00_START_HERE.md](00_START_HERE.md) pour naviguer facilement.**

