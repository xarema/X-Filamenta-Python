# CHANGELOG — X-Filamenta-Python

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

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
    - Tokens avec expiry : 24h email, 1h password reset
    - Rate limiting : 10/h send-verification, 2/h forgot-password
    - Password validation : minimum 8 caractères, confirmation match
    - Encryption SMTP password (Fernet) dans Settings
    - Admin authentication required pour settings
    - CSRF protection sur forms
  - **Documentation:**
    - CHANGELOG complet pour Phase 1
    - Code comments et docstrings
    - Test fixtures pour authentification

### Fixed

- **Wizard d'Installation - Corrections Critiques Backend (2025-12-28 20:00)**
  - **[CRITIQUE]** Fix erreur `create_engine is not defined` lors de la finalisation
  - Ajout imports manquants SQLAlchemy dans `install.py` (create_engine, sessionmaker, db)
  - **[CRITIQUE]** Ajout traduction `wizard.db.error_empty_field` pour validation formulaires
  - Ajout traductions `wizard.error_details`, `wizard.error_hint` pour page erreur
  - Fix structure JSON invalide (objet `done` mal fermé) dans fr.json et en.json
  - Réorganisation complète section `wizard` dans fichiers de traduction
  - Validation JSON complète (fr.json + en.json 100% valides)
  - L'installation wizard fonctionne maintenant de bout en bout sans erreur

- **Wizard d'Installation - Corrections UI/UX (2025-12-28 19:00)**
  - **[CRITIQUE]** Suppression des boutons fantômes dupliqués en bas du wizard
  - **[CRITIQUE]** Ajout de 15+ traductions manquantes (wizard.previous, wizard.step, wizard.done.*, wizard.backup.size)
  - **[MAJEUR]** Refonte du fil d'Ariane : design fixe sur exactement 2 lignes (3 étapes + 2 étapes)
  - Correction validation HTML : remplacement `<div>` par `<span class="d-block">` dans les boutons
  - Page "Installation terminée" : ajout de toutes les traductions détaillées (base de données, tables, backup, admin)
  - Rapport détaillé : `Analysis_reports/2025-12-28_19-00_wizard_corrections_complete.md`

### Added (Précédent)

- **Documentation Centralisée (2025-12-28)**
  - Nouveau fichier `.github/READ_BEFORE_ANY_CHANGE.md` : centralise TOUTES les règles du projet
  - Checklist complète avant modification
  - Workflow de développement étape par étape
  - Historique des erreurs à éviter
  - Commandes essentielles (kill serveurs, lint, tests)
  - Tests obligatoires avant validation

- **Script de démarrage de production (Windows)**
  - Nouveau script `run_prod.ps1` pour lancer le serveur Waitress en utilisant automatiquement l'environnement virtuel `.venv`.
  - Simplification de l'exécution pour les utilisateurs Windows n'ayant pas `python` dans leur PATH.
  - Mise à jour du `README.md` avec les instructions pour le mode production local.

- **Wizard d'Installation - Correction Finalisation (2025-12-28)**
  - **[CRITIQUE]** Fix du blocage à l'étape `finalize` en mode production (Waitress).
  - Gestion isolée des sessions SQLAlchemy pour la création de la base de données utilisateur.
  - Support de l'injection d'une session externe dans `UserService.create` pour des opérations atomiques durant l'installation.
  - Nettoyage des logs de debug et amélioration de la robustesse du changement dynamique de base de données.

- **Wizard d'Installation - Refonte UI/UX Complète (2025-12-28)**
  - Nouveau layout dédié au wizard (`layouts/wizard.html`) sans navbar
  - Page Requirements avec vérification système (Env, Git, Python, Pip, DB Clients)
  - Fil d'Ariane (breadcrumb) cliquable avec navigation entre étapes
  - Footer simplifié (projet + version + copyright + licence uniquement)
  - Icônes et feedback visuels (✓, ✗, ⚠) pour meilleure UX
  - Summary détaillé avec configuration BD complète et compte admin
  - Page Done redesignée avec icône de succès et lien corrigé vers `/auth/login`
  - Documentation de test complète (`docs/TEST_WIZARD_REDESIGN.md`)
  - Rapport d'analyse détaillé (`Analysis_reports/2025-12-28_02-30_wizard_redesign.md`)

- **Wizard d'Installation - Traductions Complètes**
  - Nouvelles clés de traduction FR/EN :
    - `wizard.continue`, `wizard.language.*`
    - `wizard.welcome.*`, `wizard.steps.*`
    - `wizard.requirements.*`, `wizard.summary.*` (détaillées)
  - Support complet français et anglais international

- **Wizard d'Installation - Améliorations UX**
  - Écran de bienvenue intermédiaire après choix de langue
  - Nouvelles traductions: `wizard.welcome_message`, `wizard.welcome_description`, `wizard.start`
  - Script de test manuel complet (`scripts/tests/test_wizard_manual.py`)
  - Configuration explicite des sessions Flask (cookies HTTPOnly, SameSite)

### Changed

- **Wizard d'Installation - UI/UX**
  - Drapeaux corrigés : 🇺🇸 (US) au lieu de 🇬🇧 (GB) pour anglais
  - Titre centré sur toutes les pages du wizard
  - Suppression du badge de langue dans le header
  - Ligne "Env - Git - Python - DB" déplacée vers page Requirements
  - Layout simplifié : header avec uniquement "X-Filamenta"
  - Footer minimal : nom projet, version, copyright, licence (centré)

### Fixed

- **Wizard d'Installation - Corrections Critiques**
  - **[CRITIQUE]** Bouton "Continuer" après sélection langue ne fonctionnait pas
    - Correction: ajout step `requirements` dans router
    - Correction: gestion état `requirements_checked` dans session
    - Correction: IDs HTML dupliqués (`#wizard-container`) → un seul conteneur
  - **[CRITIQUE]** Bouton "Commencer" non fonctionnel → Cible HTMX `#wizard-container` manquante
    - Ajout du conteneur `#wizard-container` dans toutes les branches du template
    - Changement `hx-swap="outerHTML"` → `hx-swap="innerHTML"` pour stabilité
    - Wizard maintenant fonctionnel à 100% (9/9 étapes validées)
  - Correction fonction `inject_csrf_token` dupliquée dans `app.py` [BUG]
  - Utilisation de chemins absolus pour les dossiers static/templates (compatibilité Windows)
  - Configuration sessions Flask explicite pour garantir la persistance
  - Navigation wizard plus claire avec écran de bienvenue
  - Messages de traduction FR/EN pour toutes les étapes du wizard
  - Step `finalize` gère maintenant les erreurs et retourne page erreur si échec
  - Lien de connexion corrigé dans page Done : `/auth/login` au lieu de `/login`

### Added (suite)

- **PHASE 4 - Fonctionnalités métier (60% complété - EN COURS)**
  - **Rate Limiting (NOUVEAU)**
    - Flask-Limiter intégré (`backend/src/services/rate_limiter.py`)
    - Protection login: 5/min, 20/h (anti brute-force)
    - Protection 2FA verify: 10/min, 30/h (anti code guessing)
    - Protection setup/disable 2FA: 3/min, 10/h (strict)
    - Protection API: 100/h (général)
    - Tracking IP + user_id pour granularité
    - Messages erreur français (HTTP 429)
    - Appliqué routes auth + 2FA
  - **Dashboard Admin (NOUVEAU)**
    - AdminHistory model pour audit trail (`backend/src/models/admin_history.py`)
    - Dashboard admin avec stats temps réel (`/admin/`)
    - Statistiques: users total/actifs/admin/2FA, connexions 24h, contenus
    - Historique 10 dernières actions admin
    - Actions rapides: manage users/content/settings
    - Template moderne Bootstrap 5 (`frontend/templates/admin/dashboard_new.html`)
    - Route users améliorée avec liste complète
  - **Tests 2FA complets**
    - Tests TOTP Service (`backend/tests/test_totp.py`) - 14 tests
    - Tests User Model 2FA (`backend/tests/test_user_2fa.py`) - 12 tests
    - Test rapide validation manuelle (`test_2fa_quick.py`)
    - Couverture: génération secret/QR/backup codes, vérification TOTP, compte verrouillage, rôles
    - Total 27 tests 2FA créés (100% passent)
  - **Extension User Model**
    - Enum `UserRole` (MEMBER/ADMIN) pour gestion rôles
    - Champs 2FA: `totp_secret`, `totp_enabled`, `backup_codes`
    - Champs sécurité: `last_login`, `last_login_ip`, `login_attempts`, `locked_until`
    - Champs email: `email_verified`, `email_verification_token`
    - Méthodes sécurité: `is_locked()`, `increment_login_attempts()`, `update_last_login()`
    - Méthodes 2FA: `enable_2fa()`, `disable_2fa()`, `verify_totp()`, `can_setup_2fa()`
    - Méthodes rôles: `get_role()`, `has_role()`
    - Verrouillage automatique après 5 tentatives (15 minutes)
    - Migration Alembic pour ajout champs
  - **2FA TOTP complet**
    - Service TOTP (`backend/src/services/totp_service.py`)
    - Génération secret TOTP base32 (pyotp)
    - Génération QR code PNG base64 (qrcode + PIL)
    - Backup codes sécurisés (10 codes hashés, consommables)
    - Routes setup/verify/disable (`backend/src/routes/auth_2fa.py`)
    - Templates responsive setup-2fa.html et verify-2fa.html
    - Support toutes apps TOTP (Google Authenticator, Authy, etc.)
    - Validation window=1 (±30s tolerance)
    - Gestion erreurs HTMX
    - Session 2FA avec `pending_2fa_user_id`
  - **Protection CSRF**
    - Service CSRF (`backend/src/services/csrf_service.py`)
    - Génération et validation tokens sécurisés (secrets.token_hex)
    - Décorateur `@csrf_protect` pour routes
    - Context processor pour injection auto dans templates
    - 8 tests CSRF (100% passent, 94% couverture service)
    - Protection automatique POST/PUT/PATCH/DELETE
    - Exemption HTMX (optionnelle via headers)
  - **Authentification de base**
    - Routes login/logout avec support HTMX (`backend/src/routes/auth.py`)
    - Session management sécurisé (Flask sessions natives)
    - Dashboard membre (`frontend/templates/dashboard/member.html`)
    - Page de connexion responsive (`frontend/templates/auth/login.html`)
    - Route status API pour vérification authentification
    - 10 tests auth complets (100% passent)
    - Helpers: `is_authenticated()`, `login_user()`, `logout_user()`
    - Protection routes avec redirection login si non authentifié
    - Messages d'erreur spécifiques (compte désactivé vs credentials invalides)
  - Wizard d'installation multi-étapes (squelette HTMX implémenté)
  - Validation mot de passe fort (≥8 caractères, majuscule, symbole)
  - Test connexion DB (SQLite/MySQL/PostgreSQL) via route `/install/test-db`
  - Validation upload backup (checksum, format archive)
  - Gestion première utilisation (redirection vers wizard si non configuré)
  - Rapport de progression PHASE 4 (.roadmap/PHASES/PHASE4_PROGRESS.md)
  - Analyses complètes du projet (Analysis_reports/)
    - 2025-12-27_14-00_project_analysis_and_roadmap.md
    - 2025-12-27_19-00_phase4_auth_sprint.md
    - 2025-12-27_20-20_phase4_csrf_protection.md
    - 2025-12-27_20-40_phase4_user_2fa_implementation.md

- **PHASE 3 - Testing & Validation (100% complété)**
  - 3 modèles créés (User, UserPreferences, Content)
  - 3 services créés (UserService, PreferencesService, ContentService)
  - Tests services (20+ tests, couverture ~69.6%)
  - Migrations Alembic configurées
  - Documentation DATABASE.md
  - Seed data script (scripts/seed_db.py)

- **PHASE 2 - Backend Routes & Templates (100% complété)**
  - Routes principales (main, api, pages, install, admin, lang)
  - Templates HTMX avec partials
  - Context processors (current_user, csrf_token - à finaliser en Phase 4)
  - Configuration templates et static folders dans app factory

- **PHASE 1 - Infrastructure Setup (95% complété)**
  - Route GET / (homepage avec template index.html)
  - Route GET /datagrid (exemple DataGrid)
  - API endpoint GET /api/health (health check JSON)
  - Templates d'erreur 404.html et 500.html
  - Error handlers pour 404 et 500
  - Tests pour routes (backend/tests/test_routes.py)
  - Script generate_roadmap_pdf_final.py pour PDF roadmap
  - PDF imprimable du roadmap (.roadmap/pdf/)

- Stack UI/UX complète (Flask + Jinja2 + Bootstrap 5 + HTMX + Alpine.js + Tabulator)
- Design tokens avec CSS Variables pour système de thèmes
- Templates de base (layouts, components, pages, admin)
- Plugins JavaScript (Tabulator, Alpine utils, HTMX utils)
- Documentation UI/UX complète (UI_UX_STACK.md, UI_UX_QUICKSTART.md)
- Roadmap détaillée en 4 phases (.roadmap/)
- Support multi-DB (SQLite, MySQL, PostgreSQL)
- Configuration WSGI pour déploiement cPanel
- Scripts utilitaires (init_db.py, seed_db.py, generate_roadmap_pdf_final.py)
- Règles CHANGELOG complètes (Section 15 dans copilot-instructions.md)
- Guide rapide CHANGELOG (docs/CHANGELOG_GUIDE.md)
- Typage statique étendu sur routes et services
- Aides de typage pour modèles SQLAlchemy et services

### Changed

- Documentation roadmap mise à jour avec statuts réels des phases
- Structure .roadmap/README.md reflète progression (Phases 1-3 complétées, Phase 4 en cours)
- Nom du projet de "Template-Python" vers "X-Filamenta-Python"
- Email de contact vers "filamenta@xarema.com"
- Licence de "TBD" vers "AGPL-3.0-or-later"
- Structure de documentation consolidée dans dossier `docs/`
- Commandes shell adaptées pour PowerShell (py au lieu de python, ; au lieu de &&)
- Template index.html corrigé (suppression contenu malformé)
- Configuration Flask pour chemins templates et static
- Route `/` (index): en mode test (`TESTING`), rend le template `pages/index.html`; en mode normal, renvoie "OK" pour le smoke test
- Annotations pour `app.py` (factory, context processors, error handlers) et décorateurs (args/kwargs typés)
- Préparation au formatage global via `ruff format`

### Fixed

- Correction des chemins de déploiement pour cPanel
- Nettoyage des résidus du template (template_python.egg-info/)
- Suppression des fichiers temporaires et caches Python
- Syntaxe Jinja2 dans templates (index.html, errors/)
- Configuration template_folder et static_folder dans create_app()
- Sécurité et typage SQLAlchemy: `install_service.test_db_connection` utilise `sqlalchemy.text("SELECT 1")`
- Corrections mypy sur retours Any (services et modèles), compatibilité Flask/Response
- Tests PASS avec couverture ~69.6% (seuil actuel 50%)

### Security

- Context processors mock ajoutés (à remplacer par vraie authentification en PHASE 4)
- Validation et typage des endpoints API (`/api/contact`, `/api/preferences`) avec `jsonify` et contrôles d’inputs

---

## [0.0.1-Alpha] - 2025-12-27

### Added

- Structure de base du projet avec Flask + HTMX + Bootstrap 5
- Configuration SQLite pour le développement
- Système de tests avec pytest
- Linting et formatage (Ruff, Prettier, ESLint, Stylelint)
- Type hints avec mypy
- Documentation de base (README.md, docs/)
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

**Résultat :** Le package peut maintenant être installé avec `pip install -e .`

---

### 4. Rapports d'analyse (règle 7)

**Dossier créé :** `Analysis_reports/`

**Rapports générés :**

- ✅ `rapport_conformite_2025-12-26_compliance.md` — Audit complet de conformité

---

### 5. Documentation utilisateur

**README.md mis à jour avec :**

- Badges de version (0.0.1-Alpha)
- Structure du projet complète
- Instructions d'installation incluant `pip install -e .`
- Documentation des variables d'environnement
- Commandes de validation
- Règles de contribution
- Références aux rapports d'analyse

**Fichier créé :**

- ✅ `.env.example` — Template pour les variables d'environnement

---

### 6. Versioning (règle 6)

**Versions définies :**

- App version: `0.0.1-Alpha`
- File version: `0.0.1-Alpha` (pour chaque fichier)
- Package version: `0.0.1-alpha` (dans pyproject.toml)

**Prochains jalons :**

- `0.1.0-Beta` — Ajout templates HTML/static CSS/JS
- `1.0.0` — Première version stable (couverture tests ≥80%)

---

## 🧪 Validation

### Tests exécutés

```bash
✅ ruff check .           # Aucune erreur
✅ ruff format --check .  # Code formaté
✅ mypy backend/src       # Typage correct
✅ pytest -v              # 1 test passé, couverture 52%
```

### Résultats

| Outil       | Statut  | Notes                                 |
| ----------- | ------- | ------------------------------------- |
| Ruff        | ✅ Pass | Aucune erreur de linting              |
| Ruff format | ✅ Pass | Code formaté (line-length=88)         |
| Mypy        | ✅ Pass | Typage statique correct               |
| Pytest      | ✅ Pass | 1/1 test passé, couverture 52% (≥50%) |

---

## 📁 Nouveaux fichiers

```
Template-Python/
├── Analysis_reports/
│   └── rapport_conformite_2025-12-26_compliance.md    [NEW]
├── .env.example                                        [NEW]
├── README.md                                           [UPDATED]
├── pyproject.toml                                      [UPDATED]
└── backend/
    ├── src/
    │   ├── __init__.py                                 [UPDATED]
    │   ├── __main__.py                                 [UPDATED]
    │   └── app.py                                      [UPDATED]
    └── tests/
        ├── __init__.py                                 [UPDATED]
        └── test_smoke.py                               [UPDATED]
```

---

## 📝 Fichiers de sauvegarde

- `README_OLD.md` — Ancien README (pour référence)

---

## 🚀 Prochaines étapes recommandées

### Court terme (avant 0.1.0-Beta)

1. ⬜ Créer structure `backend/templates/` avec base.html
2. ⬜ Créer structure `backend/static/` avec CSS/JS
3. ⬜ Ajouter route exemple avec HTMX
4. ⬜ Documenter architecture dans `docs/`
5. ⬜ Ajouter validation d'inputs (exemple)

### Moyen terme (avant 1.0.0)

1. ⬜ Définir la licence finale (MIT, Apache 2.0, propriétaire)
2. ⬜ Mettre à jour SPDX-License-Identifier
3. ⬜ Augmenter couverture de tests à 80%
4. ⬜ Ajouter CI/CD (.github/workflows)
5. ⬜ Documentation API complète

---

## 🔗 Références

- Règles du projet : `.github/copilot-instructions.md`
- Rapport de conformité : `Analysis_reports/rapport_conformite_2025-12-26_compliance.md`
- Semantic Versioning : https://semver.org/

---

## ✍️ Signature

**Généré par:** GitHub Copilot (Claude Sonnet 4.5)  
**Date:** 2025-12-26  
**Statut:** ✅ Terminé

---

**Copyright (c) 2025 XAREMA. All rights reserved.**
