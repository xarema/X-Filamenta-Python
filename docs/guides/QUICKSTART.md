<!--
Purpose: Quick start guide for X-Filamenta-Python
Description: Instructions for setting up and running the project locally

File: QUICKSTART.md | Repository: X-Filamenta-Python
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

# Démarrage rapide — X-Filamenta-Python

## ⚡ Installation (5 minutes)

### Windows PowerShell

```powershell
# 1. Créer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# 3. Installer les outils frontend
npm install

# 4. Créer le fichier .env (optionnel)
Copy-Item .env.example .env
```

### Linux / macOS

```bash
# 1. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# 3. Installer les outils frontend
npm install

# 4. Créer le fichier .env (optionnel)
cp .env.example .env
```

---

## 🚀 Lancer l'application

```powershell
# Méthode 1 : Avec python -m
python -m backend.src

# Méthode 2 : Avec Flask CLI
flask --app backend.src.app run

# Accéder à l'app
# http://localhost:5000
```

---

## 🧪 Exécuter les tests

```powershell
# Tests de base
pytest

# Avec couverture
pytest --cov=backend/src

# Tests spécifiques
pytest backend/tests/test_smoke.py -v
```

---

## 🔧 Formatage et linting

```powershell
# Vérifier le code
ruff check .
npm run lint

# Formatter le code
ruff format .
npm run fmt

# Type checking
mypy backend/src
```

---

## 📁 Structure clé

```
backend/src/
  ├── app.py          # Application Flask factory + SQLAlchemy
  ├── config.py       # Configuration (dev/test/prod)
  ├── models/         # Modèles de données (ORM)
  ├── routes/         # Blueprints (routes)
  ├── services/       # Logique métier
  └── utils/          # Utilitaires

backend/tests/
  ├── test_smoke.py   # Tests de base
  ├── conftest.py     # Fixtures pytest
  ├── unit/           # Tests unitaires
  └── integration/    # Tests d'intégration

frontend/
  ├── templates/      # Modèles Jinja2
  └── static/         # CSS, JS, images
```

---

## 💾 Base de données

La base de données SQLite est créée automatiquement au premier démarrage :

```
backend/instance/app.db  # Fichier BD (créé automatiquement)
```

Pour réinitialiser :

```powershell
Remove-Item backend/instance/app.db -Force
```

---

## 📚 Documentation

- [`README.md`](README.md) — Vue d'ensemble du projet
- [`INIT_CHECKLIST.md`](INIT_CHECKLIST.md) — Checklist d'initialisation
- [`CHANGELOG.md`](CHANGELOG.md) — Historique des modifications
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md) — Règles de développement

---

## ❓ Troubleshooting

### ModuleNotFoundError: No module named 'backend'

```powershell
# S'assurer que le package est installé
pip install -e .
```

### Port 5000 déjà utilisé

```powershell
# Changer le port
flask --app backend.src.app run --port 5001
```

### Erreurs SQLite

```powershell
# Supprimer la BD et relancer
Remove-Item backend/instance/app.db -Force
python -m backend.src
```

---

## 🎯 Prochaines étapes

1. Consulter [`INIT_CHECKLIST.md`](INIT_CHECKLIST.md) pour les phases suivantes
2. Créer les premiers modèles dans `backend/src/models/`
3. Implémenter les routes dans `backend/src/routes/`
4. Écrire les tests dans `backend/tests/`

Bon développement ! 🚀
