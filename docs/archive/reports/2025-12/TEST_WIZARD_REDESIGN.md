# Guide de test du Wizard d'installation

## Prérequis

1. Assurez-vous que le serveur Flask est arrêté
2. Supprimez le fichier `.installed` à la racine du projet (s'il existe)

```powershell
Remove-Item .installed -ErrorAction SilentlyContinue
```

## Démarrage du serveur

```powershell
.\.venv\Scripts\Activate.ps1
py run.py
```

Le serveur devrait démarrer sur http://localhost:5000/

## Étapes de test

### 1. Accès initial
- Ouvrez votre navigateur sur http://localhost:5000/
- ✅ Vous devriez être redirigé vers http://localhost:5000/install/
- ✅ Vous voyez la page de choix de langue avec drapeaux 🇺🇸 et 🇫🇷

### 2. Sélection de la langue
- Cliquez sur "Continuer en français" (ou "Continue in English")
- ✅ Vous voyez la page "Bienvenue" avec le titre "Assistant d'installation"
- ✅ Le header ne contient que "X-Filamenta" (pas de navbar)
- ✅ Le footer est simplifié avec projet + version + copyright

### 3. Page Welcome
- Cliquez sur le bouton "Continuer →"
- ✅ Vous voyez la page "Prérequis système"
- ✅ Le fil d'Ariane (breadcrumb) s'affiche en haut avec les étapes
- ✅ L'étape "Requirements" est active

### 4. Page Requirements
- Vérifiez les checkmarks :
  - ✅ Environnement : ✓ (vert)
  - ✅ Git : ✓ ou ✗ selon installation
  - ✅ Python : ✓ (vert)
  - ✅ Pip : ✓ (vert)
  - ✅ Database Clients : ✓ ou ⚠ selon installations
- Cliquez sur "Continuer →"
- ✅ Vous voyez la page "Base de données"

### 5. Page Database
- ✅ Vous voyez 3 onglets : 💾 SQLite, 🐬 MySQL, 🐘 PostgreSQL
- Testez avec SQLite :
  - Laissez le nom par défaut "app.db"
  - Cliquez sur "Tester la connexion"
  - ✅ Message de succès apparaît
  - ✅ Bouton "Continuer" apparaît
- Cliquez sur "Continuer"
- ✅ Vous voyez la page "Compte administrateur"

### 6. Page Admin
- Remplissez le formulaire :
  - Username : `admin`
  - Email : `admin@example.com`
  - Password : `Admin123!` (minimum 8 caractères, 1 majuscule, 1 symbole)
- Cliquez sur "Créer l'administrateur"
- ✅ Vous voyez la page "Résumé"

### 7. Page Summary
- Vérifiez le résumé :
  - ✅ Section "Configuration de la base de données"
    - Type : 💾 SQLite
    - Fichier : instance/app.db
    - URI de connexion : sqlite:///...
  - ✅ Section "Compte administrateur"
    - Username : admin
    - Email : admin@example.com
    - Password : (masqué pour la sécurité)
- Cliquez sur "Finaliser l'installation ✓"
- ✅ Vous voyez la page "Installation terminée"

### 8. Page Done
- ✅ Icône de succès ✓ en vert
- ✅ Message de confirmation
- ✅ Bouton "Aller à la connexion →"
- Cliquez sur le bouton
- ✅ Vous êtes redirigé vers http://localhost:5000/auth/login

### 9. Test de connexion
- Sur la page de login :
  - Username : `admin`
  - Password : `Admin123!`
- Cliquez sur "Se connecter"
- ✅ Vous êtes connecté et redirigé vers le dashboard

## Tests additionnels

### Test du breadcrumb (navigation arrière)
1. Supprimez `.installed` et recommencez le wizard
2. Avancez jusqu'à la page Database
3. Cliquez sur "Requirements" dans le breadcrumb
4. ✅ Vous revenez à la page Requirements
5. ✅ Vos données précédentes sont conservées

### Test de changement de langue
1. Supprimez `.installed` et recommencez
2. Sélectionnez "Continue in English"
3. ✅ Toutes les pages sont en anglais
4. ✅ Breadcrumb : Welcome > Requirements > Database > Admin > Summary

### Test responsive (mobile)
1. Appuyez sur F12 dans votre navigateur
2. Activez le mode responsive (Ctrl+Shift+M)
3. Testez sur différentes tailles d'écran
4. ✅ Le wizard reste lisible et utilisable

## Problèmes connus résolus

- ✅ ~~Redirection infinie entre / et /install/~~ → CORRIGÉ
- ✅ ~~Bouton "Continuer" ne fonctionne pas~~ → CORRIGÉ
- ✅ ~~Drapeaux GB au lieu de US~~ → CORRIGÉ (🇺🇸)
- ✅ ~~Pas d'étape Requirements visible~~ → AJOUTÉE
- ✅ ~~Summary incomplet~~ → DÉTAILS AJOUTÉS
- ✅ ~~Navbar affichée dans wizard~~ → SUPPRIMÉE
- ✅ ~~Footer encombré~~ → SIMPLIFIÉ

## En cas de problème

### Erreur "ModuleNotFoundError: No module named 'flask_limiter'"
```powershell
pip install flask-limiter
```

### Le wizard ne démarre pas
1. Vérifiez que `.installed` est supprimé
2. Vérifiez que le serveur Flask est démarré
3. Consultez les logs dans le terminal

### La base de données ne se crée pas
1. Vérifiez que le dossier `instance/` existe
2. Vérifiez les permissions d'écriture
3. Consultez les logs pour les erreurs SQL

## Aide

Si vous rencontrez des problèmes :
1. Consultez `Analysis_reports/2025-12-28_02-30_wizard_redesign.md`
2. Vérifiez les logs du serveur Flask
3. Testez avec un autre navigateur

**Bonne installation ! 🚀**

