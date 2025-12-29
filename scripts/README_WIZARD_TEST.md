# 🧪 Scripts de Test du Wizard

Ce dossier contient les scripts pour tester le wizard d'installation en mode production.

---

## 📜 Scripts disponibles

### 1. `test_wizard_prod.ps1` - Test complet du wizard
**Usage:**
```powershell
.\scripts\test_wizard_prod.ps1
```

**Ce que fait ce script:**
- ✅ Nettoie l'environnement (supprime les DB et flags)
- ✅ Vérifie l'environnement virtuel Python
- ✅ Vérifie les dépendances Python
- ✅ Vérifie la structure du projet
- ✅ Affiche les instructions de test
- ✅ Démarre le serveur Flask

**Points de test:**
- Fil d'Ariane cliquable avec checkmarks
- Création de la base de données SQLite
- Validation du compte administrateur
- Messages d'erreur localisés
- Finalisation et login

---

### 2. `verify_installation.ps1` - Vérification post-installation
**Usage:**
```powershell
.\scripts\verify_installation.ps1
```

**Ce que fait ce script:**
- ✅ Vérifie le flag d'installation
- ✅ Vérifie la base de données créée
- ✅ Liste les tables créées (si sqlite3 disponible)
- ✅ Vérifie l'utilisateur admin
- ✅ Teste la connexion à l'application
- ✅ Vérifie les fichiers statiques

**Résultat:**
- ✓ Installation réussie → Tout est OK
- ✗ Problèmes détectés → Liste des erreurs

---

### 3. `clean_wizard.ps1` - Nettoyage rapide
**Usage:**
```powershell
.\scripts\clean_wizard.ps1

# Ou en mode force (sans confirmation):
.\scripts\clean_wizard.ps1 -Force
```

**Ce que fait ce script:**
- 🗑️ Supprime les flags d'installation
- 🗑️ Supprime toutes les bases de données
- 🗑️ Permet de recommencer le wizard

---

## 🚀 Workflow de test complet

### Test initial
```powershell
# 1. Lancer le test du wizard
.\scripts\test_wizard_prod.ps1

# 2. Suivre les étapes dans le navigateur (http://localhost:5000/)

# 3. Vérifier l'installation (dans un nouveau terminal)
.\scripts\verify_installation.ps1
```

### Recommencer le test
```powershell
# 1. Arrêter le serveur Flask (Ctrl+C)

# 2. Nettoyer
.\scripts\clean_wizard.ps1

# 3. Relancer le test
.\scripts\test_wizard_prod.ps1
```

---

## 📋 Checklist de test manuel

### Étape 0: Choix de langue
- [ ] Page s'affiche correctement
- [ ] Boutons "EN" et "FR" fonctionnent
- [ ] Redirection vers étape 1 après sélection

### Étape 1: Bienvenue
- [ ] Message de bienvenue en bonne langue
- [ ] Bouton "Continuer" fonctionne
- [ ] Breadcrumb s'affiche (sans checkmark sur Bienvenue)

### Étape 2: Prérequis
- [ ] Tous les prérequis affichent ✓ ou ✗
- [ ] Versions affichées correctement
- [ ] Breadcrumb: Bienvenue a un ✓
- [ ] Clic sur "Bienvenue" dans breadcrumb fonctionne

### Étape 3: Base de données
- [ ] SQLite sélectionné par défaut
- [ ] Nom de DB pré-rempli
- [ ] Bouton "Tester la connexion" fonctionne
- [ ] Message "Connexion réussie" s'affiche
- [ ] Schéma créé (X tables)
- [ ] Boutons "Continuer sans backup" et "Restaurer un backup" affichés

### Étape 4: Compte administrateur
- [ ] Formulaire centré et bien formaté
- [ ] Validation du mot de passe
- [ ] Messages d'erreur en français (si langue FR)
- [ ] Breadcrumb: Prérequis et Database ont des ✓

### Étape 5: Résumé
- [ ] Configuration DB affichée correctement
- [ ] Compte admin affiché (mot de passe masqué)
- [ ] Tous les breadcrumbs précédents ont des ✓
- [ ] Bouton "Finaliser l'installation"

### Finalisation
- [ ] Pas de message d'erreur générique
- [ ] Si erreur: message détaillé affiché
- [ ] Si succès: redirection vers page "Installation terminée"
- [ ] Lien vers login fonctionne

### Login
- [ ] Page login accessible
- [ ] Login avec admin/password fonctionne
- [ ] Redirection vers dashboard
- [ ] Pas de loop de redirection

---

## 🔍 Vérifications post-installation

### Base de données
```powershell
# Vérifier que le fichier existe
Test-Path instance\x-filamenta_python.db

# Lister les tables (si sqlite3 installé)
sqlite3 instance\x-filamenta_python.db ".tables"

# Compter les enregistrements users
sqlite3 instance\x-filamenta_python.db "SELECT COUNT(*) FROM users;"
```

### Flag d'installation
```powershell
# Vérifier le flag
Test-Path instance\installed.flag
Get-Content instance\installed.flag
```

### Utilisateur admin
```powershell
# Via Python
python -c "from backend.src.app import create_app; from backend.src.models.user import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(username='admin').first(); print(f'Admin: {admin.username}, Email: {admin.email}, Is Admin: {admin.is_admin}')"
```

---

## 🐛 Debugging

### Le serveur ne démarre pas
```powershell
# Vérifier l'environnement virtuel
.\.venv\Scripts\Activate.ps1
python --version
pip list | Select-String "flask"

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Les tables ne se créent pas
```powershell
# Vérifier les imports de modèles
python -c "from backend.src.models.user import User; from backend.src.models.preferences import UserPreferences; print('Models OK')"

# Tester create_schema directement
python -c "from backend.src.services.install_service import InstallService; ok, msg = InstallService.create_schema('sqlite:///test.db'); print(f'{ok}: {msg}')"
```

### Messages d'erreur génériques
- Vérifier les logs dans la console du serveur
- Vérifier que `create_admin_user` retourne des messages détaillés
- Vérifier que `finalize` affiche les erreurs avec " | " séparateur

---

## 📝 Notes

- Les scripts sont conçus pour Windows PowerShell
- Les chemins sont configurés pour `D:\xarema\X-Filamenta-Python`
- Modifiez `$ProjectRoot` dans les scripts si votre projet est ailleurs
- SQLite3 est optionnel pour les vérifications (mais recommandé)

---

**Bon test ! 🚀**

