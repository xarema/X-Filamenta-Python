"""
Purpose: Guide pour l'utilisation du dossier .dev_scripts
Description: Documentation des scripts de développement et testing

File: .dev_scripts/README.md | Repository: X-Filamenta-Python
Created: 2025-12-29T12:45:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.1.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
Notes:
- Ce dossier est TRACKÉ dans Git (contrairement à la plupart des artefacts)
- À utiliser pour les scripts partagés entre développeurs
"""

# 📂 .dev_scripts — Scripts de Développement

**Statut:** Dossier tracké dans Git  
**Utilisation:** Scripts partagés, outils testing, utilities debug

---

## 📋 Contenu

Ce dossier contient les scripts partagés pour le développement et testing.

### Règles Importantes

✅ **À INCLURE dans ce dossier:**
- Scripts de test partagés (pytest, fixtures)
- Scripts de debug réutilisables
- Outils de nettoyage/migration
- Scripts d'installation dépendances

❌ **NE PAS inclure dans ce dossier:**
- Logs de serveur (*.log)
- Fichiers BD temporaires (*.db)
- Output texte volumineux
- Fichiers temporaires (*.tmp, *.temp)

### Structure Recommandée

```
.dev_scripts/
├── README.md (ce fichier)
├── test_scripts/          # Scripts de test spécifiques
│   ├── test_email.py
│   ├── test_wizard.py
│   └── test_api.py
├── utilities/             # Outils réutilisables
│   ├── clean_db.py
│   ├── reset_server.py
│   └── generate_fixtures.py
└── setup/                 # Scripts de setup
    ├── install_deps.ps1
    └── setup_env.ps1
```

---

## 🚀 Utilisation

### Exemple 1 : Ajouter un script de test

```bash
# Créer le script
echo "#!/usr/bin/env python3" > .dev_scripts/test_scripts/test_email.py

# Ajouter du contenu
# ...code...

# Commit
git add .dev_scripts/test_scripts/test_email.py
git commit -m "test: add email workflow tests"
```

### Exemple 2 : Ignorer les logs dans ce dossier

Les fichiers `.log`, `.tmp` dans `.dev_scripts/` sont ignorés par `.gitignore`.

```bash
# Ce fichier sera IGNORÉ (logique)
echo "test log" > .dev_scripts/test_scripts/server.log

# Ce fichier sera TRACKÉ (script)
echo "print('test')" > .dev_scripts/test_scripts/test.py
```

---

## 📝 Convention de Nommage

Suivre le pattern du projet :

- Scripts Python: `snake_case.py`
- Scripts PowerShell: `CamelCase.ps1`
- Tests: `test_*.py`
- Utilities: `*_utility.py` ou `*_helper.py`

---

## ✍️ Ne PAS oublier

Avant de committer un script:

1. ✅ Vérifier qu'il n'y a pas de secrets (env vars, tokens)
2. ✅ Tester localement
3. ✅ Ajouter docstring en en-tête
4. ✅ Documenter utilisation si complexe
5. ✅ Inclure dans ce README si important

---

**Dernière mise à jour:** 2025-12-29

