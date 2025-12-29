# ⚠️ LIRE OBLIGATOIREMENT AVANT TOUTE MODIFICATION

**Date création :** 2025-12-28  
**Objectif :** Fichier centralisé de TOUTES les règles à consulter avant de modifier le projet

---

## 🚨 PROCESSUS OBLIGATOIRE AVANT TOUTE MODIFICATION

### 1. ARRÊTER TOUS LES SERVEURS
```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### 2. LIRE CES FICHIERS (dans l'ordre)
1. ✅ `.github/copilot-instructions.md` — Règles générales du projet
2. ✅ `.github/USER_PREFERENCES.md` — Préférences utilisateur
3. ✅ `.github/ROUTE_CHANGE_RULES.md` — Règles routes (si modification routes)
4. ✅ `.github/SERVER_KILL_COMMANDS.md` — Commandes serveur
5. ✅ Ce fichier — Synthèse complète

### 3. DEMANDER AVANT D'AGIR
- ❌ **NE PAS** créer de nouveaux boutons/UI sans demander
- ❌ **NE PAS** modifier le design sans demander
- ❌ **NE PAS** changer les routes sans consulter ROUTE_CHANGE_RULES.md
- ✅ **TOUJOURS** proposer 2 options avant une modification structurelle

---

## 📋 RÈGLES CRITIQUES (Non-Négociables)

### Traductions
- ✅ **AUCUN texte en dur dans les templates**
- ✅ **TOUT doit être dans `backend/src/i18n/{fr,en}.json`**
- ✅ Utiliser `{{ t('wizard.key') or 'Fallback' }}`

### Design & UI
- ✅ Fil d'Ariane wizard : **TOUJOURS 2 lignes** (3 étapes ligne 1, 2 étapes ligne 2)
- ✅ Boutons : DANS les partials, PAS dans `_wizard_content.html`
- ✅ Bootstrap 5 classes en priorité, CSS custom uniquement si nécessaire
- ✅ Design responsive (mobile-first)

### Routes
- ❌ **NE JAMAIS réutiliser une route défaillante** (voir ROUTE_CHANGE_RULES.md)
- ✅ Toujours tester après modification
- ✅ Kill tous les serveurs avant modification
- ✅ Vérifier logs après redémarrage

### Code Python
- ✅ Type hints obligatoires
- ✅ Black formatting (88 chars)
- ✅ Pas de `python` direct, toujours `.venv`
- ✅ PowerShell : AUCUN émoji dans output

### Fichiers
- ✅ Headers obligatoires (voir copilot-instructions.md section 4)
- ✅ Version 0.0.1-Alpha par défaut
- ✅ License: AGPL-3.0-or-later
- ✅ Debug/test dans `scripts/`, PAS à la racine

---

## 🔄 WORKFLOW MODIFICATION

### Avant de commencer
1. Kill serveurs (`Get-Process python.exe | Stop-Process -Force`)
2. Lire fichiers règles pertinents
3. **DEMANDER** confirmation du plan de modification
4. Attendre validation utilisateur

### Pendant modification
1. Respecter conventions projet (Black, type hints, headers)
2. Ajouter traductions si nouveau texte
3. Tester en mode dev d'abord
4. Vérifier erreurs avec `get_errors`

### Après modification
1. Kill serveurs
2. Tester en mode dev
3. Vérifier logs
4. Si OK → Tester en mode prod
5. Vérifier logs prod
6. **SEULEMENT ALORS** dire à l'utilisateur d'essayer

---

## 📝 HISTORIQUE ERREURS À NE PLUS RÉPÉTER

### Erreurs de design
- ❌ Boutons dupliqués (ligne 167-170 `_wizard_content.html`) — **SUPPRIMÉS**
- ❌ Fil d'Ariane sur 1 ligne avec wrap — **CORRIGÉ** (2 lignes fixes)
- ❌ Texte en dur sans traduction — **À ÉVITER TOUJOURS**

### Erreurs de routes
- (Voir `.github/ROUTE_CHANGE_RULES.md` pour historique complet)

### Erreurs de processus
- ❌ Modifier sans kill serveurs → Conflits
- ❌ Tester avant de finaliser → Utilisateur voit erreurs
- ❌ Utiliser `python` direct → Ne fonctionne pas Windows

---

## 🧪 TESTS OBLIGATOIRES

### Avant de dire "c'est prêt"
1. ✅ `ruff check .` — Pas d'erreurs lint
2. ✅ `ruff format --check .` — Format OK
3. ✅ `mypy backend/src` — Type checking OK
4. ✅ Serveur dev → Tester wizard complet
5. ✅ Kill serveurs
6. ✅ Serveur prod → Tester wizard complet
7. ✅ Vérifier screenshots utilisateur
8. ✅ **TOUS** les liens/boutons fonctionnent
9. ✅ **TOUTES** les traductions affichées

### Si un seul test échoue
- ❌ **NE PAS** dire "essayez"
- ✅ **CORRIGER** puis **RE-TESTER** jusqu'à 100%

---

## 🎯 COMMANDES ESSENTIELLES

### Kill serveurs
```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### Lancer dev
```powershell
.\.venv\Scripts\python.exe backend\src\app.py
```

### Lancer prod
```powershell
.\.venv\Scripts\python.exe run_prod.py
```

### Lint & Format
```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\mypy.exe backend/src
```

---

## 📚 FICHIERS RÉFÉRENCE COMPLETS

| Fichier | Contenu |
|---------|---------|
| `.github/copilot-instructions.md` | Règles projet complètes (headers, versioning, CHANGELOG, etc.) |
| `.github/USER_PREFERENCES.md` | Préférences utilisateur (env, tests, workflow) |
| `.github/ROUTE_CHANGE_RULES.md` | Règles routes + historique incidents |
| `.github/SERVER_KILL_COMMANDS.md` | Toutes commandes kill serveurs |
| `backend/src/i18n/fr.json` | Traductions françaises |
| `backend/src/i18n/en.json` | Traductions anglaises |

---

## ✅ CHECKLIST FINALE AVANT COMMIT

- [ ] Tous serveurs arrêtés
- [ ] Règles projet relues
- [ ] Modifications testées en dev
- [ ] Modifications testées en prod
- [ ] Aucune erreur lint/format/type
- [ ] Toutes traductions ajoutées
- [ ] Headers fichiers à jour
- [ ] CHANGELOG.md mis à jour
- [ ] Screenshots utilisateur vérifiés
- [ ] Utilisateur confirme que tout fonctionne

---

**Dernière mise à jour :** 2025-12-28

**Note :** Si vous voyez ce fichier, c'est que vous DEVEZ le lire AVANT toute modification du projet. Aucune exception.

