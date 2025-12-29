# 🧪 Préparation Scripts de Test Wizard

**Date:** 2025-12-28T12:00:00+00:00  
**Statut:** ✅ **Scripts créés et prêts**

---

## 📋 Objectif

Créer des scripts PowerShell pour tester le wizard d'installation en mode production, comme si l'utilisateur installait l'application pour la première fois.

---

## 📁 Scripts créés

### 1. `scripts/test_wizard_prod.ps1` - Script principal de test
**Fonctionnalités:**
- ✅ Nettoyage complet de l'environnement
- ✅ Vérification environnement virtuel Python
- ✅ Vérification des dépendances
- ✅ Vérification de la structure du projet
- ✅ Instructions de test affichées
- ✅ Démarrage du serveur Flask

**Usage:**
```powershell
.\scripts\test_wizard_prod.ps1
```

---

### 2. `scripts/verify_installation.ps1` - Vérification post-installation
**Fonctionnalités:**
- ✅ Vérifie le flag d'installation
- ✅ Vérifie la base de données créée
- ✅ Liste les tables (si sqlite3 disponible)
- ✅ Vérifie l'utilisateur admin via Python
- ✅ Teste la connexion HTTP à l'application
- ✅ Vérifie les fichiers statiques

**Usage:**
```powershell
.\scripts\verify_installation.ps1
```

---

### 3. `scripts/clean_wizard.ps1` - Nettoyage rapide
**Fonctionnalités:**
- ✅ Supprime les flags d'installation
- ✅ Supprime toutes les bases de données
- ✅ Mode confirmation (ou -Force)

**Usage:**
```powershell
.\scripts\clean_wizard.ps1
# ou
.\scripts\clean_wizard.ps1 -Force
```

---

### 4. Documentation
**Fichiers créés:**
- ✅ `scripts/README_WIZARD_TEST.md` - Documentation complète
- ✅ `scripts/QUICK_START.md` - Guide rapide
- ✅ `WIZARD_TEST_COMMANDS.md` - Résumé des commandes (affiché à l'utilisateur)

---

## 🎯 Workflow de test

### Test complet
```powershell
# 1. Lancer le test
cd D:\xarema\X-Filamenta-Python
.\scripts\test_wizard_prod.ps1

# 2. Tester dans le navigateur
# → http://localhost:5000/
# → Suivre toutes les étapes

# 3. Vérifier (nouveau terminal)
.\scripts\verify_installation.ps1
```

### Recommencer le test
```powershell
# 1. Arrêter le serveur (Ctrl+C)

# 2. Nettoyer
.\scripts\clean_wizard.ps1

# 3. Relancer
.\scripts\test_wizard_prod.ps1
```

---

## ✅ Points de test couverts

### Checklist automatique (scripts)
- ✅ Environnement virtuel Python activé
- ✅ Dépendances Python installées
- ✅ Structure du projet validée
- ✅ Base de données créée
- ✅ Tables présentes
- ✅ Utilisateur admin créé
- ✅ Application accessible

### Checklist manuelle (utilisateur)
- 🔲 Fil d'Ariane cliquable
- 🔲 Checkmarks sur étapes terminées
- 🔲 Création automatique tables SQLite
- 🔲 Messages d'erreur détaillés
- 🔲 Validation compte admin
- 🔲 Finalisation sans erreur
- 🔲 Login fonctionne

---

## 🛠️ Fonctionnalités des scripts

### test_wizard_prod.ps1
**Sections:**
1. Nettoyage de l'environnement
2. Vérification environnement Python
3. Vérification dépendances
4. Vérification structure projet
5. Instructions et démarrage

**Sorties:**
- Messages colorés (Cyan, Yellow, Green, Red)
- Indicateurs ✓ / ✗
- Instructions étape par étape
- Points de vérification affichés

---

### verify_installation.ps1
**Vérifications:**
1. Flag d'installation (instance/installed.flag)
2. Base de données (instance/x-filamenta_python.db)
3. Tables via sqlite3 (si disponible)
4. Utilisateur admin via Python
5. Connexion HTTP (si serveur actif)
6. Fichiers statiques (CSS, JS)

**Résultat:**
- ✓ Installation réussie → Tout OK
- ✗ Problèmes détectés → Liste des erreurs

---

### clean_wizard.ps1
**Éléments supprimés:**
- `instance/installed.flag`
- `instance/*.db`
- `backend/instance/installed.flag`
- `backend/instance/*.db`

**Sécurité:**
- Confirmation obligatoire (sauf -Force)
- Compte les fichiers supprimés
- Messages de confirmation

---

## 📊 Améliorations vs scripts précédents

### Avant
- Scripts de test Python basiques
- Pas de workflow complet
- Pas de vérification post-installation
- Pas de nettoyage automatique

### Maintenant
✅ Scripts PowerShell professionnels  
✅ Workflow complet de A à Z  
✅ Vérifications automatiques  
✅ Nettoyage facile pour recommencer  
✅ Documentation complète  
✅ Messages colorés et clairs  

---

## 🔍 Commandes de debug incluses

### Base de données
```powershell
# Vérifier tables
sqlite3 instance\x-filamenta_python.db ".tables"

# Vérifier users
sqlite3 instance\x-filamenta_python.db "SELECT * FROM users;"
```

### Python
```powershell
# Vérifier admin
python -c "from backend.src.app import create_app; ..."

# Tester create_schema
python -c "from backend.src.services.install_service import InstallService; ..."
```

---

## 📝 Notes techniques

### Chemins configurables
Les scripts utilisent `$ProjectRoot = "D:\xarema\X-Filamenta-Python"`  
→ Modifiable si le projet est ailleurs

### Environnement virtuel
Les scripts activent automatiquement `.venv\Scripts\Activate.ps1`

### Couleurs PowerShell
- **Cyan** : Titres / Sections
- **Yellow** : Avertissements / Actions
- **Green** : Succès / OK
- **Red** : Erreurs
- **Gray** : Informations complémentaires

### Gestion d'erreurs
- `-ErrorAction SilentlyContinue` : Ignore les erreurs attendues
- Try/Catch : Pour les opérations critiques
- Vérifications avant suppression

---

## 🎯 Objectifs atteints

✅ **Scripts professionnels** - Code propre et commenté  
✅ **Workflow complet** - Du nettoyage à la vérification  
✅ **Documentation** - 4 fichiers de documentation  
✅ **Facilité d'utilisation** - Une commande pour tout  
✅ **Debugging** - Commandes de vérification incluses  

---

## 🚀 Prochaines étapes

1. **Tester les scripts** sur l'environnement de développement
2. **Valider le wizard** avec tous les scénarios
3. **Documenter les résultats** des tests
4. **Créer des screenshots** du wizard pour la documentation
5. **Préparer les scripts de déploiement** production

---

**Les scripts sont prêts pour le test en mode production ! 🎉**

---

**Fichiers créés:**
- `scripts/test_wizard_prod.ps1`
- `scripts/verify_installation.ps1`
- `scripts/clean_wizard.ps1`
- `scripts/README_WIZARD_TEST.md`
- `scripts/QUICK_START.md`
- `Analysis_reports/2025-12-28_12-00_wizard_test_scripts.md` (ce fichier)

