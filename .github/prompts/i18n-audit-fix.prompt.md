---
Name: i18n Audit & Fix (Traductions manquantes)
Version: 1.0.0
Date: 2025-12-30
Purpose: Auditer et corriger les variables i18n manquantes dans fr.json et en.json

Tags: i18n, audit, critical, bug-fix
---

# PROMPT - Audit & Correction Traductions Manquantes

## 🎯 Objectif
Corriger les 34+ variables i18n manquantes identifiées dans l'audit du 2025-12-30.

## 🔴 Variables Manquantes Identifiées

### Footer
- `footer.legal` → "Légal"
- `footer.about` → "À Propos"
- `footer.contact` → "Contact"
- `footer.github` → "GitHub"

### Pages About
- `pages.about.title` → "À Propos"
- `pages.about.features` → "Fonctionnalités"
- `pages.about.security` → "Sécurité"
- `pages.about.security_desc` → "Vos données sont protégées..."
- `pages.about.performance` → "Performance"
- `pages.about.responsive` → "Responsive Design"
- `pages.about.responsive_desc` → "Fonctionne sur tous les appareils"
- `pages.about.cta` → "Commencer maintenant"
- `pages.about.cta_features` → "Voir les fonctionnalités"
- `pages.about.cta_contact` → "Nous contacter"
- `pages.about.ctasource` → "Voir le code source"

### Pages Contact
- `pages.contact.title` → "Nous Contacter"
- `pages.contact.description` → "Des questions ? Nous sommes là pour vous aider."
- `pages.contact.form_title` → "Envoyer un message"
- `pages.contact.name_label` → "Votre nom"
- `pages.contact.email_label` → "Votre email"
- `pages.contact.subject_label` → "Sujet"
- `pages.contact.message_label` → "Message"
- `pages.contact.send` → "Envoyer"
- `pages.contact.placeholder_name` → "Jean Dupont"
- `pages.contact.placeholder_email` → "jean@example.com"
- `pages.contact.placeholder_subject` → "Sujet du message"
- `pages.contact.placeholder_message` → "Votre message ici..."
- `pages.contact.links_title` → "Autres moyens de nous joindre"
- `pages.contact.email` → "Email"
- `pages.contact.github` → "GitHub"
- `pages.contact.support` → "Support"
- `pages.contact.support_hours` → "Lundi-Vendredi, 9h-17h"
- `pages.contact.other` → "Autres"

### Admin Dashboard
- `admin.dashboard.title` → "Tableau de bord"
- `admin.dashboard.welcome` → "Bienvenue"
- `admin.dashboard.stats.title` → "Statistiques"
- `admin.dashboard.stats.errors` → "Erreurs"
- `admin.dashboard.stats.visits` → "Visites"
- `admin.dashboard.stats.users` → "Utilisateurs"
- `admin.dashboard.stats.content` → "Contenu"
- `admin.dashboard.management` → "Gestion"
- `admin.dashboard.recent_activity` → "Activité récente"

### Admin Users
- `admin.users.title` → "Gestion des utilisateurs"
- `admin.users.add_user` → "Ajouter un utilisateur"
- `admin.users.table.title` → "Utilisateurs"
- `admin.users.table.id` → "ID"
- `admin.users.table.username` → "Nom d'utilisateur"
- `admin.users.table.email` → "Email"
- `admin.users.table.role` → "Rôle"
- `admin.users.table.status` → "Statut"
- `admin.users.table.date_created` → "Créé le"
- `admin.users.table.date_modified` → "Modifié le"
- `admin.users.table.actions` → "Actions"
- `admin.users.form.title` → "Formulaire utilisateur"
- `admin.users.form.name` → "Nom"
- `admin.users.form.email` → "Email"
- `admin.users.form.role` → "Rôle"
- `admin.users.form.status` → "Statut"
- `admin.users.form.is_admin` → "Administrateur"
- `admin.users.actions.edit` → "Modifier"
- `admin.users.actions.delete` → "Supprimer"
- `admin.users.actions.save` → "Enregistrer"
- `admin.users.actions.cancel` → "Annuler"
- `admin.users.roles.user` → "Utilisateur"
- `admin.users.roles.admin` → "Administrateur"
- `admin.users.status.active` → "Actif"
- `admin.users.status.inactive` → "Inactif"

### Pages Erreur
- `error.404.title` → "Page non trouvée"
- `error.404.message` → "La page que vous recherchez n'existe pas"
- `error.404.back` → "Retourner à l'accueil"
- `error.500.title` → "Erreur serveur"
- `error.500.message` → "Une erreur est survenue"
- `error.500.back` → "Retourner à l'accueil"

## 📋 Procédure

1. ✅ Lire les fichiers actuels `fr.json` et `en.json`
2. ✅ Ajouter les clés manquantes avec traductions
3. ✅ Valider la structure JSON
4. ✅ Redémarrer le serveur
5. ✅ Vérifier que les traductions s'affichent

## 🔗 Fichiers à modifier
- `backend/src/i18n/translations/fr.json`
- `backend/src/i18n/translations/en.json`

## ✅ Validation
Après correction, les éléments suivants doivent afficher du texte:
- Page About
- Page Contact  
- Admin Dashboard
- Admin Users
- Erreur 404/500

