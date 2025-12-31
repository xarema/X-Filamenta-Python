# 🚨 RAPPEL POUR L'IA

**Purpose:** Rappel obligatoire des règles critiques pour l'IA  
**File:** `.github/AI_REMINDER.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-31  
**Last modified:** 2025-12-31

**Distributed by:** XAREMA | Coder:  AleGabMar  
**App version:** 0.0.1-Alpha | File version:  1.0.0

**License:** AGPL-3.0-or-later  
**SPDX-License-Identifier:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

**Metadata:**
- Status:  Stable
- Classification: Internal

---

## ⚠️ AVANT DE RÉPONDRE À TOUTE DEMANDE

**Tu DOIS lire ces fichiers AVANT de répondre :**

1. ✅ `.github/copilot-instructions.md` (règles principales)
2. ✅ `.github/powershell.instructions.md` (commandes PowerShell - Windows 11)
3. ✅ `.github/workflow-rules.md` (workflow de modification)
4. ✅ `.github/incidents-history.md` (erreurs passées à ne PAS répéter)
5. ✅ `.github/ai-modification-checklist.md` (checklist AVANT toute modification)

---

## 🚫 RÈGLES CRITIQUES (Vérifier AVANT chaque réponse)

### Environnement
- **OS:** Windows 11
- **Shell:** PowerShell (PAS bash/Linux)
- **Python:** `.venv\Scripts\python.exe` (JAMAIS `python` directement)

### Commandes (ABSOLUMENT INTERDIT)
- ❌ **JAMAIS** utiliser :  `grep`, `tail`, `head`, `cat`, `ls`, `rm`, `cp`, `mv`, `touch`
- ❌ **JAMAIS** utiliser : `&&` (chaînage Linux)
- ❌ **JAMAIS** utiliser : `python` directement

### Commandes (TOUJOURS utiliser)
- ✅ `Select-String` au lieu de `grep`
- ✅ `Select-Object -Last 40` au lieu de `tail -40`
- ✅ `Get-Content` au lieu de `cat`
- ✅ `Get-ChildItem` au lieu de `ls`
- ✅ `Remove-Item` au lieu de `rm`
- ✅ `.venv\Scripts\python.exe` au lieu de `python`

### Fichiers (Emplacement)
- ❌ **JAMAIS** créer de fichiers à la racine du projet
- ✅ Scripts de test → `scripts/tests/`
- ✅ Scripts de debug → `scripts/debug/`
- ✅ Utilitaires → `scripts/utils/`
- ✅ Rapports d'analyse → `Analysis_reports/`

### Fichiers (Headers obligatoires)
**AVANT de créer un fichier, vérifier `.github/copilot-instructions. md` Section 4**

Tout fichier DOIT avoir :
```
---
Purpose: <description courte>
Description: <description détaillée>

File:  <chemin/fichier> | Repository: X-Filamenta-Python
Created: <YYYY-MM-DDTHH:mm:ss±HH:MM>
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved. 

Metadata:
- Status: Draft | Stable | Deprecated
- Classification: Public | Internal | Confidential

Notes:
- <notes importantes>
---
```

---

## 🔧 SI TU CRÉES UN FICHIER

1. ✅ Vérifier l'emplacement (PAS la racine)
2. ✅ Ajouter le header complet (Section 4 de `.github/copilot-instructions.md`)
3. ✅ Utiliser la syntaxe de commentaire appropriée :
  - Python : `""".. ."""` (docstring)
  - PowerShell : `<# ...  #>`
  - Markdown : En-tête visible
  - JSON/YAML : Impossible (documenter ailleurs)

---

## 🛠️ SI TU PROPOSES DES COMMANDES

1. ✅ Lire `.github/powershell.instructions.md` EN ENTIER
2. ✅ Vérifier Section 3 (équivalents Linux → PowerShell)
3. ✅ Vérifier Section 5 (exécution Python avec venv)
4. ✅ Vérifier Section 6 (commandes kill serveur)
5. ✅ **JAMAIS** de commandes Linux

**Exemples CORRECTS :**

```powershell
# Lire un fichier
Get-Content "app.log"

# Dernières 40 lignes
Get-Content "app.log" | Select-Object -Last 40

# Chercher dans un fichier
Select-String -Pattern "ERROR" "app.log"

# Lancer Python
. \. venv\Scripts\python.exe backend\src\app.py

# Kill serveurs
Get-Process python. exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

---

## 🔄 SI TU MODIFIES DU CODE

1. ✅ Lire `.github/ai-modification-checklist.md` **EN ENTIER**
2. ✅ Suivre **TOUTES** les phases (PHASE 1 à PHASE 5)
3. ✅ Vérifier `.github/incidents-history.md` (erreurs passées)
4. ✅ Vérifier `.github/ai-broken-routes-blacklist.md` (routes cassées)
5. ✅ **JAMAIS** modifier sans avoir lu le fichier EN ENTIER d'abord

**Checklist minimum :**
- [ ] Fichier lu EN ENTIER avant modification
- [ ] Syntaxe validée après modification
- [ ] Vérification des virgules, guillemets, parenthèses
- [ ] Tests de validation (pytest, ruff, mypy)
- [ ] Rapport d'incident créé si erreur

---

## 🌐 SI TU TOUCHES À L'I18N (Traductions)

1. ✅ Lire `.github/frontend. instructions.md` Section 6 (i18n)
2. ✅ **JAMAIS** de texte hardcodé dans les templates
3. ✅ **TOUJOURS** ajouter les traductions dans **FR ET EN simultanément**
4. ✅ Utiliser `{{ t('key. path') or 'Fallback' }}`
5. ✅ Valider la syntaxe JSON après modification

**Fichiers à modifier :**
- `backend/src/i18n/locales/fr.json`
- `backend/src/i18n/locales/en.json`

**Validation :**
```powershell
. \.venv\Scripts\python. exe -c "import json; json.load(open('backend/src/i18n/locales/fr.json'))"
.\.venv\Scripts\python. exe -c "import json; json.load(open('backend/src/i18n/locales/en.json'))"
```

---

## 📋 WORKFLOW OBLIGATOIRE (Toute modification)

### Avant modification
1. ✅ Kill tous les serveurs
   ```powershell
   Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
   ```
2. ✅ Lire `.github/workflow-rules.md`
3. ✅ Vérifier `.github/incidents-history.md`

### Pendant modification
1. ✅ Suivre les conventions (Black, type hints, headers)
2. ✅ Ajouter traductions si nouveau texte
3. ✅ Tester en mode dev d'abord

### Après modification
1. ✅ Kill serveurs à nouveau
2. ✅ Valider syntaxe (ruff, mypy, pytest)
3. ✅ Tester en dev (`backend\src\app.py`)
4. ✅ Tester en prod (`run_prod.py`)
5. ✅ **SEULEMENT APRÈS** → Demander à l'utilisateur de tester

---

## 🚨 INCIDENTS À NE JAMAIS RÉPÉTER

**Voir `.github/incidents-history.md` pour la liste complète.**

**Erreurs fréquentes :**
- ❌ Utiliser des commandes Linux
- ❌ Créer des fichiers à la racine
- ❌ Oublier les headers de fichiers
- ❌ Modifier du code sans le lire EN ENTIER d'abord
- ❌ Proposer des commandes sans vérifier PowerShell rules
- ❌ Hardcoder du texte au lieu d'utiliser i18n

---

## ✅ CHECKLIST FINALE AVANT DE RÉPONDRE

- [ ] J'ai lu `.github/copilot-instructions.md`
- [ ] J'ai lu le fichier spécifique au domaine (powershell/python/frontend)
- [ ] J'ai vérifié `.github/incidents-history.md`
- [ ] Si commandes → J'ai vérifié `.github/powershell.instructions.md`
- [ ] Si fichiers → J'ai vérifié Section 4 (headers obligatoires)
- [ ] Si modification → J'ai lu `.github/ai-modification-checklist.md`
- [ ] Si i18n → J'ai vérifié `.github/frontend.instructions.md` Section 6

---

**CE FICHIER DOIT ÊTRE RÉFÉRENCÉ DANS CHAQUE PROMPT IMPORTANT :**

```
@.github/AI_REMINDER.md
Ma demande ici... 
```

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved. 
