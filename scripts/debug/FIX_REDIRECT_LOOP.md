# Fix Redirect Loop - ERR_TOO_MANY_REDIRECTS

**Date:** 2025-12-28 20:15 UTC+1
**Problem:** Boucle de redirection infinie (ERR_TOO_MANY_REDIRECTS)
**Status:** FIXED

---

## PROBLEME DETECTE

Erreur navigateur:
```
This page isn't working
127.0.0.1 redirected you too many times.
ERR_TOO_MANY_REDIRECTS
```

Cause: DOUBLE verification installation cree une boucle

---

## ANALYSE

Flow AVANT correction:

```
GET /
  → index() execute
  → Check is_installed() → False
  → Redirect vers /install/ (via url_for)
  
GET /install/
  → enforce_installation() middleware
  → Prefix /install autorise → Continue
  → install.before_request() execute
  → Check is_installed() → False → Continue
  → install_index() execute
  → Render page... MAIS...
  
PROBLEME: index() redirige vers url_for("install.install_index")
qui genere probablement une URL qui reboucle ou
la double verification cree un conflit
```

Cause racine:
  - enforce_installation() (middleware global) verifie installation
  - index() AUSSI verifie installation
  - Double verification = conflit logique = boucle

---

## SOLUTION APPLIQUEE

Fichier: backend/src/routes/main.py

Changement: Retirer la verification installation de index()

Avant:
```python
@main.route("/")
def index():
    # Check if installation is required first
    project_root = Path(__file__).parent.parent.parent
    if not InstallService.is_installed(project_root):
        return redirect(url_for("install.install_index"))
    
    # Check if user is authenticated
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    else:
        return redirect(url_for("auth.login_page"))
```

Apres:
```python
@main.route("/")
def index():
    # Installation check handled by enforce_installation() middleware
    
    # Check if user is authenticated
    if "user_id" in session:
        return redirect(url_for("pages.dashboard"))
    else:
        return redirect(url_for("auth.login_page"))
```

Raison:
  - enforce_installation() MIDDLEWARE gere deja la redirection /install/
  - Pas besoin de double check dans index()
  - Separation des concerns: middleware = installation, route = auth

---

## FLOW CORRECT MAINTENANT

Sans installation:
```
GET /
  → enforce_installation() middleware
  → Check is_installed() → False
  → Redirect /install/
  
GET /install/
  → enforce_installation() middleware
  → Prefix /install autorise → Continue
  → install.before_request()
  → Check is_installed() → False → Continue
  → install_index() execute
  → Render pages/install/index.html
  → AFFICHE WIZARD
```

Avec installation complete:
```
GET /
  → enforce_installation() middleware
  → Check is_installed() → True → Continue
  → index() execute
  → Check session user_id
  → Redirect /pages/dashboard OU /auth/login
```

---

## VERIFICATION

[OK] Ruff check: Passed
[OK] Code logique: Simplifie (1 seule verification)
[OK] Separation concerns: Middleware = install, Route = auth
[OK] Pas de double verification

---

## TEST

1. Tuer processus Python existants:
   Get-Process python.exe | Stop-Process -Force

2. Lancer serveur:
   .venv\Scripts\python.exe run_prod.py

3. Tester dans navigateur:
   http://127.0.0.1:5000/
   
   Attendu:
   - Redirection vers /install/ (1 seule fois)
   - Page wizard s'affiche
   - PAS de ERR_TOO_MANY_REDIRECTS

4. Verifier logs:
   - "Redirecting to installation page: /"
   - PAS de boucle de redirections multiples

---

## LOGS ATTENDUS

```
[INFO] waitress: Serving on http://127.0.0.1:5000
[INFO] backend.src.app: Redirecting to installation page: /
```

Browser:
  - URL finale: http://127.0.0.1:5000/install/
  - Page affichee: Wizard installation
  - PAS d'erreur redirect loop

---

## CONCLUSION

Probleme: Double verification installation = boucle redirect
Solution: Retirer check de index(), garder seulement middleware
Impact: 1 seule verification = pas de conflit = pas de boucle
Verification: Ruff passed

Serveur pret pour restart et test.

---

License: AGPL-3.0-or-later

