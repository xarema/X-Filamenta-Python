"""
Purpose: Préférences utilisateur et directives personnalisées pour le projet
Description: Configuration spécifique de l'utilisateur pour le développement

File: docs/user_preferences.md | Repository: X-Filamenta-Python
Created: 2025-12-29T14:30:00+00:00
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
- Document de référence pour les préférences utilisateur
- À lire AVANT chaque phase
- Mis à jour le 2025-12-29 suite à conversation Parathèse
"""

# 👤 PRÉFÉRENCES UTILISATEUR — X-Filamenta-Python

**Mis à jour:** 2025-12-29  
**Source:** Conversation Parathèse + Documentation Projet

---

## 🎯 Préférences Générales

### Environnement de Travail
- **OS:** Windows 11 (PowerShell v5.1)
- **Shell préféré:** PowerShell natif (NO bash/Unix aliases)
- **Python:** Via venv (`.\.venv\Scripts\python.exe`)
- **IDE:** JetBrains IntelliJ (VS Code possible)

### Conventions de Commandes
- ✅ **PowerShell Windows natif UNIQUEMENT**
- ❌ **JAMAIS** `python` directement (utiliser `.\.venv\Scripts\python.exe`)
- ❌ **JAMAIS** `mkdir` (utiliser `New-Item -ItemType Directory`)
- ❌ **JAMAIS** `ls` (utiliser `Get-ChildItem`)
- ✅ Format PowerShell spécifique Windows
- ❌ **PAS d'émojis/caractères spéciaux** dans les commandes

### Format Sortie
- ✅ Logs détaillés en PowerShell
- ✅ Structure claire avec sections
- ✅ Pas de formatage excessif
- ❌ Pas d'emojis dans les commandes (OK dans descriptions)

---

## 📋 Préférences Code

### Langage Python
- **Version cible:** Python 3.12
- **Linter:** Ruff (cf. `.github/copilot-instructions.md`)
- **Type checking:** Mypy
- **Format:** Black (88 caractères ligne)
- **Tests:** pytest avec > 85% coverage obligatoire

### Langage Web (Frontend)
- **Framework:** Flask + HTMX + Bootstrap 5
- **HTML/CSS/JS:** Prettier (88 caractères ligne)
- **No framework JS** (préférer HTMX pour interactions)
- **i18n:** Système customisé (FR/EN) OR Migration vers Flask-Babel

### Base de Données
- **Type:** SQLite (dev), PostgreSQL (prod futur)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic

---

## 🔒 Préférences Sécurité

### Configuration
- **Secrets:** JAMAIS en dur, utiliser `.env` avec env vars
- **Headers HTTP:** Tous les 7 headers implémentés (cf. middleware.py)
- **CSRF:** Protection implémentée et testée
- **Authentication:** 2FA TOTP obligatoire pour admin
- **Rate limiting:** Multi-niveaux (login, API, email)

### Licence & Attribution
- **Licence:** AGPL-3.0-or-later
- **Header requis:** Tous fichiers avec copyright © 2025 XAREMA
- **Footer:** Attribution visible (author, license, repo link)

---

## 🏗️ Préférences Architecture

### Structure Repo
- **Monorepo:** Flask backend + Frontend HTMX dans même repo
- **Dossiers clés:** 
  - `backend/src/` — Code Python
  - `frontend/` — Templates HTML
  - `docs/` — Documentation
  - `Analysis_reports/` — Rapports d'audit (tracké)
  - `.dev_scripts/` — Scripts dev (tracké)
- **Fichiers ignorés:** Logs, caches, .env (cf. `.gitignore`)

### Workflow
1. **Lire règles AVANT toute modif** (copilot-instructions.md)
2. **Petit commits atomiques** (pas big-bang refactors)
3. **Tests OBLIGATOIRES** pour tout changement
4. **Documentation** toujours à jour
5. **CHANGELOG** mis à jour à chaque feature

---

## 📊 Préférences CI/CD & DevOps

### Serveur de Développement
- **URL:** http://localhost:5000
- **Port:** 5000 (NE PAS CHANGER)
- **Lancement:** `.\.dev_scripts\utilities\start_server.ps1`
- **Nettoyage:** `.\.dev_scripts\utilities\clean_server.ps1`
- **Backup:** `.\.dev_scripts\utilities\backup_database.ps1`

### Phases de Développement
- **Durée:** 2 semaines/phase en moyenne
- **Versioning:** Semantic Versioning (v0.x.x-Beta, v1.0.0, etc.)
- **Testing:** Minimum 85% coverage OBLIGATOIRE
- **Release:** v0.1.0-Beta, v0.2.0-Beta, ... v1.0.0 (stable)

---

## 🎯 Préférences Menu Admin

### Sections du Menu (Priorité d'Implémentation)
1. **Tableau de bord** ← Core dashboard
2. **Paramètres Utilisateurs** ← Gestion users (Phase 1)
3. **Paramètres Couriel** ← Configuration SMTP (Phase 1)
4. **Paramètres Système** ← Config générale (Phase 1)
5. **Paramètres Sécurité** ← Rate limit, tokens, policies (Phase 1)
6. **Paramètres Logs** ← Niveau, rotation, retention (Phase 5)
7. **Paramètres Sauvegarde** ← Backup/restore (Phase après v1.0)
8. **Paramètres Mise à Jour** ← Versions, migrations (Phase après v1.0)

### UI/UX
- Bootstrap 5 pour tous les panneaux
- Formulaires simples et clairs
- Validation côté client + serveur
- Messages de succès/erreur visibles

---

## 📚 Préférences Documentation

### Types de Docs
- ✅ **CHANGELOG.md** — Keep a Changelog format
- ✅ **README.md** — Setup, usage, contribution
- ✅ **Code comments** — Why, not what
- ✅ **Docstrings** — Pour fonctions/classes publiques
- ✅ **Analysis_reports/** — Audits, investigations (tracké)
- ✅ **File headers** — AGPL + copyright sur tous fichiers

### Organisation
- `docs/` — Documentation utilisateur/dev
- `Analysis_reports/` — Rapports techniques
- `.dev_scripts/` — Outils de dev (avec README)
- Inline comments pour logique complexe

---

## 🚀 Préférences Workflow Phase

### Avant Démarrer Phase
- [ ] Lire `.github/copilot-instructions.md`
- [ ] Lire `docs/REFERENCE_PHASES.md`
- [ ] Lire `docs/user_preferences.md` (ce fichier)
- [ ] Lire `globalPromptFiles://copilot-powershell.md`
- [ ] Exécuter `.\.dev_scripts\utilities\clean_server.ps1`
- [ ] Exécuter `.\.dev_scripts\utilities\start_server.ps1`

### Pendant Phase
- Suivre checklist jour-par-jour dans REFERENCE_PHASES.md
- Commit atomiques avec messages clairs
- Tests OBLIGATOIRES (coverage > 85%)
- Mettre à jour CHANGELOG en parallèle

### Après Phase (Checkpoint)
- [ ] Tous tests passent
- [ ] Coverage > 85%
- [ ] CHANGELOG complet
- [ ] Version bump + tag Git
- [ ] Backup créé

---

## ✅ Préférences Communication

### Avant Commencer Travail
- **Demander confirmation** si ambiguïté
- **Proposer 2 options** avec trade-offs
- **Ne pas assumer** sans documentation

### Pendant Travail
- **Progression visible** (checklist updates)
- **Logs clairs** (pas d'output vide)
- **Pas de "tu peux tester"** → Tests INCLUS dans code

### Après Travail
- **Résumé complet** des changements
- **Checkpoint validé** avant dire "terminé"
- **100% fonctionnel** (pas 99%)

---

## 🎓 Regles Non-Négociables

### JAMAIS :
1. ❌ Modifier route existante sans tester
2. ❌ Ajouter code sans tests
3. ❌ Ignorer les règles .github/copilot-instructions.md
4. ❌ Laisser un fichier sans header AGPL
5. ❌ Utiliser `python` directement (venv OBLIGATOIRE)
6. ❌ Dire "essaie et teste" → Tests INCLUS
7. ❌ Oublier de backup après phase
8. ❌ Modifier code testé qui fonctionnait (régression)

### TOUJOURS :
1. ✅ Relire ENTIRE file après modification
2. ✅ Vérifier syntaxe (JSON, Python, HTML)
3. ✅ Chercher code existant avant refactor
4. ✅ Tester localement AVANT livrer
5. ✅ Documenter les changements
6. ✅ Garder historique Git (no force push)
7. ✅ Respecter conventions du projet
8. ✅ Nettoyer serveur entre phases

---

## 📞 Préférences Support

### Pour Erreurs
- Donner stack trace complet
- Lister tous les logs pertinents
- Montrer le fichier exact + ligne
- Proposer 2 solutions possibles

### Pour Questions
- Proposer réponse par défaut si possible
- Lister trade-offs clairement
- Ne pas demander "quoi faire ?" → Suggérer

---

## 🔄 Historique Mises à Jour

| Date | Changement |
|------|-----------|
| 2025-12-29 | Création initiale suite à Parathèse |

---

**Prochaine mise à jour:** Après chaque phase majeure

**À lire AVANT toute modification:** `.github/copilot-instructions.md` + `docs/REFERENCE_PHASES.md` + CE FICHIER

