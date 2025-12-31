<!--
Purpose: Project roadmap and immediate tasks
Description: Complete roadmap for X-Filamenta-Python with phases and priorities

File: ROADMAP.md | Repository: X-Filamenta-Python
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

# Feuille de route — X-Filamenta-Python

**Version:** 0.0.1-Alpha RC  
**Date:** 2025-12-27  
**Statut:** Planning Phase

---

## 🎯 Vue d'ensemble

Cette roadmap couvre les **tâches essentielles** pour préparer l'application avant l'ajout des fonctionnalités métier.

**Phases :**

1. ⭐ **PHASE 1 (Immédiat)** — Infrastructure & Setup
2. ⭐ **PHASE 2 (Cette semaine)** — Backend Routes & Templates
3. ⭐ **PHASE 3 (Semaine 2)** — Testing & Validation
4. 🎯 **PHASE 4 (Semaine 3+)** — Fonctionnalités métier

---

## ⭐ PHASE 1 — Infrastructure & Setup (MAINTENANT)

**Durée estimée :** 2-3 jours  
**Priorité :** CRITIQUE

### ✅ Tasks

#### 1.1 Configuration de base

- [ ] Tester la structure du projet
  ```bash
  python -m backend.src  # Vérifier que l'app démarre
  ```
- [ ] Vérifier les imports Python
  ```bash
  python -c "from backend.src.app import create_app; print('✓ OK')"
  ```
- [ ] Valider la configuration
  ```bash
  python -c "from backend.src.config import get_config; print(get_config('development'))"
  ```

#### 1.2 Base de données

- [ ] Initialiser SQLite en développement
  ```bash
  python scripts/init_db.py init
  ```
- [ ] Vérifier la création des tables
  ```bash
  python -c "from backend.src.app import db; print(db.metadata.tables.keys())"
  ```
- [ ] Tester la connexion BD
  ```bash
  python -c "from backend.src.app import db, create_app; app = create_app();
             with app.app_context(): print('✓ DB OK')"
  ```

#### 1.3 Frontend assets

- [ ] Vérifier les chemins statiques
  ```bash
  ls frontend/static/css/tokens/variables.css
  ls frontend/static/js/plugins/tabulator.js
  ```
- [ ] Vérifier les chemins templates
  ```bash
  ls frontend/templates/layouts/base.html
  ls frontend/templates/components/
  ```
- [ ] Tester `url_for()` en template
  ```jinja2
  {{ url_for('static', filename='css/main.css') }}
  ```

#### 1.4 Dépendances Python

- [ ] Installer dépendances de base
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Vérifier les imports critiques
  ```bash
  python -c "import flask, sqlalchemy, jinja2; print('✓ OK')"
  ```
- [ ] Installer dépendances dev
  ```bash
  pip install -r requirements-dev.txt
  ```

#### 1.5 Dépendances Node (optionnel pour maintenant)

- [ ] Installer npm
  ```bash
  npm install
  ```
- [ ] Vérifier Prettier/ESLint
  ```bash
  npm run lint
  ```

---

## ⭐ PHASE 2 — Backend Routes & Templates (Cette semaine)

**Durée estimée :** 3-4 jours  
**Priorité :** HAUTE

### ✅ Tasks

#### 2.1 Routes principales (Flask)

- [ ] Créer blueprint principal

  ```python
  # backend/src/routes/main.py
  from flask import Blueprint
  main = Blueprint('main', __name__)

  @main.route('/')
  def index():
      return render_template('pages/index.html')
  ```

- [ ] Enregistrer le blueprint dans app.py
  ```python
  # backend/src/app.py
  from backend.src.routes.main import main
  app.register_blueprint(main)
  ```
- [ ] Tester les routes
  ```bash
  curl http://localhost:5000/
  ```

#### 2.2 Routes API de base

- [ ] Créer blueprint API

  ```python
  # backend/src/routes/api.py
  api = Blueprint('api', __name__, url_prefix='/api')

  @api.route('/health', methods=['GET'])
  def health():
      return {'status': 'ok'}, 200
  ```

- [ ] Enregistrer blueprint API
- [ ] Tester l'endpoint
  ```bash
  curl http://localhost:5000/api/health
  ```

#### 2.3 Contexte utilisateur (pour les templates)

- [ ] Créer mock `current_user` pour développement
  ```python
  # backend/src/models/user.py
  class User:
      def __init__(self, username='dev_user', is_admin=False):
          self.username = username
          self.is_admin = is_admin
          self.is_authenticated = True
  ```
- [ ] Injecter dans templates
  ```python
  @main.route('/')
  def index():
      current_user = User(username='Jean', is_admin=False)
      return render_template('pages/index.html', current_user=current_user)
  ```

#### 2.4 Intégration des templates

- [ ] Vérifier que `base.html` charge correctement
  - Bootstrap CDN
  - CSS tokens + main.css
  - HTMX, Alpine, Tabulator CDN
  - Plugins JS (tabulator.js, alpine-utils.js, htmx-utils.js)
- [ ] Tester `navbar.html` et `footer.html`
- [ ] Tester page `index.html`
- [ ] Tester page `datagrid-example.html`

#### 2.5 Gestion des erreurs de base

- [ ] Créer 404 handler
  ```python
  @app.errorhandler(404)
  def not_found(e):
      return render_template('errors/404.html'), 404
  ```
- [ ] Créer 500 handler
  ```python
  @app.errorhandler(500)
  def server_error(e):
      return render_template('errors/500.html'), 500
  ```
- [ ] Créer templates d'erreur

#### 2.6 Système de préférences (localStorage)

- [ ] Endpoint pour sauvegarder préférences (optionnel maintenant)
  ```python
  @api.post('/preferences/<pref>')
  def set_preference(pref):
      value = request.json.get('value')
      # Session storage ou BD
      return {'status': 'ok'}, 200
  ```

---

## ⭐ PHASE 3 — Testing & Validation (Semaine 2)

**Durée estimée :** 2-3 jours  
**Priorité :** HAUTE

### ✅ Tasks

#### 3.1 Tests unitaires

- [ ] Tester imports
  ```bash
  python -m pytest backend/tests/test_smoke.py -v
  ```
- [ ] Tester factory app
  ```python
  # backend/tests/test_app.py
  def test_create_app():
      app = create_app()
      assert app is not None
      assert app.config['TESTING'] == True
  ```
- [ ] Tester routes principales
  ```python
  def test_index_route(client):
      response = client.get('/')
      assert response.status_code == 200
      assert b'X-Filamenta' in response.data
  ```
- [ ] Tester API health
  ```python
  def test_api_health(client):
      response = client.get('/api/health')
      assert response.status_code == 200
      assert response.json['status'] == 'ok'
  ```

#### 3.2 Tests d'intégration

- [ ] Tester templates
  - [ ] `index.html` affiche correctly
  - [ ] `navbar.html` inclus et clickable
  - [ ] `footer.html` avec attribution AGPL
  - [ ] `datagrid-example.html` charge Tabulator
- [ ] Tester CSS
  - [ ] Variables CSS disponibles
  - [ ] Bootstrap chargé
  - [ ] Thème light/dark toggle fonctionne
- [ ] Tester JS
  - [ ] Alpine.js fonctionne
  - [ ] HTMX fonctionne
  - [ ] Tabulator initialise

#### 3.3 Linting & Formatting

- [ ] Vérifier code Python
  ```bash
  ruff check backend/
  ```
- [ ] Formatter code Python
  ```bash
  ruff format backend/
  ```
- [ ] Vérifier types Python
  ```bash
  mypy backend/src
  ```
- [ ] Vérifier code JS
  ```bash
  npm run lint
  ```
- [ ] Formatter code JS
  ```bash
  npm run fmt
  ```

#### 3.4 Sécurité basique

- [ ] Vérifier CSRF protection (optionnel maintenant)
- [ ] Vérifier escaping HTML dans templates
- [ ] Vérifier pas de secrets en code
  ```bash
  grep -r "password\|secret\|api_key" backend/src --exclude-dir=.git
  ```
- [ ] Vérifier headers de sécurité (optionnel)

#### 3.5 Responsive & Accessibility

- [ ] Tester sur mobile (DevTools)
  - [ ] Navbar responsive
  - [ ] Grid responsive
  - [ ] Modals accessibles
- [ ] Vérifier a11y basique
  - [ ] Labels sur inputs
  - [ ] Contrast des couleurs
  - [ ] Keyboard navigation

---

## 🎯 PHASE 4 — Fonctionnalités métier (Semaine 3+)

**Durée estimée :** À définir  
**Priorité :** APRÈS phases 1-3

### ✅ Placeholder Tasks

- [x] Wizard (Partie 1) — squelette multi-étapes HTMX en place : test DB (SQLite ou URI fourni), upload backup avec vérif extension + checksum, capture checksum/filename, validation mot de passe fort pour admin, synthèse + finalize stub; guard first-run actif (bypass en test)
- [ ] Wizard (Partie 1) — à finaliser : logique restore/seed réelle (manifest + checksum), progression visuelle, erreurs explicites, retirer test de padding quand tests complets couvrent
- [ ] Authentification utilisateur
  - [ ] Login/Logout routes (HTMX)
  - [ ] 2FA TOTP + fallback email OTP optionnel
  - [ ] Politique mot de passe fort réutilisée côté auth
- [ ] Session management sécurisé (cookies, CSRF si formulaires non-htmx, throttling login/2FA)
- [ ] Modèle de données (User rôles/langue/thème/secret TOTP, Theme, Content) + migrations
- [ ] CRUD admin (users, thèmes, contenu), historique admin, dashboard (version/git/backup), outils update (dry-run/apply protégée + backup auto)
- [ ] Sauvegarde / Restauration : génération backup (manifest+checksum), restauration avec snapshot pré-restauration et dry-run
- [ ] Footer licence + lien Legal/About (AGPL) ; responsive complet ; langue/thème par défaut pour nouveaux utilisateurs

---

## 📋 Checklist détaillée PHASE 1

Copie-colle cette checklist et remplis-la au fur et à mesure :

```
PHASE 1 — Infrastructure & Setup
================================

Configuration de base:
  [ ] python -m backend.src fonctionne
  [ ] Imports Python valides
  [ ] Configuration chargée correctement

Base de données:
  [ ] python scripts/init_db.py init réussit
  [ ] Tables créées
  [ ] Connexion BD fonctionne

Frontend:
  [ ] CSS tokens chargé
  [ ] JS plugins chargés
  [ ] Templates trouvés

Dépendances:
  [ ] pip install -r requirements.txt OK
  [ ] npm install OK
  [ ] Tous les imports fonctionnent

Démarrage:
  [ ] flask run démarre l'app
  [ ] http://localhost:5000 accessible
  [ ] Pas d'erreurs dans console
```

---

## 📋 Checklist détaillée PHASE 2

```
PHASE 2 — Routes & Templates
=============================

Routes:
  [ ] Blueprint main créé
  [ ] Route / (index) fonctionne
  [ ] Blueprint API créé
  [ ] Route /api/health fonctionne
  [ ] Blueprint enregistré dans app.py

Templates:
  [ ] base.html charge correctement
  [ ] navbar.html inclus et fonctionne
  [ ] footer.html affiche attribution AGPL
  [ ] index.html affiche correctement
  [ ] datagrid-example.html charge Tabulator

Utilisateur:
  [ ] current_user disponible dans templates
  [ ] Navbar affiche nom utilisateur
  [ ] Admin link visible (si is_admin=True)
  [ ] Logout formulaire fonctionne

Erreurs:
  [ ] 404 page custom créée
  [ ] 500 page custom créée
  [ ] Navigation vers erreur teste correctement
```

---

## 📋 Checklist détaillée PHASE 3

```
PHASE 3 — Testing & Validation
==============================

Tests:
  [ ] pytest fonctionne
  [ ] test_smoke.py passe
  [ ] test_app.py créé et passe
  [ ] test_routes.py créé et passe
  [ ] Coverage > 80%

Linting:
  [ ] ruff check pass
  [ ] ruff format pass
  [ ] mypy pass (ou warnings acceptés)
  [ ] npm run lint pass

Responsive:
  [ ] Mobile (320px) OK
  [ ] Tablet (768px) OK
  [ ] Desktop (1024px) OK

Accessibility:
  [ ] Inputs ont labels
  [ ] Contraste couleurs OK
  [ ] Keyboard navigation OK

Performance:
  [ ] Pas d'erreurs console
  [ ] CSS load time < 1s
  [ ] JS load time < 2s
  [ ] Page render < 3s
```

---

## 🚀 Commandes rapides

Copie-colle pour démarrer :

```bash
# Install
pip install -r requirements.txt && npm install

# Init BD
python scripts/init_db.py init

# Run
cd backend && flask run

# Test
pytest -v

# Lint
ruff check . && npm run lint

# Format
ruff format . && npm run fmt
```

---

## 📊 Progression estimée

| Phase       | Durée     | % Temps | Statut           |
| ----------- | --------- | ------- | ---------------- |
| **Phase 1** | 2-3 jours | 30%     | ⏳ Maintenant    |
| **Phase 2** | 3-4 jours | 35%     | ⏳ Cette semaine |
| **Phase 3** | 2-3 jours | 20%     | ⏳ Semaine 2     |
| **Phase 4** | À définir | 15%     | 📅 Après Phase 3 |

---

## 🎯 Objectif final Phase 1-3

À la fin de la **PHASE 3**, tu auras :

✅ Application Flask qui démarre  
✅ Routes principales et API basique  
✅ Templates intégrés (Jinja2 + Bootstrap)  
✅ Tests validant le tout  
✅ Code clean (ruff, mypy OK)  
✅ App responsive et accessible  
✅ Prêt pour ajouter les fonctionnalités métier

---

## 📝 Notes importantes

### Environment

- **Dev :** `FLASK_ENV=development` dans `.env`
- **Test :** `FLASK_ENV=testing` pour tests
- **Prod :** `FLASK_ENV=production` (plus tard)

### Database

- **Dev :** SQLite (`instance/app.db`)
- **Test :** SQLite in-memory (`:memory:`)
- **Prod :** MySQL/PostgreSQL (configurer `.env`)

### Hot reload

Flask recharge automatiquement en développement :

- Modifiez un fichier Python → app recharge
- Modifiez un template → page recharge
- Modifiez CSS → navigateur recharge

---

## 🔗 Ressources

- [Flask Official Docs](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pytest Docs](https://docs.pytest.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)

---

## ✉️ Prochaines étapes

1. **Aujourd'hui :** Compléter PHASE 1
2. **Cette semaine :** Compléter PHASE 2
3. **Semaine prochaine :** Compléter PHASE 3
4. **Semaine 3+ :** Ajouter les fonctionnalités métier

---

**Bonne chance ! 🚀**

Mets à jour ce document au fur et à mesure et partage ta progression !
