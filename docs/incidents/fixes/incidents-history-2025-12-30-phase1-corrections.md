# Phase 1 - Corrections des bugs i18n

**Date:** 2025-12-30  
**Phase:** Phase 1 - Traductions manquantes  
**Statut:** ✅ EN COURS

---

## Contexte

Suite à l'analyse des bugs rapportés, nous procédons à la correction systématique des variables de traduction manquantes dans le système i18n.

---

## Bugs identifiés

### 1. Variables de traduction manquantes

**Fichiers affectés:**
- `backend/src/i18n/translations/fr.json`
- Templates HTML utilisant ces variables

**Variables manquantes identifiées:**

#### ✅ **CORRIGÉ** - Section `pages.features`:
- `cta_features` - Ajouté: "Découvrir les fonctionnalités"

#### ✅ **CORRIGÉ** - Section `pages.about`:
- `ctasource` - Corrigé de `cta_source` à `ctasource`: "Voir le code source sur GitHub"

#### 🔄 **EN ATTENTE** - Section `footer`:
Les variables suivantes existent dans `en.json` mais manquent dans `fr.json`:
- `footer.legal` → Besoin d'ajouter
- `pages.about.features` → Besoin de vérifier l'utilisation
- `pages.about.security` → Variable existe déjà
- `pages.about.security_desc` → Variable existe déjà
- `pages.about.performance` → Variable existe déjà
- `pages.about.responsive` → Variable existe déjà
- `pages.about.responsive_desc` → Variable existe déjà
- `pages.about.cta` → Variable existe déjà
- `pages.about.cta_features` → Variable existe déjà
- `pages.about.cta_contact` → Variable existe déjà

#### 🔄 **EN ATTENTE** - Section `pages.contact`:
- `other` → Besoin de vérifier
- `email_label` → Besoin de vérifier
- `github_label` → Besoin de vérifier
- `support_label` → Besoin de vérifier
- `support_hours` → Besoin de vérifier
- `send` → Variable existe déjà
- `placeholder_name` → Besoin de vérifier
- `placeholder_email` → Besoin de vérifier
- `placeholder_subject` → Besoin de vérifier
- `placeholder_message` → Besoin de vérifier

#### 🔄 **EN ATTENTE** - Section `admin.dashboard.stats`:
- `errors` → Besoin de vérifier
- `visits` → Besoin de vérifier

#### 🔄 **EN ATTENTE** - Section `admin.dashboard`:
- `management` → Besoin de vérifier

#### 🔄 **EN ATTENTE** - Section `admin.users.table`:
- `date_created` → Besoin de vérifier
- `name` → Besoin de vérifier

#### 🔄 **EN ATTENTE** - Section `admin.users.form`:
- `name` → Besoin de vérifier
- `email` → Variable existe déjà
- `role` → Besoin de vérifier

#### 🔄 **EN ATTENTE** - Section `admin.users.actions`:
- `save` → Besoin de vérifier
- `cancel` → Besoin de vérifier

---

## Actions correctives effectuées

### ✅ Corrections terminées

1. **Variable `pages.features.cta_features`**
   - **Fichier:** `backend/src/i18n/translations/fr.json`
   - **Action:** Ajout de la variable manquante
   - **Valeur FR:** "Découvrir les fonctionnalités"
   - **Commit:** À venir

2. **Variable `pages.about.ctasource`**
   - **Fichier:** `backend/src/i18n/translations/fr.json`
   - **Action:** Correction du nom de variable (était `cta_source`, maintenant `ctasource`)
   - **Valeur FR:** "Voir le code source sur GitHub"
   - **Commit:** À venir

---

## Actions correctives en cours

### 🔄 Vérification nécessaire

Avant d'ajouter les variables manquantes, nous devons:

1. **Vérifier l'utilisation réelle dans les templates**
   - Rechercher les occurrences de `footer.legal`, `pages.contact.other`, etc.
   - Confirmer que les variables sont effectivement utilisées

2. **Comparer `fr.json` et `en.json`**
   - Identifier toutes les différences de structure
   - Synchroniser les deux fichiers

3. **Valider avec les templates HTML**
   - S'assurer que chaque variable utilisée dans les templates existe dans les deux fichiers de traduction

---

## Prochaines étapes

1. ✅ Rechercher toutes les occurrences de variables i18n dans les templates
2. ⏳ Comparer exhaustivement `fr.json` et `en.json`
3. ⏳ Ajouter toutes les variables manquantes dans `fr.json`
4. ⏳ Valider la syntaxe JSON
5. ⏳ Tester l'application en FR et EN
6. ⏳ Documenter les changements dans le CHANGELOG

---

## Notes techniques

### Structure attendue

```json
{
  "footer": {
    "legal": "Légal",  // ← MANQUANT dans fr.json
    "about": "À propos",
    "contact": "Contact",
    "github": "GitHub",
    "copyright": "© 2025 XAREMA. Tous droits réservés.",
    "license": "Sous licence AGPL-3.0"
  }
}
```

### Commandes de validation

```bash
# Valider la syntaxe JSON
py -c "import json; json.load(open('backend/src/i18n/translations/fr.json'))"

# Comparer les clés entre EN et FR
# (script à créer)
```

---

## Références

- **Instructions principales:** `.github/copilot-instructions.md`
- **Bugs rapportés:** Conversation avec l'utilisateur (2025-12-30)
- **Fichiers concernés:**
  - `backend/src/i18n/translations/fr.json`
  - `backend/src/i18n/translations/en.json`
  - Templates HTML (à identifier)

---

**Dernière mise à jour:** 2025-12-30T12:00:00-05:00
**Auteur:** GitHub Copilot (AI Assistant)
**Statut global:** 🔄 EN COURS (Phase 1 partiellement complétée)

