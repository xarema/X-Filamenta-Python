# Rapport de correction des bugs - i18n, Préférences et Dashboard

**Date**: 2025-12-30 16:00  
**Scope**: Correction de 8 bugs identifiés  
**Statut**: 🔧 EN COURS

---

## 🐛 Bugs identifiés

### 1. Dashboard toujours en français
**Problème**: Texte hardcodé au lieu d'utiliser `t()`  
**Fichier**: `frontend/templates/dashboard/member.html`  
**Solution**: Remplacer tout texte hardcodé par `{{ t('key') }}`

### 2. Variable manquante `pages.about.cta_source`
**Problème**: Clé manquante dans fr.json et en.json  
**Fichiers**: 
- `backend/src/i18n/translations/fr.json`
- `backend/src/i18n/translations/en.json`  
**Solution**: Ajouter la clé dans les deux fichiers

### 3. Erreur 415 dans /preferences
**Problème**: HTMX n'envoie pas `Content-Type: application/json`  
**Fichier**: `frontend/templates/pages/preferences.html`  
**Solution**: Ajouter `hx-headers='{"Content-Type": "application/json"}'` ou utiliser form-data

### 4. Modification utilisateur ne fonctionne pas (admin/users)
**Problème**: Modal d'édition ne soumet pas les changements  
**Fichier**: `frontend/templates/admin/users.html`  
**Solution**: Vérifier le formulaire et l'endpoint

### 5. Variables admin/settings ne fonctionnent pas
**Problème**: Clés i18n manquantes ou mal référencées  
**Fichier**: `frontend/templates/admin/settings.html`  
**Solution**: Ajouter les clés manquantes

### 6. Paramètres admin/settings ne se sauvegardent pas
**Problème**: Endpoint non fonctionnel  
**Fichier**: `backend/src/routes/admin.py`  
**Solution**: Vérifier la logique de sauvegarde

### 7. Mot de passe oublié ne répond pas
**Problème**: Bouton ou route manquant  
**Fichier**: `frontend/templates/admin/settings.html`  
**Solution**: Implémenter l'action

### 8. Variables auth/register ne fonctionnent pas
**Problème**: Clés i18n non définies  
**Fichier**: `frontend/templates/auth/register.html`  
**Solution**: Ajouter les clés manquantes

---

## 📝 Plan de correction

### Étape 1: Ajouter clés i18n manquantes
- [x] Identifier toutes les clés manquantes
- [ ] Ajouter dans fr.json
- [ ] Ajouter dans en.json
- [ ] Valider la structure JSON

### Étape 2: Corriger le dashboard
- [ ] Remplacer texte hardcodé
- [ ] Tester changement de langue

### Étape 3: Corriger les préférences
- [ ] Fixer l'erreur Content-Type
- [ ] Tester sauvegarde

### Étape 4: Corriger admin/users
- [ ] Vérifier le formulaire d'édition
- [ ] Tester la sauvegarde

### Étape 5: Corriger admin/settings
- [ ] Ajouter les clés i18n
- [ ] Fixer la sauvegarde
- [ ] Implémenter mot de passe oublié

### Étape 6: Corriger auth/register
- [ ] Ajouter les clés i18n
- [ ] Tester le formulaire

---

## 🔧 Corrections appliquées

*(À remplir au fur et à mesure)*


