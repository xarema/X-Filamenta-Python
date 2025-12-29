<!--
------------------------------------------------------------------------------
Purpose: Documentation du système i18n
Description: Guide pour ajouter de nouvelles langues à l'application

File: backend/src/i18n/README.md | Repository: X-Filamenta-Python
Created: 2025-12-28T20:00:00+01:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public
------------------------------------------------------------------------------
-->

# 🌍 Système de traduction (i18n)

## 📂 Structure

Chaque fichier JSON représente une langue :

- `en.json` — Anglais (langue par défaut)
- `fr.json` — Français
- `es.json` — Espagnol (à créer)
- `de.json` — Allemand (à créer)
- etc.

## 🆕 Ajouter une nouvelle langue

### 1. Créer le fichier de traduction

Copiez `en.json` et renommez-le avec le code ISO 639-1 de la langue :

```bash
cp en.json es.json  # Pour l'espagnol
cp en.json de.json  # Pour l'allemand
cp en.json it.json  # Pour l'italien
```

### 2. Traduire le contenu

Ouvrez le nouveau fichier et traduisez **toutes les valeurs** (ne modifiez jamais les clés) :

```json
{
  "wizard": {
    "title": "Asistente de instalación",  // ✅ Traduction en espagnol
    "continue": "Continuar"
  }
}
```

### 3. Tester la langue

Relancez le serveur — la langue sera **automatiquement détectée** :

```bash
# Tuer les processus
Get-Process -Name python | Where-Object {$_.Path -like "*\.venv\*"} | Stop-Process -Force

# Démarrer le serveur
.\.venv\Scripts\python.exe run_prod.py
```

## 🔍 Détection automatique

Le système détecte la langue dans cet ordre :

1. **Session** : Si l'utilisateur a choisi une langue (`/lang/fr`)
2. **Navigateur** : Via le header `Accept-Language`
3. **Défaut** : Anglais (`en`)

## 🌐 Langues supportées actuellement

| Code | Langue    | Fichier     | Statut |
|------|-----------|-------------|--------|
| `en` | English   | `en.json`   | ✅ OK  |
| `fr` | Français  | `fr.json`   | ✅ OK  |
| `es` | Español   | —           | ❌ À créer |
| `de` | Deutsch   | —           | ❌ À créer |
| `it` | Italiano  | —           | ❌ À créer |
| `pt` | Português | —           | ❌ À créer |

## 📝 Structure des clés

Utilisez la notation à points pour organiser les traductions :

```json
{
  "wizard": {
    "title": "Installation Wizard",
    "db": {
      "title": "Database",
      "test_success": "Connection successful!"
    }
  }
}
```

Dans les templates :

```html
{{ t('wizard.title') }}
{{ t('wizard.db.title') }}
{{ t('wizard.db.test_success') }}
```

## 🔧 Fonctions disponibles

### Dans les templates Jinja

```html
{{ t('wizard.title') }}
{{ t('wizard.continue') or 'Continue' }}  <!-- Avec fallback -->
```

### Dans le code Python

```python
from backend.src.utils.i18n import t, get_available_languages

# Traduction
text = t('wizard.title')

# Liste des langues disponibles
languages = get_available_languages()
# → {'en': 'English', 'fr': 'Français'}
```

## ⚠️ Règles importantes

1. **Ne jamais modifier les clés** — seulement les valeurs
2. **Toujours garder la même structure** dans tous les fichiers JSON
3. **Tester avec plusieurs navigateurs** pour vérifier la détection
4. **Utiliser UTF-8** pour les caractères spéciaux (émojis, accents, etc.)

## 🐛 Dépannage

### La langue n'est pas détectée

Vérifiez le header `Accept-Language` de votre navigateur :

```python
# Dans une route Flask
from flask import request
print(request.headers.get('Accept-Language'))
```

### Les traductions ne s'affichent pas

1. Vérifiez que le fichier JSON est valide (pas d'erreur de syntaxe)
2. Vérifiez que la clé existe dans tous les fichiers de langue
3. Relancez le serveur pour recharger les traductions

### Ajouter un fallback

```html
{{ t('wizard.new_key') or 'Default text if key missing' }}
```

## 📚 Ressources

- [Codes de langue ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- [JSON Validator](https://jsonlint.com/)
- [Unicode Characters](https://unicode-table.com/)

---

**Dernière mise à jour** : 2025-12-28  
**Mainteneur** : AleGabMar

