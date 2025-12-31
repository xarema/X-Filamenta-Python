# 📋 PLAN DÉTAILLÉ PHASE 3 — Fonctionnalités Business

**Date création:** 2025-12-29T23:15:00+01:00  
**Auteur:** GitHub Copilot  
**Basé sur:** Audit complet + Analyse features_inventory.md + Conversation  
**Durée estimée:** 15-20 jours  
**Objectif:** Compléter les fonctionnalités business pour v1.0.0

---

## ⚠️ IMPORTANT: À VALIDER AVANT DÉMARRAGE

**CE PLAN CONTIENT DES PROPOSITIONS DE FONCTIONNALITÉS.**

Chaque sprint nécessite **TON APPROBATION** avant de commencer le développement.

**Questions à me poser pour CHAQUE sprint:**
- ✅ "Oui, continue Sprint X" → Je code
- ❌ "Non, skip Sprint X" → Je passe au suivant
- 🔄 "Modifie Sprint X: [détails]" → J'adapte le plan
- ❓ "Explique Sprint X en détail" → Je détaille les user stories

---

## 📊 ÉTAT ACTUEL (Post-Phase 2)

### ✅ Déjà Implémenté (Très solide)

**Infrastructure & Core:**
- ✅ Flask app factory + Blueprints
- ✅ SQLAlchemy multi-DB (SQLite/MySQL/PostgreSQL)
- ✅ Alembic migrations (4 fichiers)
- ✅ Installation wizard 7 étapes
- ✅ i18n complet (fr/en)
- ✅ Security headers (CSP, CORS, CSRF, HSTS)

**Authentification & Sécurité:**
- ✅ Login/Logout complet
- ✅ 2FA TOTP + backup codes
- ✅ Email verification workflow
- ✅ Password reset workflow
- ✅ Rate limiting (login, 2FA, API)
- ✅ Session management sécurisé
- ✅ Password strength validation
- ✅ Account locking (tentatives échouées)

**Admin:**
- ✅ Dashboard admin (statistiques basiques)
- ✅ Settings page (SMTP, cache, features)
- ✅ Cache management (test, clear, stats)
- ✅ User listing (view only)
- ✅ Admin history logging

**Performance:**
- ✅ Cache multi-backend (Redis/Filesystem/Memory)
- ✅ Database optimizations (+140% throughput)
- ✅ Frontend optimizations (-88% load time)
- ✅ Asset bundling + minification
- ✅ Gzip compression

**Tests & Documentation:**
- ✅ 160+ tests (79 backend, reste fixtures)
- ✅ Documentation extensive (40+ rapports)
- ✅ CHANGELOG complet
- ✅ Guides déploiement

### ❌ Fonctionnalités Manquantes (Identifiées)

Selon `FEATURES_COMPLETE_INVENTORY.md` et audit:

**Admin:**
- ❌ CRUD complet users (create, edit, delete via UI)
- ❌ CRUD complet content (create, edit, delete via UI)
- ❌ User roles/permissions management
- ❌ Bulk operations (import/export users)
- ❌ Advanced admin dashboard (graphiques, tendances)

**Utilisateur:**
- ❌ Page profil utilisateur complet
- ❌ Upload avatar
- ❌ Gestion préférences avancées (UI complète)
- ❌ Notifications utilisateur
- ❌ Activity log utilisateur

**Fonctionnalités Avancées:**
- ❌ Système de recherche (full-text)
- ❌ API REST complète + documentation (Swagger)
- ❌ Export données (CSV, JSON, PDF)
- ❌ Import données en masse
- ❌ Webhooks (optionnel)
- ❌ Plugins/Extensions system

**Testing:**
- ❌ Tests e2e complets (Playwright/Selenium)
- ❌ Fixtures complètes (admin_user, authenticated_client)
- ❌ Load testing automatisé (CI)

**Documentation:**
- ❌ Documentation utilisateur finale
- ❌ Guides vidéo (optionnel)
- ❌ FAQ complète

---

## 🎯 SPRINTS PHASE 3 (Propositions)

### 📅 Sprint 1: CRUD Admin Complet (5 jours)

**Objectif:** Permettre aux admins de gérer users/content via UI

#### User Stories

**US-1.1:** En tant qu'admin, je veux créer un nouvel utilisateur manuellement
- Form: username, email, password, role (admin/user), is_active
- Validation côté serveur
- Envoi email bienvenue (optionnel)
- Redirection vers user list avec message success

**US-1.2:** En tant qu'admin, je veux éditer un utilisateur existant
- Form pré-rempli avec données actuelles
- Possibilité reset password (génère nouveau + email)
- Possibilité activer/désactiver compte
- Lock/unlock account si verrouillé

**US-1.3:** En tant qu'admin, je veux supprimer un utilisateur
- Confirmation modale (sécurité)
- Soft delete (is_active=False) OU hard delete
- Option: anonymiser données au lieu supprimer
- Logging dans admin_history

**US-1.4:** En tant qu'admin, je veux gérer les contenus
- CRUD complet (create, edit, delete)
- Prévisualisation avant publication
- Versioning basique (created_at, updated_at)

#### Fichiers à créer/modifier

**Backend:**
- `backend/src/routes/admin_users.py` (déjà existe, ajouter CRUD)
- `backend/src/routes/admin_content.py` (nouveau)
- `backend/src/services/admin_service.py` (nouveau, centraliser logique)

**Frontend:**
- `frontend/templates/admin/users_create.html` (nouveau)
- `frontend/templates/admin/users_edit.html` (nouveau)
- `frontend/templates/admin/users_delete_confirm.html` (nouveau)
- `frontend/templates/admin/content_create.html` (nouveau)
- `frontend/templates/admin/content_edit.html` (nouveau)

**Tests:**
- `backend/tests/test_admin_crud_users.py` (nouveau, 15+ tests)
- `backend/tests/test_admin_crud_content.py` (nouveau, 10+ tests)

#### Questions à me poser

1. **Soft delete ou hard delete users?**
   - A) Soft delete (is_active=False, données conservées)
   - B) Hard delete (suppression BDD)
   - C) Option admin (choix au moment de delete)

2. **Email automatique lors création user?**
   - A) Oui, toujours
   - B) Non, jamais
   - C) Checkbox optionnel dans form

3. **Roles prédéfinis ou custom?**
   - A) Seulement admin/user (actuel)
   - B) Ajouter moderator/editor/viewer
   - C) System permissions granulaires (complexe)

---

### 📅 Sprint 2: Profil Utilisateur Complet (4 jours)

**Objectif:** Permettre aux users de gérer leur profil

#### User Stories

**US-2.1:** En tant qu'user, je veux voir mon profil
- Page `/profile` avec toutes mes infos
- Avatar (si implémenté)
- Email, username, role, created_at, last_login
- Statistiques personnelles (optionnel)

**US-2.2:** En tant qu'user, je veux éditer mon profil
- Modifier email (avec ré-vérification)
- Modifier username (si permis)
- Modifier préférences (langue, thème, notifications)

**US-2.3:** En tant qu'user, je veux changer mon mot de passe
- Form: old password, new password, confirm
- Validation strength
- Session invalidation (autres devices)

**US-2.4:** En tant qu'user, je veux uploader un avatar (optionnel)
- Upload image (PNG, JPG, max 2MB)
- Crop/resize automatique
- Stockage: `instance/avatars/user_{id}.ext`

**US-2.5:** En tant qu'user, je veux voir mon activity log
- Dernières connexions (IP, date, user-agent)
- Actions importantes (password change, 2FA enable, etc.)

#### Fichiers à créer/modifier

**Backend:**
- `backend/src/routes/profile.py` (nouveau blueprint)
- `backend/src/services/avatar_service.py` (nouveau, si avatar)
- Modifier `backend/src/models/user.py` (ajouter champ avatar_url)
- Migration Alembic: `005_add_user_avatar.py`

**Frontend:**
- `frontend/templates/profile/index.html` (nouveau)
- `frontend/templates/profile/edit.html` (nouveau)
- `frontend/templates/profile/change_password.html` (nouveau)
- `frontend/templates/profile/avatar_upload.html` (nouveau, optionnel)
- `frontend/templates/profile/activity_log.html` (nouveau)

**Tests:**
- `backend/tests/test_profile.py` (nouveau, 20+ tests)
- `backend/tests/test_avatar_upload.py` (nouveau, 10+ tests si avatar)

#### Questions à me poser

4. **Avatar upload: oui ou non?**
   - A) Oui, fonctionnalité complète
   - B) Non, pas prioritaire
   - C) Placeholder (Gravatar uniquement)

5. **Username modifiable?**
   - A) Oui, une fois tous les 30 jours
   - B) Non, jamais modifiable
   - C) Admin only

6. **Activity log détail?**
   - A) Basique (last 10 logins)
   - B) Complet (toutes actions)
   - C) Pas d'activity log

---

### 📅 Sprint 3: API REST + Documentation (4 jours)

**Objectif:** API publique documentée pour intégrations

#### User Stories

**US-3.1:** En tant que dev externe, je veux accéder à une API REST documentée
- Endpoints CRUD: `/api/v1/users`, `/api/v1/content`
- Documentation Swagger/OpenAPI interactive
- Authentification: API keys ou JWT

**US-3.2:** En tant qu'admin, je veux gérer les API keys
- Génération API key
- Révocation API key
- Rate limiting par key

#### Fichiers à créer/modifier

**Backend:**
- `backend/src/routes/api_v1.py` (nouveau, API REST)
- `backend/src/services/api_key_service.py` (nouveau)
- `backend/src/models/api_key.py` (nouveau)
- Migration: `006_add_api_keys.py`

**Documentation:**
- `backend/src/openapi.yaml` (nouveau, spec OpenAPI)
- Installer `flask-swagger-ui`

**Tests:**
- `backend/tests/test_api_v1.py` (nouveau, 30+ tests)

#### Questions à me poser

7. **API publique: oui ou non?**
   - A) Oui, complet
   - B) Non, interne only
   - C) Partial (read-only)

8. **Authentication API?**
   - A) API keys
   - B) JWT tokens
   - C) Les deux

---

### 📅 Sprint 4: Recherche & Export (3 jours)

**Objectif:** Recherche avancée + export données

#### User Stories

**US-4.1:** En tant qu'admin, je veux chercher dans users/content
- Full-text search (SQLite FTS5 ou PostgreSQL)
- Filtres: rôle, status, date range
- Pagination résultats

**US-4.2:** En tant qu'admin, je veux exporter des données
- Export users: CSV, JSON
- Export content: CSV, JSON, PDF
- Sélection colonnes à exporter

#### Fichiers à créer/modifier

**Backend:**
- `backend/src/services/search_service.py` (nouveau)
- `backend/src/services/export_service.py` (nouveau)
- Modifier routes admin

**Tests:**
- `backend/tests/test_search.py` (nouveau)
- `backend/tests/test_export.py` (nouveau)

#### Questions à me poser

9. **Full-text search: quelle solution?**
   - A) SQLite FTS5 (simple, intégré)
   - B) PostgreSQL full-text (performant)
   - C) Elasticsearch (très performant, complexe)

10. **Export formats?**
    - A) CSV uniquement
    - B) CSV + JSON
    - C) CSV + JSON + PDF

---

### 📅 Sprint 5: Tests e2e + Documentation Finale (4 jours)

**Objectif:** Tests complets + documentation utilisateur

#### Tasks

**Tests:**
- Installer Playwright ou Selenium
- Tests e2e: Installation wizard, Login, Admin CRUD, Profile
- Tests fixtures complètes (admin_user, etc.)
- Load testing automatisé (CI)

**Documentation:**
- Guide utilisateur final (PDF + HTML)
- Guide admin complet
- FAQ (20+ questions)
- Tutoriels vidéo (optionnel)
- README.md final (badges, screenshots)

#### Fichiers à créer

**Tests:**
- `backend/tests/e2e/` (nouveau dossier)
- `backend/tests/e2e/test_wizard.py`
- `backend/tests/e2e/test_auth.py`
- `backend/tests/e2e/test_admin.py`
- `backend/tests/fixtures/complete_fixtures.py` (nouveau)

**Documentation:**
- `docs/user_guide.md` (nouveau)
- `docs/admin_guide.md` (nouveau)
- `docs/FAQ.md` (nouveau)
- `docs/API.md` (si Sprint 3)

---

## 📊 RÉCAPITULATIF PHASE 3

| Sprint | Durée | Effort | Risque | Priorité |
|--------|-------|--------|--------|----------|
| Sprint 1: CRUD Admin | 5j | L | Moyen | ⭐⭐⭐ HAUTE |
| Sprint 2: Profil User | 4j | M | Faible | ⭐⭐⭐ HAUTE |
| Sprint 3: API REST | 4j | M | Moyen | ⭐⭐ MOYENNE |
| Sprint 4: Search/Export | 3j | M | Faible | ⭐⭐ MOYENNE |
| Sprint 5: Tests e2e/Docs | 4j | M | Faible | ⭐⭐⭐ HAUTE |

**Total:** 20 jours

---

## ❓ QUESTIONS GLOBALES À ME POSER

**Avant de commencer Phase 3, réponds à ces questions:**

### Scope Phase 3

**Q1:** Veux-tu faire **TOUS** les sprints ou seulement certains?
- A) Tous les 5 sprints (20 jours, v1.0.0 très complet)
- B) Sprints 1, 2, 5 uniquement (13 jours, v1.0.0 essentiel)
- C) Autre combinaison (spécifie)

**Q2:** Priorité absolue?
- A) CRUD Admin (Sprint 1)
- B) Profil User (Sprint 2)
- C) Tests e2e (Sprint 5)

**Q3:** API REST (Sprint 3): nécessaire v1.0.0?
- A) Oui, indispensable
- B) Non, reporter v1.1.0
- C) Partial (read-only)

**Q4:** Features avancées (Sprint 4): nécessaire v1.0.0?
- A) Oui, search + export critiques
- B) Non, reporter v1.1.0
- C) Search oui, export non

### Détails Techniques

**Q5:** Upload avatar utilisateur?
- A) Oui
- B) Non
- C) Gravatar uniquement

**Q6:** Soft delete ou hard delete users?
- A) Soft delete
- B) Hard delete
- C) Admin choisit

**Q7:** Roles utilisateur?
- A) Admin/User uniquement (actuel)
- B) Ajouter moderator/editor
- C) Permissions granulaires

**Q8:** Full-text search engine?
- A) SQLite FTS5
- B) PostgreSQL full-text
- C) Elasticsearch

**Q9:** Tests e2e framework?
- A) Playwright
- B) Selenium
- C) Pas de tests e2e

**Q10:** Documentation finale format?
- A) Markdown uniquement
- B) Markdown + PDF
- C) Markdown + PDF + vidéos

---

## 🚀 PROCHAINES ACTIONS

**1. TOI:** Réponds aux 10 questions ci-dessus

**2. MOI:** J'adapte le plan selon tes réponses

**3. NOUS:** On commence Sprint par sprint avec ton approbation

---

**Fichier:** docs/PHASE3_PLAN_DETAILED.md  
**Statut:** BROUILLON (à valider)  
**Créé:** 2025-12-29T23:15:00+01:00  
**Auteur:** GitHub Copilot

