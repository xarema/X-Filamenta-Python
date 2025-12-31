"""
Purpose: Fichier de référence des phases du projet et menu admin
Description: Document de référence pour tracker l'avancement et la structure du menu admin

File: docs/REFERENCE_PHASES.md | Repository: X-Filamenta-Python
Created: 2025-12-29T12:30:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Fichier de référence pour suivi des phases
- À mettre à jour à chaque avancement
- Contient aussi la structure du menu admin
"""

# 📋 PHASES DU PROJET — FICHIER DE RÉFÉRENCE

**Dernière mise à jour:** 2025-12-29  
**Version du document:** 0.1.0

---

## 🎯 PHASE ACTUELLE

### ➡️ Phase Actuellement En Cours

**Phase 1 — Email Workflows & Settings**

- **État:** 🔴 À commencer (30% de préparation)
- **Dates planifiées:** 2025-12-29 → 2026-01-12 (2 semaines)
- **Version cible:** v0.1.0-Beta
- **Priorité:** 🔴 CRITIQUE

---

## 📅 PHASES COMPLÈTES

### ✅ Phase Complétée : Wizard Installation & Auth 2FA

**Dates:** 2025-12-27 → 2025-12-28  
**Livrables:**
- ✅ Wizard installation complet et testé
- ✅ Authentification 2FA TOTP
- ✅ Rate limiting multi-niveaux
- ✅ Admin panel basique
- ✅ Sécurité headers HTTP
- ✅ Système i18n FR/EN

---

## 📊 TIMELINE GLOBALE

| # | Phase | Durée | Dates | Version | État |
|---|-------|-------|-------|---------|------|
| **1** | Email Workflows & Settings | 2 sem | 29/12 - 12/01 | v0.1.0-Beta | 🔴 À COMMENCER |
| **2** | Performance & Cache Redis | 2 sem | 13/01 - 26/01 | v0.2.0-Beta | ⏳ Après Ph1 |
| **3** | API v2 & Notifications | 3 sem | 27/01 - 16/02 | v0.3.0-Beta | ⏳ Après Ph2 |
| **4** | UI Contenus & Upload | 2 sem | 17/02 - 02/03 | v0.4.0-Beta | ⏳ Après Ph3 |
| **5** | Monitoring & DevOps CI/CD | 2 sem | 03/03 - 16/03 | v0.5.0-RC1 | ⏳ Parallèle Ph2 |
| **6** | Tests & Documentation | 2 sem | 17/03 - 30/03 | v0.9.0-RC2 | ⏳ Après Ph5 |
| **7** | Audit & Release v1.0.0 | 2 sem | 31/03 - 15/04 | **v1.0.0** | ⏳ Final |

**Total:** ~15 semaines → **v1.0.0 cible:** 2026-04-15

---

## 🏗️ DÉTAIL PHASE 1 — Email Workflows & Settings

### Sprint 1.1 — Email Verification (5 jours)

**Jour 1-2: EmailService**
- [ ] Configuration SMTP (env vars: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS)
- [ ] Templates HTML + texte
- [ ] Fonction send_email(to, subject, template, context)
- [ ] Tests mock SMTP

**Jour 3-4: Routes & Workflows**
- [ ] Route `POST /auth/send-verification` — Générer token, envoyer email
- [ ] Route `GET /auth/verify-email/<token>` — Valider token
- [ ] Model token avec expiration 24h
- [ ] Templates email/verification.html, auth/email-sent.html

**Jour 5: Tests & Docs**
- [ ] Tests 10+ cas
- [ ] Tests intégration workflow
- [ ] Documentation

### Sprint 1.2 — Password Reset (5 jours)

**Jour 1-2: Routes Password Reset**
- [ ] Route `GET /auth/forgot-password` — Formulaire
- [ ] Route `POST /auth/forgot-password` — Envoyer email
- [ ] Route `GET /auth/reset-password/<token>` — Formulaire reset
- [ ] Route `POST /auth/reset-password/<token>` — Valider password
- [ ] Token expiration 1h
- [ ] Rate limiting 3/heure

**Jour 3-4: Settings Model & UI**
- [ ] Modèle Settings (clé-valeur avec encryption)
- [ ] Route `GET /admin/settings` — UI paramètres
- [ ] Route `POST /admin/settings` — Sauvegarder
- [ ] UI configuration SMTP
- [ ] Migration DB

**Jour 5: Tests**
- [ ] Tests 15+ cas
- [ ] Tests Settings
- [ ] Documentation

### Critères de succès Phase 1

- [ ] Email verification end-to-end fonctionnel
- [ ] Password reset end-to-end fonctionnel
- [ ] Settings UI accessible
- [ ] Configuration SMTP persistante
- [ ] Tests coverage > 85%
- [ ] **v0.1.0-Beta taguée**

---

## 🔌 AUTRES PHASES (BRÈVES)

### Phase 2 — Cache Redis
- [ ] Setup Redis (local + docker)
- [ ] CacheService
- [ ] Cache sessions + rate limiting
- [ ] DB indexes

### Phase 3 — API v2 & Notifications
- [ ] JWT authentication
- [ ] Endpoints CRUD /api/v2/
- [ ] Model Notification
- [ ] UI notifications

### Phase 4 — Contenus & Upload
- [ ] Model Content
- [ ] UI CRUD contenus
- [ ] Upload fichiers
- [ ] Galerie médias

### Phase 5 — Monitoring & DevOps
- [ ] GitHub Actions CI/CD
- [ ] Logs structurés
- [ ] Sentry intégration
- [ ] Prometheus metrics

### Phase 6 — Tests & Documentation
- [ ] Coverage > 90%
- [ ] Documentation complète
- [ ] API Swagger

### Phase 7 — Audit & Release
- [ ] Audit sécurité
- [ ] Bug fixes
- [ ] **Release v1.0.0**

---

## 🎛️ STRUCTURE DU MENU ADMIN

### Sections Admin Planifiées

Basé sur Q2, voici la structure proposée :

```
📊 Admin
├── 📈 Tableau de bord
│   ├── Stats utilisateurs
│   ├── Stats login
│   └── Stats erreurs
│
├── 👥 Paramètres Utilisateurs
│   ├── Gestion utilisateurs (CRUD)
│   ├── Rôles & permissions
│   ├── Features flags utilisateur
│   └── Audit trail login
│
├── 📧 Paramètres Couriel
│   ├── Configuration SMTP
│   ├── Templates emails
│   ├── Variables traduction
│   ├── Test d'envoi
│   └── Historique envois
│
├── ⚙️ Paramètres Système
│   ├── Configuration générale
│   │   ├── Nom site
│   │   ├── Logo
│   │   ├── Footer
│   │   └── Langues activées
│   ├── Features flags
│   │   ├── Inscription activée
│   │   ├── 2FA requis
│   │   ├── Verification email requis
│   │   └── Upload activé
│   └── Limites
│       ├── Max utilisateurs
│       ├── Max fichiers/user
│       └── Max stockage
│
├── 🔒 Paramètres Sécurité
│   ├── Rate limiting
│   │   ├── Login (tentatives/heure)
│   │   ├── Email (envois/heure)
│   │   ├── API (requêtes/heure)
│   │   └── Durée lockout (minutes)
│   ├── Token validity
│   │   ├── Email verification (heures)
│   │   ├── Password reset (heures)
│   │   └── JWT (heures)
│   ├── Policy mot de passe
│   │   ├── Longueur min
│   │   ├── Caractères requis
│   │   └── Expiration
│   └── CORS/API keys
│
├── 📊 Paramètres Logs
│   ├── Niveau logs (DEBUG/INFO/WARNING/ERROR)
│   ├── Rotation logs
│   ├── Rétention (jours)
│   ├── Format logs
│   └── Viewing logs
│
├── 💾 Paramètres Sauvegarde
│   ├── Créer backup
│   ├── Restaurer backup
│   ├── Historique backups
│   ├── Planifier backups auto
│   └── Télécharger backup
│
├── 🔄 Paramètres Mise à Jour
│   ├── Vérifier mises à jour
│   ├── Historique versions
│   ├── Migrations
│   ├── Changelog
│   └── Update automatique
│
├── 📄 Contenu
│   ├── Gestion contenus (si implémenté)
│   ├── Catégories
│   └── Upload fichiers
│
└── ℹ️ À Propos
    ├── Version
    ├── Licence
    ├── Crédit/Attribution
    └── Support
```

### Détail Sections

#### 👥 Paramètres Utilisateurs
**Route:** `/admin/users`  
**Fonctionnalités:**
- Liste tous utilisateurs (tableau)
- Créer nouveau compte
- Éditer détails utilisateur
- Reset 2FA
- Débloquer compte
- Supprimer utilisateur
- Voir audit trail

#### 📧 Paramètres Couriel
**Route:** `/admin/email-settings`  
**Fonctionnalités:**
- Form SMTP (host, port, user, password, TLS)
- Sélectionner provider (Mailtrap/SendGrid/custom)
- Tester configuration (bouton "Envoyer test")
- Gérer templates (HTML + texte)
- Variables traduisibles
- Log historique envois

#### ⚙️ Paramètres Système
**Route:** `/admin/system-settings`  
**Fonctionnalités:**
- Branding (logo, footer text)
- Langues activées (FR, EN, etc.)
- Features flags on/off
- Limites stockage/utilisateurs

#### 🔒 Paramètres Sécurité
**Route:** `/admin/security-settings`  
**Fonctionnalités:**
- Rate limiting sliders
- Token validity inputs
- Policy mot de passe
- CORS allowlist
- API keys management

#### 📊 Paramètres Logs
**Route:** `/admin/logs-settings`  
**Fonctionnalités:**
- Niveau logs (dropdown)
- Rotation auto
- Rétention (jours)
- Viewer logs récents (tail)

#### 💾 Paramètres Sauvegarde
**Route:** `/admin/backup-settings`  
**Fonctionnalités:**
- Bouton "Créer backup maintenant"
- Liste backups (tableau)
- Restaurer backup (sélect + confirm)
- Planifier backups auto (cron)
- Télécharger backup

#### 🔄 Paramètres Mise à Jour
**Route:** `/admin/update-settings`  
**Fonctionnalités:**
- Afficher version actuelle
- Bouton "Vérifier mises à jour"
- Changelog
- Historique versions
- Migrations liste
- Auto-update toggle

---

## 📌 RÈGLES IMPORTANTES

### Pour Modifier ce Fichier

1. **Chaque nouvelle tâche commence par `[ ]` (unchecked)**
2. **Quand tâche complétée:** changer en `[x]` + date
3. **Quand phase complétée:** changer `🔴` en `✅`
4. **Mettre à jour "Dernière mise à jour" à chaque changement**

### Exemple

**AVANT:**
```
- [ ] Email verification workflow
```

**APRÈS (complété):**
```
- [x] Email verification workflow (2025-12-30)
```

### Ne JAMAIS

- ❌ Modifier le contenu de phases passées sans documenter
- ❌ Ajouter nouvelles phases sans accord
- ❌ Supprimer sections sans backup
- ❌ Oublier de mettre à jour cette référence

---

## 🎯 POINTS DE CONTRÔLE (Checkpoints)

### Checkpoint 1 — Fin Phase 1 (2026-01-12)

✅ Email verification fonctionnel  
✅ Password reset fonctionnel  
✅ Settings model + UI  
✅ Tests > 85% Phase 1  
✅ v0.1.0-Beta taguée

**Action:** SI OK → Phase 2 démarre, SINON → Debug

---

### Checkpoint 2 — Fin Phase 2 (2026-01-26)

✅ Redis fonctionnel  
✅ Cache hit rate > 70%  
✅ Performance < 200ms  
✅ Tests > 85% Phase 2  
✅ v0.2.0-Beta taguée

**Action:** SI OK → Phase 3, SINON → Optimisations

---

### Checkpoint 3 — Fin Phase 5 (2026-03-16)

✅ GitHub Actions CI/CD fonctionnel  
✅ Logs structurés  
✅ Monitoring actif  
✅ v0.5.0-RC1 taguée

**Action:** SI OK → Production ready, SINON → Debug DevOps

---

## 📚 DOCUMENTS LIÉS

- 📄 `docs/ROADMAP_TO_V1.0.md` — Roadmap détaillé
- 📄 `Analysis_reports/2025-12-29_ROADMAP_VS_IMPLEMENTATION_ANALYSIS.md` — État vs Planifié
- 📄 `.github/copilot-instructions.md` — Règles projet
- 📄 `CHANGELOG.md` — Historique releases

---

## ✍️ NOTES

**Pour les prochaines phases:**
- Chaque section du menu admin sera implémentée progressivement
- Priorité : Couriel → Sécurité → Système → Sauvegarde → Mise à jour
- Tests requis pour chaque nouvelle section (> 85% coverage)

---

**Prochaine étape:** Démarrer Phase 1 — Email Workflows & Settings

🚀 **Phase 1 commence:** 2025-12-29

