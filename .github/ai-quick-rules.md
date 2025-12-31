# ⚡ Règles AI Rapides (Version Condensée)

**Purpose:** Version condensée des règles critiques pour rappel rapide  
**File:** `.github/AI_QUICK_RULES.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-31  
**Last modified:** 2025-12-31

**Distributed by:** XAREMA | Coder: AleGabMar  
**App version:** 0.0.1-Alpha | File version: 1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

**Metadata:**
- Status: Stable
- Classification: Internal

---

## 🖥️ Environnement

- **OS:** Windows 11
- **Shell:** PowerShell (PAS bash)
- **Python:** `.venv\Scripts\python.exe` (JAMAIS `python`)

---

## 🚫 JAMAIS utiliser (Commandes Linux)

| ❌ Interdit | ✅ Utiliser à la place |
|-------------|------------------------|
| `grep` | `Select-String` |
| `tail -40` | `Select-Object -Last 40` |
| `head -20` | `Select-Object -First 20` |
| `cat` | `Get-Content` |
| `ls` | `Get-ChildItem` |
| `rm` | `Remove-Item` |
| `cp` | `Copy-Item` |
| `mv` | `Move-Item` |
| `python` | `.venv\Scripts\python.exe` |
| `&&` | `;` ou nouvelles lignes |

---

## 📁 Emplacement des fichiers

| Type | ❌ Interdit | ✅ Correct |
|------|-------------|-----------|
| Tests | Racine | `scripts/tests/` |
| Debug | Racine | `scripts/debug/` |
| Utils | Racine | `scripts/utils/` |
| Rapports | Racine | `Analysis_reports/` |

---

## 📝 Headers de fichiers (OBLIGATOIRE)

**Tout fichier DOIT avoir :**

```
---
Purpose: <description>
File: <chemin> | Repository: X-Filamenta-Python
Created: <date>
Distributed by:  XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0
License: AGPL-3.0-or-later
---
```

**Voir `.github/copilot-instructions.md` Section 4 pour le template complet.**

---

## 🛠️ Commandes PowerShell essentielles

### Kill serveurs (TOUJOURS avant modification)
```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### Lancer Python
```powershell
# Dev
.\.venv\Scripts\python.exe backend\src\app.py

# Prod
. \.venv\Scripts\python. exe run_prod.py
```

### Lire logs
```powershell
# Dernières 40 lignes
Get-Content "logs/app.log" | Select-Object -Last 40

# Chercher erreurs
Select-String -Pattern "ERROR" "logs/app.log"

# Suivi en temps réel
Get-Content "logs/app.log" -Tail 40 -Wait
```

### Validation
```powershell
# Lint
. \.venv\Scripts\ruff. exe check . 

# Format
.\.venv\Scripts\ruff.exe format --check .

# Type check
.\.venv\Scripts\mypy.exe backend/src

# Tests
.\.venv\Scripts\pytest.exe -v
```

---

## 🌐 Traductions (i18n)

### Règles
- ❌ **JAMAIS** de texte hardcodé
- ✅ **TOUJOURS** ajouter dans `fr.json` ET `en.json`
- ✅ Utiliser `{{ t('key.path') or 'Fallback' }}`

### Fichiers
```
backend/src/i18n/locales/
├── fr.json
└── en.json
```

### Validation
```powershell
.\.venv\Scripts\python. exe -c "import json; json.load(open('backend/src/i18n/locales/fr.json'))"
.\.venv\Scripts\python.exe -c "import json; json. load(open('backend/src/i18n/locales/en.json'))"
```

---

## 🔄 Workflow modification

### 1. Avant
```powershell
# Kill serveurs
Get-Process python.exe | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 2. Pendant
- Lire fichier EN ENTIER avant modification
- Suivre conventions (Black, type hints)
- Ajouter traductions si texte

### 3. Après
```powershell
# Kill à nouveau
Get-Process python.exe | Stop-Process -Force -ErrorAction SilentlyContinue

# Valider
.\.venv\Scripts\ruff.exe check .
.\. venv\Scripts\mypy. exe backend/src
.\.venv\Scripts\pytest.exe

# Tester dev
.\.venv\Scripts\python.exe backend\src\app.py

# Tester prod
.\.venv\Scripts\python.exe run_prod.py
```

---

## 📚 Fichiers à lire AVANT de répondre

| Situation | Fichiers à lire |
|-----------|-----------------|
| **Toute demande** | `.github/copilot-instructions.md` |
| **Commandes** | `.github/powershell.instructions.md` |
| **Modification code** | `.github/ai-modification-checklist.md` |
| **Workflow** | `.github/workflow-rules.md` |
| **Erreurs passées** | `.github/incidents-history.md` |
| **Routes cassées** | `.github/ai-broken-routes-blacklist.md` |
| **Python** | `.github/python.instructions.md` |
| **Frontend/i18n** | `.github/frontend.instructions.md` |

---

## ✅ Checklist rapide

- [ ] Commandes PowerShell (PAS Linux)
- [ ] Python via `.venv\Scripts\python.exe`
- [ ] Fichiers dans `scripts/`, PAS racine
- [ ] Headers obligatoires ajoutés
- [ ] Traductions FR + EN ajoutées
- [ ] Serveurs kill avant ET après modification
- [ ] Tests validés (ruff, mypy, pytest)
- [ ] Testé en dev ET prod

---

**Utilisation :**

```
@.github/AI_QUICK_RULES.md
Ma demande rapide...
```

**Pour plus de détails, voir `.github/AI_REMINDER.md` (version complète).**

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved. 
