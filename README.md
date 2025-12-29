# X-Filamenta-Python

**Version:** 0.0.1-Alpha RC  
**License:** AGPL-3.0-or-later  
**Distributed by:** XAREMA  
**Coder:** AleGabMar

---

## 🎉 Version RC (Release Candidate)

Cette version est prête pour le déploiement sur :
- ✅ **cPanel** (WSGI via Setup Python App)
- ✅ **VPS/Linux** (Gunicorn + Nginx)
- ✅ **Docker** (Compose complet)
- ✅ **Local** (Development)

Avec support de **SQLite, MySQL et PostgreSQL**.

---
## 📚 Documentation

**La documentation complète se trouve dans [docs/](docs/)**

### 🚀 COMMENCEZ ICI

- 📖 **[docs/00_START_HERE.md](docs/00_START_HERE.md)** — ⭐ Lire en premier !
- ⚡ **[docs/guides/01_QUICKSTART.md](docs/guides/01_QUICKSTART.md)** — Installation rapide (5 min)
- 📚 **[docs/REFERENCE.md](docs/REFERENCE.md)** — Référence complète

### 🌍 Déploiement

| Plateforme | Guide | Durée |
|-----------|-------|-------|
| **cPanel** | [docs/deployment/01_CPANEL.md](docs/deployment/01_CPANEL.md) | 30 min |
| **VPS/Linux** | [docs/deployment/02_VPS_LINUX.md](docs/deployment/02_VPS_LINUX.md) | 1h |
| **Docker** | [docs/deployment/03_DOCKER.md](docs/deployment/03_DOCKER.md) | 15 min |

### 📖 Documentation complète

- **Guides** → [docs/guides/](docs/guides/)
- **Fonctionnalités** → [docs/features/](docs/features/)
- **Architecture** → [docs/architecture/](docs/architecture/)
- **Sécurité** → [docs/security/](docs/security/)
- **Contribution** → [docs/contributing/](docs/contributing/)
- **Dépannage** → [docs/troubleshooting/](docs/troubleshooting/)

---

## Description

Application web Filamenta développée avec :
- **Backend:** Flask (Python 3.12+)
- **Frontend:** HTMX + Bootstrap 5
- **Outillage:** Ruff, Prettier, ESLint, Stylelint, pytest, mypy

Ce template suit les règles de développement définies dans `.github/copilot-instructions.md`.

---

## Structure du projet

```
X-Filamenta-Python/
├── backend/
│   ├── src/                  # Code source Flask
│   │   ├── models/           # Modèles de données (ORM)
│   │   ├── routes/           # Blueprints (routes)
│   │   ├── services/         # Logique métier
│   │   ├── utils/            # Utilitaires
│   │   ├── __init__.py
│   │   ├── __main__.py       # Point d'entrée (python -m backend.src)
│   │   └── app.py            # Application factory
│   └── tests/                # Tests pytest
│       ├── unit/             # Tests unitaires
│       ├── integration/      # Tests d'intégration
│       ├── fixtures/         # Fixtures pytest
│       └── conftest.py
├── frontend/
│   ├── static/               # Assets statiques
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── fonts/
│   └── templates/            # Modèles Jinja2
│       ├── layouts/          # Layouts
│       ├── components/       # Composants
│       └── pages/            # Pages
├── config/                   # Fichiers de configuration
├── docs/                     # Documentation
│   ├── api/
│   ├── architecture/
│   └── guides/
├── Analysis_reports/         # Rapports d'analyse
├── .github/
│   └── copilot-instructions.md  # Règles de développement
├── scripts/                  # Scripts utilitaires
├── pyproject.toml            # Configuration Python
├── package.json              # Configuration Node.js
├── requirements.txt          # Dépendances production
├── requirements-dev.txt      # Dépendances développement
└── README.md
```

---

## Prérequis

- **Python:** 3.12+
- **Node.js:** 18+
- **Git:** pour pre-commit hooks

---

## Installation

### Windows PowerShell

```powershell
# Créer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer les dépendances Python
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Installer le package en mode éditable
pip install -e .

# Installer les outils frontend
npm install

# Installer les hooks pre-commit
pre-commit install
```

### Linux/macOS (bash/zsh)

```bash
# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate

# Installer les dépendances Python
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Installer le package en mode éditable
pip install -e .

# Installer les outils frontend
npm install

# Installer les hooks pre-commit
pre-commit install
```

---

## Commandes utiles

### Formatage et linting

```bash
# Python
make fmt-py          # Formater avec Ruff
make lint-py         # Linter avec Ruff + mypy

# Frontend
make fmt-front       # Formater avec Prettier
make lint-front      # Linter avec ESLint + Stylelint

# Tout
make fmt             # Formater Python + Frontend
make lint            # Linter Python + Frontend
```

### Tests

```bash
make test-py         # Exécuter pytest avec couverture
pytest -v            # Exécuter pytest en mode verbeux
```

### Développement

```bash
# Démarrer le serveur de développement
python -m backend.src        # Via Python
npm run dev:py               # Via npm

# Application accessible sur http://127.0.0.1:5000
```

### Production (Windows local)

Pour tester le mode production avec Waitress (similaire à un serveur de prod) :

```powershell
# Utiliser le script de confort
.\run_prod.ps1

# OU manuellement via le venv
.\.venv\Scripts\python.exe run_prod.py
```

---

## Variables d'environnement

Créez un fichier `.env` à la racine (copier depuis `.env.example` si disponible) :

```bash
# Flask
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True              # Ne jamais utiliser en production !

# Serveur
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

**⚠️ Sécurité:**
- Ne **jamais** committer de fichier `.env` avec des secrets réels
- Utiliser des variables d'environnement en production
- Générer des clés secrètes fortes (`python -c "import secrets; print(secrets.token_hex())"`)

---

## Validation du code

Avant de committer, assurez-vous que tout passe :

```bash
# Vérifications automatiques
ruff check .
ruff format --check .
mypy backend/src --explicit-package-bases
pytest
npm run lint
npm run fmt -- --check
```

Les hooks pre-commit exécuteront automatiquement ces vérifications.

---

## Rapports d'analyse

Tous les rapports d'analyse (audits, reviews, décisions architecturales) sont stockés dans `Analysis_reports/` au format Markdown avec horodatage.

Voir le rapport de conformité : `Analysis_reports/rapport_conformite_2025-12-26_compliance.md`

---

## Versioning

Ce template suit le **Semantic Versioning** :

- **0.0.1-Alpha** : Version initiale (actuelle)
- **0.1.0-Beta** : Première version avec templates/static complets
- **1.0.0** : Première version stable

Voir `.github/copilot-instructions.md` (section 6) pour les règles de versioning.

---

## Contribution

1. Suivre les règles dans `.github/copilot-instructions.md`
2. Ajouter des en-têtes obligatoires à tous les nouveaux fichiers
3. Documenter avec docstrings et commentaires explicites
4. Maintenir la couverture de tests > 50% (objectif 80% pour v1.0.0)
5. Exécuter `make lint` et `make test` avant de committer

---

## License

**TBD** — À définir selon votre usage.

Pour un template open-source, considérer : MIT, Apache 2.0  
Pour un usage interne : Propriétaire

---

## Support

Pour des questions ou problèmes :
- Consulter `.github/copilot-instructions.md`
- Vérifier les rapports dans `Analysis_reports/`
- Contacter : AleGabMar (XAREMA)

---

**Copyright (c) 2025 XAREMA. All rights reserved.**

