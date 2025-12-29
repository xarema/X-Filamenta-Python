---
Purpose: Frequently asked questions
Description: Common questions and quick answers

File: docs/troubleshooting/faq.md | Repository: X-Filamenta-Python
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

# ❓ FAQ — Questions Fréquemment Posées

---

## 🚀 Installation & Démarrage

### Q: Comment installer l'application localement ?
**A:** Voir [../guides/01_QUICKSTART.md](../guides/01_QUICKSTART.md)

Résumé rapide :
```bash
git clone <repo>
cd X-Filamenta-Python
python -m venv .venv
.venv\Scripts\activate  # ou source .venv/bin/activate
pip install -r requirements.txt
npm install
python run_prod.py
# Accédez à http://127.0.0.1:5000
```

### Q: Comment accéder à l'application une fois démarrée ?
**A:** http://127.0.0.1:5000

Le wizard d'installation s'affiche automatiquement à la première visite.

### Q: J'obtiens une erreur "Address already in use" au démarrage
**A:** Voir [common-issues.md#address-already-in-use](common-issues.md#address-already-in-use)

---

## 🔐 Authentification & Sécurité

### Q: Comment activer 2FA ?
**A:** Une fois connecté :
1. Allez dans `/account/security/2fa`
2. Cliquez "Activer 2FA"
3. Scannez le QR code avec Google Authenticator, Authy, etc.
4. Entrez un code pour confirmer
5. Sauvegardez les codes de secours

### Q: J'ai perdu mes codes de secours 2FA
**A:** Vous pouvez les régénérer depuis `/account/security/2fa`. Les anciens codes seront invalidés.

### Q: Comment réinitialiser un mot de passe oublié ?
**A:** Demandez à l'administrateur de réinitialiser votre compte.

*(Fonctionnalité "Mot de passe oublié" à implémenter)*

---

## 💾 Base de données

### Q: Quelle BD devrais-je utiliser ?
**A:** 
- **SQLite** : Dev, tests, petites installations
- **MySQL** : Production légère-moyenne
- **PostgreSQL** : Production robuste/complexe

Voir [../features/database.md](../features/database.md) pour détails.

### Q: Comment changer de BD après installation ?
**A:** 
1. Modifier `SQLALCHEMY_DATABASE_URI` dans `.env`
2. Relancer l'application
3. Optionnel : Restaurer un backup depuis l'interface d'administration

### Q: Comment faire un backup ?
**A:** 
```bash
# SQLite
cp instance/app.db instance/app.db.backup

# MySQL
mysqldump -u user -p database > backup.sql

# PostgreSQL
pg_dump -U user -d database > backup.sql
```

---

## 🌍 Langues & Internationalisation

### Q: Comment ajouter une nouvelle langue ?
**A:** Voir [../features/internationalization.md#ajouter-une-nouvelle-langue](../features/internationalization.md#ajouter-une-nouvelle-langue)

Résumé :
1. Copier `backend/src/i18n/en.json` → `backend/src/i18n/xx.json`
2. Traduire tous les textes
3. Ajouter le code dans `SUPPORTED_LANGUAGES`

### Q: Une traduction est manquante
**A:** Créez une issue avec :
- Le texte non traduit
- Où l'avez-vous trouvé
- La langue affectée

### Q: Comment changer la langue de l'interface ?
**A:** 
- Pendant l'installation : Choisir dès le départ
- Après installation : Depuis `/account/preferences`

---

## 🚀 Déploiement

### Q: Comment déployer en production ?
**A:** Voir [../deployment/README.md](../deployment/README.md) et choisir votre plateforme :
- [cPanel](../deployment/01_CPANEL.md)
- [VPS/Linux](../deployment/02_VPS_LINUX.md)
- [Docker](../deployment/03_DOCKER.md)

### Q: Quelle plateforme choisir ?
**A:**
- **Petit budget** : cPanel (facile, managed)
- **Plus de contrôle** : VPS/Linux (configuration complète)
- **Containerisé** : Docker (portable, scalable)

### Q: Comment faire un backup avant déploiement ?
**A:** Consultez le guide déploiement de votre plateforme. Généralement :
```bash
# Backup BD + fichiers
cp -r instance/ backup_$(date +%Y%m%d)/
mysqldump ... > database_$(date +%Y%m%d).sql
```

---

## 👨‍💻 Développement

### Q: Comment ajouter une nouvelle page ?
**A:** Voir [../guides/04_DEVELOPMENT.md](../guides/04_DEVELOPMENT.md)

Résumé :
1. Créer template : `frontend/templates/pages/mypage.html`
2. Créer route : `backend/src/routes/mypage.py`
3. Enregistrer blueprint dans `app.py`

### Q: Comment tester mon code ?
**A:** Voir [../contributing/testing.md](../contributing/testing.md)

```bash
pytest backend/tests/
ruff check .
mypy backend/src/
```

### Q: Comment contribuer un bug fix ?
**A:** Voir [../contributing/README.md](../contributing/README.md)

1. Fork → Branch → Code → Tests
2. Commit clair + message
3. PR avec description

---

## ❌ Erreurs courantes

### Q: "ModuleNotFoundError: No module named 'flask'"
**A:** 
```bash
pip install -r requirements.txt
```

### Q: "ConnectionRefusedError" avec la BD
**A:** Voir [common-issues.md#database-connection-refused](common-issues.md#database-connection-refused)

### Q: "Permission denied" sur les fichiers
**A:** 
```bash
chmod -R 755 instance/
chmod -R 755 frontend/static/
```

---

## 📞 Obtenir de l'aide

1. **Consulter** cette FAQ
2. **Chercher** dans [common-issues.md](common-issues.md)
3. **Lire** le guide approprié
4. **Créer** une issue sur GitHub

---

**→ N'hésitez pas à poser des questions !**

