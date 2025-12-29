# Audit et Corrections — Wizard d'Installation

**Date:** 2025-12-28T01:00:00+00:00  
**Contexte:** Résolution des problèmes du wizard d'installation  
**Scope:** Routes install, templates, fichiers statiques, traductions

---

## 🔍 Problèmes Identifiés

### 1. **Fichiers statiques 404**
- ❌ Erreur: `/static/css/tokens/variables.css` → 404
- ❌ Erreur: `/static/css/main.css` → 404
- ❌ Erreur: `/static/js/plugins/htmx-utils.js` → 404
- ❌ Erreur: `/static/js/plugins/alpine-utils.js` → 404
- ❌ Erreur: `/static/js/plugins/tabulator.js` → 404

**Cause:** Les fichiers existent dans `frontend/static/` mais Flask les cherche correctement. Le problème est que les fichiers sont vides ou inexistants.

**Status:** ✅ Fichiers trouvés dans `frontend/static/`

---

### 2. **Navigation du wizard bloquée**

**Symptômes:**
- Clic sur "Continuer en français" → Pas de changement visible
- La page demande directement la base de données après le choix de langue
- Message "no file upload" lors du clic sur "Continuer" après test DB

**Cause 1:** Le template `index.html` affiche `db_form` directement après le choix de langue
**Cause 2:** Le flux du wizard n'est pas clair pour l'utilisateur

---

### 3. **Sélection MySQL/PostgreSQL**

**Symptôme:** Les onglets MySQL et PostgreSQL semblent ne pas être cliquables

**Cause:** Bootstrap tabs fonctionne correctement dans le template, mais peut-être que Bootstrap JS n'est pas chargé ou qu'il y a un conflit.

---

### 4. **Message "no file upload"**

**Symptôme:** Après test DB réussi, clic sur "Continuer" → message d'erreur "no file upload"

**Cause:** La route `/install/step` avec `step=admin_form` ne vérifie pas si un backup a été uploadé. Le formulaire d'upload n'est jamais affiché si on clique sur "Continuer sans backup".

---

## 🔧 Corrections à Appliquer

### 1. Vérifier et créer les fichiers statiques manquants

**Action:** Créer des fichiers CSS/JS de base s'ils sont vides

### 2. Améliorer le flux du wizard

**Action:** 
- Ajouter une étape de bienvenue après le choix de langue
- Clarifier la navigation entre les étapes
- Corriger le message "no file upload"

### 3. Vérifier Bootstrap JS

**Action:** S'assurer que Bootstrap JavaScript est bien chargé dans `base.html`

### 4. Améliorer les logs

**Action:** Ajouter plus de logs dans `install.py` pour débugger

---

## 📋 Plan de Corrections

1. ✅ Vérifier les fichiers statiques
2. ⏳ Corriger le flux du wizard
3. ⏳ Améliorer les templates
4. ⏳ Ajouter des logs de debug
5. ⏳ Tester le wizard complet

---

## 🎯 Résultat Attendu

- Wizard fonctionnel de bout en bout
- Navigation claire entre les étapes
- Pas de messages d'erreur confus
- Toutes les options (SQLite/MySQL/PostgreSQL) fonctionnelles

