# Guide des Prompts Agent GitHub Copilot

**Purpose:** Documentation des prompts disponibles pour GitHub Copilot Agent  
**File:** .  github/prompts/README.md | Repository:   X-Filamenta-Python

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.  

---

## 📚 Table des matières

- [Prompts de Développement](#prompts-de-développement)
  - [create-htmx-endpoint](#1-create-htmx-endpoint)
  - [add-wizard-step](#2-add-wizard-step)
  - [refactor-route](#3-refactor-route)
  - [add-feature-complete](#4-add-feature-complete)
  - [migrate-dependency](#5-migrate-dependency)
  - [fix-security-issue](#6-fix-security-issue)
- [Prompts d'Analyse](#prompts-danalyse)
  - [analyze-project-stack](#7-analyze-project-stack)
  - [list-project-features](#8-list-project-features)
- [Prompts de Qualité](#prompts-de-qualité)
  - [dev-quality](#9-dev-quality)
  - [security-audit](#10-security-audit)
  - [repository-cleanup](#11-repository-cleanup)
- [Prompts de Configuration](#prompts-de-configuration)
  - [venv-setup-windows](#12-venv-setup-windows)

---

## Prompts de Développement

### 1. create-htmx-endpoint

**Fichier:** `.github/prompts/create-htmx-endpoint.prompt. md`

#### 📝 Description

Crée un endpoint HTMX complet avec : 
- Route Flask backend
- Template partiel HTMX
- Traductions i18n (FR + EN)
- Tests pytest
- Documentation

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez : 
- ✅ Ajouter une nouvelle interaction AJAX/HTMX
- ✅ Créer un endpoint qui retourne du HTML partiel
- ✅ Implémenter une action utilisateur (supprimer, éditer, créer)
- ✅ Ajouter un formulaire avec soumission asynchrone

#### 📋 Exemples d'utilisation

**Cas 1 : Supprimer un élément de liste**
```
User story:   L'utilisateur peut supprimer un article de la liste sans recharger la page
Endpoint URL: /api/articles/<id>
Méthode: DELETE
Target: #article-{id}
Swap: outerHTML
```

**Cas 2 : Charger plus de résultats (pagination)**
```
User story:  Charger les 10 prochains résultats en cliquant sur "Plus"
Endpoint URL: /api/search/results
Méthode: GET
Target:   #results-list
Swap: afterend
```

**Cas 3 : Modifier un champ inline**
```
User story: Modifier le titre d'un article directement dans la liste
Endpoint URL:   /api/articles/<id>/title
Méthode: PUT
Target:  #article-title-{id}
Swap: outerHTML
```

#### ✅ Ce que le prompt génère

- ✅ Route Flask avec validation d'entrée
- ✅ Service layer (si logique complexe)
- ✅ Template partiel HTMX avec Bootstrap 5
- ✅ Traductions FR + EN avec fallback
- ✅ Tests (happy path + cas d'erreur)
- ✅ Mise à jour CHANGELOG. md

#### ⚠️ Prérequis

- Flask blueprint existant
- Service layer (si nécessaire)
- Templates de base (layouts, partials)
- Fichiers i18n (fr.json, en.json)

---

### 2. add-wizard-step

**Fichier:** `.github/prompts/add-wizard-step.prompt.md`

#### 📝 Description

Ajoute une nouvelle étape au wizard d'installation avec :
- Route GET (afficher formulaire) + POST (traiter données)
- Template HTML avec formulaire
- Validation des champs
- Gestion de session (sauvegarder étape)
- Traductions complètes
- Tests

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Ajouter une étape au wizard d'installation
- ✅ Configurer un nouveau paramètre (BD, cache, email, etc.)
- ✅ Collecter des données utilisateur en plusieurs étapes
- ✅ Implémenter un processus multi-étapes (onboarding, configuration)

#### 📋 Exemples d'utilisation

**Cas 1 : Configuration cache (Redis)**
```
Step Number: 6
Step Name: Configuration du cache
Description: Configurer Redis ou filesystem cache
Form Fields:  
  - cache_type (select:  redis/filesystem)
  - redis_host (text, requis si redis)
  - redis_port (number, requis si redis)
Validation: Redis host/port requis si type=redis
```

**Cas 2 : Configuration email SMTP**
```
Step Number:  7
Step Name: Configuration email
Description: Paramètres SMTP pour envoi d'emails
Form Fields:
  - smtp_server (text, requis)
  - smtp_port (number, default 587)
  - smtp_username (text, requis)
  - smtp_password (password, requis)
  - use_tls (checkbox, default true)
Validation:  Test connexion SMTP
```

**Cas 3 : Sélection fonctionnalités**
```
Step Number: 8
Step Name: Activation des fonctionnalités
Description: Choisir les modules à activer
Form Fields: 
  - enable_2fa (checkbox)
  - enable_email_verification (checkbox)
  - enable_registration (checkbox)
Validation: Aucune (optionnelles)
```

#### ✅ Ce que le prompt génère

- ✅ Route `/wizard/step<N>` (GET + POST)
- ✅ Template `wizard/step<N>.html`
- ✅ Fonction de validation (si complexe)
- ✅ Traductions FR + EN
- ✅ Mise à jour breadcrumb (fil d'Ariane)
- ✅ Tests (GET, POST success, POST error, session)
- ✅ Mise à jour CHANGELOG.md

#### ⚠️ Spécificités Wizard

- ⚠️ **Breadcrumb:** Maintenir layout 2 lignes (3 étapes + 2 étapes)
- ⚠️ **Boutons:** Utiliser partial `_step_buttons.html` (ne pas dupliquer)
- ⚠️ **Session:** Sauvegarder dans `session["wizard_step_<N>"]`
- ⚠️ **Traductions:** AUCUN texte en dur

---

### 3. refactor-route

**Fichier:** `.github/prompts/refactor-route.prompt.md`

#### 📝 Description

Refactorise une route Flask existante pour améliorer : 
- Qualité du code (extraire logique métier)
- Type hints complets
- Gestion d'erreurs robuste
- Performance
- Maintenabilité

#### 🎯 Quand l'utiliser ?

Utilisez ce prompt quand vous devez :
- ✅ Nettoyer une route trop complexe
- ✅ Extraire logique métier vers service layer
- ✅ Ajouter type hints manquants
- ✅ Améliorer gestion d'erreurs
- ✅ Optimiser performance
- ✅ Rendre code testable

#### 📋 Exemples d'utilisation

**Cas 1 : Route avec trop de logique**
```
Endpoint:  /users/<int:user_id>
Fichier: backend/src/routes/users.py
Problèmes: 
  - Logique métier dans la route (validation, calculs)
  - Pas de type hints
  - Gestion d'erreurs basique
  - Requêtes DB directes (pas de service)
Objectifs:  Extraire vers UserService, ajouter types, améliorer erreurs
```

**Cas 2 : Route N+1 queries**
```
Endpoint: /api/posts
Fichier: backend/src/routes/api.py
Problèmes:
  - N+1 queries (charge auteurs en boucle)
  - Pas de pagination
  - Pas de mise en cache
Objectifs: Eager loading, pagination, cache
```

**Cas 3 : Route sans validation**
```
Endpoint: /api/contact (POST)
Fichier: backend/src/routes/api.py
Problèmes:
  - Pas de validation d'entrée
  - Pas de sanitization
  - Pas de rate limiting
Objectifs: Validation complète, sanitize, rate limit
```

#### ✅ Ce que le prompt génère

- ✅ Route refactorisée (handler mince)
- ✅ Service layer créé/mis à jour
- ✅ Type hints complets
- ✅ Docstrings détaillés
- ✅ Gestion d'erreurs robuste
- ✅ Logging approprié
- ✅ Tests mis à jour
- ✅ Rapport d'analyse (si changement majeur)
- ✅ Mise à jour CHANGELOG.md

#### ⚠️ Workflow obligatoire

1. ⚠️ **Tuer serveurs AVANT** toute modification
2. ⚠️ **Lire** `.github/workflow-rules.md`
3. ⚠️ **Vérifier** `.github/incidents-history.md`
4. ⚠️ **Tester** en dev ET prod après modification

---

### 4. add-feature-complete

**Fichier:** `.github/prompts/add-feature-complete.prompt.md`

#### 📝 Description

Ajoute une fonctionnalité complète de A à Z :
- Modèles de données (SQLAlchemy)
- Service layer (logique métier)
- Routes Flask (API + pages)
- Templates HTMX + Bootstrap 5
- Traductions i18n
- Tests complets (unit + integration)
- Documentation

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Ajouter une nouvelle fonctionnalité majeure
- ✅ Créer un nouveau module (ex: gestion articles, commentaires, tags)
- ✅ Implémenter un user story complet
- ✅ Développer une feature complexe avec BD + UI + API

#### 📋 Exemples d'utilisation

**Cas 1 : Système de commentaires**
```
Feature: Système de commentaires
User Stories:
  - En tant qu'utilisateur, je peux commenter un article
  - En tant qu'admin, je peux modérer les commentaires
  - En tant qu'utilisateur, je peux éditer/supprimer mes commentaires
Requirements:
  - Modèle Comment (texte, auteur, article, date, status)
  - CRUD complet (API + UI)
  - Pagination
  - Modération admin
  - Notifications email (optionnel)
```

**Cas 2 : Gestion de tags**
```
Feature: Système de tags
User Stories:
  - En tant qu'admin, je peux créer/éditer/supprimer des tags
  - En tant qu'utilisateur, je peux filtrer contenu par tag
  - En tant qu'utilisateur, je vois les tags populaires
Requirements:
  - Modèle Tag (nom, slug, couleur)
  - Relation many-to-many avec Content
  - Autocomplete dans formulaires
  - Page de filtre par tag
  - Stats tags populaires
```

**Cas 3 : Notifications**
```
Feature: Système de notifications
User Stories:
  - En tant qu'utilisateur, je reçois des notifications in-app
  - En tant qu'utilisateur, je peux marquer comme lu
  - En tant qu'utilisateur, je peux configurer préférences
Requirements:  
  - Modèle Notification (type, message, lu, date)
  - Temps réel (WebSocket ou polling)
  - Badge de compteur non-lus
  - Page liste notifications
  - Paramètres notifications (email, push, in-app)
```

#### ✅ Ce que le prompt génère

**Backend:**
- ✅ Modèle SQLAlchemy (avec relations, indexes, contraintes)
- ✅ Migration Alembic
- ✅ Service layer (CRUD + logique métier)
- ✅ Routes Flask (CRUD API + pages)
- ✅ Validation d'entrée
- ✅ Gestion d'erreurs

**Frontend:**
- ✅ Templates (liste, détail, création, édition)
- ✅ Partials HTMX
- ✅ Formulaires Bootstrap 5
- ✅ Modals, alerts, confirmations
- ✅ Traductions FR + EN complètes

**Tests:**
- ✅ Tests service layer (unit tests)
- ✅ Tests routes (integration tests)
- ✅ Couverture ≥ 90%

**Documentation:**
- ✅ Rapport d'analyse (design decisions)
- ✅ Rapport d'implémentation
- ✅ Mise à jour CHANGELOG.md
- ✅ Docstrings complètes

#### ⚠️ Processus obligatoire

1. ⚠️ **Pré-implémentation:** Rapport d'analyse détaillé
2. ⚠️ **Tuer serveurs** avant toute modification
3. ⚠️ **Migration BD:** Créer + revoir + appliquer
4. ⚠️ **Tests:** Écrire PENDANT le développement (pas après)
5. ⚠️ **Validation:** Tester dev + prod avant commit

---

### 5. migrate-dependency

**Fichier:** `.github/prompts/migrate-dependency.prompt.md`

#### 📝 Description

Migre une dépendance (bibliothèque, framework) vers une nouvelle version de manière sécurisée : 
- Analyse d'impact
- Application des breaking changes
- Tests complets
- Plan de rollback
- Documentation

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Mettre à jour une dépendance majeure (breaking changes)
- ✅ Migrer vers nouvelle version de framework (Flask 2→3, Bootstrap 5.2→5.3)
- ✅ Corriger vulnérabilités de sécurité (CVE)
- ✅ Adopter nouvelles fonctionnalités d'une bibliothèque

#### 📋 Exemples d'utilisation

**Cas 1 : Flask 2.3 → 3.0**
```
Dependency: Flask
Current Version:   2.3.0
Target Version:  3.0.0
Reason:  Nouvelles fonctionnalités + correctifs de sécurité
Breaking Changes:
  - Module flask.json réorganisé
  - Werkzeug APIs changées
  - Click 8.x requis
```

**Cas 2 : SQLAlchemy 1.4 → 2.0**
```
Dependency: SQLAlchemy
Current Version: 1.4.48
Target Version: 2.0.0
Reason: Performance + nouvelles features ORM 2.0
Breaking Changes:
  - Query API changée (execute() obligatoire)
  - engine.execute() supprimé
  - Nouvelles méthodes select()
```

**Cas 3 : Bootstrap 5.2 → 5.3**
```
Dependency: Bootstrap
Current Version: 5.2.3
Target Version: 5.3.0
Ecosystem: CSS/Framework
Reason: Nouveaux utilitaires + bugfixes
Breaking Changes:  Minimal (surtout additions)
```

#### ✅ Ce que le prompt génère

- ✅ Rapport d'analyse d'impact (fichiers affectés)
- ✅ Liste des breaking changes à appliquer
- ✅ Code mis à jour (imports, API calls, templates)
- ✅ Tests mis à jour (si API changée)
- ✅ Plan de rollback documenté
- ✅ Rapport de migration complet
- ✅ Mise à jour CHANGELOG.md (section Dependencies)

#### ⚠️ Processus sécurisé

1. ⚠️ **Backup BD** (si migration majeure)
2. ⚠️ **Branche dédiée** (`migrate-<dep>-v<version>`)
3. ⚠️ **Analyse AVANT** modification
4. ⚠️ **Tests complets** (automatisés + manuels)
5. ⚠️ **Performance check** (avant/après)
6. ⚠️ **Rollback testé** (vérifier que c'est possible)

---

### 6. fix-security-issue

**Fichier:** `.github/prompts/fix-security-issue.prompt.md`

#### 📝 Description

Analyse et corrige une vulnérabilité de sécurité de manière professionnelle :
- Rapport d'analyse confidentiel
- Correction sécurisée
- Tests de non-régression
- Documentation incident
- Disclosure responsable

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Corriger une vulnérabilité détectée (scan, audit, rapport)
- ✅ Patcher un CVE
- ✅ Résoudre un problème de sécurité signalé
- ✅ Implémenter une correction de sécurité urgente

#### 📋 Exemples d'utilisation

**Cas 1 : SQL Injection**
```
Vulnerability: SQL Injection dans endpoint /search
Severity: Critical
Affected: backend/src/routes/search.  py
Discovery: Security audit automatique (Bandit)
Description:   Interpolation directe de query string dans SQL
```

**Cas 2 :  XSS (Cross-Site Scripting)**
```
Vulnerability: Stored XSS dans champ bio utilisateur
Severity: High
Affected: backend/src/templates/profile.html, backend/src/routes/users.py
Discovery: Rapport de sécurité externe
Description:  Bio affichée avec |safe sans sanitization
```

**Cas 3 :  IDOR (Insecure Direct Object Reference)**
```
Vulnerability:  IDOR permet de supprimer users d'autres users
Severity: Critical
Affected: backend/src/routes/users.py (DELETE /users/<id>)
Discovery: Pentest interne
Description: Pas de vérification authorization (user_id != current_user)
```

**Cas 4 :  Hardcoded Secrets**
```
Vulnerability: SECRET_KEY hardcodée dans config. py
Severity: Critical
Affected: backend/src/config.py
Discovery: Git history scan (gitleaks)
Description: SECRET_KEY = "dev-secret-123" commité
```

#### ✅ Ce que le prompt génère

**Analyse:**
- ✅ Rapport confidentiel (`YYYY-MM-DD_security-<issue>-CONFIDENTIAL.md`)
- ✅ Vecteur d'attaque documenté
- ✅ Impact évalué (données, utilisateurs affectés)
- ✅ Versions affectées

**Correction:**
- ✅ Code patché (route, template, service)
- ✅ Tests de sécurité (exploit attempts)
- ✅ Tests de non-régression
- ✅ Scan sécurité post-fix

**Documentation:**
- ✅ CHANGELOG.md (section Security)
- ✅ `.github/incidents-history.md` (incident record)
- ✅ Security advisory (si disclosure publique)
- ✅ CVE (si applicable)

#### ⚠️ Workflow sécurité STRICT

1. ⚠️ **NE PAS commit** fix avant disclosure coordonnée
2. ⚠️ **Branche privée** (accès restreint)
3. ⚠️ **Rapport confidentiel** (ne pas commit si sensible)
4. ⚠️ **Tests d'exploitation** (confirmer vulnérabilité)
5. ⚠️ **Rotation credentials** (si secrets exposés)
6. ⚠️ **Backport** (corriger versions anciennes)

---

## Prompts d'Analyse

### 7. analyze-project-stack

**Fichier:** `.github/prompts/analyze-project-stack. prompt.md`

#### 📝 Description

Analyse complète de la stack technologique du projet :
- Langages utilisés
- Frameworks et bibliothèques
- Base de données
- Outils de build et développement
- Infrastructure et déploiement
- Sécurité et authentification

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Documenter la stack technique (onboarding, audit)
- ✅ Préparer une présentation du projet
- ✅ Identifier les technologies utilisées (nouveau sur projet)
- ✅ Planifier une migration technologique
- ✅ Créer un README technique

#### 📋 Sortie attendue

Le prompt génère un rapport structuré avec : 

**Langages:**
- Python 3.12
- JavaScript (ES6+)
- HTML5, CSS3
- SQL (SQLite/MySQL/PostgreSQL)
- Bash/PowerShell (scripts)

**Frontend:**
- HTMX 1.9+
- Bootstrap 5.3
- Alpine.js (optionnel)
- Tabulator (DataGrid)

**Backend:**
- Flask 3.0+
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Waitress (WSGI production)

**Base de données:**
- SQLite (dev)
- MySQL / PostgreSQL (prod)
- Redis (cache, optionnel)

**Build & Dev:**
- npm (frontend)
- pip (Python)
- Ruff (linting + formatting)
- Mypy (type checking)
- pytest (tests)

**DevOps & Infrastructure:**
- GitHub Actions (CI/CD)
- Docker (optionnel)
- cPanel / VPS (déploiement)

**Sécurité:**
- Flask-Login (authentification)
- bcrypt (hashing passwords)
- TOTP (2FA)
- CSRF protection (Flask-WTF)

**Autres:**
- Git (version control)
- Markdown (documentation)
- i18n (internationalisation FR/EN)

#### ✅ Utilité

- ✅ Onboarding nouveaux développeurs
- ✅ Documentation technique
- ✅ Audit technologique
- ✅ Planification migrations
- ✅ Évaluation dépendances

---

### 8. list-project-features

**Fichier:** `.github/prompts/list-project-features.prompt. md`

#### 📝 Description

Liste exhaustive de toutes les fonctionnalités implémentées dans le projet, organisées par catégorie : 
- Features principales
- UI/UX
- API
- Authentification
- Admin
- Notifications
- Intégrations externes

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Créer une documentation fonctionnelle
- ✅ Audit des features (ce qui existe vs.  roadmap)
- ✅ Onboarding produit (product managers, clients)
- ✅ Préparer release notes
- ✅ Identifier features manquantes

#### 📋 Sortie attendue (exemple X-Filamenta)

**Core Features:**
- Installation wizard multi-étapes (9 étapes)
- Gestion utilisateurs (CRUD)
- Gestion contenu (CRUD)
- Système de préférences utilisateur

**Authentification & Autorisation:**
- Login/Logout
- Password reset (email)
- Email verification
- 2FA TOTP (Google Authenticator, Authy)
- Backup codes
- Account lockout (5 tentatives)
- Role-Based Access Control (MEMBER/ADMIN)
- Session management sécurisé

**Admin Panel:**
- Dashboard avec statistiques
- Gestion utilisateurs (liste, création, édition, suppression)
- Gestion contenu
- Admin history (audit trail)
- Settings (SMTP, features, site)

**Performance & Cache:**
- Multi-backend cache (Redis, Filesystem, Memory)
- Service-level caching (UserService, ContentService)
- Cache invalidation hooks
- Database connection pooling
- Eager loading (prévention N+1)

**Notifications:**
- Email notifications (SMTP)
- Rate limiting (anti brute-force)

**i18n:**
- Support multi-langue (FR, EN)
- Template function `t()` avec fallback

**Security:**
- CSRF protection
- Password hashing (bcrypt)
- SQL injection prevention (ORM)
- XSS prevention (auto-escaping)
- Secure sessions (HttpOnly, SameSite, Secure)

#### ✅ Utilité

- ✅ Documentation produit
- ✅ Release notes
- ✅ Audit fonctionnel
- ✅ Comparaison roadmap vs.  réalisé
- ✅ Présentation client/stakeholders

---

## Prompts de Qualité

### 9. dev-quality

**Fichier:** `.github/prompts/dev-quality.prompt.md`

#### 📝 Description

Guide complet pour maintenir une **qualité de code élevée** pendant le développement actif, avec focus sur :
- Formatage automatique (Black, isort)
- Linting rapide (Ruff)
- Type hints basiques (mypy)
- Sécurité essentielle
- Documentation minimale
- Tests ciblés

**Philosophy:** "Clean code, fast workflow"

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Onboarding développeur junior/intermédiaire
- ✅ Établir standards de code pour l'équipe
- ✅ Configurer environnement de développement
- ✅ Créer workflow quotidien
- ✅ Préparer codebase pour review

#### 📋 Ce qu'il couvre

**Phase 1: Formatage (Auto)**
- Black (formatage Python)
- isort (tri imports)
- Commande:  `make format`

**Phase 2: Linting (Rapide)**
- Ruff (linter ultra-rapide)
- Auto-fix erreurs communes
- Commande: `make lint`

**Phase 3: Sécurité Basique**
- Top 5 erreurs à éviter: 
  1. Secrets hardcodés
  2. SQL injection
  3. XSS
  4. Debug mode en prod
  5. Sessions non sécurisées

**Phase 4: Type Hints**
- Type hints essentiels (pas perfectionniste)
- Mypy relaxé (dev mode)
- Commande: `mypy app/`

**Phase 5: Documentation Minimale**
- Docstrings pour APIs publiques
- Pas de sur-documentation
- Focus:  ce qui n'est pas évident

**Phase 6: Tests Rapides**
- Couverture 60-70% (dev)
- Tests critiques seulement
- Commande: `make test`

**Workflow Quotidien:**
```bash
# Matin
source venv/bin/activate
git pull

# Pendant dev
flask run --debug

# Avant commit
make format
make lint
make test
git commit
```

#### ✅ Objectifs qualité (dev)

- 📏 Formatage:  **100%** (automatique)
- 🔍 Linting: **0 erreurs**
- 🧪 Coverage: **60-70%**
- 📝 Docstrings: **APIs publiques seulement**
- 🔒 Sécurité:  **Pas d'erreurs évidentes**

#### ⚠️ Ce que ce n'est PAS

- ❌ Pas pour production (voir security-audit)
- ❌ Pas perfectionniste (pragmatique)
- ❌ Pas 100% coverage (focus critical paths)

---

### 10. security-audit

**Fichier:** `.github/prompts/security-audit.prompt.md`

#### 📝 Description

Audit de sécurité **complet et approfondi** avec remédiation automatisée :
- Scan dépendances (CVE)
- Scan secrets (git history)
- Analyse code (SAST)
- Configuration Flask sécurisée
- Type safety complète (mypy strict)
- Tests de pénétration
- Compliance (OWASP, GDPR)

**Philosophy:** "Production-ready security"

#### 🎯 Quand l'utiliser ?

Utilisez ce prompt quand vous devez : 
- ✅ Préparer mise en production
- ✅ Audit sécurité pré-release
- ✅ Résoudre findings pentest
- ✅ Certification sécurité (ISO, SOC2)
- ✅ Après incident de sécurité
- ✅ Audit compliance annuel

#### 📋 Ce qu'il couvre

**Phase 1: Scan Sécurité**
- `pip-audit` — Vulnérabilités dépendances
- `safety` — CVE database
- `gitleaks` — Secrets git history
- `bandit` — SAST Python
- `semgrep` — Patterns vulnérables

**Phase 2: Code Quality Enterprise**
- `mypy --strict` — 100% type coverage
- `ruff` — Linting agressif (tous les checks)
- `radon` — Complexité cyclomatique < 10
- `interrogate` — Documentation 95%+

**Phase 3: Configuration Sécurisée**
- Flask security headers
- Session configuration
- HTTPS enforcement (Talisman)
- Rate limiting (Flask-Limiter)
- CSRF protection
- Content Security Policy

**Phase 4: Authentification Enterprise**
- Password hashing (bcrypt 12+ rounds)
- Account lockout
- 2FA enforcement
- Secure password reset
- RBAC (Role-Based Access Control)

**Phase 5: Tests Sécurité**
- Tests exploitation (SQL injection, XSS, IDOR)
- Tests autorisation
- Tests rate limiting
- Tests session management

**Phase 6: CI/CD Sécurisé**
- GitHub Actions (minimal permissions)
- Dependabot
- CodeQL
- Secret scanning
- SAST dans pipeline

#### ✅ Critères de succès

**Sécurité:**
- ✅ 0 vulnérabilités `pip-audit`
- ✅ 0 secrets détectés
- ✅ 0 critical issues Bandit
- ✅ A+ rating securityheaders.com

**Code Quality:**
- ✅ `mypy --strict` 100%
- ✅ `ruff` 0 erreurs
- ✅ Coverage ≥ 80%
- ✅ Complexité < 10
- ✅ Documentation ≥ 95%

**Performance:**
- ✅ Page load < 2s
- ✅ API response < 200ms (p95)
- ✅ Queries optimisées

#### ⚠️ Deliverables

- ✅ Security Report (vulns trouvées/fixées)
- ✅ Code Quality Report (métriques avant/après)
- ✅ Remediation Log (tous les changements)
- ✅ Risk Assessment (risques restants)
- ✅ Recommendations (améliorations futures)

---

### 11. repository-cleanup

**Fichier:** `.github/prompts/repository-cleanup. prompt.md`

#### 📝 Description

Nettoyage et organisation **complète** du repository pour le rendre cohérent, maintenable et production-ready :
- Structure de dossiers logique
- Documentation de qualité
- Configuration Git optimale
- GitHub workflows
- Developer Experience (DX)

**Philosophy:** "Professional, production-ready repository"

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Préparer projet pour open-source
- ✅ Onboarding nouvelle équipe
- ✅ Refonte repository legacy
- ✅ Standardisation multi-projets
- ✅ Audit organisation

#### 📋 Tâches couvertes

**1. Structure Repository**
- Analyse hiérarchie actuelle
- Proposition structure best practices
- Relocation fichiers mal placés
- Suppression dossiers vides/redondants
- Séparation concerns (src, docs, tests, config)

**2. Documentation**
- README. md complet (badges, install, quickstart, contributing)
- CONTRIBUTING.md (style, PRs, tests)
- CHANGELOG.md ([Keep a Changelog](https://keepachangelog.com/))
- LICENSE
- CODE_OF_CONDUCT.md
- SECURITY.md
- Structure `/docs` (architecture, api, guides, development)

**3. Configuration Git**
- `.gitignore` optimisé (catégorisé, pas de doublons)
- `.gitattributes` (line endings, binary files)

**4. GitHub Configuration**
- Workflows CI/CD (optimisés, cachés, nommés)
- Issue templates (bug, feature, question)
- PR template (checklist, description, testing)
- CODEOWNERS (review automatique)
- Dependabot (automated updates)

**5. Organisation Code**
- Naming conventions cohérentes
- Placement fichiers logique
- Dead code removal
- TODO → Issues

**6. Dependencies**
- Audit (unused, outdated, vulns)
- Séparation prod/dev
- Lock versions
- Documentation choix

**7. Developer Experience**
- Scripts setup (`setup.sh`, Makefile)
- `.editorconfig`
- Linters/formatters configurés
- Pre-commit hooks
- `.env.example`
- Docker support

**8. Quality Assurance**
- Test coverage visible
- Scripts validés/documentés
- Examples fonctionnels
- URLs docs validées

#### ✅ Deliverables

- ✅ Summary Report (changements + raisons)
- ✅ Migration Guide (si structure changée)
- ✅ Recommendations (améliorations futures)
- ✅ Checklist Status (tasks complétées)

#### ⚠️ Stratégie exécution

1. **Analyser** (comprendre état actuel)
2. **Prioriser** (high-impact, low-risk d'abord)
3. **Incrémental** (pas tout d'un coup)
4. **Tester** (rien ne casse)
5. **Documenter** (commit messages clairs)
6. **Review** (double-check)

---

## Prompts de Configuration

### 12. venv-setup-windows

**Fichier:** `.github/prompts/venv-setup-windows.prompt.md`

#### 📝 Description

Guide **ultra-détaillé** pour configurer un environnement virtuel Python sur **Windows 11** avec **PowerShell** et **IntelliJ IDEA** :
- Nettoyage ancien venv
- Création nouveau venv
- Installation dépendances
- Configuration IntelliJ IDEA
- Vérification setup
- Troubleshooting Windows/PowerShell

**Philosophy:** "Clean slate, zero conflicts"

#### 🎯 Quand l'utiliser ? 

Utilisez ce prompt quand vous devez :
- ✅ Setup initial projet (nouveau développeur)
- ✅ Réinitialisation environnement (venv corrompu)
- ✅ Migration Python version (3.10 → 3.12)
- ✅ Résolution problèmes venv
- ✅ Documentation onboarding Windows

#### 📋 Ce qu'il couvre

**Phase 1: Clean Up**
- Suppression ancien venv
- Nettoyage cache Python (`__pycache__`, `*.pyc`)
- Vérification Python installé (3.11+)

**Phase 2: Création venv**
- Enable PowerShell script execution
- `python -m venv venv`
- Activation venv (`.\venv\Scripts\Activate. ps1`)
- Vérification activation

**Phase 3: Installation**
- Upgrade pip
- Install requirements. txt
- Install dev tools (black, ruff, mypy, pytest)
- Vérification installations

**Phase 4: IntelliJ IDEA**
- Configure Python SDK (automatic + manual)
- Flask support
- Run configuration
- Python Integrated Tools
- Code Style
- External Tools (Black, Ruff)
- File Watchers (auto-format on save)

**Phase 5: Vérification**
- Script automatique (`verify_setup.ps1`)
- Tests quick commands
- Vérification IntelliJ

**Phase 6: Troubleshooting**
- Issue 1: Scripts disabled
- Issue 2: Python not found
- Issue 3: SSL errors
- Issue 4: Module not found in IntelliJ
- Issue 5: Permission denied
- Issue 6: Long path error
- Issue 7: Flask routes not recognized

**Bonus: PowerShell Functions**
- `filamenta` → Navigate to project
- `venv` → Activate venv
- `flaskrun` → Start Flask server
- `test` → Run tests
- `fmt` → Format code

#### ✅ One-Command Setup

Le prompt fournit un script **automatisé complet** : 

```powershell
.\setup_venv.ps1
```

Qui fait TOUT :
- Clean
- Create venv
- Activate
- Upgrade pip
- Install dependencies
- Install dev tools
- Verify

#### ⚠️ Checklist finale

**Initial Setup:**
- [ ] Python 3.11+ installé
- [ ] PowerShell execution policy:  RemoteSigned
- [ ] Venv créé:  `D:\xarema\X-Filamenta-Python\venv`
- [ ] Venv activé (prompt montre `(venv)`)
- [ ] Dependencies installées
- [ ] Dev tools installés

**IntelliJ IDEA:**
- [ ] Project ouvert
- [ ] Python SDK configuré
- [ ] Flask support enabled
- [ ] Run configuration créée
- [ ] pytest configuré
- [ ] Black/Ruff external tools

**Vérification:**
- [ ] `python --version` → Python 3.11+
- [ ] `pip list` → Flask, pytest, black, ruff
- [ ] `flask run` → Serveur démarre
- [ ] IntelliJ reconnaît imports

---

## 📊 Tableau Récapitulatif

| Prompt | Type | Durée | Niveau | Usage |
|--------|------|-------|--------|-------|
| **create-htmx-endpoint** | Dev | 10-20 min | Junior+ | Endpoint AJAX simple |
| **add-wizard-step** | Dev | 20-30 min | Intermédiaire | Étape wizard |
| **refactor-route** | Dev | 30-60 min | Intermédiaire+ | Clean code |
| **add-feature-complete** | Dev | 2-4 heures | Senior | Feature complète |
| **migrate-dependency** | Dev | 1-3 heures | Senior | Migration lib/framework |
| **fix-security-issue** | Sécurité | 1-2 heures | Senior+ | Vulnérabilité |
| **analyze-project-stack** | Analyse | 5-10 min | Tous | Documentation tech |
| **list-project-features** | Analyse | 10-15 min | Tous | Documentation produit |
| **dev-quality** | Qualité | Setup | Junior+ | Workflow quotidien |
| **security-audit** | Qualité | 4-8 heures | Lead+ | Pré-production |
| **repository-cleanup** | Qualité | 3-6 heures | Senior+ | Refonte repo |
| **venv-setup-windows** | Config | 20-30 min | Tous | Setup initial |

---

## 💡 Conseils d'utilisation

### Pour débutants

**Commencez par :**
1. `venv-setup-windows` — Setup environnement
2. `dev-quality` — Apprendre standards code
3. `create-htmx-endpoint` — Premier endpoint simple
4. `analyze-project-stack` — Comprendre stack

### Pour développeurs intermédiaires

**Utilisez régulièrement :**
1. `create-htmx-endpoint` — Endpoints rapides
2. `add-wizard-step` — Étapes wizard
3. `refactor-route` — Améliorer code existant
4. `add-feature-complete` — Features moyennes

### Pour seniors/leads

**Outils stratégiques :**
1. `security-audit` — Avant production
2. `repository-cleanup` — Standardisation
3. `migrate-dependency` — Migrations majeures
4. `fix-security-issue` — Incidents critiques

---

## 🔗 Références

- **Règles générales :** `.github/copilot-instructions.md`
- **Règles Python :** `.github/python.instructions.md`
- **Règles Frontend :** `.github/frontend.instructions.md`
- **Règles Workflow :** `.github/workflow-rules.md`
- **Historique incidents :** `.github/incidents-history.md`

---

## 📞 Support

Pour questions ou suggestions sur les prompts :
- 📧 Email : [filamenta@xarema.com](mailto:filamenta@xarema.com)
- 🐛 Issues : [GitHub Issues](https://github.com/xarema/X-Filamenta-Python/issues)
- 📝 Créer nouveau prompt :  Proposer dans une issue avec label `prompt`

---

**Happy coding with Copilot Agent!   🚀**

**Copyright © 2025 XAREMA.  All rights reserved.**