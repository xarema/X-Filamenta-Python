# Checklist de Test - Phase 1 Corrections i18n

**Date:** 2025-12-30 17:30  
**URL Test:** http://127.0.0.1:5000  
**Testeur:** À compléter

---

## ✅ Pré-requis

- [x] Cache vidé (`instance/sessions/*` et `cache/*`)
- [x] Fichier `fr.json` corrigé et validé
- [x] Serveur redémarré avec fichier corrigé
- [ ] Navigateur en mode privé (pour éviter cache navigateur)

---

## 🧪 Tests de Traductions Françaises

### 1. Page d'Accueil (/)

- [ ] Navbar affiche texte français (pas "nav.home")
- [ ] Footer affiche "Légal" (pas "footer.legal")
- [ ] Bouton langue affiche "Français"
- [ ] Titre page en français

### 2. Page À Propos (/about)

- [ ] Section "Fonctionnalités" affiche texte FR
- [ ] Bouton "Voir le code source" affiché (pas "pages.about.cta_source")
- [ ] Tous les paragraphes en français
- [ ] Footer correct

### 3. Page Contact (/contact)

- [ ] Label "Envoyer" (pas "pages.contact.send")
- [ ] Placeholder email correct
- [ ] Placeholder nom correct
- [ ] Placeholder message correct
- [ ] Section "Autres moyens de contact" (pas "pages.contact.other")

### 4. Page Connexion (/login)

- [ ] Titre "Connexion" affiché
- [ ] Labels en français
- [ ] Bouton "Se connecter" (pas "auth.login.submit")
- [ ] Lien "Première utilisation ? Installer X-Filamenta"

### 5. Dashboard Membre (/dashboard)

**⚠️ Nécessite connexion avec admin/test**

- [ ] Titre "Tableau de bord"
- [ ] Message de bienvenue en français
- [ ] Stats en français (Contenu, Activité, Préférences)
- [ ] Bouton "Déconnexion"
- [ ] Toutes les cartes en français

### 6. Page Admin - Utilisateurs (/admin/users)

**⚠️ Nécessite connexion admin**

- [ ] Colonne "Nom" (pas "admin.users.table.name")
- [ ] Colonne "Date de création" (pas "admin.users.table.date_created")
- [ ] Bouton "Enregistrer" (pas "admin.users.actions.save")
- [ ] Bouton "Annuler" (pas "admin.users.actions.cancel")

### 7. Page Admin - Paramètres (/admin/settings)

**⚠️ Nécessite connexion admin**

- [ ] Toutes les sections en français
- [ ] Labels formulaires en français
- [ ] Bouton "Enregistrer" fonctionne
- [ ] Pas de variables affichées

### 8. Page Préférences (/preferences)

**⚠️ Nécessite connexion**

- [ ] Titre "Préférences" affiché
- [ ] Sélecteur de langue fonctionne
- [ ] Sélecteur de thème fonctionne
- [ ] Bouton "Enregistrer" fonctionne (PAS d'erreur !)
- [ ] Message de succès affiché

---

## 🔄 Tests de Changement de Langue

### Test FR → EN

1. [ ] Aller sur n'importe quelle page
2. [ ] Changer langue vers "English"
3. [ ] Page se rafraîchit en anglais
4. [ ] Navbar en anglais
5. [ ] Footer en anglais
6. [ ] Contenu en anglais

### Test EN → FR

1. [ ] Langue = English
2. [ ] Changer vers "Français"
3. [ ] Page se rafraîchit en français
4. [ ] Tout en français (navbar, footer, contenu)

### Test de Persistance

1. [ ] Changer langue vers FR
2. [ ] Naviguer sur plusieurs pages
3. [ ] Langue reste FR sur toutes les pages
4. [ ] Fermer le navigateur
5. [ ] Rouvrir → Langue toujours FR (si "Remember me")

---

## 🐛 Tests de Bugs Spécifiques

### Bug 1: Variables affichent nom au lieu de texte

**Avant:** footer.legal, pages.about.cta_source, etc.  
**Après:** Texte français affiché

- [ ] ✅ Footer affiche "Légal" et non "footer.legal"
- [ ] ✅ About affiche texte et non "pages.about.cta_source"
- [ ] ✅ Aucune variable visible nulle part

### Bug 2: Dashboard hardcodé en français

**Avant:** Texte hardcodé, ne change pas de langue  
**Après:** Dashboard multi-langue

- [ ] ✅ Dashboard en FR quand langue = FR
- [ ] ✅ Dashboard en EN quand langue = EN
- [ ] ✅ Changement de langue change le dashboard

### Bug 3: Navbar toujours en anglais

**Avant:** Navbar reste EN même en FR  
**Après:** Navbar suit la langue

- [ ] ✅ Navbar FR quand langue = FR
- [ ] ✅ Navbar EN quand langue = EN
- [ ] ✅ "Accueil" / "Home" selon langue

### Bug 4: Préférences erreur 415

**Avant:** Erreur lors de la sauvegarde  
**Après:** Sauvegarde fonctionne

- [ ] ✅ Changer langue → Sauvegarder → Succès
- [ ] ✅ Changer thème → Sauvegarder → Succès
- [ ] ✅ Pas de message d'erreur

### Bug 5: Redirect loop

**Avant:** Boucle de redirection après connexion  
**Après:** Connexion normale

- [ ] ✅ Login → Redirect vers dashboard
- [ ] ✅ Pas de boucle infinie
- [ ] ✅ Navigation normale

---

## 📊 Résultats

### Statistiques

- **Total tests:** 45
- **Tests réussis:** ___/45
- **Tests échoués:** ___/45
- **Bugs critiques:** ___
- **Bugs mineurs:** ___

### Bugs Trouvés

*(Liste à compléter pendant les tests)*

1. ...
2. ...
3. ...

### Validation Globale

- [ ] ✅ Traductions françaises fonctionnent à 100%
- [ ] ✅ Changement de langue fonctionne
- [ ] ✅ Pas de variables affichées
- [ ] ✅ Tous les boutons en français
- [ ] ✅ Tous les formulaires en français

---

## 📝 Notes du Test

*(Section libre pour observations)*

---

## ✅ Conclusion

**Phase 1 validation:**

- [ ] ✅ Toutes les traductions françaises fonctionnent
- [ ] ✅ Tous les bugs i18n corrigés
- [ ] ✅ Prêt pour Phase 2 (bugs backend)

**Testé par:** ___________  
**Date:** 2025-12-30  
**Signature:** ___________

