# ✅ PROCHAINE ACTION — PHASE 1 CONTINUE

**Créé:** 2025-12-29 15:20 UTC+1  
**Status:** Infrastructure analysée, prêt à continuer

---

## 📊 CE QUE TU DOIS SAVOIR

✅ **Infrastructure 100% PRÊTE** (EmailService, Settings, User tokens, Templates)

❌ **Routes manquent** (Email verification, Password reset, Admin settings)

❌ **Templates auth manquent** (5 pages)

❌ **Tests absent** (À créer)

---

## 🎯 PROCHAIN TRAVAIL — Ordre d'Exécution

### ÉTAPE 1: Routes Email Verification (1 heure)

**Fichier:** `backend/src/routes/auth.py`

**À ajouter après les routes existantes:**

1. **Route POST /auth/send-verification** (25 lignes)
   - Récupérer user logué
   - Générer token : `user.generate_email_verification_token()`
   - Envoyer email : `EmailService.send_verification_email()`
   - Rediriger `auth/email-sent.html`

2. **Route GET /auth/verify-email/<token>** (20 lignes)
   - Rechercher user par token
   - Valider : `user.verify_email_token(token)`
   - Marquer vérifié : `user.mark_email_verified()`
   - Afficher `auth/email-verified.html`

---

### ÉTAPE 2: Routes Password Reset (1.5 heure)

**Fichier:** `backend/src/routes/auth.py`

**À ajouter:**

1. **Route GET /auth/forgot-password** (10 lignes)
   - Afficher formulaire `auth/forgot-password.html`

2. **Route POST /auth/forgot-password** (20 lignes)
   - Récupérer email
   - Trouver user
   - Générer token : `user.generate_password_reset_token()`
   - Envoyer email
   - Rediriger `auth/password-reset-sent.html`
   - Rate limit: 2/heure

3. **Route GET /auth/reset-password/<token>** (15 lignes)
   - Valider token existe
   - Afficher `auth/reset-password.html`

4. **Route POST /auth/reset-password/<token>** (25 lignes)
   - Valider passwords correspondent
   - Reset : `user.reset_password_with_token(token, password)`
   - Afficher confirmation
   - Rediriger login

---

### ÉTAPE 3: Templates Auth (1 heure)

**Fichiers à créer dans** `frontend/templates/auth/`:

1. **email-sent.html** (20 lignes)
   - Message attente
   - Email affiché
   - Lien resend (optionnel)

2. **email-verified.html** (15 lignes)
   - Confirmation succès
   - Bouton "Aller au login"

3. **forgot-password.html** (25 lignes)
   - Formulaire email
   - Validation client

4. **reset-password.html** (30 lignes)
   - Formulaire password
   - Formulaire password confirm
   - Validation strength

5. **password-reset-sent.html** (15 lignes)
   - Message attente
   - Lien "Retour login"

---

### ÉTAPE 4: Tests (1.5 heure)

**Fichier à améliorer/créer:** `backend/tests/test_email_verification.py`

**À tester (10+ cas):**
- [ ] Send verification email
- [ ] Verify valid token
- [ ] Verify expired token
- [ ] Verify wrong token
- [ ] Mark email verified
- [ ] Rate limiting send-verification

**Tests password reset (15+ cas):**
- [ ] Send reset email
- [ ] Reset with valid token
- [ ] Reset with expired token
- [ ] Passwords don't match
- [ ] Rate limiting forgot-password
- [ ] Update password success

---

### ÉTAPE 5 (Optionnel Jour 2): Admin Settings

**Route GET /admin/settings** (20 lignes)
- Récupérer settings
- Afficher form

**Route POST /admin/settings** (25 lignes)
- Sauvegarder settings
- Flash message

**Route POST /admin/settings/test-smtp** (15 lignes)
- Test SMTP
- Return JSON

**Améliorer template** `admin/settings.html`
- Ajouter sections SMTP, tokens, features

---

## 📋 CHECKLIST IMMÉDIATE

### Avant de Coder

- [ ] Lire `.github/copilot-instructions.md`
- [ ] Lire `docs/REFERENCE_PHASES.md`
- [ ] Lire `docs/user_preferences.md`
- [ ] Lire `globalPromptFiles://copilot-powershell.md`
- [ ] Nettoyer serveur : `.\.dev_scripts\utilities\clean_server.ps1`
- [ ] Démarrer serveur : `.\.dev_scripts\utilities\start_server.ps1`

### Code à Implémenter (Ordre)

1. **Routes email verification** (2 routes) — 1 heure
2. **Routes password reset** (4 routes) — 1.5 heure
3. **Templates auth** (5 pages) — 1 heure
4. **Tests** (25+ cas) — 1.5 heure
5. **Admin settings** (optionnel) — 1 heure

**TOTAL: 5-6 heures** (~1 journée complète)

---

## 🚀 COMMENCER MAINTENANT

**Question:** Veux-tu que je commence à coder maintenant ?

**Réponds par:**
- ✅ `OUI` — Start immediately
- 🤔 `ATTENDS` — Need clarification
- 📚 `RELIS` — Need more info

---

**JE SUIS PRÊT À CODER!** 🎯

*Attending for your GO command...*

