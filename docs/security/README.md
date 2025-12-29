---
Purpose: Security documentation index
Description: Guides for securing and hardening X-Filamenta-Python

File: docs/security/README.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:05:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public

---

# 🔒 Sécurité — X-Filamenta-Python

**Guides de sécurité et bonnes pratiques.**

---

## 🎯 Sections principales

| Document | Sujet |
|----------|-------|
| [best-practices.md](best-practices.md) | Bonnes pratiques générales |
| [csrf-protection.md](csrf-protection.md) | Protection contre CSRF |
| [2fa.md](2fa.md) | Authentification 2FA (TOTP) |
| [secrets-management.md](secrets-management.md) | Gestion des secrets |

---

## 🔐 Sécurité intégrée

### ✅ Fonctionnalités de sécurité

- **Session sécurisées** : Flask sessions avec secret key
- **Authentification** : Login + password hashing (bcrypt)
- **2FA TOTP** : Authentification multi-facteurs
- **CSRF Protection** : Tokens sur tous les formulaires
- **Rate Limiting** : Protection contre les attaques par force brute
- **Headers de sécurité** : CSP, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security
- **Validation inputs** : Sanitization de tous les inputs
- **Parameterized Queries** : Pas de SQL injection (SQLAlchemy ORM)
- **Logging sécurisé** : Pas de données sensibles loggées

---

## 🧑‍💻 Pour les développeurs

1. **Lire** : [best-practices.md](best-practices.md)
2. **Lire** : [csrf-protection.md](csrf-protection.md)
3. **Lire** : [2fa.md](2fa.md)
4. **Lire** : [secrets-management.md](secrets-management.md)
5. **Implémenter** : Suivre les guidelines dans votre code

---

## 🔍 Pour les auditeurs/ops

**Checklist de sécurité** :

- [ ] Vérifier les headers HTTP (HTTPS, CSP, etc.)
- [ ] Vérifier les sessions (secret key, httponly, secure flags)
- [ ] Vérifier 2FA (TOTP, backup codes)
- [ ] Vérifier CSRF protection (tokens valides)
- [ ] Vérifier rate limiting (pas accessible sans limite)
- [ ] Vérifier logs (pas de données sensibles)
- [ ] Vérifier secrets (.env, pas hardcodés)

---

## 📚 Documentation supplémentaire

- **Features** → [../features/authentication.md](../features/authentication.md)
- **Architecture** → [../architecture/backend.md](../architecture/backend.md)
- **Déploiement** → [../deployment/README.md](../deployment/README.md)

---

**→ Consultez les guides détaillés pour chaque aspect de la sécurité.**

