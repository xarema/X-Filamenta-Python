---
Purpose: Common issues and solutions
Description: Troubleshooting guide for frequent problems

File: docs/troubleshooting/common-issues.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:15:00+01:00
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

# 🔧 Problèmes courants & Solutions

---

## 🚀 Démarrage & Installation

### Address already in use (Port 5000)

**Erreur :**
```
OSError: [Errno 48] Address already in use
```

**Causes possibles :**
- L'application est déjà lancée dans un autre terminal
- Un autre service utilise le port 5000

**Solutions :**

**Option 1 : Trouver et arrêter le processus**
```powershell
# Windows
Get-Process -Name python | Where-Object {$_.Path -like "*\.venv\*"} | Stop-Process -Force

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

**Option 2 : Utiliser un autre port**
```bash
export FLASK_PORT=5001
python run_prod.py
# Accédez à http://127.0.0.1:5001
```

---

### ImportError ou ModuleNotFoundError

**Erreur :**
```
ModuleNotFoundError: No module named 'flask'
```

**Cause :** Dépendances non installées

**Solution :**
```bash
pip install -r requirements.txt
npm install
```

**Vérifier :** `pip list | grep flask`

---

### Virtual environment non activé

**Symptôme :** Les commandes `pip` ou `python` utilisent la version système

**Solution :**
```bash
# Windows
.\.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Vérifier : le prompt doit montrer (.venv)
```

---

## 💾 Base de données

### Database connection refused

**Erreur :**
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
[Errno 2003] Can't connect to MySQL server on 'localhost:3306'
```

**Causes possibles :**
- Serveur BD non lancé
- Credentials invalides
- BD n'existe pas

**Solutions :**

**Vérifier que le serveur BD est lancé :**
```bash
# MySQL
mysql -u root -p  # Doit accepter la connexion

# PostgreSQL
psql -U postgres  # Doit accepter la connexion
```

**Vérifier les credentials dans .env :**
```bash
# Doit correspondre aux identifiants créés
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@host:3306/dbname
```

**Créer la BD si manquante :**
```sql
-- MySQL
CREATE DATABASE filamenta CHARACTER SET utf8mb4;

-- PostgreSQL
CREATE DATABASE filamenta;
```

---

### No such table: users

**Erreur :**
```
sqlite3.OperationalError: no such table: users
```

**Cause :** Les tables n'ont pas été créées (wizard non finalisé)

**Solutions :**

**Option 1 : Relancer le wizard**
```bash
rm instance/installed.flag
python run_prod.py
# Accédez à http://127.0.0.1:5000 et complétez le wizard
```

**Option 2 : Créer les tables manuellement (dev)**
```python
from backend.src.app import create_app
from backend.src.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Tables créées !")
```

---

### Database is locked (SQLite)

**Erreur :**
```
sqlite3.OperationalError: database is locked
```

**Cause :** Autre processus accède à la BD SQLite

**Solutions :**

1. **Attendre** (généralement temporaire)
2. **Redémarrer l'app :**
   ```bash
   # Arrêter
   Ctrl+C
   
   # Attendre 5s
   sleep 5
   
   # Redémarrer
   python run_prod.py
   ```

3. **Vérifier les processus :**
   ```bash
   # Windows
   Get-Process | Where-Object {$_.Handles -gt 100} | Select-Object Name
   
   # Linux
   lsof instance/app.db
   ```

---

## 🔐 Authentification & Sécurité

### Redirect too many times (Login loop)

**Erreur :**
```
ERR_TOO_MANY_REDIRECTS
This page isn't working. localhost redirected you too many times.
```

**Causes possibles :**
- Session invalide
- Cookies corrompus
- Redirection mal configurée

**Solutions :**

1. **Vider les cookies :**
   - Chrome/Firefox : F12 → Application → Cookies → Supprimer tout
   - Ou utiliser mode Incognito

2. **Vérifier la session :**
   ```python
   from flask import session
   print(session)  # Doit contenir 'user_id'
   ```

3. **Vérifier la config :**
   - `.env` doit contenir : `SECRET_KEY=...`
   - `SESSION_COOKIE_SECURE=False` (dev) ou `True` (prod)

---

### Cannot verify csrf token

**Erreur :**
```
BadRequest: 400 Bad Request - CSRF token missing or invalid
```

**Causes :**
- Token CSRF manquant dans le formulaire
- Token expiré

**Solutions :**

**Vérifier le formulaire :**
```html
<form method="POST">
    {{ csrf_token() }}  <!-- MUST be present -->
    <!-- autres champs -->
</form>
```

**Avec HTMX :**
```html
<button hx-post="/endpoint" 
        hx-headers='{"X-CSRFToken": "{{ csrf_token() }}"}'> 
    Click
</button>
```

---

## 🌍 Frontend

### Static files not loading (CSS/JS)

**Symptôme :** Page défigurée, CSS manquant, JS non chargé

**Cause :** Fichiers statiques non trouvés

**Solutions :**

```bash
# Vérifier que les fichiers existent
ls -la frontend/static/

# Vérifier les permissions
chmod -R 755 frontend/static/

# Vider le cache navigateur
F12 → Network → Disable cache → Refresh
```

**En prod :** Configurer Nginx/Apache pour servir les statiques

---

### HTMX not working / requests pending

**Symptôme :** Boutons HTMX ne répondent pas

**Solutions :**

1. **Vérifier HTMX chargé :**
   ```bash
   # F12 → Console
   > htmx  # Doit afficher l'objet htmx
   ```

2. **Vérifier les endpoints :**
   ```bash
   # F12 → Network
   # Vérifier que les requêtes vont aux bons endpoints
   ```

3. **Vérifier les erreurs :**
   ```bash
   # F12 → Console → Voir les erreurs
   # F12 → Network → Voir les réponses (4xx, 5xx)
   ```

---

## 📝 Logs & Débogage

### Voir les logs en dev

```bash
# Logs Flask
export FLASK_ENV=development
python run_prod.py  # Logs plus détaillés

# Logs application
tail -f instance/logs/app.log  # Si applicable
```

### Activer le debug mode

```python
# Temporaire dans app.py
app.debug = True

# Ou via env
export FLASK_DEBUG=1
python run_prod.py
```

---

## 🆘 Obtenir de l'aide

Si votre problème n'est pas listé :

1. **Vérifier les logs** : Chercher les messages d'erreur
2. **Reproduire** : Essayer d'identifier les étapes exactes
3. **Créer une issue** : Sur GitHub avec contexte complet
   - Description du problème
   - Étapes pour reproduire
   - Logs/erreurs
   - Environment (OS, Python version, etc.)

---

**→ Consultez [faq.md](faq.md) pour les questions générales.**

