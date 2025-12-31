"""
Purpose: Plan d'exécution détaillé Phase 1 — Email Workflows & Settings
Description: Roadmap jour par jour pour les 2 semaines de Phase 1

File: Analysis_reports/2025-12-29_PHASE1_EXECUTION_PLAN.md | Repository: X-Filamenta-Python
Created: 2025-12-29T14:00:00+00:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
"""

# 🚀 PHASE 1 — PLAN D'EXÉCUTION DÉTAILLÉ

**Dates:** 2025-12-29 → 2026-01-12 (2 semaines)  
**Version cible:** v0.1.0-Beta  
**Priorité:** 🔴 CRITIQUE

---

## 📅 CALENDRIER JOUR PAR JOUR

### SEMAINE 1 — Email Verification

#### 🗓️ JOUR 1-2 (29-30 Dec) — EmailService Foundation

**Tâches:**
- [ ] Créer `backend/src/services/email_service.py`
  - Configuration SMTP depuis env vars
  - Support Mailtrap (dev) & SendGrid (prod)
  - Méthode `send_email(to, subject, template, context)`
  - Logging structured
  - Tests avec mock SMTP

**Fichiers à créer:**
```
backend/src/services/email_service.py (150 lignes)
```

**Fichiers à modifier:**
```
pyproject.toml — ajouter dépendances email (si besoin)
.env.example — ajouter SMTP_* variables
```

**Tests:** 5+ tests unitaires

---

#### 🗓️ JOUR 3-4 (31 Dec - 1 Jan) — Email Verification Routes & Models

**Tâches:**
- [ ] Créer modèle `EmailToken` (`backend/src/models/email_token.py`)
  - Champs: id, user_id, token (UUID), email, type, expires_at, created_at
  - Méthode `is_valid()`, `is_expired()`

- [ ] Créer routes dans `backend/src/routes/auth.py`
  - `POST /auth/send-verification` → Générer token, envoyer email
  - `GET /auth/verify-email/<token>` → Valider, marquer email vérifié

- [ ] Créer templates
  - `frontend/templates/emails/verification.html` (HTML responsive)
  - `frontend/templates/emails/verification.txt` (plain text)
  - `frontend/templates/auth/email-sent.html` (page attente)
  - `frontend/templates/auth/email-verified.html` (confirmation)

- [ ] Migrations DB pour EmailToken

**Tests:** 8+ tests (generation, validation, expiration, email sending)

---

#### 🗓️ JOUR 5 (2 Jan) — Tests & Documentation

**Tâches:**
- [ ] Tests intégration email verification (end-to-end)
- [ ] Mise à jour CHANGELOG
- [ ] Documentation README (email verification section)
- [ ] Vérifier coverage > 85% pour email

**Checkpoint:** Email verification 100% fonctionnel

---

### SEMAINE 2 — Password Reset & Settings

#### 🗓️ JOUR 6-7 (3-4 Jan) — Password Reset Routes

**Tâches:**
- [ ] Ajouter routes dans `backend/src/routes/auth.py`
  - `GET /auth/forgot-password` → Formulaire email
  - `POST /auth/forgot-password` → Générer token 1h, envoyer email
  - `GET /auth/reset-password/<token>` → Formulaire nouveau password
  - `POST /auth/reset-password/<token>` → Valider & mettre à jour password

- [ ] Créer templates
  - `frontend/templates/emails/password-reset.html`
  - `frontend/templates/emails/password-reset.txt`
  - `frontend/templates/auth/forgot-password.html`
  - `frontend/templates/auth/reset-password.html`

- [ ] Rate limiting strict (3 requêtes/heure)
  - Utiliser rate_limiter existant ou améliorer

**Tests:** 10+ tests (token generation, expiration, reset validation)

---

#### 🗓️ JOUR 8-9 (5-6 Jan) — Settings Model & UI

**Tâches:**
- [ ] Créer modèle `Settings` (`backend/src/models/settings.py`)
  - Champs: id, key, value, type (string/int/bool), description, created_at
  - Clés prédéfinies: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_TLS
  - Encryption pour valeurs sensibles (Fernet)

- [ ] Service `SettingsService` (`backend/src/services/settings_service.py`)
  - `get(key, default=None)`
  - `set(key, value)`
  - `get_all()`
  - Cache avec invalidation

- [ ] Routes admin dans `backend/src/routes/admin.py`
  - `GET /admin/settings` → Page paramètres (menu admin)
  - `POST /admin/settings` → Sauvegarder
  - `POST /admin/settings/test-smtp` → Tester configuration SMTP

- [ ] Template `frontend/templates/admin/settings.html`
  - Section SMTP (host, port, user, password, TLS checkbox)
  - Bouton "Test SMTP"
  - Autres settings (site name, etc.)

- [ ] Migrations DB pour Settings table

**Tests:** 8+ tests (get, set, encryption, cache)

---

#### 🗓️ JOUR 10 (7 Jan) — Integration Tests & Polish

**Tâches:**
- [ ] Tests intégration complète password reset (e2e)
- [ ] Tests Settings CRUD
- [ ] Vérifier coverage > 85% pour password reset & settings
- [ ] Cleanup code, docstrings, type hints

**Checkpoint:** Password reset & Settings 100% fonctionnels

---

#### 🗓️ JOUR 11-12 (8-9 Jan) — Tests Finaux & Documentation

**Tâches:**
- [ ] Tests complets (15+ cas)
- [ ] Tests d'intégration workflow entier (signup → verify email → login)
- [ ] Tests password reset workflow complet
- [ ] Ruff check & mypy validation
- [ ] CHANGELOG complet pour Phase 1
- [ ] README update avec guide email config

**Checkpoint:** Tous les tests passent, coverage > 85%

---

#### 🗓️ JOUR 13-14 (10-12 Jan) — Release v0.1.0-Beta

**Tâches:**
- [ ] Version bump: 0.0.1-Alpha → 0.1.0-Beta
  - pyproject.toml
  - File headers (App version)
  
- [ ] Tag Git: v0.1.0-Beta
- [ ] Créer release notes
- [ ] Backup BD (script .dev_scripts)
- [ ] Validation finale

**Checkpoint:** v0.1.0-Beta released & tested

---

## 🎯 CRITÈRES DE SUCCÈS PHASE 1

### Fonctionnalités
- [x] Email verification end-to-end
- [x] Password reset end-to-end
- [x] Settings model & UI
- [x] SMTP configuration persistante
- [x] Encryption sensible data

### Qualité
- [x] Tests > 15 cas
- [x] Coverage > 85%
- [x] Ruff check clean
- [x] Mypy clean
- [x] Docstrings completes

### Documentation
- [x] CHANGELOG updated
- [x] README email section
- [x] Code comments
- [x] Docstrings

### DevOps
- [x] v0.1.0-Beta tagged
- [x] Backup created

---

## 📦 DÉPENDANCES À VÉRIFIER

### Python packages déjà présents?
```
flask — oui
flask-sqlalchemy — oui
flask-limiter — oui
```

### À ajouter (si besoin)
```
python-dotenv — pour env vars
cryptography — pour Fernet encryption (ou utiliser secrets)
```

**À vérifier:** `pip list` dans venv

---

## 🔧 STRUCTURE DE CODE PROPOSÉE

### Fichiers à créer

```
backend/src/
├── models/
│   ├── email_token.py (NEW)
│   └── settings.py (NEW)
├── services/
│   ├── email_service.py (NEW)
│   └── settings_service.py (NEW)
└── routes/
    └── auth.py (MODIFY — ajouter routes verification & reset)

frontend/templates/
├── admin/
│   └── settings.html (NEW)
├── auth/
│   ├── email-sent.html (NEW)
│   ├── email-verified.html (NEW)
│   ├── forgot-password.html (NEW)
│   └── reset-password.html (NEW)
└── emails/
    ├── verification.html (NEW)
    ├── verification.txt (NEW)
    ├── password-reset.html (NEW)
    └── password-reset.txt (NEW)
```

---

## ⚠️ POINTS CRITIQUES À RESPECTER

1. **HEADERS** — Chaque fichier DOIT avoir le header AGPL complet
2. **TESTS** — Aucun test = pas de commit
3. **COVERAGE** — Minimum 85% pour Phase 1
4. **DOCUMENTATION** — Mettre à jour REFERENCE_PHASES.md checklist
5. **BACKUP** — Créer backup après chaque sprint
6. **CLEAN_SERVER** — Nettoyer avant démarrer si erreur

---

## 🎓 UTILISATION SCRIPTS .dev_scripts

### Avant démarrer jour 1
```powershell
.\.dev_scripts\utilities\clean_server.ps1
.\.dev_scripts\utilities\start_server.ps1
```

### Après chaque sprint
```powershell
.\.dev_scripts\utilities\backup_database.ps1
```

### Si erreur majeure
```powershell
.\.dev_scripts\utilities\clean_server.ps1 -Full
.\.dev_scripts\utilities\start_server.ps1
```

---

## 📝 MISES À JOUR À FAIRE

### REFERENCE_PHASES.md
- Mettre à jour checkboxes jour après jour
- Marquer [x] quand tâche complétée

### CHANGELOG.md
- Ajouter section `## [0.1.0-Beta] - 2026-01-12`
- Énumérer features ajoutées

### File headers
- Mettre à jour `Last modified (Git)` → Datetime + short-sha
- Garder `App version: 0.1.0-Beta`

---

## 🚀 DÉMARRER MAINTENANT ?

**Status:** ✅ PRÊT

**Prochaine action:**
1. Lire les règles `.github/copilot-instructions.md` (FAIT)
2. Vérifier `docs/REFERENCE_PHASES.md` (FAIT)
3. **COMMENCER JOUR 1: EmailService**

**Timeline:** 2025-12-29 → 2026-01-12

🎯 **OBJECTIF:** v0.1.0-Beta avec Email Workflows 100% fonctionnels

---

**Plan créé:** 2025-12-29 14:00 UTC+1

