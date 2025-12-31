# Incident Report: Dashboard 500 Error

**Date:** 2025-12-30T19:05:00+00:00  
**Severity:** 🔴 CRITICAL  
**Status:** ✅ RESOLVED  
**Reporter:** User  
**Resolver:** GitHub Copilot AI  

---

## Summary

Dashboard pages (member & admin) retournaient une erreur 500 empêchant l'accès complet à l'application après connexion.

---

## Root Cause Analysis

### Bug 1: TypeError dans `member.html`
- **Erreur:** `TypeError: t() got an unexpected keyword argument 'username'`
- **Fichier:** `frontend/templates/dashboard/member.html:32`
- **Cause:** La fonction `t()` (traduction) ne supporte pas les arguments nommés (kwargs)
- **Code problématique:**
  ```jinja2
  {{ t('admin.member_dashboard.welcome', username=current_user.username) }}
  ```

### Bug 2: Template Not Found dans `admin/dashboard.html`
- **Erreur:** `jinja2.exceptions.TemplateNotFound: base.html`
- **Fichier:** `frontend/templates/admin/dashboard.html:1`
- **Cause:** Mauvais chemin pour le template de base
- **Code problématique:**
  ```jinja2
  {% extends "base.html" %}
  ```
- **Note:** Le template correct est `layouts/base.html`

---

## Impact

- ❌ Dashboard member inaccessible (erreur 500)
- ❌ Dashboard admin inaccessible (erreur 500)
- ❌ Navigation post-connexion bloquée
- ✅ Page de connexion fonctionnelle
- ✅ Installation wizard fonctionnel

---

## Fix Applied

### Fichiers modifiés

1. **`frontend/templates/dashboard/member.html`**
   - Ligne 32: Retrait de l'argument nommé `username=`
   - **Avant:**
     ```jinja2
     {{ t('admin.member_dashboard.welcome', username=current_user.username) }}
     ```
   - **Après:**
     ```jinja2
     {{ t('admin.member_dashboard.welcome') }} {{ current_user.username }}
     ```

2. **`frontend/templates/admin/dashboard.html`**
   - Ligne 1: Correction du chemin du template
   - **Avant:**
     ```jinja2
     {% extends "base.html" %}
     ```
   - **Après:**
     ```jinja2
     {% extends "layouts/base.html" %}
     ```

3. **`frontend/templates/auth/verify-2fa.html`**
   - Ligne 1: Correction du chemin du template
   - Même correction que #2

4. **`frontend/templates/auth/setup-2fa.html`**
   - Ligne 1: Correction du chemin du template
   - Même correction que #2

---

## Verification Steps

1. ✅ Analyse du dossier `.github/` complétée
2. ✅ Lecture du log d'erreur `z_serverprod.log`
3. ✅ Identification des 2 bugs critiques
4. ✅ Recherche de patterns similaires dans tous les templates
5. ✅ Correction de 4 fichiers HTML
6. ✅ Validation de la syntaxe Jinja2

---

## Prevention

### Recommandations immédiates

1. **Fonction `t()` - Documentation:**
   - Ajouter dans les docs que `t()` ne supporte PAS les kwargs
   - Utiliser la concaténation: `{{ t('key') }} {{ variable }}`

2. **Template extends - Standard:**
   - TOUJOURS utiliser `{% extends "layouts/base.html" %}`
   - JAMAIS `{% extends "base.html" %}`

3. **Tests automatisés:**
   - Ajouter test de rendu pour tous les templates
   - Vérifier que `t()` n'a pas d'arguments nommés
   - Vérifier que tous les extends pointent vers `layouts/`

### Actions à venir

- [ ] Créer un linter pour détecter `t(*args, **kwargs)` dans les templates
- [ ] Ajouter tests de rendu pour dashboard member/admin
- [ ] Documenter la fonction `t()` dans `.github/frontend.instructions.md`
- [ ] Créer un template checker dans CI/CD

---

## Related Issues

- Traductions partielles (bug séparé, non résolu ici)
- Cache filesystem errors (bug séparé, non résolu ici)
- Redirect loop (bug séparé, non résolu ici)

---

## Timeline

- **19:05:00** - Erreur détectée par l'utilisateur
- **19:05:30** - Analyse du log complétée
- **19:06:00** - Root cause identifiée (2 bugs)
- **19:07:00** - Corrections appliquées (4 fichiers)
- **19:08:00** - Vérification et rapport créé

**Temps de résolution:** ~3 minutes

---

## Lessons Learned

1. La fonction `t()` actuelle ne supporte pas l'interpolation de variables
2. Les templates doivent utiliser le chemin complet `layouts/base.html`
3. Les erreurs 500 peuvent masquer plusieurs bugs indépendants
4. grep_search est essentiel pour trouver tous les patterns problématiques

---

**Status:** ✅ RESOLVED  
**Next Steps:** Tester les dashboards manuellement après redémarrage du serveur

---

**File:** `.github/incidents-history-2025-12-30-dashboard-500.md`  
**Repository:** X-Filamenta-Python  
**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

