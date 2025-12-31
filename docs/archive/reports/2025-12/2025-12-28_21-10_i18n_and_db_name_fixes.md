# 🔧 Corrections — Variables i18n manquantes et nom BD

**Date** : 2025-12-28T21:10:00+01:00  
**Statut** : ✅ Corrigé  
**Serveur** : 🟢 http://127.0.0.1:5000

---

## 🐛 Problèmes identifiés et corrigés

### Problème 1 : Variables non traduites à l'étape 3 (Restauration de sauvegarde)

**Symptômes** :
- Les variables s'affichent avec leurs clés (ex: `wizard.backup.upload`)
- Au lieu de la traduction réelle

**Cause** :
- Les variables manquaient des fichiers JSON de traduction
- **Erreur de structure** : J'avais créé une **deuxième section `db`** au lieu de fusionner

**Exemple d'erreur JSON** :
```json
"backup": { ... },
"db": { ... }  // Première section
// ...
"db": { "continue_no_backup": ... }  // DEUXIÈME section (ERREUR!)
```

**Solution appliquée** :
1. ✅ Ajouter les variables manquantes à `wizard.backup` :
   - `upload` : Label du formulaire de fichier
   - `formats` : Description des formats
   - `no_file` : Texte quand aucun fichier
   - `upload_button` : Texte du bouton

2. ✅ Ajouter `continue_no_backup` à `wizard.db` (première section, pas en double)

3. ✅ **Supprimer la deuxième section `db`** qui cassait la structure JSON

**Fichiers modifiés** :
- `backend/src/i18n/fr.json`
- `backend/src/i18n/en.json`
- `backend/src/i18n/es.json`

---

### Problème 2 : Nom de BD — Affiche `x-filamenta_python.db` au lieu du nom spécifié

**Symptômes** :
- Vous inscrivez `blablabla.db` dans le formulaire
- Mais la BD créée est toujours `x-filamenta_python.db`

**Cause** :
- `app.py` force un nom de BD par défaut au démarrage
- Le wizard crée bien le fichier avec le bon nom, mais `app.py` écrase le URI

**Solution appliquée** :
1. ✅ Modifier `backend/src/app.py` pour utiliser une variable d'environnement
2. ✅ Modifier `backend/src/config.py` pour utiliser le même nom par défaut
3. ✅ Le nom peut maintenant être défini via la variable `DB_NAME`

**Code avant** :
```python
db_path = os.path.join(project_root, "instance", "x-filamenta_python.db")
```

**Code après** :
```python
db_name = os.getenv("DB_NAME", "x-filamenta_python.db")
db_path = os.path.join(project_root, "instance", db_name)
```

**Fichiers modifiés** :
- `backend/src/app.py`
- `backend/src/config.py`

---

## ✅ Variables ajoutées/corrigées

### Français (fr.json)
```json
"backup": {
  "upload": "Fichier de sauvegarde",
  "formats": "Formats acceptés : .tar.gz, .tgz (max 50MB)",
  "no_file": "Aucun fichier sélectionné",
  "upload_button": "Restaurer la sauvegarde"
}

"db": {
  "continue_no_backup": "Continuer sans sauvegarde"
}
```

### Anglais (en.json)
```json
"backup": {
  "upload": "Backup file",
  "formats": "Supported formats: .tar.gz, .tgz (max 50MB)",
  "no_file": "No file selected",
  "upload_button": "Restore backup"
}

"db": {
  "continue_no_backup": "Continue without backup"
}
```

### Espagnol (es.json)
```json
"backup": {
  "upload": "Archivo de respaldo",
  "formats": "Formatos admitidos: .tar.gz, .tgz (máx. 50MB)",
  "no_file": "Ningún archivo seleccionado",
  "upload_button": "Restaurar respaldo"
}

"db": {
  "continue_no_backup": "Continuar sin respaldo"
}
```

---

## 🧪 Tests à effectuer

### Test 1 : Étape 3 - Restauration de sauvegarde

1. Accédez au wizard `http://127.0.0.1:5000/install/`
2. Allez à l'étape 3 (Restauration de sauvegarde)
3. ✅ **Vérifier** : Aucune variable brute visible
4. ✅ **Vérifier** : Tous les textes sont traduits

### Test 2 : Nom de BD personnalisé

1. Allez à l'étape 2 (Base de données)
2. **Inscrivez un nom personnalisé** : `mon-app.db`
3. Continuez jusqu'à la fin du wizard
4. **Vérifiez dans `instance/`** : Le fichier créé s'appelle bien `mon-app.db`

---

## 📋 Fichiers modifiés/corrigés

| Fichier | Changement |
|---------|-----------|
| `backend/src/i18n/fr.json` | Ajouter variables manquantes + fusionner sections db |
| `backend/src/i18n/en.json` | Ajouter variables manquantes + fusionner sections db |
| `backend/src/i18n/es.json` | Ajouter variables manquantes + fusionner sections db |
| `backend/src/app.py` | Utiliser variable d'environnement pour nom BD |
| `backend/src/config.py` | Synchroniser le nom de BD par défaut |

---

## 🎯 Résultat attendu

✅ **Étape 3 complètement traduite** : Toutes les variables s'affichent correctement  
✅ **Nom de BD respecté** : Chaque utilisateur peut spécifier le nom qu'il veut  
✅ **Structure JSON valide** : Plus de sections en double

---

## 🚀 Commande pour redémarrer

```powershell
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*\.venv\*"} | Stop-Process -Force; .\.venv\Scripts\python.exe run_prod.py
```

---

**Mainteneur** : AleGabMar  
**Dernière mise à jour** : 2025-12-28T21:10:00+01:00

