# 🔴 RAPPORT CORRECTION - Session Persistence Fix
**Date:** 30 Décembre 2025 | **Heure:** 10:00 UTC  
**Status:** 🔴 EN COURS | **Priority:** CRITIQUE

---

## **PROBLÈME ROOT CAUSE**

### **Session Non-Persistante Après Login**

**Symptôme:** Boucle de redirection `/login` ↔ `/dashboard`

**Cause Racine:**
- `login_user(user)` est appelé dans le POST `/auth/login`
- Mais `Flask-Login` sauvegarde `user_id` dans **la session Flask**
- La session Flask utilise le filesystem via `Flask-Session`
- Le cache filesystem essaie de sérialiser l'objet User ENTIER via notre cache_service (ERREUR!)
- La session n'est PAS sauvegardée → `current_user.is_authenticated` reste False
- `/dashboard` redirige vers `/auth/login`
- Boucle infinie!

**Localisation Exacte:**
- `auth.py` ligne 125-150 (POST login handler)
- `app.py` ligne 245 (context_processor inject_auth_status)

---

## **SOLUTIONS**

### **FIX #1: Désactiver le cache pour les objets User**
```python
# Dans cache_service.py - adapter le code pour PASSER le cache si c'est un User
if isinstance(value, User):
    # Never cache User objects, let Flask-Session handle it
    return
```

### **FIX #2: Vérifier que Flask-Login sauvegarde `user_id` pas l'objet**
Flask-Login DOIT sauvegarder seulement l'ID utilisateur, pas l'objet entier.

### **FIX #3: Vérifier les headers de la réponse POST login**
Le POST doit retourner un header `HX-Redirect` ou `Location` pointant vers `/dashboard`

---

## **ÉTAPES DE CORRECTION**

1. **URGENT:** Modifier `cache_service.py` pour skipper les objets User
2. **URGENT:** Ajouter logs de debug dans `login()` POST handler
3. **URGENT:** Vérifier que Flask-Session persiste correctement
4. **HIGH:** Tester le login flow complètement (POST → session saved → redirect → dashboard)

---

## **TEST VALIDATION**

```bash
# 1. Démarrer server
.\.venv\Scripts\python.exe run_prod.py

# 2. Terminal 2: Tester login avec curl
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' \
  -v  # Show headers

# 3. Vérifier:
#    - Session cookie dans la réponse
#    - Pas d'erreur JSON serialization
#    - Redirection vers /dashboard (HTTP 303 ou HX-Redirect header)
```


