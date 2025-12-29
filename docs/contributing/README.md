---
Purpose: Contributing guidelines index
Description: How to contribute to X-Filamenta-Python

File: docs/contributing/README.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:05:00+01:00
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

# 🤝 Contribuer — X-Filamenta-Python

**Guide complet pour contribuer au projet.**

---

## 📋 Sections principales

| Document | Sujet |
|----------|-------|
| [code-standards.md](code-standards.md) | Standards de code |
| [testing.md](testing.md) | Testing et couverture |
| [release-process.md](release-process.md) | Processus de release |

---

## 🚀 Commencer à contribuer

### Prérequis

- Python 3.12+
- Node.js 18+
- Git
- Connaissance de Flask, HTMX, Bootstrap

### Étapes initiales

1. **Fork** le repository
2. **Clone** votre fork
3. **Installer** les dépendances :
   ```bash
   pip install -r requirements.txt
   npm install
   ```
4. **Créer une branche** :
   ```bash
   git checkout -b feature/ma-feature
   ```
5. **Développer** en suivant les standards
6. **Tester** (tests + lint)
7. **Commit** avec message clair
8. **Push** et créer une PR

---

## 📖 Avant de commencer

**Lire obligatoirement** :
1. [code-standards.md](code-standards.md) — Standards de code
2. [testing.md](testing.md) — Comment tester
3. [../.github/copilot-instructions.md](../../.github/copilot-instructions.md) — Règles IA du projet

---

## 🎯 Types de contributions

### 🐛 Signaler un bug
→ Créer une issue avec :
- Description claire du bug
- Étapes pour reproduire
- Résultat attendu vs actuel
- Environment (OS, Python version, etc.)

### 🎨 Proposer une amélioration
→ Créer une discussion ou issue avec :
- Description de l'amélioration
- Motivation
- Approche proposée

### 📝 Améliorer la documentation
→ Éditez directement le fichier markdown et créez une PR

### 💻 Coder une fonctionnalité/fix
→ Suivez le workflow ci-dessus

---

## ✅ Checklist avant PR

- [ ] Code suit les standards (voir [code-standards.md](code-standards.md))
- [ ] Tous les tests passent (`pytest`)
- [ ] Lint passe (`ruff`, `mypy`)
- [ ] Nouveau code a des tests
- [ ] Documentation mise à jour
- [ ] Commit messages clairs et en français
- [ ] Pas de secrets hardcodés

---

## 📚 Documentation supplémentaire

- **Guides** → [../guides/04_DEVELOPMENT.md](../guides/04_DEVELOPMENT.md)
- **Architecture** → [../architecture/README.md](../architecture/README.md)
- **Sécurité** → [../security/README.md](../security/README.md)

---

**Merci de contribuer à X-Filamenta-Python ! 🙏**

