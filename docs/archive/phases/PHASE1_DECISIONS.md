"""
Purpose: Résumé des décisions Phase 1 — Email Workflows & Settings
Description: Validation complète de toutes les réponses aux questions de clarification

File: docs/PHASE1_DECISIONS.md | Repository: X-Filamenta-Python
Created: 2025-12-29T02:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Décisions finalisées le 2025-12-29
- Basé sur consultation utilisateur directe
"""

# 📋 RÉSUMÉ DES DÉCISIONS — PHASE 1

**Date validation:** 2025-12-29  
**Phase:** Phase 1 — Email Workflows & Settings  
**Version cible:** v0.1.0-Beta  
**Statut:** ✅ TOUTES LES DÉCISIONS CONFIRMÉES

---

## ✅ RÉCAPITULATIF COMPLET DES RÉPONSES

### Q1 — Configuration SMTP (Mailtrap vs alternatives)

**Votre réponse:** ✅ OK

**Décision finale:**
- **Développement:** Mailtrap.io (capture emails, pas d'envoi réel)
- **Production:** SendGrid (service professionnel, 100+ emails/jour gratuit)
- **Validation:** Switchable via env vars (`MAIL_PROVIDER=mailtrap` ou `sendgrid`)

**Implémentation:**
- Service `EmailService` avec support multi-providers
- Configuration via `.env` en développement
- Credentials SecureString en production

✅ **CONFIRMÉ**

---

### Q2 — Stockage des credentials SMTP

**Votre réponse:** ✅ OK

**Décision finale:**
- **Développement:** Fichier `.env` (non commité, local uniquement)
- **Production:** Settings model en DB (encrypted avec Fernet)
- **Interface:** Admin panel pour configuration SMTP production-ready

**Implémentation:**
- `.env` template avec exemples Mailtrap
- Settings model + migration Alembic
- UI admin pour test/save SMTP config
- Validation connexion SMTP avec bouton "Tester"

✅ **CONFIRMÉ**

---

### Q3 — Templates emails (Bootstrap Email vs alternatives)

**Votre réponse:** ✅ OK MAIS + Ajout texte brut

**Décision finale:**
- **Format HTML:** Bootstrap Email (responsive, professionnel)
- **Format texte brut:** Parallèle (fallback pour clients non-HTML)
- **Sélection:** Flag configurable dans Settings admin pour choisir format

**Spécifications détaillées:**

#### 3.1 Templates structure
```
frontend/templates/emails/
├── verification.html (Bootstrap Email)
├── verification.txt (texte brut)
├── password_reset.html (Bootstrap Email)
├── password_reset.txt (texte brut)
└── notification.html (Bootstrap Email)
└── notification.txt (texte brut)
```

#### 3.2 Fonction flag admin
- Setting: `email_format` (enum: `html_only`, `txt_only`, `html_with_fallback`)
- Défaut: `html_with_fallback` (HTML avec texte brut en fallback)
- Affichage: Settings admin UI avec radio buttons
- Stockage: Settings table (encrypted)

#### 3.3 EmailService logic
```python
def send_email(to: str, subject: str, template_name: str, context: dict):
    # Déterminer format basé sur setting
    email_format = self.get_setting('email_format')
    
    if email_format in ['html_only', 'html_with_fallback']:
        html_body = render_template(f"{template_name}.html", **context)
    
    if email_format in ['txt_only', 'html_with_fallback']:
        text_body = render_template(f"{template_name}.txt", **context)
    
    # Envoyer avec body approprié
    message = Message(
        subject=subject,
        recipients=[to],
        html=html_body if 'html_body' in locals() else None,
        body=text_body if 'text_body' in locals() else None
    )
    mail.send(message)
```

✅ **CONFIRMÉ + AJOUT FONCTION FLAG**

---

### Q4 — Obligation email verification avant connexion

**Votre réponse:** ✅ OK

**Décision finale:**
- **Feature flag:** `email_verification_required` (configurable en Settings)
- **Défaut:** `False` (utilisateur peut se connecter, rappels via notifications)
- **Optionnel:** Admin peut activer pour forcer vérification avant login

**Implémentation:**
- Setting dans Settings model
- Check dans route login: `if setting.email_verification_required and not user.email_verified: redirect to /auth/verify`
- UI notification/banner si email non vérifié
- Bouton resend verification email

✅ **CONFIRMÉ**

---

### Q5 — Validité token email (24h vs alternatives)

**Votre réponse:** ✅ OK MAIS + Configurable admin

**Décision finale:**
- **Défaut:** 24 heures (standard sécurité email)
- **Configurable:** Oui, via Settings admin
- **Range acceptable:** 1h à 7 jours (validation)
- **Stockage:** `email_verification_token_expiry` en Settings (int: heures)

**Implémentation:**
- Setting: `email_verification_token_expiry_hours` (type: integer, default: 24)
- UI Settings: Input numérique avec tooltip (1-168 heures)
- Logique: `token_expiry = now + timedelta(hours=setting_value)`
- Validation DB: Flag `email_verified` + `email_verification_token_expiry` timestamp

✅ **CONFIRMÉ + CONFIGURABLE EN ADMIN**

---

### Q6 — Validité token password reset (1h vs alternatives)

**Votre réponse:** 1 heure + ✅ Configurable admin

**Décision finale:**
- **Défaut:** 1 heure (sécurité stricte)
- **Configurable:** Oui, via Settings admin
- **Range acceptable:** 15 min à 24 heures
- **Stockage:** `password_reset_token_expiry_minutes` en Settings

**Implémentation:**
- Setting: `password_reset_token_expiry_minutes` (type: integer, default: 60)
- UI Settings: Dropdown prédéfini (15, 30, 60, 120, 240, 1440 min) + input custom
- Logique: `token_expiry = now + timedelta(minutes=setting_value)`
- Validation DB: `password_reset_token` + `password_reset_token_expiry` timestamp

✅ **CONFIRMÉ + CONFIGURABLE EN ADMIN**

---

### Q7 — Rate limiting reset password (2 demandes/heure)

**Votre réponse:** 2 demandes/heure + ✅ Configurable admin

**Décision finale:**
- **Défaut:** 2 demandes par heure (protège contre spam)
- **Configurable:** Oui, via Settings admin
- **Range acceptable:** 1 à 10 demandes par heure
- **Stockage:** `password_reset_rate_limit_per_hour` en Settings

**Implémentation:**
- Setting: `password_reset_rate_limit_per_hour` (type: integer, default: 2)
- UI Settings: Input numérique avec tooltip (1-10)
- Logique: Rate limiter basé sur email/IP
- Message erreur i18n: "Trop de demandes, réessayez dans X minutes"

✅ **CONFIRMÉ + CONFIGURABLE EN ADMIN**

---

### Q8 — Champs Settings Model

**Votre réponse:** ✅ TOUS LES FONCTIONS (avec coches)

**Décision finale - Champs Settings inclus:**

#### ✅ Groupe SMTP Config
- `smtp_host` (string) - Mailtrap: `smtp.mailtrap.io`
- `smtp_port` (integer) - Défaut: 465
- `smtp_user` (string encrypted)
- `smtp_password` (string encrypted)
- `smtp_tls_enabled` (boolean) - Défaut: True
- `smtp_from_email` (string) - `noreply@exemple.com`
- `smtp_from_name` (string) - `X-Filamenta`

#### ✅ Groupe Email Features
- `email_verification_required` (boolean) - Défaut: False
- `email_verification_token_expiry_hours` (integer) - Défaut: 24
- `password_reset_token_expiry_minutes` (integer) - Défaut: 60
- `password_reset_rate_limit_per_hour` (integer) - Défaut: 2
- `email_format` (enum: html_only/txt_only/html_with_fallback) - Défaut: html_with_fallback

#### ✅ Groupe Features Flags
- `registration_enabled` (boolean) - Défaut: False
- `2fa_required` (boolean) - Défaut: False

#### ✅ Groupe Site Config
- `site_name` (string) - Défaut: `X-Filamenta`
- `site_url` (string) - Défaut: `http://localhost:5000`
- `logo_url` (string) - Défaut: `/static/logo.png`
- `footer_text` (string) - Défaut: `© 2025 XAREMA`

#### Non inclus en Phase 1 (reportés Phase 2+)
- [ ] Pagination defaults
- [ ] Upload limits
- [ ] Session config
- [ ] Rate limiting custom

**Implémentation:**
- Model Settings avec 18 champs
- UI Settings admin avec 4 sections (collapsible)
- Validation types + ranges
- Migration Alembic avec données par défaut

✅ **CONFIRMÉ — TOUS LES CHAMPS**

---

### Q9 — Encryption valeurs sensibles

**Votre réponse:** ✅ OK

**Décision finale:**
- **Méthode:** Fernet (symmetric encryption)
- **Key:** Dérivée de `SECRET_KEY` Flask
- **Champs encrypted:** `smtp_password`, `smtp_user`, toutes valeurs sensibles
- **Validation:** Décrypt automatique à la lecture

**Implémentation:**
```python
# Champs à encrypter dans Settings model
encrypted_fields = ['smtp_user', 'smtp_password']

# Utiliser SQLAlchemy-Cryptography ou custom Fernet wrapper
def get_encrypted_value(key: str) -> str:
    fernet_key = Fernet(base64.urlsafe_b64encode(app.config['SECRET_KEY'][:32]))
    encrypted = self.data.get(key)
    return fernet_key.decrypt(encrypted).decode()
```

✅ **CONFIRMÉ**

---

### Q10 — Script de test complet

**Votre réponse:** ✅ OK

**Décision finale:**
- **Localisation:** `scripts/tests/test_phase1_email.py`
- **Contenu:** Script de validation complète workflow email
- **Fonctionnalités:**
  - Nettoyage DB automatique
  - Test email verification (mock + réel)
  - Test password reset (mock + réel)
  - Test Settings SMTP config
  - Instructions claires
  - Options debug/prod

**Implémentation:**
```
scripts/tests/test_phase1_email.py
├── Clean DB
├── Start server
├── Test 1: Email Verification Workflow
├── Test 2: Password Reset Workflow
├── Test 3: Settings SMTP Config
├── Test 4: Rate Limiting
├── Generate Report
└── Cleanup
```

✅ **CONFIRMÉ**

---

### Q11 — Migration DB

**Votre réponse:** ✅ OK

**Décision finale:**
- **Outil:** Alembic (standard du projet)
- **Migration:** `alembic revision -m "add_settings_model_and_email_fields"`
- **Contenu:**
  - Table Settings (clé-valeur)
  - Colonnes User (email_verified, email_verification_token, etc.)
  - Index sur champs importants

**Implémentation:**
```
migrations/versions/
├── 003_add_settings_model.py
└── 004_add_email_verification_fields.py
```

✅ **CONFIRMÉ**

---

### Q12 — Documentation Phase 1

**Votre réponse:** ✅ OK

**Décision finale:**
- **Niveau:** Standard (guide admin + API)
- **Contenu:**
  - Guide admin SMTP (configuration, test)
  - API docs email endpoints
  - Schéma Settings model
  - Screenshots configuration
  - Exemples curl

**Fichiers documentation:**
```
docs/
├── guides/ADMIN_EMAIL_CONFIG.md
├── api/EMAIL_ENDPOINTS.md
├── MIGRATION_PHASE1.md
└── SCREENSHOTS/ (admin settings UI)
```

✅ **CONFIRMÉ**

---

## 📊 TABLEAU RÉCAPITULATIF FINAL

### Décisions par catégorie

| Catégorie | Q | Décision | Configurable | Statut |
|-----------|---|----------|-------------|--------|
| **SMTP** | Q1 | Mailtrap (dev) → SendGrid (prod) | Env var | ✅ |
| **Config** | Q2 | .env (dev) + DB (prod) | Oui | ✅ |
| **Templates** | Q3 | Bootstrap Email + Texte brut | Flag admin | ✅ |
| **Email Vérif** | Q4 | Configurable (feature flag) | Oui | ✅ |
| **Token Email** | Q5 | 24h (configurable) | Oui (1-168h) | ✅ |
| **Token Password** | Q6 | 1h (configurable) | Oui (15m-24h) | ✅ |
| **Rate Limit Reset** | Q7 | 2/h (configurable) | Oui (1-10/h) | ✅ |
| **Settings** | Q8 | 18 champs (SMTP + Features + Site) | Oui (18 champs) | ✅ |
| **Encryption** | Q9 | Fernet (symmetric) | N/A | ✅ |
| **Tests** | Q10 | Script complet `test_phase1_email.py` | N/A | ✅ |
| **Migration** | Q11 | Alembic (standard) | N/A | ✅ |
| **Docs** | Q12 | Standard (guide admin) | N/A | ✅ |

---

## 🎯 RÉSUMÉ DÉCISIONS IMPORTANTES

### Points forts de vos décisions

1. ✅ **Flexibilité maximale** — Presque tout configurable en admin
2. ✅ **Sécurité renforcée** — Encryption Fernet + rate limiting
3. ✅ **Expérience utilisateur** — Formats email multiples (HTML + texte)
4. ✅ **Production-ready** — Settings en DB, credentials sécurisés
5. ✅ **Testabilité** — Script complet de validation

### Fonctionnalités bonus ajoutées (par rapport à la roadmap)

1. 🎁 **Configurabilité Settings** — Q5, Q6, Q7 configurable admin
2. 🎁 **Texte brut emails** — Q3 + flag sélection format
3. 🎁 **Tous les champs Settings** — Q8 complet (18 champs)

---

## 📝 PROCHAINES ÉTAPES

### Avant implémentation Phase 1

1. ✅ **Vérification:** Toutes les décisions validées
2. ⏳ **Prochaine action:** Commencer implémentation Sprint 1.1

### Fichiers à créer/modifier

**Nouveaux:**
- `backend/src/services/email_service.py` (EmailService)
- `backend/src/models/settings.py` (Settings model)
- `frontend/templates/emails/` (templates)
- `scripts/tests/test_phase1_email.py` (test script)
- `migrations/versions/003_add_settings_model.py` (migration Alembic)

**À modifier:**
- `backend/src/models/user.py` (ajouter champs email verification)
- `backend/src/routes/auth.py` (ajouter routes email verification)
- `backend/src/app.py` (enregistrer Settings model)
- `backend/src/i18n/fr.json` et `en.json` (traductions)

---

## ✅ VALIDATION FINALE

**Toutes vos demandes sont respectées :**

- ✅ Q1 — SMTP configuré (Mailtrap/SendGrid)
- ✅ Q2 — Config .env + Settings UI
- ✅ Q3 — Bootstrap Email + texte brut + flag sélection
- ✅ Q4 — Email verification configurable
- ✅ Q5 — Token email 24h (configurable en admin)
- ✅ Q6 — Token password 1h (configurable en admin)
- ✅ Q7 — Rate limit 2/h (configurable en admin)
- ✅ Q8 — Tous les champs Settings (18 champs)
- ✅ Q9 — Encryption Fernet
- ✅ Q10 — Script test complet
- ✅ Q11 — Migration Alembic
- ✅ Q12 — Documentation standard

**Phase 1 est prête à être implémentée ! 🚀**

---

**Récapitulatif créé:** 2025-12-29  
**Status:** ✅ APPROUVÉ  
**Prochaine étape:** Sprint 1.1 — Email Verification Service

Voulez-vous que je **commence immédiatement l'implémentation de Sprint 1.1** ?

