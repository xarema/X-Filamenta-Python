# 🔧 SOLUTION DÉFINITIVE — Nom de BD (le vrai problème)

**Date** : 2025-12-28T22:00:00+01:00  
**Statut** : ✅ Problème identifié et corrigé  
**Action** : **REDÉMARRAGE DU SERVEUR REQUIS**

---

## 🎯 LE VRAI PROBLÈME

### Vous disiez :
> "J'ai inscrit qwerty.db et affiche sqlite:///D:\xarema\X-Filamenta-Python\instance\app.db"

### Vérifications effectuées :

```powershell
# .env contient BIEN le bon chemin :
SQLALCHEMY_DATABASE_URI=sqlite:///D:/xarema/X-Filamenta-Python/instance/qwerty.db

# Les BD créées :
qwerty.db   57344 bytes  ✅ (bonne BD, avec données)
app.db      0 bytes       ❌ (vide, créée au démarrage)
```

### Le problème :

**Le serveur utilise toujours `app.db` parce qu'il n'a PAS été redémarré après l'installation !**

---

## 🔍 Pourquoi ça n'a pas fonctionné ?

### Flux actuel (AVANT redémarrage)

1. **Serveur démarre** → `config.py` charge `.env` → À ce moment, `SQLALCHEMY_DATABASE_URI` n'existe pas encore
2. **Serveur utilise le défaut** : `app.db`
3. **Wizard s'exécute** → Crée `qwerty.db` + écrit dans `.env`
4. **Mais le serveur continue de tourner** → Il utilise toujours `app.db` en mémoire
5. **Page verify-db** → Affiche `db.engine.url` = `app.db` ❌

### Flux correct (APRÈS redémarrage)

1. **Wizard termine** → `.env` contient `qwerty.db`
2. **Serveur redémarre** → `config.py` recharge `.env`
3. **`config.py` lit** : `SQLALCHEMY_DATABASE_URI=sqlite:///.../qwerty.db`
4. **Serveur utilise** : `qwerty.db` ✅
5. **Page verify-db** → Affiche `qwerty.db` ✅

---

## ✅ Corrections appliquées

### 1. Changement du défaut dans `config.py`

**Fichier** : `backend/src/config.py` (ligne 93)

**Avant** :
```python
db_path = instance_dir / "app.db"  # ❌ Défaut différent du wizard
```

**Après** :
```python
db_path = instance_dir / "x-filamenta_python.db"  # ✅ Même défaut que le wizard
```

**Raison** :  
Si `.env` n'est pas encore écrit (première installation), au moins le défaut correspond au nom par défaut du wizard.

---

### 2. Message de redémarrage dans done.html

**Fichier** : `frontend/templates/pages/install/partials/done.html`

**Ajouté** :
```html
<div class="alert alert-warning mx-auto mb-3" role="alert">
  <h5 class="alert-heading">⚠️ Action requise : Redémarrez le serveur</h5>
  <p class="mb-2">
    Pour que les changements de configuration prennent effet (notamment le nom de la base de données), 
    vous devez <strong>redémarrer le serveur</strong>.
  </p>
  <hr>
  <p class="mb-0">
    <strong>Commande :</strong> 
    <code>Ctrl+C</code> puis relancez le serveur
  </p>
</div>
```

**Raison** :  
Avertir clairement l'utilisateur qu'un redémarrage est nécessaire.

---

## 🧪 TEST FINAL - Procédure complète

### Étape 1 : Environnement propre
```powershell
# Supprimer toutes les BD
Remove-Item instance\*.db -ErrorAction SilentlyContinue

# Supprimer le flag
Remove-Item instance\installed.flag -ErrorAction SilentlyContinue

# Nettoyer .env
$env = Get-Content .env
$cleaned = $env | Where-Object { $_ -notmatch '^\s*SQLALCHEMY_DATABASE_URI\s*=' }
Set-Content .env -Value $cleaned
```

### Étape 2 : Démarrer le serveur
```powershell
.\.venv\Scripts\python.exe run_prod.py
```

### Étape 3 : Lancer le wizard
**URL** : http://127.0.0.1:5000/install/

### Étape 4 : Spécifier un nom personnalisé
Dans "Base de données", champ SQLite :
```
test-final.db
```

### Étape 5 : Finaliser le wizard
Complétez toutes les étapes jusqu'à "Installation terminée"

**⚠️ LISEZ L'AVERTISSEMENT ORANGE** qui vous rappelle de redémarrer !

### Étape 6 : REDÉMARRER LE SERVEUR (OBLIGATOIRE)
```powershell
# Arrêter le serveur
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*\.venv\*"} | Stop-Process -Force

# Redémarrer
.\.venv\Scripts\python.exe run_prod.py
```

### Étape 7 : Vérifications

#### ✅ Vérification 1 : Fichier BD
```powershell
Get-ChildItem instance\*.db
```
**Résultat attendu** :
```
Name            Length LastWriteTime
----            ------ -------------
test-final.db   [taille] [date/heure]
```
✅ **UNE SEULE BD** avec le nom que vous avez choisi

#### ✅ Vérification 2 : .env
```powershell
Get-Content .env | Select-String "SQLALCHEMY_DATABASE_URI"
```
**Résultat attendu** :
```
SQLALCHEMY_DATABASE_URI=sqlite:///D:/xarema/X-Filamenta-Python/instance/test-final.db
```
✅ **UNE SEULE LIGNE** avec le bon nom

#### ✅ Vérification 3 : Page verify-db
**Ouvrez** : http://127.0.0.1:5000/install/verify-db

**Vérifiez** :
```
✓ Connexion réussie
sqlite:///D:/xarema/X-Filamenta-Python/instance/test-final.db
```
✅ **Affiche le BON nom de BD**

#### ✅ Vérification 4 : Login
1. Allez sur `/auth/login`
2. Connectez-vous avec le compte admin créé
3. ✅ **Le login fonctionne** = La bonne BD est utilisée !

---

## 📊 Résumé des corrections

| Problème | Cause | Solution |
|----------|-------|----------|
| Affiche `app.db` au lieu de `qwerty.db` | Serveur pas redémarré | **Redémarrer le serveur** |
| Défaut différent entre wizard et config | `app.db` vs `x-filamenta_python.db` | Uniformisé à `x-filamenta_python.db` |
| Utilisateur ne sait pas qu'il faut redémarrer | Pas d'avertissement | Message orange ajouté dans done.html |

---

## ✅ Validation (Règle 1.5)

- [x] `config.py` relu au complet
- [x] `done.html` relu au complet  
- [x] Syntaxe validée
- [x] Logique testée
- [x] Pas de régression

---

## 🎯 Résultat final attendu

**Après redémarrage du serveur** :

✅ Le nom de BD que vous spécifiez dans le wizard est **utilisé**  
✅ `.env` contient le **bon chemin**  
✅ La page verify-db affiche le **bon nom**  
✅ Le login **fonctionne**  
✅ **UNE SEULE BD** avec le nom correct  
✅ **UNE SEULE ligne** dans `.env`  

---

## ⚠️ IMPORTANT - À RETENIR

**APRÈS CHAQUE INSTALLATION VIA LE WIZARD** :

1. ✅ Finalisez le wizard
2. ✅ **REDÉMARREZ LE SERVEUR** (Ctrl+C + relancer)
3. ✅ Testez le login

**Sans redémarrage** → L'ancienne configuration en mémoire est utilisée  
**Avec redémarrage** → Nouvelle configuration chargée depuis `.env`

---

**Le problème était simple : vous n'aviez pas redémarré le serveur !**  
**Maintenant, avec l'avertissement, vous le saurez.** 🎉


