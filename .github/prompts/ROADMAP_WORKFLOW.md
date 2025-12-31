# Complete Workflow Guide - All Prompts

**Purpose:** Guide complet de tous les prompts disponibles pour le projet  
**File:** . github/prompts/ROADMAP_WORKFLOW.md | Repository: X-Filamenta-Python

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA.  All rights reserved.

---

## 📚 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Prompts Roadmap](#prompts-roadmap)
- [Prompts Développement](#prompts-développement)
- [Prompts Test & Debug](#prompts-test--debug)
- [Prompts Production](#prompts-production)
- [Workflows Complets](#workflows-complets)
- [Calendrier](#calendrier)
- [Troubleshooting](#troubleshooting)

---

## Vue d'ensemble

Le projet utilise **8 prompts spécialisés** couvrant tout le cycle de vie du développement.

### **Catégories**

| Catégorie | Prompts | Objectif |
|-----------|---------|----------|
| **Roadmap** | 4 prompts | Gestion roadmap projet |
| **Développement** | 1 prompt | Compléter features incomplètes |
| **Test & Debug** | 2 prompts | Tests + débogage |
| **Production** | 1 prompt | Préparation déploiement |

**Total : 8 prompts**

---

## Prompts Roadmap

### 1. 🔍 `analyze-code-vs-roadmap`

**Objectif :** Analyser code source réel vs roadmap pour identifier écarts

**Ce qu'il fait :**
- ✅ Scanne tout le code (models, routes, services, templates, tests)
- ✅ Compare roadmap vs implémentation réelle
- ✅ Identifie features marquées ✅ mais incomplètes
- ✅ Découvre features non planifiées (dans code, pas roadmap)
- ✅ Calcule métriques précises (vraie completion %, test coverage)
- ✅ Génère rapport détaillé avec preuves (fichiers, LOC)

**Inputs :**
- Scope:  all-phases | specific-phase | specific-feature
- Analysis Depth: shallow | deep | comprehensive
- Compare with Previous: yes | no | latest

**Outputs :**
- `Analysis_reports/YYYY-MM-DD_code-vs-roadmap.md`

**Fréquence :** Bi-hebdomadaire  
**Durée :** 15-30 min  
**Fichier :** `.github/prompts/analyze-code-vs-roadmap. prompt. md`

---

### 2. 🔄 `sync-roadmap-from-analysis`

**Objectif :** Appliquer automatiquement corrections du rapport code-vs-roadmap

**Ce qu'il fait :**
- ✅ Lit rapport `code-vs-roadmap.md`
- ✅ Parse gaps, unplanned features, recommendations
- ✅ Génère plan de correction (JSON)
- ✅ Applique corrections automatiquement :
  - Downgrade features incomplètes (100% → 70%)
  - Marque features découvertes (0% → 100%)
  - Ajoute features non planifiées
  - Met à jour métriques (completion %)
  - Synchronise README. md + CHANGELOG.md
- ✅ Génère rapport de sync

**Inputs :**
- Report: latest | specific-date
- Scope: all | completion-only | unplanned-only
- Mode: auto-apply | review-first | dry-run
- Backup: yes | no | auto

**Outputs :**
- `.roadmap/` files updated
- `Analysis_reports/YYYY-MM-DD_roadmap-sync.md`

**Fréquence :** Après `analyze-code-vs-roadmap`  
**Durée :** 10-15 min  
**Fichier :** `.github/prompts/sync-roadmap-from-analysis.prompt.md`

---

### 3. ✏️ `update-roadmap`

**Objectif :** Mettre à jour roadmap manuellement (sans analyse code)

**Ce qu'il fait :**
- ✅ Analyse documentation (docs/, CHANGELOG, README)
- ✅ Compare roadmap planifié vs état déclaré
- ✅ Met à jour progression des phases
- ✅ Identifie features complétées/bloquées
- ✅ Génère rapport de statut
- ✅ Synchronise README et CHANGELOG

**Inputs :**
- Scope: all | specific-phase | specific-feature
- Update Type: progress-review | phase-completion | full-audit
- Date: YYYY-MM-DD
- Context: (description changements)

**Outputs :**
- `.roadmap/` files updated
- `Analysis_reports/YYYY-MM-DD_roadmap-status.md`

**Fréquence :** Hebdomadaire  
**Durée :** 10-20 min  
**Fichier :** `.github/prompts/update-roadmap.prompt.md`

---

### 4. 🧹 `cleanup-roadmap`

**Objectif :** Nettoyer et organiser dossier `.roadmap/`

**Ce qu'il fait :**
- ✅ Archive phases complétées (100%)
- ✅ Supprime fichiers obsolètes (. bak, ~, .tmp)
- ✅ Supprime anciens rapports (>90 jours)
- ✅ Réorganise structure (archive/completed, archive/deprecated)
- ✅ Valide liens Markdown
- ✅ Génère INDEX.md pour navigation

**Inputs :**
- Scope: all | completed-phases | old-reports | structure-only
- Archive Completed: yes | no
- Remove Old Reports: 30 | 60 | 90 | never
- Reorganize Structure: yes | no
- Validate Links: yes | no

**Outputs :**
- `.roadmap/` reorganized
- `.roadmap/INDEX.md` (NEW)
- `Analysis_reports/YYYY-MM-DD_roadmap-cleanup.md`

**Fréquence :** Mensuel  
**Durée :** 15-30 min  
**Fichier :** `.github/prompts/cleanup-roadmap.prompt.md`

---

## Prompts Développement

### 5. 📋 `generate-completion-plan`

**Objectif :** Générer plan actionnable pour compléter features incomplètes

**Ce qu'il fait :**
- ✅ Lit rapport `code-vs-roadmap.md` (section "Incorrectly Completed")
- ✅ Analyse code existant (what exists, what's missing)
- ✅ Définit acceptance criteria (Definition of Done)
- ✅ Génère plan détaillé par feature :
  - Tasks numérotées avec priorité
  - Steps détaillés pour chaque task
  - Code templates (tests, docs, routes)
  - Time estimates
  - Dependencies
- ✅ Fournit ordre recommandé (sprint plan)

**Inputs :**
- Report: latest | specific-date
- Scope: all-incomplete | specific-feature | critical-only
- Detail Level: high-level | detailed | comprehensive
- Include Estimates: yes | no

**Outputs :**
- `Analysis_reports/YYYY-MM-DD_completion-plan-[feature].md`
- `Analysis_reports/YYYY-MM-DD_completion-summary.md` (si multiple)

**Fréquence :** Après `analyze-code-vs-roadmap` (si gaps)  
**Durée :** 20-40 min  
**Fichier :** `.github/prompts/generate-completion-plan.prompt. md`

---

## Prompts Test & Debug

### 6. 🧪 `generate-test-suite`

**Objectif :** Générer suite de tests complète (unit + integration + edge cases)

**Ce qu'il fait :**
- ✅ Analyse code cible (feature/module/service)
- ✅ Identifie toutes méthodes publiques
- ✅ Génère tests :
  - Unit tests (isolés, mocked)
  - Integration tests (routes, DB)
  - Edge case tests (erreurs, limites)
  - Performance tests (si applicable)
- ✅ Génère fixtures pytest
- ✅ Génère config pytest (`conftest.py`)
- ✅ Génère docs tests (`tests/README.md`)
- ✅ Génère GitHub Action CI/CD

**Inputs :**
- Target: feature | module | route | service | model | function
- Name: (nom de la cible)
- Test Type: unit | integration | e2e | all
- Coverage Goal: 80% | 90% | 100%
- Edge Cases: yes | no | comprehensive
- Framework: pytest | unittest

**Outputs :**
- `backend/tests/test_[name].py`
- `backend/tests/conftest.py`
- `backend/tests/README.md`
- `.github/workflows/tests.yml`

**Fréquence :** Nouvelle feature OU feature sans tests  
**Durée :** 30-60 min  
**Fichier :** `.github/prompts/generate-test-suite.prompt.md`

---

### 7. 🐛 `debug-issue`

**Objectif :** Déboguer et corriger bug/erreur avec analyse root cause

**Ce qu'il fait :**
- ✅ Collecte informations (error trace, logs, recent changes)
- ✅ Reproduit issue (minimal reproduction)
- ✅ Analyse root cause (5 Whys)
- ✅ Identifie stratégie de fix
- ✅ Implémente fix
- ✅ Ajoute regression test
- ✅ Met à jour callers (si API change)
- ✅ Génère debug report
- ✅ Documente prévention

**Inputs :**
- Issue:  (description erreur)
- Type: bug | error | test-failure | performance | security
- Severity: critical | high | medium | low
- Location: route | service | model | template | test | deployment
- Reproduce: (steps to reproduce)
- Expected vs Actual: (comportement)
- Environment: dev | prod | test | docker | cpanel

**Outputs :**
- Code fixed
- `backend/tests/test_[issue]. py` (regression test)
- `Analysis_reports/YYYY-MM-DD_debug-issue-NNN.md`

**Fréquence :** Quand bug détecté  
**Durée :** 15-90 min  
**Fichier :** `.github/prompts/debug-issue.prompt.md`

---

## Prompts Production

### 8. 🚀 `pre-production-cleanup`

**Objectif :** Nettoyage complet et validation avant déploiement production

**Ce qu'il fait :**
- ✅ **Backup complet** (code + DB)
- ✅ **Nettoie fichiers** (__pycache__, *.pyc, logs, IDE files)
- ✅ **Venv propre** (supprime + recrée, prod deps SEULEMENT)
- ✅ **Valide configs** (. env production, config.py sécurisé)
- ✅ **Audit sécurité** (bandit, safety, pip-audit, secrets scan)
- ✅ **Valide code** (ruff, black, mypy, complexity)
- ✅ **Exécute tests** (100% pass requis, coverage ≥80%)
- ✅ **Valide DB** (migrations à jour, backup existe)
- ✅ **Optimise assets** (CSS/JS minifiés)
- ✅ **Génère checklist** (PRE_PRODUCTION_CHECKLIST.md)
- ✅ **Rapport GO/NO-GO** (statut déploiement)

**Inputs :**
- Target: cpanel | vps | docker | aws | azure
- Type: initial | update | hotfix | rollback
- Mode: validate-only | cleanup-and-validate | aggressive-cleanup
- Backup: yes | no | auto
- Skip:  none | tests | linting | docs | security

**Outputs :**
- Cleaned codebase (debug files removed)
- Fresh venv (prod deps only)
- `PRE_PRODUCTION_CHECKLIST.md`
- `Analysis_reports/YYYY-MM-DD_pre-prod-cleanup.md`

**Fréquence :** Avant CHAQUE déploiement production  
**Durée :** 30-60 min  
**Fichier :** `.github/prompts/pre-production-cleanup. prompt.md`

---

## Workflows Complets

### 🗓️ Workflow 1 : Mise à jour hebdomadaire SIMPLE

**Quand :** Tous les lundis matin  
**Durée :** 10-15 min

```powershell
@copilot update-roadmap

Scope: all
Update Type: progress-review
Date: [today]
Context: Weekly progress update
```

**Résultat :**
- ✅ Roadmap à jour
- ✅ Rapport généré

---

### 🔍 Workflow 2 :  Audit bi-hebdomadaire APPROFONDI

**Quand :** Tous les 2 lundis (semaines paires)  
**Durée :** 35-45 min

```powershell
# 1. Analyser code vs roadmap
@copilot analyze-code-vs-roadmap

Scope: all-phases
Analysis Depth: deep
Compare with Previous: yes

# 2. Appliquer corrections automatiquement
@copilot sync-roadmap-from-analysis

Report: latest
Mode: review-first
Backup: yes
```

**Résultat :**
- ✅ Gaps identifiés
- ✅ Roadmap corrigé automatiquement
- ✅ Métriques précises

---

### 🎯 Workflow 3 :  Fin de phase

**Quand :** Phase supposée complète  
**Durée :** 50-70 min

```powershell
# 1. Vérifier phase vraiment complète
@copilot analyze-code-vs-roadmap

Scope: specific-phase
Phase: 2
Analysis Depth: comprehensive

# 2. Si gaps → générer plan complétion
@copilot generate-completion-plan

Report: latest
Scope: all-incomplete
Detail Level: comprehensive
Include Estimates:  yes

# 3. (Developer complète features selon plan)

# 4. Re-vérifier
@copilot analyze-code-vs-roadmap

Scope: specific-phase
Phase: 2

# 5. Si 100% → sync + cleanup
@copilot sync-roadmap-from-analysis

Mode: auto-apply

@copilot cleanup-roadmap

Scope: completed-phases
Archive Completed: yes
```

**Résultat :**
- ✅ Phase vérifiée 100% complète
- ✅ Archivée proprement

---

### 📊 Workflow 4 : Audit mensuel COMPLET

**Quand :** Premier lundi du mois  
**Durée :** 80-110 min

```powershell
# 1. Analyse comprehensive
@copilot analyze-code-vs-roadmap

Scope: all-phases
Analysis Depth: comprehensive
Compare with Previous: latest

# 2. Sync roadmap
@copilot sync-roadmap-from-analysis

Report: latest
Mode: auto-apply
Backup: yes

# 3. Cleanup complet
@copilot cleanup-roadmap

Scope: all
Archive Completed: yes
Remove Old Reports: 90
Reorganize Structure: yes
Validate Links: yes
```

**Résultat :**
- ✅ Audit complet
- ✅ Roadmap à jour
- ✅ Dossier propre

---

### 🚀 Workflow 5 :  Développement nouvelle feature

**Quand :** Nouvelle feature à développer  
**Durée :** Variable (heures à jours)

```powershell
# 1. Développer feature (code)
# ...  (coding)

# 2. Générer tests
@copilot generate-test-suite

Target: feature
Name: [Feature Name]
Test Type: all
Coverage Goal: 90%
Edge Cases: comprehensive

# 3. Exécuter tests
pytest backend/tests/test_[feature].py -v

# 4. Si test échoue → debug
@copilot debug-issue

Issue: [description]
Type: test-failure
Severity: medium

# 5. Feature complète → analyser
@copilot analyze-code-vs-roadmap

Scope: specific-feature
Feature: [Feature Name]

# 6. Sync roadmap
@copilot sync-roadmap-from-analysis
```

**Résultat :**
- ✅ Feature développée
- ✅ Tests complets
- ✅ Bugs corrigés
- ✅ Roadmap à jour

---

### 🐛 Workflow 6 :  Bug en production

**Quand :** Bug critique détecté  
**Durée :** 30-120 min

```powershell
# 1. Debug issue
@copilot debug-issue

Issue: [error description]
Type: error
Severity: critical
Location:  [route/service/etc]
Reproduce: [steps]
Expected vs Actual: [behavior]
Environment: prod

# 2. Générer regression test
@copilot generate-test-suite

Target: [buggy component]
Test Type: integration
Coverage Goal: 90%
Edge Cases: yes

# 3. Valider fix
pytest backend/tests/ -v

# 4. Cleanup avant hotfix deploy
@copilot pre-production-cleanup

Target: [prod environment]
Type: hotfix
Mode: cleanup-and-validate
Backup:  yes

# 5. Deploy hotfix
# ... (deployment)
```

**Résultat :**
- ✅ Bug corrigé
- ✅ Tests ajoutés
- ✅ Déployé en sécurité

---

### 🎯 Workflow 7 : Déploiement production

**Quand :** Avant CHAQUE déploiement  
**Durée :** 40-70 min

```powershell
# 1. Cleanup + validation complète
@copilot pre-production-cleanup

Target: [cpanel/vps/docker/aws]
Type: [initial/update]
Mode: cleanup-and-validate
Backup:  yes
Skip: none

# 2. Lire rapport (GO/NO-GO)
code Analysis_reports/[latest]_pre-prod-cleanup.md

# 3. Si GO → Deploy
# ... (deployment selon environment)

# 4. Post-deployment
# - Monitor logs
# - Verify features
# - Rollback if issues
```

**Résultat :**
- ✅ Production clean
- ✅ Tous checks PASS
- ✅ Déploiement sécurisé

---

## Calendrier

### 📅 Calendrier recommandé

| Fréquence | Action | Prompt(s) | Durée |
|-----------|--------|-----------|-------|
| **Hebdomadaire** (Lundi) | Mise à jour roadmap | `update-roadmap` | 10 min |
| **Bi-hebdomadaire** (Lundi pair) | Audit code vs roadmap | `analyze` + `sync` | 35 min |
| **Mensuel** (1er lundi) | Audit + Cleanup complet | `analyze` + `sync` + `cleanup` | 80 min |
| **Fin de phase** | Vérification + Archive | `analyze` + `sync` + `cleanup` | 60 min |
| **Nouvelle feature** | Develop + Test | `generate-test-suite` + `debug` | Variable |
| **Bug détecté** | Debug + Fix | `debug-issue` | 30-120 min |
| **Avant deploy** | Cleanup production | `pre-production-cleanup` | 40 min |

---

### 🗓️ Exemple calendrier Janvier-Mars 2025

**Janvier :**
- ✅ 06/01 (Lun): Mise à jour hebdo (`update-roadmap`)
- 🔍 13/01 (Lun pair): **Audit bi-hebdo** (`analyze` + `sync`)
- ✅ 15/01 (Mer): **Phase 1 complétée** → `analyze` + `sync` + `cleanup`
- ✅ 20/01 (Lun): Mise à jour hebdo (`update-roadmap`)
- 🔍 27/01 (Lun pair): **Audit bi-hebdo** (`analyze` + `sync`)

**Février :**
- 📊 03/02 (Lun): **Audit mensuel** → `analyze` (comprehensive) + `sync` + `cleanup`
- ✅ 10/02 (Lun): Mise à jour hebdo (`update-roadmap`)
- 🔍 17/02 (Lun pair): **Audit bi-hebdo** (`analyze` + `sync`)
- ✅ 24/02 (Lun): Mise à jour hebdo (`update-roadmap`)

**Mars :**
- 🚀 03/03 (Lun): **Audit mensuel + Q1 Review** → `analyze` + `sync` + `cleanup`
- ✅ 10/03 (Lun): Mise à jour hebdo (`update-roadmap`)
- 🔍 17/03 (Lun pair): **Audit bi-hebdo** (`analyze` + `sync`)
- ✅ 24/03 (Lun): Mise à jour hebdo (`update-roadmap`)
- 🚀 28/03 (Ven): **Production deploy** → `pre-production-cleanup`
- 📊 31/03 (Lun): **Revue Q1** → `analyze` (comprehensive)

---

## Troubleshooting

### ❓ "Quel prompt utiliser ?"

| Situation | Prompt |
|-----------|--------|
| Lundi matin routine | `update-roadmap` |
| Doute sur exactitude roadmap | `analyze-code-vs-roadmap` |
| Phase supposée complète | `analyze-code-vs-roadmap` (specific-phase) |
| Features incomplètes trouvées | `generate-completion-plan` |
| Nouvelle feature à coder | (code) → `generate-test-suite` |
| Test échoue | `debug-issue` |
| Bug en prod | `debug-issue` |
| Avant déploiement | `pre-production-cleanup` |
| Fin de mois | `analyze` + `sync` + `cleanup` |

---

### ❓ "Ordre d'exécution roadmap ?"

**Optimal :**
```
analyze-code-vs-roadmap → sync-roadmap-from-analysis → cleanup-roadmap
```

**Rapide (hebdo) :**
```
update-roadmap
```

**Complet (mensuel) :**
```
analyze (comprehensive) → sync → cleanup
```

---

### ❓ "Différence analyze vs update ?"

| Aspect | analyze-code-vs-roadmap | update-roadmap |
|--------|-------------------------|----------------|
| **Source** | Code source (fichiers) | Documentation |
| **Méthode** | Scan ligne par ligne | Analyse statut |
| **Trouve** | Écarts code vs roadmap | Progression features |
| **Durée** | 15-30 min | 10-20 min |
| **Fréquence** | Bi-hebdo/Mensuel | Hebdo |

**Analogie :**
- `analyze` = Audit comptable (vérifier comptes)
- `update` = Mise à jour livre (noter transactions)

---

### ❓ "Feature incomplète, que faire ?"

```powershell
# 1. Générer plan complétion
@copilot generate-completion-plan

Report: latest
Scope: specific-feature
Feature: [name]
Detail Level: comprehensive

# 2. Suivre plan (coding)

# 3. Vérifier complétion
@copilot analyze-code-vs-roadmap

Scope: specific-feature
```

---

### ❓ "Tests manquants, comment générer ?"

```powershell
@copilot generate-test-suite

Target: feature
Name: [Feature Name]
Test Type: all
Coverage Goal: 90%
Edge Cases: comprehensive
```

---

### ❓ "Bug trouvé, comment déboguer ?"

```powershell
@copilot debug-issue

Issue: [description complète]
Type: bug | error | test-failure
Severity: critical | high | medium | low
Location: [où ça se passe]
Reproduce:  [steps]
```

---

### ❓ "Avant déploiement, checklist ?"

```powershell
@copilot pre-production-cleanup

Target: [environment]
Mode: cleanup-and-validate
Backup: yes

# Puis lire rapport GO/NO-GO
code Analysis_reports/[latest]_pre-prod-cleanup.md
```

---

## Checklist Rapide

### ✅ Avant analyze-code-vs-roadmap
- [ ] Code récent commité
- [ ] Tests passent
- [ ] Choisir bon depth (shallow/deep/comprehensive)

### ✅ Avant sync-roadmap-from-analysis
- [ ] `analyze-code-vs-roadmap` exécuté
- [ ] Rapport lu et compris
- [ ] Mode choisi (auto-apply/review-first)

### ✅ Avant update-roadmap
- [ ] Changements récents documentés
- [ ] CHANGELOG. md à jour

### ✅ Avant cleanup-roadmap
- [ ] `update-roadmap` ou `sync` exécuté
- [ ] Roadmap à jour
- [ ] Backup si changements majeurs

### ✅ Avant generate-completion-plan
- [ ] Rapport `code-vs-roadmap` existe
- [ ] Gaps identifiés clairement

### ✅ Avant generate-test-suite
- [ ] Code cible implémenté
- [ ] Fichier cible existe

### ✅ Avant debug-issue
- [ ] Issue reproductible
- [ ] Logs collectés
- [ ] Recent changes documentés

### ✅ Avant pre-production-cleanup
- [ ] Tests passent 100%
- [ ] Backup planifié
- [ ] Rollback plan prêt

---

## Matrice Décision Rapide

| Si vous voulez... | Utilisez... | Durée |
|-------------------|-------------|-------|
| Vérifier si roadmap exact | `analyze-code-vs-roadmap` | 20 min |
| Corriger roadmap automatiquement | `sync-roadmap-from-analysis` | 15 min |
| Mettre à jour roadmap manuellement | `update-roadmap` | 10 min |
| Nettoyer dossier roadmap | `cleanup-roadmap` | 20 min |
| Plan pour finir feature | `generate-completion-plan` | 30 min |
| Créer tests pour feature | `generate-test-suite` | 45 min |
| Corriger bug | `debug-issue` | 60 min |
| Préparer production | `pre-production-cleanup` | 50 min |

---

## Références

### Prompts
- [analyze-code-vs-roadmap. prompt. md](. github/prompts/analyze-code-vs-roadmap.prompt. md)
- [sync-roadmap-from-analysis. prompt.md](.github/prompts/sync-roadmap-from-analysis.prompt.md)
- [update-roadmap.prompt.md](.github/prompts/update-roadmap.prompt.md)
- [cleanup-roadmap.prompt.md](.github/prompts/cleanup-roadmap.prompt. md)
- [generate-completion-plan.prompt.md](.github/prompts/generate-completion-plan.prompt.md)
- [generate-test-suite. prompt.md](.github/prompts/generate-test-suite. prompt.md)
- [debug-issue.prompt.md](.github/prompts/debug-issue.prompt.md)
- [pre-production-cleanup.prompt. md](.github/prompts/pre-production-cleanup.prompt. md)

### Documentation
- [. roadmap/README.md](.roadmap/README.md)
- [.roadmap/INDEX.md](.roadmap/INDEX.md)
- [CHANGELOG.md](CHANGELOG.md)

### Règles
- [.github/copilot-instructions.md](.github/copilot-instructions.md)
- [.github/workflow-rules.md](.github/workflow-rules.md)

---

## Support

Pour questions ou problèmes :
- 📖 Lire ce guide en entier
- 🐛 Vérifier [Troubleshooting](#troubleshooting)
- 📧 Email : [filamenta@xarema.com](mailto:filamenta@xarema.com)
- 🔗 Issues : [GitHub Issues](https://github.com/xarema/X-Filamenta-Python/issues)

---

**Bon workflow !    🚀**

**8 prompts ultra-complets pour gérer tout le cycle de vie du projet !   **

**Copyright © 2025 XAREMA.    All rights reserved.**
