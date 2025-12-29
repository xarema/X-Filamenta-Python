---
Purpose: Troubleshooting and FAQ index
Description: Common issues, solutions, and frequently asked questions

File: docs/troubleshooting/README.md | Repository: X-Filamenta-Python
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

# ❓ Dépannage — X-Filamenta-Python

**Aide au dépannage et réponses aux questions fréquentes.**

---

## 📋 Sections principales

| Document | Sujet |
|----------|-------|
| [common-issues.md](common-issues.md) | Problèmes courants et solutions |
| [faq.md](faq.md) | Questions fréquemment posées |

---

## 🔍 Trouver une solution

### 1. **Je reçois une erreur**
→ Consultez [common-issues.md](common-issues.md)

Recherchez :
- Le message d'erreur exact
- L'étape/action qui la cause
- L'environment (OS, Python version, etc.)

### 2. **J'ai une question générale**
→ Consultez [faq.md](faq.md)

Parcourez les catégories :
- Installation & Déploiement
- Utilisation & Fonctionnalités
- Développement
- Sécurité

### 3. **Mon problème n'est pas listé**
→ Actions recommandées :
1. Vérifier les logs
2. Consulter les guides appropriés
3. Créer une issue sur GitHub

---

## 🆘 Déboguer rapidement

### Vérifier les logs
```bash
# Logs de l'application
tail -f instance/logs/app.log

# Logs serveur (si applicable)
sudo journalctl -u filamenta -f
```

### Vérifier la configuration
```bash
# Environnement
cat .env

# Configuration BD
# Vérifier que la BD est accessible et contient les tables
```

### Relancer l'application
```bash
# Arrêter
Ctrl+C

# Nettoyer les caches
rm -rf .mypy_cache .ruff_cache .pytest_cache __pycache__

# Relancer
python run_prod.py
```

---

## 💡 Conseils utiles

### Pour les développeurs
- Activez le mode DEBUG local (`FLASK_ENV=development`)
- Utilisez `print()` ou logging pour déboguer
- Relancez après chaque modification
- Vérifiez les dépendances (`pip install -r requirements.txt`)

### Pour les admins/ops
- Vérifiez les logs du serveur (nginx, apache, etc.)
- Vérifiez la BD (tables, données, permissions)
- Vérifiez les permissions de fichiers
- Vérifiez l'espace disque

### Pour les utilisateurs
- Vider le cache du navigateur
- Essayer un autre navigateur
- Vérifier la connexion internet
- Contacter l'administrateur

---

## 📞 Obtenir de l'aide

### 1. Avant de chercher de l'aide
- [ ] Consulter [common-issues.md](common-issues.md)
- [ ] Consulter [faq.md](faq.md)
- [ ] Consulter les logs
- [ ] Essayer de redémarrer

### 2. Chercher de l'aide
- Créer une issue sur GitHub (avec contexte complet)
- Consulter les issues existantes (peut-être que quelqu'un a le même problème)

### 3. Signaler un bug
Inclure :
- Description claire
- Étapes pour reproduire
- Résultat attendu vs actuel
- Environment (OS, Python, etc.)
- Logs pertinents

---

## 📚 Documentation supplémentaire

- **Guides** → [../guides/README.md](../guides/README.md)
- **Déploiement** → [../deployment/README.md](../deployment/README.md)
- **Sécurité** → [../security/README.md](../security/README.md)

---

**→ Consultez les guides détaillés pour solutions spécifiques.**

