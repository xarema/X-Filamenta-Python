<!--
Purpose: Quick reference for HTML documentation generation
Description: Fast commands and usage guide for HTML docs

File: docs/HTML/QUICK_REFERENCE.md | Repository: X-Filamenta-Python
Created: 2025-12-28T21:55:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public
-->

# Documentation HTML — Référence Rapide

## ⚡ Commandes Rapides

### Générer la Documentation

```powershell
# Depuis la racine du projet
.\.venv\Scripts\python.exe scripts\utils\generate_html_docs.py
```

### Ouvrir dans le Navigateur

```powershell
# Navigateur par défaut
Start-Process 'docs\HTML\index.html'

# Microsoft Edge
Start-Process microsoft-edge:file:///D:/xarema/X-Filamenta-Python/docs/HTML/index.html
```

### Installer les Dépendances

```powershell
.\.venv\Scripts\python.exe -m pip install Markdown Pygments
```

---

## 📊 Statistiques

- **Pages totales:** 146 fichiers HTML
- **Documentation:** 56 fichiers docs/
- **Rapports d'analyse:** 87 rapports
- **Temps génération:** ~5 secondes

---

## 📂 Pages Principales

| Page | Description |
|------|-------------|
| `index.html` | Page d'accueil |
| `all-pages.html` | Index complet toutes pages |
| `analysis-reports.html` | Index rapports par date |
| `00_START_HERE.html` | Guide démarrage |
| `guides-QUICKSTART.html` | Installation rapide |
| `REFERENCE.html` | Référence technique |

---

## 🎯 Sections de Navigation

### Getting Started
- Home
- Start Here
- Quick Start
- Reference

### Features
- Overview
- Authentication (2FA)
- Installation Wizard
- Internationalization (i18n)
- Database Support

### Deployment
- Overview
- cPanel (30 min)
- VPS/Linux (1 hour)
- Docker (15 min)

### Architecture
- Overview
- Database
- WSGI & Multi-DB

### Security
- Best Practices

### Help
- Troubleshooting
- FAQ
- Common Issues
- Analysis Reports

---

## 🔧 Maintenance

### Après modification d'un .md

```powershell
# Regénérer automatiquement
.\.venv\Scripts\python.exe scripts\utils\generate_html_docs.py
```

### Vérifier les dépendances

```powershell
.\.venv\Scripts\python.exe -m pip list | Select-String -Pattern "Markdown|Pygments"
```

### Compter les fichiers générés

```powershell
Get-ChildItem -Path "docs\HTML" -Filter "*.html" | Measure-Object | Select-Object -ExpandProperty Count
```

---

## 📝 Notes

- Tous les fichiers `.md` de `docs/` et `Analysis_reports/` sont convertis
- Le CSS dans `style.css` n'est jamais écrasé
- Les liens `.md` dans le markdown ne sont pas auto-convertis en `.html`
- Utiliser UTF-8 pour tous les fichiers sources

---

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

