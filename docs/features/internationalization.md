---
Purpose: Internationalization (i18n) documentation
Description: Multi-language support and translation system

File: docs/features/internationalization.md | Repository: X-Filamenta-Python
Created: 2025-12-28T23:10:00+01:00
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

# 🌍 Internationalisation (i18n)

**Support de plusieurs langues avec fallback automatique.**

---

## 🎯 Vue d'ensemble

L'application supporte **2 langues** avec système de traduction complet :

- 🇺🇸 **Anglais (EN)** — Défaut système
- 🇫🇷 **Français (FR)** — Maintenu

### Sélection de langue

- **Installation** : Choix explicite lors du wizard
- **Utilisateur** : Peut changer dans les paramètres
- **Fallback** : EN si traduction manquante

---

## 📁 Structure des traductions

```
backend/src/i18n/
├── en.json      # Traductions anglais (complet)
├── fr.json      # Traductions français (complet)
└── README.md    # Guide des traductions
```

### Format JSON

```json
{
  "wizard": {
    "step": "Step",
    "welcome": "Welcome",
    "authentication": {
      "login": "Log in",
      "password": "Password"
    }
  }
}
```

---

## 💻 Utilisation en code

### Backend (Python/Jinja2)

```python
# Récupérer traduction
from backend.src.utils.i18n import t

message = t('wizard.welcome')  # "Bienvenue" en FR, "Welcome" en EN
```

Dans les templates Jinja2 :

```html
<h1>{{ t('wizard.welcome') }}</h1>
<p>{{ t('wizard.description') or 'Fallback text' }}</p>
```

### Frontend (HTML/JavaScript)

```html
<!-- Traduction côté serveur -->
<button>{{ t('button.submit') }}</button>

<!-- Avec HTMX -->
<div hx-post="/endpoint" 
     hx-prompt="{{ t('prompt.confirm') }}">
  Click me
</div>
```

---

## 🔄 Sélection de langue

### Endpoint

**GET /lang/{code}?start={0|1}**

- `code` : `en` ou `fr`
- `start` : Si 1, lance le wizard

### Exemple

```html
<a href="/lang/fr?start=1">Français</a>
<a href="/lang/en">English</a>
```

### Stockage

- Session : `session['lang'] = 'fr'`
- Persiste durant la session
- Utilisateur peut changer depuis les paramètres

---

## ➕ Ajouter une nouvelle langue

### Étape 1 : Créer le fichier

Copier `backend/src/i18n/en.json` → `backend/src/i18n/xx.json` (xx = code langue)

### Étape 2 : Traduire

Remplacer toutes les valeurs par les traductions

### Étape 3 : Tester

```python
# Dans un script test
from backend.src.services.i18n_service import I18nService
service = I18nService(default_lang='xx')
assert service.get('wizard.welcome', 'xx') == "..." # Traduction
```

### Étape 4 : Activer

Ajouter dans `backend/src/routes/lang.py` :

```python
SUPPORTED_LANGUAGES = ['en', 'fr', 'xx']
```

---

## 🔍 Vérification des traductions

### Scripts de test

```bash
# Vérifier que toutes les clés sont traduites
python scripts/check_i18n_completeness.py

# Lister les traductions manquantes
python scripts/list_missing_i18n.py
```

### Fallback

- Clé manquante en FR → Utilise EN
- Clé manquante dans les deux → Affiche clé brute (dev) ou texte par défaut

---

## 🏆 Best practices

✅ **Faire :**
- Utiliser des clés hiérarchisées (`wizard.step.welcome`)
- Regrouper par domaine (`auth.*, wizard.*, error.*`)
- Laisser des valeurs par défaut (`t('key') or 'Default text'`)

❌ **Éviter :**
- Traductions concaténées en code
- Interpolation de variables dans JSON (pas supporté)
- Pluriels complexes (pas de système pluriel)

---

## 📚 Ressources

- **Architecture** → [../architecture/frontend.md](../architecture/frontend.md)
- **Guides** → [../guides/README.md](../guides/README.md)

---

**→ Consultez `backend/src/i18n/en.json` pour voir toutes les traductions disponibles.**

