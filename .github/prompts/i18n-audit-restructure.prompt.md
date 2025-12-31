Purpose: Audit complet et analyse de la stack i18n actuelle
Description: Ce prompt effectue une analyse approfondie de toutes les variables linguistiques, détecte les incohérences, les textes hardcodés, et génère un rapport détaillé avec recommandations.

File: . github/prompts/i18n-audit-restructure.prompt.md | Repository: X-Filamenta-Python
Created: 2025-12-30T09:00:00-05:00
Last modified (Git): TBD | Commit: TBD

Distributed by:  XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License:  AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA.  All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Notes:
- Exécuter AVANT l'implémentation de la nouvelle stack
- Génère un rapport dans Analysis_reports/

---

# 🔍 Audit et Restructuration i18n — Analyse Complète

## 📋 Objectifs

1. **Analyser** toute la stack i18n actuelle (Flask-Babel, fichiers JSON, templates)
2. **Identifier** toutes les variables linguistiques utilisées dans le projet
3. **Détecter** les textes hardcodés et les traductions manquantes
4. **Vérifier** la cohérence entre EN/FR
5. **Générer** un rapport d'audit complet avec recommandations

---

## 🎯 Périmètre d'Analyse

### 1️⃣ Backend Python
- ✅ Analyser tous les fichiers `backend/src/**/*.py`
- ✅ Identifier les appels à `gettext()`, `t()`, `_()`, `lazy_gettext()`
- ✅ Détecter les strings hardcodées dans les messages flash, logs, erreurs
- ✅ Vérifier l'utilisation de `current_app.config['BABEL_DEFAULT_LOCALE']`

### 2️⃣ Frontend Templates
- ✅ Analyser tous les fichiers `frontend/templates/**/*.html`
- ✅ Identifier tous les `{{ t('...') }}`, `{{ _('...') }}`
- ✅ Détecter les textes hardcodés dans HTML
- ✅ Vérifier la cohérence des variables linguistiques

### 3️⃣ Fichiers JSON de traduction
- ✅ Analyser `backend/src/i18n/*. json` (si existants)
- ✅ Vérifier `frontend/static/lang/*. json`
- ✅ Identifier les clés orphelines (présentes dans JSON mais jamais utilisées)
- ✅ Identifier les clés manquantes (utilisées dans code mais absentes de JSON)

### 4️⃣ Configuration
- ✅ Vérifier `backend/src/config.py` (LANGUAGES, BABEL_*)
- ✅ Analyser `backend/src/app.py` (initialisation Babel)
- ✅ Vérifier les routes de changement de langue

---

## 📊 Livrables Attendus

### Rapport d'Audit (Markdown)

**Fichier:** `Analysis_reports/YYYY-MM-DD_HH-mm_i18n-audit-complete.md`

**Structure du rapport:**

```markdown
# Audit i18n — X-Filamenta-Python
**Date:** YYYY-MM-DD HH:mm
**Auditeur:** GitHub Copilot
**Version projet:** 0.1.0-Beta

---

## 📈 Statistiques Globales

- **Fichiers Python analysés:** X
- **Templates HTML analysés:** X
- **Variables linguistiques détectées:** X
- **Textes hardcodés détectés:** X
- **Langues supportées:** EN, FR
- **Clés JSON manquantes:** X
- **Clés JSON orphelines:** X

---

## 🔴 Problèmes Critiques

### 1. Textes Hardcodés
| Fichier | Ligne | Texte Hardcodé | Suggestion |
|---------|-------|----------------|------------|
| `backend/src/routes/auth.py` | 123 | "Invalid credentials" | `t('auth.login.error.invalid_credentials')` |
| ...  | ... | ... | ... |

### 2. Variables Linguistiques Manquantes
| Variable Utilisée | Fichier | Langue Manquante |
|-------------------|---------|------------------|
| `wizard.title` | `install.html` | FR |
| ...  | ... | ... |

### 3. Incohérences de Structure
| Problème | Détails |
|----------|---------|
| Fichiers JSON non synchronisés | `en.json` a 245 clés, `fr.json` a 198 clés |
| ...  | ... |

---

## ⚠️ Avertissements

### 1. Variables Orphelines (présentes dans JSON mais jamais utilisées)
- `old. deprecated. key` (dans `en.json`, `fr.json`)
- ...

### 2. Structure JSON Incohérente
- `en.json` utilise `auth.login.title`
- `fr.json` utilise `auth.connexion.titre` ❌

---

## ✅ Recommandations

### Priorité 🔴 CRITIQUE
1. **Supprimer tous les textes hardcodés** dans `backend/src/routes/`
2. **Compléter les traductions FR manquantes** (47 clés)
3. **Standardiser la structure JSON** (EN = référence)

### Priorité 🟠 IMPORTANTE
1. **Migrer vers JSON hiérarchique** (facilite la maintenance)
2. **Ajouter lazy loading** (améliore performance)
3. **Implémenter gestion admin des langues**

### Priorité 🟢 AMÉLIORATION
1. Ajouter validation automatique (CI/CD)
2. Documenter conventions de nommage
3. Ajouter script de synchronisation EN/FR

---

## 📋 Inventaire Complet des Variables

### Backend (`backend/src/`)
**Fichier:  auth.py**
- `t('auth.login.title')` ✅ EN ✅ FR
- `t('auth.login.error.invalid')` ✅ EN ❌ FR
- ... 

**Fichier: install.py**
- `t('wizard.title')` ❌ EN ❌ FR (hardcodé)
- ...

### Frontend (`frontend/templates/`)
**Fichier: base.html**
- `{{ t('nav.home') }}` ✅ EN ✅ FR
- ...

---

## 🔧 Plan d'Action Recommandé

### Phase 1 : Nettoyage (1-2h)
- [ ] Supprimer variables orphelines
- [ ] Corriger textes hardcodés critiques

### Phase 2 :  Complétion (2-3h)
- [ ] Ajouter traductions FR manquantes
- [ ] Standardiser structure JSON

### Phase 3 : Migration (3-4h)
- [ ] Implémenter nouvelle stack (JSON hiérarchique)
- [ ] Ajouter lazy loading + cache
- [ ] Tests complets

### Phase 4 :  Admin UI (2-3h)
- [ ] Créer interface gestion langues (Tabulator.js)
- [ ] Ajouter upload de nouvelles langues
- [ ] Documentation

---

## 📎 Annexes

### A. Liste Complète des Fichiers Analysés
- `backend/src/app.py`
- `backend/src/routes/auth.py`
- ... 

### B. Conventions de Nommage Recommandées
domain.page.component.action.type
Exemples:
- auth.login.title
- auth. login.error.invalid_credentials
- wizard.step.requirements.title

### C. Commandes de Test
# Vérifier syntaxe JSON
.\.venv\Scripts\python.exe -m json.tool backend/src/i18n/en.json

# Comparer clés EN/FR
.\. venv\Scripts\python.exe scripts/compare_i18n. py

---

**Rapport généré le:** YYYY-MM-DD HH:mm:ss
**Durée d'analyse:** X minutes
```

---

## 🛠️ Instructions d'Exécution

### Étapes à Suivre

1. **Analyser Backend Python**
  - Lire tous les fichiers `backend/src/**/*.py`
  - Extraire appels à fonctions de traduction
  - Détecter strings hardcodées

2. **Analyser Frontend Templates**
  - Lire tous les fichiers `frontend/templates/**/*.html`
  - Extraire variables `{{ t('...') }}`
  - Détecter textes hardcodés dans HTML

3. **Analyser Fichiers JSON**
  - Charger `en.json`, `fr.json`
  - Comparer structures
  - Identifier différences

4. **Générer Rapport**
  - Créer fichier dans `Analysis_reports/`
  - Format: `YYYY-MM-DD_HH-mm_i18n-audit-complete.md`
  - Suivre structure ci-dessus

5. **Validation**
  - Vérifier syntaxe Markdown
  - Compter statistiques
  - Générer plan d'action

---

## ✅ Critères de Succès

- [ ] Tous les fichiers Python analysés
- [ ] Tous les templates HTML analysés
- [ ] Tous les JSON comparés
- [ ] Rapport complet généré
- [ ] Statistiques exactes
- [ ] Plan d'action clair et priorisé

---

## 🔗 Références

- **Projet:** X-Filamenta-Python
- **Documentation i18n:** `docs/i18n/`
- **Règles:** `.github/copilot-instructions.md`
- **Prompt suivant:** `.github/prompts/i18n-restructure-tabulator. prompt.md`

---

**Exécution:**
```
AI: Exécute ce prompt en analysant TOUT le code du projet.
Génère le rapport d'audit complet dans Analysis_reports/.
```
