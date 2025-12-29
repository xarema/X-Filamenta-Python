---
Purpose: Authentication and security features documentation
Description: Comprehensive guide to login, 2FA, CSRF protection, and security

File: docs/features/authentication.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:10:00+01:00
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

# 🔐 Authentification & 2FA

**Authentification sécurisée avec support 2FA (TOTP).**

---

## 🎯 Vue d'ensemble

L'authentification X-Filamenta-Python comporte trois niveaux de sécurité :

1. **Authentification simple** : Username/Email + Mot de passe
2. **2FA TOTP** : Code à usage unique (authenticator app)
3. **Backup codes** : Codes de secours si authenticator perdu

---

## 🔑 Authentification simple

### Flux de login

```
1. Utilisateur accède à /auth/login
2. Remplit formulaire : username/email + password
3. Validation des credentials
4. Si 2FA activé → Redirection vers /auth/2fa-verify
5. Si 2FA désactivé → Création session → Redirection dashboard
```

### Spécifications techniques

**Endpoint :** `POST /auth/login`

**Paramètres :**
- `username_or_email` : String (username ou email)
- `password` : String (mot de passe)
- `remember_me` : Boolean (optionnel, défaut=false)

**Réponses :**
- `200 OK` : Login réussi → Redirection dashboard/2FA
- `401 Unauthorized` : Credentials invalides
- `429 Too Many Requests` : Trop de tentatives (rate limit)
- `500 Server Error` : Erreur serveur

**Sécurité :**
- ✅ Hash bcrypt (cost=12)
- ✅ Rate limiting (5 essais/heure par IP)
- ✅ CSRF token requis
- ✅ Session sécurisée (HttpOnly, Secure, SameSite)

---

## 🔑 2FA TOTP (Time-based One-Time Password)

### Activation 2FA

**Flux :**

```
1. Utilisateur accède à /account/security/2fa
2. Génération secret TOTP (32 chars base32)
3. Affichage QR code
4. Utilisateur scanne avec authenticator (Google Authenticator, Authy, etc.)
5. Utilisateur entre code du phone (6 digits)
6. Validation et activation
7. Génération backup codes (10x codes 8-digits)
8. Affichage + demande de sauvegarde
```

**Specs TOTP :**
- Algorithme : SHA-1
- Fenêtre temps : 30 secondes
- Digits : 6
- Fenêtre validation : ±1 période (60s total)

### Vérification 2FA

**Endpoint :** `POST /auth/2fa-verify`

**Paramètres :**
- `code` : String (6 digits du phone)
- OU `backup_code` : String (code de secours 8-digits)

**Réponses :**
- `200 OK` : Vérification réussie → Création session
- `401 Unauthorized` : Code invalide
- `429 Too Many Requests` : Trop de tentatives (rate limit)

**Sécurité :**
- ✅ Codes invalidés après utilisation
- ✅ Fenêtre temps stricte (±30s)
- ✅ Rate limiting (3 essais/5min par utilisateur)
- ✅ Backup codes hashés (bcrypt)

---

## 🆘 Backup codes

### Génération

À l'activation de 2FA :
- 10 codes de 8 digits générés aléatoirement
- Tous hashés au stockage
- Affichés une seule fois à l'utilisateur
- L'utilisateur doit copier/coller ou télécharger

### Utilisation

- Chaque code ne peut être utilisé qu'une fois
- Utilisable à la place du code TOTP
- Cas d'usage : perte de l'authenticator

### Régénération

- Possible depuis /account/security/2fa
- Invalide tous les anciens codes
- Affiche nouveaux codes

---

## 🛡️ CSRF Protection

### Mise en œuvre

**Token CSRF :**
- ✅ Généré par Flask-WTF
- ✅ Stocké en session (HttpOnly)
- ✅ Inclus dans tous les formulaires (`{{ csrf_token() }}`)
- ✅ Validé automatiquement sur POST/PUT/DELETE

**Dans les templates :**
```html
<form method="POST">
    {{ csrf_token }}
    <!-- Autres champs -->
</form>
```

Ou avec HTMX :
```html
<button hx-post="/endpoint" hx-headers='{"X-CSRFToken": "{{ csrf_token() }}"}'>
    Bouton
</button>
```

### Endpoints protégés

- ✅ `/auth/login` - POST
- ✅ `/auth/logout` - POST
- ✅ `/auth/2fa-verify` - POST
- ✅ Tous les formulaires utilisateur

---

## 📊 Scénarios de sécurité

### Scénario 1 : Login simple

```
User → /auth/login
       → Saisit credentials
       → POST /auth/login (CSRF token inclus)
       → Serveur valide (bcrypt, rate limit)
       → Session créée (HttpOnly)
       → Redirection /dashboard
```

### Scénario 2 : Login + 2FA

```
User → /auth/login
       → Saisit credentials
       → POST /auth/login (CSRF token)
       → Serveur → /auth/2fa-verify (session temporaire)
       → User scanne authenticator
       → Saisit code TOTP (6 digits)
       → POST /auth/2fa-verify (CSRF token)
       → Serveur valide TOTP (fenêtre temps strict)
       → Session complète créée
       → Redirection /dashboard
```

### Scénario 3 : Code TOTP perdu

```
User → /auth/login + credentials
       → /auth/2fa-verify
       → Impossible scanner phone
       → Utilise backup code (8 digits)
       → POST /auth/2fa-verify?type=backup
       → Serveur invalide ce code
       → Session complète créée
       → Peut régénérer codes depuis compte
```

### Scénario 4 : Attaque par force brute

```
Attacker → /auth/login
          → 100 POST /auth/login en 1 heure
          → Après 5 tentatives → 429 Too Many Requests
          → IP bloquée temporairement
          → Rate limit reset après 1 heure
```

---

## 🔒 Stockage des credentials

| Données | Stockage | Sécurité |
|---------|----------|----------|
| Password | DB (bcrypt hash) | ✅ Hash non réversible |
| TOTP Secret | DB (clair, DB chiffré à déploiement) | ✅ DB sécurisée |
| Backup Codes | DB (bcrypt hash) | ✅ Hash non réversible |
| Session Token | Session (HttpOnly, Secure) | ✅ Cookie sécurisé |

---

## 📋 Checklist sécurité

- [x] Password hashing (bcrypt cost=12)
- [x] Rate limiting authentification
- [x] Session HttpOnly + Secure + SameSite
- [x] CSRF tokens sur tous les formulaires
- [x] 2FA TOTP avec validat fenêtre temps
- [x] Backup codes hashés
- [x] Pas de credentials loggés
- [x] Validation stricte des inputs
- [x] Timeouts de session
- [x] Logging des actions sensibles

---

## 📚 Ressources

- **Guide sécurité** → [../security/best-practices.md](../security/best-practices.md)
- **CSRF Protection** → [../security/csrf-protection.md](../security/csrf-protection.md)
- **2FA Guide** → [../security/2fa.md](../security/2fa.md)

---

**→ Consultez les guides spécialisés pour des détails techniques.**

