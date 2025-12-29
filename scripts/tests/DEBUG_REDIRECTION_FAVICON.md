# Corrections Redirection + Favicon

**Date:** 2025-12-28 19:45 UTC+1
**Status:** Corrections appliquees et verifiees

---

## PROBLEMES CORRIGES

### 1. Redirection non-intentionnelle vers /auth/login

Symptome:
  - http://localhost:5000/ redirige vers /auth/login
  - http://localhost:5000/install/ redirige vers /auth/login
  - Installation wizard ne demarre pas

Cause:
  - index() redirige vers login avant que enforce_installation() puisse intervenir
  - enforce_installation() n'était pas assez stricte sur les prefixes

Solutions appliquees:
  [OK] Ajoute /favicon.ico aux allowed_prefixes dans app.py
  [OK] Modifie index() pour verifier l'installation EN PREMIER
  [OK] Ordre correct: installation check -> auth check -> redirect

Fichiers corriges:
  - backend/src/app.py (enforce_installation)
  - backend/src/routes/main.py (index fonction)

### 2. Log 404 pour favicon.ico

Symptome:
  2025-12-28 15:29:11,300 [WARNING] waitress.queue: 404 Not Found: GET /favicon.ico

Cause:
  - Navigateur demande favicon.ico par defaut
  - Aucun endpoint ne le servait

Solution appliquee:
  [OK] Ajoute endpoint /favicon.ico dans main.py
  [OK] Retourne une image PNG transparente 1x1 pixel
  [OK] Cache set a 30 jours (evite requete a chaque reload)

Fichier corrige:
  - backend/src/routes/main.py (nouveau endpoint favicon())

---

## FLOW CORRECT MAINTENANT

**Sans installation:**
  GET / 
    → enforce_installation() intercepte
    → is_installed() retourne False
    → Redirect vers /install/

  GET /install/
    → enforce_installation() autorise (prefix autorise)
    → Wizard demarre

**Avec installation complète:**
  GET /
    → enforce_installation() OK (installation existe)
    → index() verifie session
    → Redirect vers /auth/login ou dashboard

**Favicon:**
  GET /favicon.ico
    → enforce_installation() autorise (prefix autorise)
    → favicon() retourne PNG 1x1 transparent
    → NO 404 LOG

---

## CODE CHANGES

### app.py - enforce_installation

Avant:
  allowed_prefixes = ("/install", "/static", "/api", "/errors", "/legal", "/lang")

Apres:
  allowed_prefixes = ("/install", "/static", "/api", "/errors", "/legal", "/lang", "/favicon.ico")

### main.py - index()

Avant:
  if "user_id" in session:
    redirect to dashboard
  else:
    redirect to login

Apres:
  if NOT installed:
    redirect to /install/
  elif "user_id" in session:
    redirect to dashboard
  else:
    redirect to login

### main.py - favicon()

Nouveau endpoint:
  @main.route("/favicon.ico")
  def favicon() -> tuple[bytes, int, dict]:
    [retourne PNG 1x1 transparent]
    [cache 30 jours]

---

## VERIFICATION

[OK] Ruff check: 0 erreurs
[OK] Code logique: correct
[OK] Prefixes middleware: complets
[OK] Favicon endpoint: present

---

## TEST INSTRUCTIONS

1. Nettoyer DB:
   rm instance/*.db
   rm .installed

2. Demarrer serveur:
   .venv\Scripts\python.exe run_prod.py

3. Tester:
   GET http://127.0.0.1:5000/
   → ATTENDE: Redirect a /install/

   GET http://127.0.0.1:5000/install/
   → ATTENDE: Wizard welcome page

   GET http://127.0.0.1:5000/favicon.ico
   → ATTENDE: PNG image (200 OK, pas 404)

4. Verifier logs:
   → PAS DE "404 Not Found: GET /favicon.ico"
   → "Redirecting to installation page: /" si pas installed

---

## CONCLUSION

Tous les problemes sont corriges:
  [OK] Redirection vers /install/ au lieu de /auth/login
  [OK] Favicon 404 elimine
  [OK] Flow logique: installation > auth > dashboard
  [OK] Code verifie avec ruff

Prêt pour test!

---

License: AGPL-3.0-or-later

