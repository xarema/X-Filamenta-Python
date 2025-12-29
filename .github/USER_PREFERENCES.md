# Préférences Utilisateur — Référence AI

**Date création :** 2025-12-28  
**Usage :** Stocker les préférences et décisions utilisateur pour référence future AI

---

## 🎯 Environnement & Exécution

### Python / Commandes
- ✅ **Toujours utiliser `.venv`** pour exécution Python
- ❌ **Ne JAMAIS utiliser `python` direct** dans PowerShell (problème Windows)
- ✅ **Commandes via `.venv\Scripts\activate.ps1` puis python/pytest/etc.**
- ✅ **PowerShell : PAS d'émoji dans les commandes/sorties** (formatage clean uniquement)

---

## 📁 Organisation Fichiers

### Fichiers Debug / Test
- ✅ **NE PAS stocker à la racine**
- ✅ **Utiliser dossier dédié :** `scripts/debug/` ou `scripts/tests/`
- ✅ Garder racine propre (seulement fichiers essentiels)

### Structure attendue
```
scripts/
├── debug/          ← Scripts de débogage
├── tests/          ← Scripts de test manuels
└── utils/          ← Utilitaires divers
```

---

## 🧪 Workflow Tests Wizard

### Q1 : Nettoyage DB avant test
- ✅ **OUI** — Toujours nettoyer DB pour simuler première installation
- Action : Supprimer `instance/*.db` avant tests

### Q2 : Mode de lancement
- **Phase 1 (Debug) :** Mode développement
  - `debug=True`
  - Logs verbeux
  - Erreurs détaillées
  - Meilleur pour identifier problèmes

- **Phase 2 (Validation Finale) :** Mode production
  - Waitress WSGI
  - Configuration production
  - Test réaliste avant déploiement

### Q3 : Script de test dédié
- ✅ **OUI** — Créer script réutilisable
- Localisation : `scripts/tests/test_wizard_clean.py` ou similaire
- Fonctionnalités :
  - Nettoyage DB automatique
  - Lancement serveur
  - Instructions claires
  - Options debug/prod

---

## 🔧 Règles Générales

### Avant toute modification
- ✅ **Toujours demander confirmation** avant changements
- ✅ Lire `.github/copilot-instructions.md` systématiquement
- ✅ Respecter conventions du projet

### Debugging
- ✅ Utiliser meilleur agent disponible (Plan pour analyse complexe)
- ✅ Backend ET Frontend debugging si nécessaire
- ✅ Logs détaillés + traçabilité

---

## 📚 Documentation HTML

### Génération
- ✅ **Script disponible:** `scripts/utils/generate_html_docs.py`
- ✅ **Commande:**
  ```powershell
  .\.venv\Scripts\python.exe scripts\utils\generate_html_docs.py
  ```
- ✅ **Output:** `docs/HTML/` (146 pages)
- ✅ **Inclut:** Toute la doc + 87 rapports d'analyse

### Visualisation
```powershell
# Ouvrir dans navigateur par défaut
Start-Process 'docs\HTML\index.html'

# Ouvrir dans Edge
Start-Process microsoft-edge:file:///D:/xarema/X-Filamenta-Python/docs/HTML/index.html
```

### Dépendances
```powershell
.\.venv\Scripts\python.exe -m pip install Markdown Pygments
```

---

## 📋 Historique Décisions

### 2025-12-28 — Test Wizard Installation
- Q1 : Nettoyer DB avant test → **OUI**
- Q2 : Mode lancement → **Debug d'abord, puis Prod**
- Q3 : Script test dédié → **OUI**
- Organisation : Fichiers test dans `scripts/tests/`

---

**Ce fichier sera mis à jour avec nouvelles préférences au fil du temps.**

License: AGPL-3.0-or-later  
Dernière mise à jour: 2025-12-28

