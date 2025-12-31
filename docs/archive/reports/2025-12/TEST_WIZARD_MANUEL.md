# 🧙 TEST DU WIZARD D'INSTALLATION - RAPPORT

**Date:** 2025-12-27  
**Status:** ✅ **PRÊT POUR TEST**

---

## 📋 PRÉPARATION

### 1. État Actuel

✅ Flag d'installation sauvegardé (`installed.flag.backup`)  
✅ Guard d'installation activé dans `app.py`  
✅ Imports corrigés (`Response`, `Any`)  
✅ Serveur Flask démarré

### 2. Configuration

**URL serveur:** http://localhost:5000  
**Redirect auto:** Vers `/install/` si pas installé

---

## 🧪 TESTS À EFFECTUER

### Test 1: Redirection Automatique ✅

**Action:**
1. Ouvrir navigateur
2. Accéder à http://localhost:5000

**Résultat attendu:**
- Redirection automatique vers `/install/`
- Page wizard d'installation affichée

**Vérifier:**
- [ ] Redirection fonctionne
- [ ] Page wizard chargée
- [ ] Pas d'erreur 404/500

### Test 2: Page Wizard ✅

**URL:** http://localhost:5000/install/

**Vérifier:**
- [ ] Choix de langue (FR/EN) affiché
- [ ] Environnement détecté (OS, Python, Git, etc.)
- [ ] Boutons "Continue in English" / "Continuer en français"
- [ ] Interface Bootstrap 5 responsive

### Test 3: Étape 1 - Choix Langue ✅

**Action:**
1. Cliquer "Continuer en français"

**Résultat attendu:**
- Session language = `fr`
- Formulaire DB affiché

**Vérifier:**
- [ ] Langue changée
- [ ] Formulaire DB en français

### Test 4: Étape 2 - Configuration DB ✅

**Formulaire affiché:**
- Input DB URI
- Exemples (SQLite, MySQL, PostgreSQL)
- Bouton "Tester la connexion"

**Test avec SQLite:**
```
sqlite:///instance/app.db
```

**Action:**
1. Saisir URI SQLite
2. Cliquer "Tester la connexion"

**Résultat attendu:**
- Test connexion exécuté
- Message succès ✅ ou erreur ❌
- Bouton "Suivant" activé si succès

**Vérifier:**
- [ ] Formulaire fonctionne
- [ ] Test connexion OK
- [ ] Messages appropriés

### Test 5: Étape 3 - Upload Backup (Optionnel) ⚠️

**Formulaire affiché:**
- Input file (`.tar.gz`, `.tgz`)
- Bouton "Passer" (skip)

**Action:**
1. Cliquer "Passer" (pas de backup)

**Résultat attendu:**
- Passage à l'étape suivante
- Pas d'erreur

**Vérifier:**
- [ ] Skip fonctionne
- [ ] Pas obligatoire

### Test 6: Étape 4 - Création Admin ✅

**Formulaire affiché:**
- Username
- Email  
- Password

**Données test:**
```
Username: admin
Email: admin@test.com
Password: Admin123!
```

**Action:**
1. Saisir données admin
2. Cliquer "Suivant"

**Résultat attendu:**
- Validation password fort
- Erreur si password faible
- Succès si password OK

**Vérifier:**
- [ ] Validation fonctionne
- [ ] Messages d'erreur clairs
- [ ] Password fort accepté

### Test 7: Étape 5 - Résumé ✅

**Affiché:**
- DB URI configurée
- Admin username/email
- Bouton "Finaliser"

**Action:**
1. Vérifier récapitulatif
2. Cliquer "Finaliser l'installation"

**Résultat attendu:**
- Application configuration DB
- Création admin en database
- Création flag `instance/installed.flag`
- Redirect vers login ou dashboard

**Vérifier:**
- [ ] Résumé correct
- [ ] Finalisation OK
- [ ] Flag créé
- [ ] Redirect appropriée

### Test 8: Post-Installation ✅

**Action:**
1. Rafraîchir page (F5)
2. Accéder à http://localhost:5000

**Résultat attendu:**
- **PAS** de redirection wizard
- Accès normal à l'application
- Login avec compte admin créé

**Vérifier:**
- [ ] Wizard inaccessible
- [ ] Application accessible
- [ ] Admin peut se connecter

---

## 🔍 TESTS SÉCURITÉ

### Test S1: Path Traversal (Backup)

**Si backup testé:**
- Upload fichier avec `../` dans nom
- Vérifier rejet

### Test S2: Password Faible

**Tester passwords:**
- `admin` → ❌ Rejeté
- `Admin` → ❌ Rejeté (pas de symbole)
- `admin123` → ❌ Rejeté (pas maj/symbole)
- `Admin123!` → ✅ Accepté

### Test S3: Email Invalide

**Tester emails:**
- `admin` → ❌ Rejeté
- `admin@` → ❌ Rejeté
- `admin@test.com` → ✅ Accepté

---

## 🐛 TESTS ERREURS

### Test E1: DB Invalide

**Action:**
- Saisir URI invalide: `invalid://db`
- Tester connexion

**Attendu:**
- Message erreur connexion
- Bouton "Suivant" désactivé

### Test E2: Backup Trop Gros

**Si upload testé:**
- Upload fichier > 50MB
- Vérifier rejet avec message

### Test E3: Extension Invalide

**Si upload testé:**
- Upload `.zip` ou `.exe`
- Vérifier rejet

---

## 📊 CHECKLIST COMPLÈTE

### Fonctionnel
- [ ] Redirection auto vers wizard
- [ ] Choix langue FR/EN
- [ ] Détection environnement
- [ ] Formulaire DB
- [ ] Test connexion DB
- [ ] Upload backup (skip)
- [ ] Formulaire admin
- [ ] Validation password
- [ ] Résumé config
- [ ] Finalisation
- [ ] Flag créé
- [ ] Redirect post-install

### Sécurité
- [ ] Password fort requis
- [ ] Email validé
- [ ] Path traversal bloqué
- [ ] Extensions whitelist
- [ ] Taille max backup

### UX/UI
- [ ] Interface responsive
- [ ] Messages clairs
- [ ] Erreurs inline
- [ ] Bootstrap 5 styling
- [ ] Navigation fluide
- [ ] Pas de bugs visuels

---

## 🎯 RÉSULTAT ATTENDU

**À la fin du wizard:**

✅ Database configurée  
✅ Admin créé (username: admin)  
✅ Flag installation: `instance/installed.flag`  
✅ Application accessible  
✅ Wizard inaccessible  
✅ Login admin fonctionne  

---

## 🔄 RÉINITIALISER TEST

**Pour retester le wizard:**

```powershell
# 1. Arrêter serveur (Ctrl+C)

# 2. Supprimer flag
Remove-Item instance\installed.flag

# 3. Optionnel: Supprimer DB test
Remove-Item instance\test_wizard.db -ErrorAction SilentlyContinue

# 4. Relancer serveur
python run.py

# 5. Accéder http://localhost:5000
```

---

## 📝 COMMANDES RAPIDES

### Vérifier Flag
```powershell
Test-Path instance\installed.flag
```

### Voir Contenu Flag
```powershell
Get-Content instance\installed.flag
```

### Restaurer Flag Original
```powershell
Move-Item instance\installed.flag.backup instance\installed.flag -Force
```

### Vérifier DB Créée
```powershell
Test-Path instance\app.db
```

### Tester Connexion Admin
```powershell
# Après installation, login avec:
# Username: admin
# Password: Admin123!
```

---

## 🎊 SUCCÈS COMPLET

**Wizard fonctionnel si:**

1. ✅ Toutes étapes complétées sans erreur
2. ✅ Admin créé et peut se connecter
3. ✅ Flag installation créé
4. ✅ Wizard inaccessible après install
5. ✅ Application opérationnelle
6. ✅ Validation sécurité OK
7. ✅ UX fluide et claire

---

**Test wizard préparé:** 2025-12-27  
**Serveur:** ✅ Démarré sur http://localhost:5000  
**Status:** ✅ **PRÊT POUR TEST MANUEL**

**Accédez à http://localhost:5000 pour commencer le test !** 🧙✨

