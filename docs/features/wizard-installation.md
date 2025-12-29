---
Purpose: Installation wizard documentation
Description: Complete guide to the multi-step installation wizard

File: docs/features/wizard-installation.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:10:00+01:00
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

# 🧙 Installation Wizard

**Assistant d'installation multi-étapes pour configurer l'application.**

---

## 🎯 Vue d'ensemble

Le wizard d'installation guide les utilisateurs à travers les étapes essentielles :

1. ✅ Sélection de langue
2. ✅ Vérification des prérequis système
3. ✅ Configuration de la base de données
4. ✅ (Optionnel) Restauration de backup
5. ✅ Création du compte administrateur
6. ✅ Résumé et finalisation

---

## 📋 Flux d'installation

### Étape 1 : Sélection de langue

**URL :** `GET /install/`

**Actions :**
- Affiche deux drapeaux : 🇺🇸 EN | 🇫🇷 FR
- Sélection de la langue de l'installation
- Sauvegarde en session

**Sortie :** Redirection vers Étape 2 (Prérequis)

---

### Étape 2 : Vérification des prérequis

**URL :** `GET /install/step?step=requirements`

**Vérifications :**
```
✓ Environnement
  - OS (Linux/Windows/macOS)
  - Architecture (x64/arm64)
  - Python version (3.12+)

✓ Outils système
  - Git
  - Pip
  - Virtual environment

⚠ Clients BD (optionnel si SQLite)
  - MySQL client
  - PostgreSQL client
```

**Statuts :**
- 🟢 Vert : Présent et OK
- 🟡 Jaune : Optionnel ou avertissement
- 🔴 Rouge : Manquant (bloquant)

**Sortie :** Bouton "Continuer" → Étape 3 (Base de données)

---

### Étape 3 : Configuration base de données

**URL :** `GET /install/step?step=db_form`

**Options (Onglets) :**

#### SQLite (Développement/léger)
```
Fichier BD : [app.db________________]
```
- Défaut : `app.db`
- Stocké dans `instance/`
- Idéal pour : Dev local, tests, petites installations

#### MySQL (Production)
```
Host :        [localhost____]
Port :        [3306___]
Nom BD :      [filamenta____________]
Utilisateur : [root__]
Mot de passe: [••••••]
```
- Driver : `pymysql`
- Min : MySQL 5.7 ou MariaDB 10.2

#### PostgreSQL (Production)
```
Host :        [localhost____]
Port :        [5432___]
Nom BD :      [filamenta____________]
Utilisateur : [postgres__]
Mot de passe: [••••••]
```
- Driver : `psycopg2`
- Min : PostgreSQL 11

**Après sélection :** Bouton "Tester la connexion" → Étape 4 (Test BD)

---

### Étape 4 : Test de connexion

**URL :** `POST /install/step?step=db_test`

**Vérifications :**
- 🟢 Serveur accessible
- 🟢 BD existe (ou créable)
- 🟢 Permissions utilisateur OK

**Résultat :**
- ✅ Succès → Continuer
- ❌ Erreur → Modifier configuration → Retester

**Sortie :** Étape 5 (Restauration backup - optionnel)

---

### Étape 5 : Restauration backup (optionnel)

**URL :** `GET /install/step?step=upload_form`

**Options :**

```
① Continuer sans backup
   → Passer à étape suivante
   → BD créée vide

② Restaurer un backup (fichier .tar.gz)
   → Upload fichier
   → Validation et extraction
   → Restauration des tables
```

**Format backup :** `.tar.gz` avec :
```
- db_backup.sql (dump complet)
- metadata.json (infos backup)
```

**Sortie :** Étape 6 (Compte administrateur)

---

### Étape 6 : Compte administrateur

**URL :** `GET /install/step?step=admin_form`

**Champs :**
```
Nom d'utilisateur : [admin_______________]
Email :            [admin@example.com____]
Mot de passe :     [••••••]
Confirmer :        [••••••]
```

**Validation :**
- Username : 3-50 chars, alphanumériques + _ -
- Email : Format valide
- Password : Min 8 chars, complexité recommandée
- Confirmation : Identique au password

**Sortie :** Bouton "Finaliser" → Étape 7 (Résumé)

---

### Étape 7 : Résumé & Finalisation

**URL :** `GET /install/step?step=summary`

**Affichage :**
```
✓ Langue :            Français
✓ Prérequis :        Vérifiés
✓ BD :               MySQL (localhost:3306/filamenta)
✓ Backup :          Restauré (ou "Aucun")
✓ Admin :           admin@example.com
```

**Actions :**
- "Corriger" : Retour aux étapes précédentes
- "Finaliser" : Lance la création/initialisation

**Sortie :** POST /install/finalize → Étape 8 (Complet)

---

### Étape 8 : Installation terminée

**URL :** `GET /install/done`

**Affichage :**
```
✅ Installation terminée avec succès !

✓ Base de données  : Créée et initialisée
✓ Tables           : Créées
✓ Admin créé       : Oui
✓ Marqueur         : Enregistré

⚠️ Action requise : Redémarrer le serveur
```

**Boutons :**
- "Se connecter" → `/auth/login`
- "Vérifier la BD" → `/install/verify-db` (debug)

---

## 🔄 Redirection automatique

**Si l'application n'est pas installée :**
- `GET /` → Redirection vers `/install/`
- Toute autre route → Redirection vers `/install/`
- Sauf : `/auth/` (pour login si besoin)

**Si l'application est installée :**
- `GET /install/` → Redirection vers `/` (ou dashboard)

---

## 💾 État de l'installation

**Marqueur :** `instance/installed.flag`

- Créé à la fin du wizard
- Contient : timestamp et version
- Utilisé pour détecter si installé

**Variables sauvegardées :**
- `.env` : `SQLALCHEMY_DATABASE_URI` (persiste après redémarrage)
- `session` : `wizard_state` (tempor aire durant wizard)

---

## 🔒 Sécurité du wizard

✅ **CSRF protection** : Tokens sur tous les POST  
✅ **Rate limiting** : Pas d'attaques par brute-force  
✅ **Validation stricte** : Inputs validés et sanitizés  
✅ **Pas de credentials loggés** : Sauf debug intentionnel  
✅ **BD sécurisée** : Pas d'expositions via erreurs  
✅ **Session sécurisée** : HttpOnly, Secure, SameSite  

---

## 🧪 Tester le wizard

### Mode développement
```bash
# Supprimer le marqueur d'installation
rm instance/installed.flag

# Redémarrer
python run_prod.py

# Accéder à http://127.0.0.1:5000
# → Redirection automatique vers /install/
```

### Mode production
```bash
# Le wizard s'affiche uniquement si not installed.flag existe
# Pour réinitialiser :
rm instance/installed.flag
systemctl restart filamenta  # ou sudo service filamenta restart
```

---

## 📚 Ressources

- **Guides de déploiement** → [../deployment/README.md](../deployment/README.md)
- **Architecture BD** → [database.md](database.md)
- **Sécurité** → [../security/README.md](../security/README.md)

---

**→ Consultez les guides de déploiement pour intégrer le wizard dans votre environnement.**

