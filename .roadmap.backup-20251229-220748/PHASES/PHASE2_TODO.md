<!--
Purpose: Phase 2 todo items
Description: Tasks for Phase 2 - Backend Routes & Templates

File: .roadmap/PHASES/PHASE2_TODO.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public
-->

# TODO — PHASE 2 (Backend Routes & Templates)

**Statut :** À faire maintenant après PHASE 1 ✅  
**Durée estimée :** 3-4 jours  
**Priorité :** HAUTE  
**Commencé:** 2025-12-27

---

## 📋 Vue d'ensemble

Phase 2 consiste à créer toutes les routes principales, intégrer les templates avec les données réelles, et mettre en place la gestion du contexte utilisateur.

**Objectif :** App avec toutes les pages principales fonctionnelles + API endpoints

---

## 🎯 JOUR 1 - Routes Principales (3-4 heures)

### Task 1: Créer routes pour pages publiques

**Durée:** 1h

```bash
Routes à créer:
  GET /about             - Page à propos
  GET /contact           - Contact/formulaire
  GET /features          - Fonctionnalités
  GET /pricing           - Tarification (optionnel)
```

Files:

- [ ] `backend/src/routes/pages.py` (nouveau blueprint)
- [ ] `frontend/templates/pages/about.html`
- [ ] `frontend/templates/pages/contact.html`
- [ ] `frontend/templates/pages/features.html`

### Task 2: Créer routes admin

**Durée:** 1h

```bash
Routes à créer:
  GET /admin             - Dashboard admin
  GET /admin/users       - Liste utilisateurs (CRUD)
  GET /admin/settings    - Paramètres app
  GET /admin/content     - Gestion contenu
```

Files:

- [ ] `backend/src/routes/admin.py` (nouveau blueprint)
- [ ] `frontend/templates/admin/dashboard.html`
- [ ] `frontend/templates/admin/users.html`
- [ ] `frontend/templates/admin/settings.html`

### Task 3: Étendre API routes

**Durée:** 1h

```bash
Endpoints à ajouter:
  GET /api/config        - Configuration app
  GET /api/version       - Version de l'app
  POST /api/contact      - Formulaire contact
  GET /api/data/stats    - Statistiques (placeholder)
```

Files:

- [ ] Modifier `backend/src/routes/api.py`
- [ ] Ajouter validators pour POST /api/contact

### Task 4: Tester les routes

**Durée:** 30 min

- [ ] Tests routes GET (vérifier status 200)
- [ ] Tests routes inexistantes (404)
- [ ] Tests API endpoints

---

## 🎯 JOUR 2 - Templates & Contexte Utilisateur (3-4 heures)

### Task 5: Améliorer template base.html

**Durée:** 1h

- [ ] Navbar dynamique (avec liens)
- [ ] Footer avec infos légales
- [ ] Sidebar optionnelle pour admin
- [ ] Gestion du contexte utilisateur

Files:

- [ ] Modifier `frontend/templates/layouts/base.html`
- [ ] Créer `frontend/templates/components/navbar.html`
- [ ] Créer `frontend/templates/components/footer.html`

### Task 6: Créer service utilisateur

**Durée:** 1h

```python
UserService avec:
  - get_current_user()
  - is_admin()
  - has_permission(action)
  - get_user_preferences()
```

Files:

- [ ] Créer `backend/src/services/user_service.py`
- [ ] Intégrer dans context processors

### Task 7: Système de préférences utilisateur

**Durée:** 1h

- [ ] Modèle Preferences en BD
- [ ] Route GET/POST /preferences
- [ ] Template de préférences
- [ ] HTMX pour mise à jour en temps réel

Files:

- [ ] Ajouter modèle dans `backend/src/models/`
- [ ] Créer `frontend/templates/pages/preferences.html`
- [ ] Route HTMX dans api.py

### Task 8: Intégrer pagination + filtrage

**Durée:** 30 min

- [ ] Pagination pour listes (users, content)
- [ ] Filtres simples
- [ ] Sort options

---

## 🎯 JOUR 3 - Notification System & Polish (2-3 heures)

### Task 9: Système de notifications HTMX

**Durée:** 1h

```bash
Notifications:
  - Success/error/info messages
  - Toast notifications (HTMX + Alpine)
  - Persistent notifications
```

Files:

- [ ] `frontend/templates/components/notifications.html`
- [ ] `frontend/static/js/notifications.js`
- [ ] Backend service pour notifications

### Task 10: Améliorer pages existantes

**Durée:** 1h

- [ ] index.html → plus riche
- [ ] datagrid-example.html → avec vraies données
- [ ] Error pages → intégration design

### Task 11: Tests routes complètes

**Durée:** 30 min

- [ ] Tests pour toutes les routes
- [ ] Tests API endpoints
- [ ] Tests context processors

Files:

- [ ] Modifier/étendre `backend/tests/test_routes.py`
- [ ] Ajouter `backend/tests/test_api.py`
- [ ] Ajouter `backend/tests/test_services.py`

### Task 12: Documentation mise à jour

**Durée:** 30 min

- [ ] Mettre à jour `backend/README.md`
- [ ] Documenter API endpoints
- [ ] Ajouter exemples d'utilisation

---

## 📊 Checklist Rapide

### Jour 1 - Routes

- [ ] Task 1: Pages publiques (about, contact, features)
- [ ] Task 2: Admin routes (dashboard, users, settings)
- [ ] Task 3: API endpoints (config, version, contact, stats)
- [ ] Task 4: Tests routes

### Jour 2 - Templates & Contexte

- [ ] Task 5: base.html + navbar + footer
- [ ] Task 6: UserService
- [ ] Task 7: Système préférences
- [ ] Task 8: Pagination + filtrage

### Jour 3 - Polish

- [ ] Task 9: Notification system
- [ ] Task 10: Améliorer pages
- [ ] Task 11: Tests complets
- [ ] Task 12: Documentation

---

## 🎯 Bonus (si temps)

- [ ] Database models pour users, preferences, notifications
- [ ] Migration script pour BD
- [ ] Seed data pour développement
- [ ] API documentation (OpenAPI/Swagger)

---

## 📝 Notes Importantes

1. **Stack respectée:** Flask + Jinja2 + Bootstrap 5 + HTMX + Alpine.js
2. **Conventions:** Suivre les règles dans `.github/copilot-instructions.md`
3. **Tests:** Tester après chaque route créée
4. **Commits:** Faire des commits atomiques
5. **Documentation:** Garder à jour

---

## 🚀 Commandes Utiles

```bash
# Démarrer l'app
cd backend
flask run --debug

# Tests
pytest -v --no-cov

# Linting
ruff check backend/src
ruff format backend/src

# Type checking
mypy backend/src --explicit-package-bases
```

---

## 📚 Références

- `backend/README.md` - Backend structure
- `docs/UI_UX_STACK.md` - Design guidelines
- `docs/UI_UX_QUICKSTART.md` - Quick reference
- `.github/copilot-instructions.md` - Code rules

---

**Last Updated:** 2025-12-27
**Status:** READY TO START 🚀
