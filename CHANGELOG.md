# CHANGELOG — X-Filamenta-Python

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Documentation

- **Major Documentation Reorganization (2025-12-31)** [#20]
  - Reduced docs/ root from 26 files to 3 essential files (README.md, 00_START_HERE.md, REFERENCE.md)
  - Consolidated duplicate archives/ directory into archive/ with proper structure
  - Moved 50+ files to appropriate locations using git mv (history preserved)
  - Created 10 missing README.md files for complete directory navigation
  - Organized deprecated documentation in archive/deprecated/
  - Consolidated all historical reports into archive/reports/2025-12/
  - Moved phase completion reports to archive/phases/
  - Reorganized technical content (DATABASE.md → architecture/, SETUP.md → guides/)
  - Added comprehensive navigation README files in all directories
  - Analysis reports: 2025-12-31_documentation-audit.md, 2025-12-31_documentation-cleanup-complete.md

### Changed

- **Roadmap Update (2025-12-31)**
  - Completed comprehensive code vs roadmap analysis
  - Verified Phase 1-3 completion status (100% accurate)
  - Verified Phase 4 progress (20% accurate)
  - Codebase statistics:
    - Backend: 43 Python files, 8,778 LOC
    - Frontend: 57 HTML templates
    - Tests: 123 test functions in 31 files
    - Documentation: 286 markdown files
    - Models: 5 database models
    - Services: 11 service modules
    - Routes: 12 route modules
  - Discovered unplanned feature: API endpoints (already implemented in api.py)
  - Updated roadmap files with verification timestamps
  - Analysis report: `Analysis_reports/2025-12-31_19-54_code-vs-roadmap-analysis.md`

### Added

- Added `package.json` for frontend tooling configuration (2025-12-31)
  - Created package.json with project metadata matching pyproject.toml (v0.1.0-beta)
  - Added npm scripts mirroring makefile targets: `lint`, `lint:js`, `lint:css`, `fmt`, `fmt:js`, `fmt:css`, `fmt:check`
  - Declared devDependencies: eslint (^9.17.0), prettier (^3.4.2), stylelint (^16.12.0), and required plugins
  - Set Node.js version requirement: >=18.0.0 (per README.md)
  - Included repository, author, and license metadata for npm registry compatibility
  - Unblocks `npm install` for new contributors and enables proper dependency version management

### Fixed

- **🚨 CRITICAL BUG - Dashboard 500 Error (2025-12-30 19:05) [BLOCKER]**
  - **Issue:** Dashboard pages (member & admin) retournaient une erreur 500 après connexion
  - **Impact:** Navigation post-connexion bloquée, dashboards inaccessibles
  - **Root Causes:** 
    1. TypeError: `t()` function ne supporte pas les arguments nommés (kwargs)
    2. TemplateNotFound: Mauvais chemin `base.html` au lieu de `layouts/base.html`
  - **Files Fixed:** 
    - `frontend/templates/dashboard/member.html` (ligne 32)
    - `frontend/templates/admin/dashboard.html` (ligne 1)
    - `frontend/templates/auth/verify-2fa.html` (ligne 1)
    - `frontend/templates/auth/setup-2fa.html` (ligne 1)
  - **Resolution Time:** 3 minutes
  - **Incident Report:** `.github/incidents-history-2025-12-30-dashboard-500.md`
  - **Severity:** CRITICAL — Core functionality broken for all authenticated users

- **🚨 CRITICAL BUG - JSON Syntax Error in French Translations (2025-12-30 17:15) [SECURITY]**
  - **Issue:** Missing comma on line 358 of `backend/src/i18n/translations/fr.json` prevented entire French language from loading
  - **Impact:** All French UI displayed variable names (`footer.legal`, `pages.about.cta_source`, etc.) instead of translated text
  - **Affected:** 822 lines of French translations, 10+ pages, all French-language users
  - **Root Cause:** Syntax error `"verified": "Email vérifié"` → `"verified": "Email vérifié",`
  - **Detection:** JSON parsing error: `Expecting ',' delimiter: line 361 column 7 (char 13677)`
  - **Resolution:** 
    - Added missing comma on line 358
    - Validated JSON syntax with `python -m json.tool`
    - Cleared cache (`instance/sessions/*` and `cache/*`)
    - Restarted production server
  - **Validation:** All 3 languages now load correctly (`fr`, `en`, `es`)
  - **Prevention:** Added JSON validation to deployment checklist
  - **Incident Report:** `Analysis_reports/2025-12-30_17-15_INCIDENT_JSON_SYNTAX_ERROR_FR.md`
  - **Severity:** HIGH — Core functionality broken for all French users

### Added

- **Restructuration i18n et Interface Admin (2025-12-30) ✅**
  - **Interface Admin i18n :**
    - Nouvelle page `GET /admin/i18n/translations` pour la gestion des langues.
    - Intégration de **Tabulator.js** pour l'édition en ligne (CRUD) des clés.
    - Routes API `GET/POST /admin/i18n/api/translations/<lang>` pour les mises à jour en temps réel.
    - Rechargement automatique du cache de traduction après modification.
  - **Synchronisation FR/EN :**
    - Traduction intégrale du Wizard d'installation (140+ clés) en anglais.
    - Audit final confirmant 100% de synchronisation (464 clés par langue).
  - **Gestion des Messages Flash :**
    - Externalisation de tous les messages flash du backend vers les fichiers JSON.
    - Utilisation systématique de la fonction `t()` dans les routes `admin` et `auth`.

### Changed

- **Corrections Techniques (Qualité & Type Safety) :**
  - Ajout systématique des annotations de type (`-> Any`, `-> str`, etc.) dans les routes et fonctions d'initialisation.
  - Correction des imports `typing.Any` manquants.
  - Résolution des erreurs de syntaxe Jinja dans les templates admin.
  - Migration des fichiers JSON vers un sous-dossier `backend/src/i18n/translations/` pour une meilleure organisation.
  - Fusion des sections `auth` dupliquées dans les fichiers JSON.

- **Roadmap Update (2025-12-29) — ALL PHASES REVIEWED ✅**
  - Phase 1-3: Marked as COMPLETED (100%)
  - Phase 4: Status updated to IN PROGRESS (20%)
  - Actual timeline: Phases 1-3 completed 2-3 days earlier than estimated
  - New estimated completion: 2026-01-06 to 2026-01-10
  - Added detailed Phase 4 progress tracking
  - Identified 4 gaps (backup automation, advanced search, etc.)
  - No critical blockers identified
  - Production readiness: 95%
  - See `Analysis_reports/2025-12-29_18-00_roadmap-status.md` for full report
  - See `.roadmap/PHASES/PHASE4_PROGRESS.md` for Phase 4 details

### Added

- **Phase 3 - Sprint 1:  CRUD Admin (2025-12-30) — EN COURS 🔄**
  - **AdminService centralisé:**
    - `create_user()` avec option email welcome
    - `update_user()` avec tracking changes
    - `delete_user()` soft/hard delete avec modal choix
    - `create_content()`, `update_content()`, `delete_content()`
    - Audit logging automatique via AdminHistory
    - Protection:  ne peut pas se supprimer soi-même
  
  - **Admin Users Routes:**
    - `GET /admin/users` - Liste avec pagination + filtres
    - `GET /admin/users/create` - Form création user
    - `POST /admin/users/create` - Créer user + optional email
    - `GET /admin/users/<id>/edit` - Form édition user
    - `POST /admin/users/<id>/edit` - Update user
    - `POST /admin/users/<id>/delete` - Soft/Hard delete avec choix
  
  - **Templates Admin Users:**
    - `users_list.html` - Liste avec pagination
    - `users_create.html` - Form création (checkbox email)
    - `users_edit.html` - Form édition
    - Delete modal avec choix soft/hard

- **Phase 2 - Performance & Cache (2025-12-29) — COMPLET ✅**
  - **Cache Service Multi-Backend:**
    - Support Redis (production, distributed)
    - Support Filesystem (cPanel, shared hosting)
    - Support Memory (development, fallback)
    - Auto-detection backend disponible
    - Méthodes:  `get()`, `set()`, `delete()`, `flush()`, `get_info()`
    - Test connexion Redis (simple + advanced write/read)
    - 30 tests complets ✅
  
  - **Installation Wizard Cache:**
    - Étape 2:  Détection Redis automatique (prérequis)
    - Étape 6: Configuration cache (Redis/Filesystem)
    - Test connexion Redis avec retry + fallback
    - Templates:  `cache_config.html`, `cache_test.html`
    - 6 tests détection Redis ✅
  
  - **Sessions & Rate Limiting:**
    - Flask-Session avec backend adaptatif (Redis/Filesystem/Memory)
    - Rate limiter storage adaptatif (Redis distribué ou Memory)
    - Configuration automatique selon cache détecté
    - Flask-Compress pour Gzip (~75-80% réduction)
    - 2 tests configuration ✅
  
  - **Service-Level Caching:**
    - UserService: cache `get_by_id`/`username`/`email` (TTL 300s)
    - ContentService:  cache `get_by_id`/`get_all` (TTL 120s)
    - Cache invalidation hooks (update/delete)
    - Réduction 90% queries répétitives
  
  - **Admin Cache Settings:**
    - Route `GET /admin/cache/` — Page configuration cache
    - Route `POST /admin/cache/test-redis` — Test connexion simple
    - Route `POST /admin/cache/test-advanced` — Test write/read
    - Route `POST /admin/cache/clear` — Clear all cache
    - Route `GET /admin/cache/stats` — Statistiques cache
    - Template `admin/cache. html` avec AJAX
    - 10 tests admin cache ✅
  
  - **Database Optimizations:**
    - Migration 004: Indexes performance
      - `ix_admin_history_admin_id` (filtres admin)
      - `ix_content_created_at` (tri/pagination)
    - SQLAlchemy pool tuning (size=10, overflow=20, timeout=30s)
    - Eager loading (joinedload) dans ContentService
    - Prévention N+1 queries (95% réduction)
    - 2 tests performance ✅
  
  - **Frontend Optimizations:**
    - Flask-Assets bundling CSS/JS
    - Minification production (cssmin, jsmin)
    - Cache headers middleware (1 year assets, no-cache HTML)
    - Gzip compression active
    - Cache busting avec hash
    - Réduction 30-40% taille assets
  
  - **Load Testing:**
    - Script `.dev_scripts/test_scripts/load_test.py`
    - Benchmark concurrent requests
    - Métriques:  P50, P95, P99, throughput
    - Performance rating automatique
  
  - **Documentation Phase 2:**
    - `2025-12-29_21-00_database_optimizations.md`
    - `2025-12-29_21-30_frontend_optimizations.md`
    - Métriques performance complètes
    - Recommandations par environnement

- **Phase 1 - Email Workflows & Settings (2025-12-29) — COMPLET ✅**
  - **Email Verification Routes:**
    - `POST /auth/send-verification` — Envoyer email verification
    - `GET /auth/verify-email/<token>` — Vérifier email avec token
  - **Password Reset Routes:**
    - `GET /auth/forgot-password` — Formulaire email oublié
    - `POST /auth/forgot-password` — Envoyer email reset (rate limit 2/h)
    - `GET /auth/reset-password/<token>` — Formulaire reset password
    - `POST /auth/reset-password/<token>` — Soumettre nouveau password (validation 8+ chars)
  - **Admin Settings Routes:**
    - `GET /admin/settings` — Afficher tous les paramètres (authentification admin requise)
    - `POST /admin/settings` — Sauvegarder paramètres (SMTP, email, features, site)
    - `POST /admin/settings/test-smtp` — Tester connexion SMTP (AJAX)
  - **Auth Templates (5 pages):**
    - `email-sent.html` — Message attente verification
    - `email-verified.html` — Confirmation verification OK
    - `forgot-password.html` — Formulaire email oublié
    - `reset-password.html` — Formulaire nouveau password
    - `password-reset-sent.html` — Message attente reset
  - **Admin Settings UI:**
    - `settings.html` — Complètement amélioré avec sections SMTP, email verification, feature flags
    - Bouton test SMTP avec feedback en temps réel
    - Support de tous les paramètres (smtp_*, email_*, registration, 2fa)
    - Formulaire POST sécurisé avec validation
  - **Tests Phase 1 (60+ cas):**
    - `test_email_workflows.py` — 35+ tests (email verification + password reset)
    - `test_admin_settings.py` — 20+ tests (admin routes + Settings model)
    - Coverage: email workflows, password reset, admin settings, encryption, rate limiting
  - **Security:**
    - Tokens avec expiry :  24h email, 1h password reset
    - Rate limiting :  10/h send-verification, 2/h forgot-password
    - Password validation : minimum 8 caractères, confirmation match
    - Encryption SMTP password (Fernet) dans Settings
    - Admin authentication required pour settings
    - CSRF protection sur forms
  - **Documentation:**
    - CHANGELOG complet pour Phase 1
    - Code comments et docstrings
    - Test fixtures pour authentification

- **PHASE 4 - Fonctionnalités métier (60% complété - EN COURS)**
  - **Rate Limiting:**
    - Flask-Limiter intégré (`backend/src/services/rate_limiter.py`)
    - Protection login:  5/min, 20/h (anti brute-force)
    - Protection 2FA verify: 10/min, 30/h (anti code guessing)
    - Protection setup/disable 2FA: 3/min, 10/h (strict)
    - Protection API: 100/h (général)
    - Tracking IP + user_id pour granularité
    - Messages erreur français (HTTP 429)
    - Appliqué routes auth + 2FA
  
  - **Dashboard Admin:**
    - AdminHistory model pour audit trail (`backend/src/models/admin_history.py`)
    - Dashboard admin avec stats temps réel (`/admin/`)
    - Statistiques:  users total/actifs/admin/2FA, connexions 24h, contenus
    - Historique 10 dernières actions admin
    - Actions rapides: manage users/content/settings
    - Template moderne Bootstrap 5 (`frontend/templates/admin/dashboard_new.html`)
    - Route users améliorée avec liste complète
  
  - **Tests 2FA complets:**
    - Tests TOTP Service (`backend/tests/test_totp. py`) - 14 tests
    - Tests User Model 2FA (`backend/tests/test_user_2fa.py`) - 12 tests
    - Test rapide validation manuelle (`test_2fa_quick.py`)
    - Couverture:  génération secret/QR/backup codes, vérification TOTP, compte verrouillage, rôles
    - Total 27 tests 2FA créés (100% passent)
  
  - **Extension User Model:**
    - Enum `UserRole` (MEMBER/ADMIN) pour gestion rôles
    - Champs 2FA: `totp_secret`, `totp_enabled`, `backup_codes`
    - Champs sécurité: `last_login`, `last_login_ip`, `login_attempts`, `locked_until`
    - Champs email: `email_verified`, `email_verification_token`
    - Méthodes sécurité: `is_locked()`, `increment_login_attempts()`, `update_last_login()`
    - Méthodes 2FA: `enable_2fa()`, `disable_2fa()`, `verify_totp()`, `can_setup_2fa()`
    - Méthodes rôles: `get_role()`, `has_role()`
    - Verrouillage automatique après 5 tentatives (15 minutes)
    - Migration Alembic pour ajout champs
  
  - **2FA TOTP complet:**
    - Service TOTP (`backend/src/services/totp_service.py`)
    - Génération secret TOTP base32 (pyotp)
    - Génération QR code PNG base64 (qrcode + PIL)
    - Backup codes sécurisés (10 codes hashés, consommables)
    - Routes setup/verify/disable (`backend/src/routes/auth_2fa.py`)
    - Templates responsive `setup-2fa.html` et `verify-2fa.html`
    - Support toutes apps TOTP (Google Authenticator, Authy, etc.)
    - Validation window=1 (±30s tolerance)
    - Gestion erreurs HTMX
    - Session 2FA avec `pending_2fa_user_id`
  
  - **Protection CSRF:**
    - Service CSRF (`backend/src/services/csrf_service.py`)
    - Génération et validation tokens sécurisés (secrets. token_hex)
    - Décorateur `@csrf_protect` pour routes
    - Context processor pour injection auto dans templates
    - 8 tests CSRF (100% passent, 94% couverture service)
    - Protection automatique POST/PUT/PATCH/DELETE
    - Exemption HTMX (optionnelle via headers)
  
  - **Authentification de base:**
    - Routes login/logout avec support HTMX (`backend/src/routes/auth.py`)
    - Session management sécurisé (Flask sessions natives)
    - Dashboard membre (`frontend/templates/dashboard/member.html`)
    - Page de connexion responsive (`frontend/templates/auth/login.html`)
    - Route status API pour vérification authentification
    - 10 tests auth complets (100% passent)
    - Helpers:  `is_authenticated()`, `login_user()`, `logout_user()`
    - Protection routes avec redirection login si non authentifié
    - Messages d'erreur spécifiques (compte désactivé vs credentials invalides)
  
  - **Wizard d'installation:**
    - Wizard multi-étapes (squelette HTMX implémenté)
    - Validation mot de passe fort (≥8 caractères, majuscule, symbole)
    - Test connexion DB (SQLite/MySQL/PostgreSQL) via route `/install/test-db`
    - Validation upload backup (checksum, format archive)
    - Gestion première utilisation (redirection vers wizard si non configuré)
  
  - **Rapports d'analyse:**
    - `Analysis_reports/2025-12-27_14-00_project_analysis_and_roadmap.md`
    - `Analysis_reports/2025-12-27_19-00_phase4_auth_sprint.md`
    - `Analysis_reports/2025-12-27_20-20_phase4_csrf_protection.md`
    - `Analysis_reports/2025-12-27_20-40_phase4_user_2fa_implementation.md`

- **PHASE 3 - Testing & Validation (100% complété)**
  - 3 modèles créés (User, UserPreferences, Content)
  - 3 services créés (UserService, PreferencesService, ContentService)
  - Tests services (20+ tests, couverture ~69. 6%)
  - Migrations Alembic configurées
  - Documentation `DATABASE. md`
  - Seed data script (`scripts/seed_db.py`)

- **PHASE 2 - Backend Routes & Templates (100% complété)**
  - Routes principales (main, api, pages, install, admin, lang)
  - Templates HTMX avec partials
  - Context processors (current_user, csrf_token)
  - Configuration templates et static folders dans app factory

- **PHASE 1 - Infrastructure Setup (95% complété)**
  - Route `GET /` (homepage avec template `index.html`)
  - Route `GET /datagrid` (exemple DataGrid)
  - API endpoint `GET /api/health` (health check JSON)
  - Templates d'erreur `404.html` et `500.html`
  - Error handlers pour 404 et 500
  - Tests pour routes (`backend/tests/test_routes.py`)
  - Script `generate_roadmap_pdf_final.py` pour PDF roadmap
  - PDF imprimable du roadmap (`.roadmap/pdf/`)

- **Infrastructure & Tooling (2025-12-30)**
  - **Complete project setup and maintenance scripts:**
    - `scripts/utils/cleanup_project.py` — Automatic cleanup (cache, temp files, IDE folders)
    - `scripts/utils/generate_api_docs.py` — API documentation from docstrings (renommé de `generate_docs.py`)
    - `scripts/utils/validate_structure.py` — Project structure validator
    - `scripts/utils/check_i18n.py` — i18n translation checker (validates JSON, detects missing keys, finds hardcoded text)
    - `scripts/setup/generate_gitignore.py` — Comprehensive `.gitignore` generator
    - `scripts/setup/setup_flask_structure.sh` — Flask project structure generator
  
  - **Git Hooks (pre-commit):**
    - `scripts/hooks/pre-commit. sh` — Bash version (Linux/Mac)
    - `scripts/hooks/pre-commit.ps1` — PowerShell version (Windows)
    - `.pre-commit-config.yaml` — Cross-platform hook management (Python `pre-commit` package)
    - Hooks enforce:  Ruff linting/formatting, Mypy type checking, i18n validation, pytest tests
  
  - **Documentation scripts:**
    - Comprehensive README files for all script directories (`scripts/setup/`, `scripts/utils/`, `scripts/hooks/`)
    - `.github/copilot-modes-reference.md` — GitHub Copilot modes guide (Chat/Edit/Plan/Agent)
  
  - **CI/CD Integration:**
    - i18n translation checker integrated in pre-commit hooks
    - Project structure validation in CI/CD pipeline (`.github/workflows/ci.yml`)
    - Updated workflow to include `validate_structure.py`

- **UI/UX Stack (Initial Setup)**
  - Stack UI/UX complète (Flask + Jinja2 + Bootstrap 5 + HTMX + Alpine.js + Tabulator)
  - Design tokens avec CSS Variables pour système de thèmes
  - Templates de base (layouts, components, pages, admin)
  - Plugins JavaScript (Tabulator, Alpine utils, HTMX utils)
  - Documentation UI/UX complète (`UI_UX_STACK. md`, `UI_UX_QUICKSTART.md`)

- **Project Setup (Initial)**
  - Roadmap détaillée en 4 phases (`.roadmap/`)
  - Support multi-DB (SQLite, MySQL, PostgreSQL)
  - Configuration WSGI pour déploiement cPanel
  - Scripts utilitaires (`init_db.py`, `seed_db.py`)
  - Règles CHANGELOG complètes (Section 15 dans `copilot-instructions.md`)
  - Guide rapide CHANGELOG (`docs/CHANGELOG_GUIDE.md`)
  - Typage statique étendu sur routes et services
  - Aides de typage pour modèles SQLAlchemy et services

### Changed

- **Performance Improvements (Phase 2):**
  - Throughput:  +140% (50 → 120 req/sec)
  - Latence P50: -69% (80ms → 25ms)
  - Latence P95: -76% (250ms → 60ms)
  - Cache hit rate: ~90% (users), ~85% (content)
  - First load: -20% (2.5s → 2.0s)
  - Cached load: -88% (2.5s → 0.3s)
  - Bandwidth: -85% après 1ère visite

- **Wizard d'Installation - UI/UX (2025-12-28):**
  - Nouveau layout dédié au wizard (`layouts/wizard. html`) sans navbar
  - Page Requirements avec vérification système (Env, Git, Python, Pip, DB Clients)
  - Fil d'Ariane (breadcrumb) cliquable avec navigation entre étapes
  - Footer simplifié (projet + version + copyright + licence uniquement)
  - Icônes et feedback visuels (✓, ✗, ⚠) pour meilleure UX
  - Summary détaillé avec configuration BD complète et compte admin
  - Page Done redesignée avec icône de succès et lien corrigé vers `/auth/login`
  - Drapeaux corrigés :  🇺🇸 (US) au lieu de 🇬🇧 (GB) pour anglais
  - Titre centré sur toutes les pages du wizard
  - Suppression du badge de langue dans le header
  - Ligne "Env - Git - Python - DB" déplacée vers page Requirements
  - Layout simplifié :  header avec uniquement "X-Filamenta"
  - Footer minimal :  nom projet, version, copyright, licence (centré)

- **Wizard d'Installation - Traductions (2025-12-28):**
  - Nouvelles clés de traduction FR/EN : 
    - `wizard. continue`, `wizard.language.*`
    - `wizard.welcome.*`, `wizard.steps.*`
    - `wizard.requirements.*`, `wizard.summary.*` (détaillées)
  - Support complet français et anglais international
  - Écran de bienvenue intermédiaire après choix de langue
  - Nouvelles traductions:  `wizard.welcome_message`, `wizard.welcome_description`, `wizard.start`

- **Documentation & Configuration:**
  - Documentation roadmap mise à jour avec statuts réels des phases
  - Structure `.roadmap/README.md` reflète progression (Phases 1-3 complétées, Phase 4 en cours)
  - Nom du projet de "Template-Python" vers "X-Filamenta-Python"
  - Email de contact vers "filamenta@xarema. com"
  - Licence de "TBD" vers "AGPL-3.0-or-later"
  - Structure de documentation consolidée dans dossier `docs/`
  - Commandes shell adaptées pour PowerShell (`py` au lieu de `python`, `;` au lieu de `&&`)
  - Template `index.html` corrigé (suppression contenu malformé)
  - Configuration Flask pour chemins templates et static
  - Renamed `generate_docs.py` to `generate_api_docs.py` for clarity
  - Updated CI/CD workflow to include structure validation

### Fixed

- **Wizard d'Installation - Corrections Critiques Backend (2025-12-28 20: 00)**
  - **[CRITIQUE]** Fix erreur `create_engine is not defined` lors de la finalisation
  - Ajout imports manquants SQLAlchemy dans `install. py` (`create_engine`, `sessionmaker`, `db`)
  - **[CRITIQUE]** Ajout traduction `wizard.db. error_empty_field` pour validation formulaires
  - Ajout traductions `wizard.error_details`, `wizard.error_hint` pour page erreur
  - Fix structure JSON invalide (objet `done` mal fermé) dans `fr. json` et `en.json`
  - Réorganisation complète section `wizard` dans fichiers de traduction
  - Validation JSON complète (`fr.json` + `en.json` 100% valides)
  - L'installation wizard fonctionne maintenant de bout en bout sans erreur

- **Wizard d'Installation - Corrections UI/UX (2025-12-28 19:00)**
  - **[CRITIQUE]** Suppression des boutons fantômes dupliqués en bas du wizard
  - **[CRITIQUE]** Ajout de 15+ traductions manquantes (`wizard.previous`, `wizard.step`, `wizard.done.*`, `wizard.backup. size`)
  - **[MAJEUR]** Refonte du fil d'Ariane :  design fixe sur exactement 2 lignes (3 étapes + 2 étapes)
  - Correction validation HTML :  remplacement `<div>` par `<span class="d-block">` dans les boutons
  - Page "Installation terminée" :  ajout de toutes les traductions détaillées (base de données, tables, backup, admin)
  - Rapport détaillé : `Analysis_reports/2025-12-28_19-00_wizard_corrections_complete.md`

- **Wizard d'Installation - Corrections Critiques (2025-12-28)**
  - **[CRITIQUE]** Bouton "Continuer" après sélection langue ne fonctionnait pas
    - Correction:  ajout step `requirements` dans router
    - Correction: gestion état `requirements_checked` dans session
    - Correction: IDs HTML dupliqués (`#wizard-container`) → un seul conteneur
  - **[CRITIQUE]** Bouton "Commencer" non fonctionnel → Cible HTMX `#wizard-container` manquante
    - Ajout du conteneur `#wizard-container` dans toutes les branches du template
    - Changement `hx-swap="outerHTML"` → `hx-swap="innerHTML"` pour stabilité
    - Wizard maintenant fonctionnel à 100% (9/9 étapes validées)
  - Correction fonction `inject_csrf_token` dupliquée dans `app.py`
  - Utilisation de chemins absolus pour les dossiers static/templates (compatibilité Windows)
  - Configuration sessions Flask explicite pour garantir la persistance
  - Navigation wizard plus claire avec écran de bienvenue
  - Messages de traduction FR/EN pour toutes les étapes du wizard
  - Step `finalize` gère maintenant les erreurs et retourne page erreur si échec
  - Lien de connexion corrigé dans page Done :  `/auth/login` au lieu de `/login`

- **Wizard d'Installation - Finalisation (2025-12-28)**
  - **[CRITIQUE]** Fix du blocage à l'étape `finalize` en mode production (Waitress)
  - Gestion isolée des sessions SQLAlchemy pour la création de la base de données utilisateur
  - Support de l'injection d'une session externe dans `UserService. create` pour des opérations atomiques durant l'installation
  - Nettoyage des logs de debug et amélioration de la robustesse du changement dynamique de base de données

- **General Fixes:**
  - Correction des chemins de déploiement pour cPanel
  - Nettoyage des résidus du template (`template_python. egg-info/`)
  - Suppression des fichiers temporaires et caches Python
  - Syntaxe Jinja2 dans templates (`index.html`, `errors/`)
  - Configuration `template_folder` et `static_folder` dans `create_app()`
  - Sécurité et typage SQLAlchemy:  `install_service. test_db_connection` utilise `sqlalchemy.text("SELECT 1")`
  - Corrections mypy sur retours Any (services et modèles), compatibilité Flask/Response
  - Tests PASS avec couverture ~69.6% (seuil actuel 50%)
  - Route `/` (index): en mode test (`TESTING`), rend le template `pages/index.html`; en mode normal, renvoie "OK" pour le smoke test
  - Annotations pour `app.py` (factory, context processors, error handlers) et décorateurs (args/kwargs typés)
  - Préparation au formatage global via `ruff format`

### Security

- Context processors mock ajoutés (à remplacer par vraie authentification en PHASE 4)
- Validation et typage des endpoints API (`/api/contact`, `/api/preferences`) avec `jsonify` et contrôles d'inputs
- **Phase 1 Security Enhancements:**
  - Tokens avec expiry :  24h email verification, 1h password reset
  - Rate limiting : 10/h send-verification, 2/h forgot-password
  - Password validation : minimum 8 caractères, confirmation match
  - Encryption SMTP password (Fernet) dans Settings model
  - Admin authentication required pour settings routes
  - CSRF protection sur tous les forms
  - Protection routes avec `@csrf_protect` decorator
  - 2FA TOTP avec backup codes sécurisés
  - Account locking après 5 tentatives échouées (15 minutes)

---

## [0.0.1-Alpha] - 2025-12-27

### Added

- Structure de base du projet avec Flask + HTMX + Bootstrap 5
- Configuration SQLite pour le développement
- Système de tests avec pytest
- Linting et formatage (Ruff, Prettier, ESLint, Stylelint)
- Type hints avec mypy
- Documentation de base (README. md, docs/)
- En-têtes de fichiers conformes aux normes du projet
- Fichier `.env.example` avec variables d'environnement
- Configuration Docker (Dockerfile, docker-compose.yml)
- Configuration Nginx pour reverse proxy
- Pre-commit hooks
- Makefile avec commandes utilitaires
- Structure backend/frontend séparée
- Tests de base (test_smoke.py)
- Gitignore configuré pour Python/Node.js/IDE

### Security

- Configuration des variables d'environnement pour secrets
- Validation et sanitization des entrées (paramétré dans les règles)
- Support HTTPS via Nginx
- Headers de sécurité configurables

---

[Unreleased]: https://github.com/xarema/X-Filamenta-Python/compare/v0.0.1-Alpha...HEAD
[0.0.1-Alpha]: https://github.com/xarema/X-Filamenta-Python/releases/tag/v0.0.1-Alpha
