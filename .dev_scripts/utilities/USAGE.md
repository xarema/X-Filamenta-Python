"""
Purpose: Guide d'utilisation des scripts de développement
Description: Documentation pour utiliser les outils de backup et nettoyage

File: .dev_scripts/utilities/USAGE.md | Repository: X-Filamenta-Python
Created: 2025-12-29T13:15:00+00:00
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
- Guide rapide pour utiliser les utilities
"""

# 📚 GUIDE UTILISATION — .dev_scripts/utilities

## Scripts Disponibles

### 1. start_server.ps1 — Démarrer le serveur

**Utilisation:**
```powershell
.\.dev_scripts\utilities\start_server.ps1
```

**Ce que ça fait:**
- Tue les processus sur port 5000
- Lance le serveur via run_prod.py
- Affiche les logs en temps réel

**Arrêter:** Ctrl+C

---

### 2. clean_server.ps1 — Nettoyer le serveur

**Utilisation:**
```powershell
.\.dev_scripts\utilities\clean_server.ps1
```

**Ce que ça fait:**
- Libère le port 5000
- Supprime BD (*.db)
- Supprime .env

**Avec nettoyage complet (caches Python):**
```powershell
.\.dev_scripts\utilities\clean_server.ps1 -Full
```

---

### 3. backup_database.ps1 — Créer un backup

**Utilisation simple (nom auto):**
```powershell
.\.dev_scripts\utilities\backup_database.ps1
```

Crée un fichier: `.dev_scripts/backups/x-filamenta_backup_YYYY-MM-DD_HH-mm-ss.tar.gz`

**Avec nom custom:**
```powershell
.\.dev_scripts\utilities\backup_database.ps1 -OutputName "backup_phase1_complete.tar.gz"
```

Crée: `.dev_scripts/backups/backup_phase1_complete.tar.gz`

---

## 🔄 Workflow Typique

### Après compléter le Wizard

```powershell
# 1. Créer le backup de la BD
.\.dev_scripts\utilities\backup_database.ps1

# Le fichier est maintenant sauvegardé dans:
# .dev_scripts/backups/x-filamenta_backup_2025-12-29_13-15-00.tar.gz
```

### Avant démarrer une nouvelle phase

```powershell
# 1. Nettoyer complètement
.\.dev_scripts\utilities\clean_server.ps1

# 2. Relancer le serveur
.\.dev_scripts\utilities\start_server.ps1

# 3. Le Wizard démarre automatiquement
# Complète-le pour la nouvelle phase
```

---

## 📝 Notes Importantes

- Les backups sont en `.tar.gz` (compressé)
- Les scripts utilisent le venv (`.\.venv\`)
- Pas de secrets stockés
- Les logs continuent pendant que le serveur tourne

---

**Prochaine étape:** Complète le Wizard, puis lance `backup_database.ps1`

