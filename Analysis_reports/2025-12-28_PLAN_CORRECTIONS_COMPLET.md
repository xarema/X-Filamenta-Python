# PLAN DE CORRECTION COMPLET - 2025-12-28 17:50

## PROBLÈMES IDENTIFIÉS (PAR L'UTILISATEUR)

1. ❌ Prérequis PIP skip mais affiché
2. ❌ Script sécuritaire ? À vérifier
3. ❌ Message erreur page DB: "wizard.db.error" (clé i18n)
4. ❌ Messages champs vides en anglais
5. ❌ Boutons l'un sous l'autre (doivent être sur même ligne)
6. ❌ Backup validé mais fichier.tar.gz vide
7. ❌ Variables vides dans templates (texte direct au lieu de i18n)
8. ❌ Page done: pas de confirmation tables backup installées
9. ❌ /install/verify-db = 404

## ACTIONS À PRENDRE (DANS L'ORDRE)

### 1. CRÉER FICHIER DE LANGUE FR COMPLET
- backend/src/translations/fr.json
- Toutes les clés wizard.* utilisées dans templates
- Pas de texte en dur dans templates

### 2. CORRIGER ROUTE /install/verify-db (404)
- Vérifier que route est bien enregistrée
- Vérifier before_request ne bloque pas

### 3. CORRIGER MESSAGES ERREUR DB
- db_form.html: utiliser clés i18n
- db_test.html: utiliser clés i18n
- admin_form.html: validation champs

### 4. CORRIGER BOUTONS (MÊME LIGNE)
- done.html: flexbox ou inline-block

### 5. CORRIGER VALIDATION BACKUP
- Vérifier que fichier n'est pas vide
- Afficher taille fichier
- Vérifier contenu (tar.gz doit avoir fichiers)

### 6. CORRIGER PAGE DONE
- Afficher si backup restauré
- Afficher tables du backup
- Afficher nombre enregistrements restaurés

### 7. RETIRER PIP DES PRÉREQUIS
- requirements.html: ne pas afficher pip

### 8. AUDIT SÉCURITÉ
- Validation inputs
- Pas de SQL injection
- Pas de path traversal
- CSRF tokens

## FICHIERS À MODIFIER

1. backend/src/translations/fr.json (CRÉER)
2. backend/src/routes/install.py (verify-db)
3. frontend/templates/pages/install/partials/db_form.html
4. frontend/templates/pages/install/partials/db_test.html
5. frontend/templates/pages/install/partials/admin_form.html
6. frontend/templates/pages/install/partials/done.html
7. frontend/templates/pages/install/partials/requirements.html
8. backend/src/services/install_service.py (backup validation)

## RÈGLES À SUIVRE

✅ Lire .github/copilot-instructions.md AVANT toute modif
✅ Lire .github/ROUTE_CHANGE_RULES.md AVANT modif routes
✅ Utiliser UNIQUEMENT clés i18n (pas texte direct)
✅ Tester en DEV puis PROD
✅ Ne PAS refaire erreurs précédentes
✅ Suivre le plan étape par étape

## DÉBUT DES CORRECTIONS

Date: 2025-12-28 17:50

