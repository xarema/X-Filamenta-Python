# 🔧 SOLUTION FINALE — Nom de BD personnalisé

**Date** : 2025-12-28T21:30:00+01:00  
**Statut** : ✅ Code corrigé — Test requis

---

## 🎯 RÉSUMÉ DU PROBLÈME

**Vous spécifiez un nom de BD** : `blablabla.db`  
**Mais la BD utilisée est** : `app.db`

---

## 🔍 CAUSES IDENTIFIÉES

### 1. `app.py` forçait `app.db` par défaut ❌
```python
# Code problématique (CORRIGÉ)
if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    db_path = os.path.join(project_root, "instance", "app.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
```

### 2. `config.py` ne chargeait PAS `.env` ❌
Le fichier `.env` existe, mais Python ne le lit pas automatiquement.

### 3. Le wizard sauvegardait dans `.env` mais...
L'écriture échouait ou ne s'exécutait pas jusqu'à la fin.

---

## ✅ CORRECTIONS APPLIQUÉES

### 1. Suppression du fallback `app.db` dans `app.py`
**Fichier** : `backend/src/app.py`

**Avant** :
```python
if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    db_path = os.path.join(project_root, "instance", "app.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
```

**Après** :
```python
# Supprimé — config.py gère la BD
```

### 2. Ajout de `load_dotenv()` dans `config.py`
**Fichier** : `backend/src/config.py`

**Ajouté** :
```python
import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, env vars must be set manually
```

### 3. Code du wizard pour sauvegarder dans `.env`
**Fichier** : `backend/src/routes/install.py` (lignes ~347-372)

Le wizard sauvegarde maintenant la BD dans `.env` après l'installation réussie.

---

## 🧪 TEST REQUIS

### Option 1 : Refaire le wizard complet (RECOMMANDÉ)

1. **Supprimer** : `instance/installed.flag`
   ```powershell
   Remove-Item instance\installed.flag -ErrorAction SilentlyContinue
   ```

2. **Démarrer le serveur** :
   ```powershell
   Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*\.venv\*"} | Stop-Process -Force
   .\.venv\Scripts\python.exe run_prod.py
   ```

3. **Lancer le wizard** : `http://127.0.0.1:5000/install/`

4. **Spécifier un nom personnalisé** : `mon-test.db`

5. **Finaliser l'installation**

6. **Vérifier `.env`** :
   ```powershell
   Get-Content .env | Select-String "SQLALCHEMY_DATABASE_URI"
   ```
   ✅ Doit afficher : `SQLALCHEMY_DATABASE_URI=sqlite:///D:/xarema/X-Filamenta-Python/instance/mon-test.db`

7. **Redémarrer le serveur**

8. **Vérifier que la BD utilisée est bien `mon-test.db`**

### Option 2 : Configurer manuellement `.env`

1. **Éditer `.env`** et remplacer :
   ```
   # SQLALCHEMY_DATABASE_URI=sqlite:///./app.db
   ```
   
   Par (décommenté) :
   ```
   SQLALCHEMY_DATABASE_URI=sqlite:///D:/xarema/X-Filamenta-Python/instance/votre-nom.db
   ```

2. **Redémarrer le serveur**

---

## 📝 FICHIERS MODIFIÉS

| Fichier | Modification |
|---------|--------------|
| `backend/src/app.py` | Suppression du fallback `app.db` |
| `backend/src/config.py` | Ajout de `load_dotenv()` |
| `backend/src/routes/install.py` | Sauvegarde dans `.env` après install |

---

## ✅ VALIDATION

- [x] Syntaxe Python validée (py_compile)
- [x] Code revu au complet
- [x] `load_dotenv()` ajouté
- [x] Fallback `app.db` supprimé
- [x] Wizard sauvegarde dans `.env`

---

## 🚀 PROCHAINE ÉTAPE

**TESTEZ en refaisant le wizard complet** pour confirmer que tout fonctionne.

Si problème persiste, vérifiez :
1. Que `.env` contient `SQLALCHEMY_DATABASE_URI=...`
2. Que la ligne n'est PAS commentée (`#`)
3. Que le chemin est correct

---

**Le problème est résolu en théorie. Test utilisateur requis.**


