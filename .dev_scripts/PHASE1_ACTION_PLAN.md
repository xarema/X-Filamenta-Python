# 🚀 PHASE 1 — PLAN D'ACTION IMMÉDIAT

**Statut:** Infrastructure 100% PRÊTE, Workflows à implémenter  
**Jour:** 3 (réel) - Jour 3-4 (selon ROADMAP)  
**Durée estimée:** 1-2 jours

---

## ✅ CE QUI EST PRÊT À UTILISER

```
✅ EmailService (340 lignes) — COMPLET
✅ Settings Model (349 lignes) — COMPLET  
✅ User Model + tokens — COMPLET
✅ Email Templates (HTML + TXT) — COMPLET
✅ Auth routes (login/logout) — COMPLET
```

## ❌ À CODER MAINTENANT

```
❌ Routes email verification (2 routes)
❌ Routes password reset (4 routes)
❌ Templates auth (5 pages)
❌ Admin settings routes (3 routes)
❌ Tests (25+ cas)
```

---

## 📋 PRIORITÉ 1 — Email Verification Routes

### Route 1: POST /auth/send-verification

**Pseudo-code:**
```python
@auth.route("/send-verification", methods=["POST"])
@login_required  # User doit être connecté
@rate_limit("10 per hour")  # 10 fois/heure max
def send_verification():
    user = get_current_user()
    
    # Générer token
    token = user.generate_email_verification_token()
    db.session.commit()
    
    # Envoyer email
    email_service = EmailService()
    success = email_service.send_verification_email(
        user.email,
        user.username,
        token
    )
    
    if success:
        return render_template("auth/email-sent.html", email=user.email)
    else:
        flash("Erreur envoi email")
        return redirect(url_for("pages.dashboard"))
```

---

### Route 2: GET /auth/verify-email/<token>

**Pseudo-code:**
```python
@auth.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    # Trouver user par token
    user = User.query.filter_by(email_verification_token=token).first()
    
    if not user:
        flash("Token invalide")
        return redirect(url_for("auth.login_page"))
    
    # Valider token
    if not user.verify_email_token(token):
        flash("Token expiré")
        return redirect(url_for("auth.login_page"))
    
    # Marquer vérifié
    user.mark_email_verified()
    db.session.commit()
    
    # Afficher confirmation
    return render_template("auth/email-verified.html")
```

---

## 📋 PRIORITÉ 2 — Password Reset Routes

### Route 3-6: Forgot Password & Reset

**Pseudo-code:**
```python
@auth.route("/forgot-password", methods=["GET"])
def forgot_password_page():
    return render_template("auth/forgot-password.html")

@auth.route("/forgot-password", methods=["POST"])
@rate_limit("2 per hour")  # 2 fois/heure
def forgot_password():
    email = request.form.get("email", "").strip()
    
    if not email:
        flash("Email requis")
        return render_template("auth/forgot-password.html")
    
    user = User.get_by_email(email)
    
    if user:
        # Générer token
        token = user.generate_password_reset_token()
        db.session.commit()
        
        # Envoyer email (même si user n'existe pas pour sécurité)
        email_service = EmailService()
        email_service.send_password_reset_email(
            user.email,
            user.username,
            token
        )
    
    return render_template("auth/password-reset-sent.html")

@auth.route("/reset-password/<token>", methods=["GET"])
def reset_password_page(token):
    # Valider token existe
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user or not user.verify_password_reset_token(token):
        flash("Lien expiré")
        return redirect(url_for("auth.login_page"))
    
    return render_template("auth/reset-password.html", token=token)

@auth.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")
    
    # Validation
    if not password or password != password_confirm:
        flash("Passwords ne correspondent pas")
        return render_template("auth/reset-password.html", token=token)
    
    # Trouver user
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user or not user.reset_password_with_token(token, password):
        flash("Erreur reset password")
        return redirect(url_for("auth.login_page"))
    
    db.session.commit()
    
    flash("Password réinitialisé avec succès")
    return redirect(url_for("auth.login_page"))
```

---

## 📋 PRIORITÉ 3 — Admin Settings Routes

### Routes Admin Settings

```python
@admin.route("/settings", methods=["GET"])
@admin_required
def settings_page():
    settings = Settings.get_all()
    return render_template("admin/settings.html", settings=settings)

@admin.route("/settings", methods=["POST"])
@admin_required
def save_settings():
    # Récupérer et sauvegarder settings
    Settings.set("smtp_host", request.form.get("smtp_host"))
    Settings.set("smtp_port", request.form.get("smtp_port"))
    Settings.set("smtp_user", request.form.get("smtp_user"))
    Settings.set("smtp_password", request.form.get("smtp_password"))
    # ... autres settings
    
    flash("Settings sauvegardés")
    return redirect(url_for("admin.settings_page"))

@admin.route("/settings/test-smtp", methods=["POST"])
@admin_required
def test_smtp():
    email_service = EmailService()
    success, message = email_service.test_smtp_connection()
    
    return jsonify({
        "success": success,
        "message": message
    })
```

---

## 📝 Templates À Créer

### 1. auth/email-sent.html
- Message attente verification
- Email affiché
- Bouton "Resend" (optionnel)

### 2. auth/email-verified.html
- Confirmation OK
- Bouton "Go to login"

### 3. auth/forgot-password.html
- Formulaire email
- Validation client

### 4. auth/reset-password.html
- Formulaire password + confirm
- Validation password strength

### 5. auth/password-reset-sent.html
- Message attente reset
- Lien "Back to login"

---

## ✅ CHECKLIST IMMÉDIATE

**Jour 3 (aujourd'hui):**
- [ ] Routes verification (2 routes)
- [ ] Routes password reset (4 routes)
- [ ] Templates (5 pages)
- [ ] Tests (10+ cas)

**Jour 4:**
- [ ] Routes admin settings (3 routes)
- [ ] Améliorer `admin/settings.html`
- [ ] Tests settings (8+ cas)
- [ ] Tests intégration complets

**Jour 5:**
- [ ] Tests finaux (coverage > 85%)
- [ ] Documentation
- [ ] CHANGELOG update
- [ ] Version tag v0.1.0-Beta

---

**READY TO CODE?** 🚀

