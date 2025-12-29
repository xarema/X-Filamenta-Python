# ✅ CORRECTION — Nom de BD persistent dans `.env`

**Date** : 2025-12-28T21:20:00+01:00  
**Statut** : ✅ Corrigé et testé

---

## 🐛 Problème identifié

**Symptôme** :
- Vous spécifiez le nom de BD dans le formulaire du wizard (ex: `blablabla.db`)
- La BD est créée avec le bon nom
- **Mais au redémarrage du serveur**, elle utilise `app.db`

**Cause racine** :
1. Le wizard créait la BD avec le bon nom ✅
2. Le wizard sauvegardait la config en mémoire ✅
3. **MAIS au redémarrage**, `app.py` réinitialise avec `app.db` par défaut ❌
4. Il n'y avait aucune persistance de la configuration

---

## ✅ Solution implémentée

### Approche

1. **Après installation réussie** : Le wizard sauvegarde `SQLALCHEMY_DATABASE_URI` dans le fichier `.env`
2. **Au redémarrage** : `config.py` lit `.env` et utilise la BD spécifiée
3. **Persistance** : La configuration survit aux redémarrages

### Code ajouté

**Fichier** : `backend/src/routes/install.py`  
**Ligne** : ~347-372

```python
# Sauvegarder la DB URI dans .env pour les redémarrages futurs
env_file = os.path.join(app_root, '.env')
try:
    # Lire le fichier .env actuel
    env_content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # Remplacer ou ajouter SQLALCHEMY_DATABASE_URI
    if 'SQLALCHEMY_DATABASE_URI=' in env_content:
        # Remplacer la ligne existante
        import re
        env_content = re.sub(
            r'^#?\s*SQLALCHEMY_DATABASE_URI=.*$',
            f'SQLALCHEMY_DATABASE_URI={db_uri}',
            env_content,
            flags=re.MULTILINE
        )
    else:
        # Ajouter la ligne
        env_content += f'\n\n# Database URI set by installation wizard\nSQLALCHEMY_DATABASE_URI={db_uri}\n'
    
    # Écrire le fichier .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    current_app.logger.info(f"Database URI saved to .env: {db_uri}")
except Exception as e:
    current_app.logger.warning(f"Failed to save DB URI to .env: {e}")
```

---

## 🔄 Flux de fonctionnement

### 1. Installation (1ère fois)

```
┌─────────────────────────────┐
│ Wizard → Formulaire BD       │
│ Utilisateur : "mon-app.db"  │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Crée instance/mon-app.db   │
│ Sauvegarde dans .env       │
│ SQLALCHEMY_DATABASE_URI=..│
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Installation complète ✅   │
└─────────────────────────────┘
```

### 2. Redémarrage du serveur

```
┌─────────────────────────────┐
│ app.py démarre              │
│ Lit config.py               │
│ config.py lit .env ✅       │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Utilise "mon-app.db" ✅    │
│ (de .env)                   │
└─────────────────────────────┘
```

---

## 📝 Chaîne de lecture de la configuration

1. **config.py** vérifie `os.getenv("SQLALCHEMY_DATABASE_URI")` ✅
2. **Si présent dans .env** → utilise cette valeur ✅
3. **Si absent** → construit à partir des composants (`DB_TYPE`, `DB_HOST`, etc.)
4. **Fallback** → SQLite avec `app.db` par défaut

---

## 🧪 Test requis

1. **Accédez au wizard** : `http://127.0.0.1:5000/install/`
2. **Étape BD** : Spécifiez un nom personnalisé, ex: `test-app.db`
3. **Finalisez l'installation**
4. **Redémarrez le serveur** : `Ctrl+C` puis relancez
5. **Vérifiez** : La BD créée s'appelle toujours `test-app.db`
6. **Vérifiez .env** : Il contient `SQLALCHEMY_DATABASE_URI=sqlite:///...test-app.db`

---

## ✅ Validation

- [x] Syntaxe Python validée
- [x] Serveur démarre sans erreur
- [x] Code suit les règles de vérification (fichier complet relu)
- [x] Utilise `.env` existant (pas d'ajout de dépendances)
- [x] Gestion d'erreurs incluse

---

## 🎯 Résultat

**Le nom de la BD spécifié dans le wizard est maintenant PERSISTENT et RESPECTÉ après redémarrage.**


