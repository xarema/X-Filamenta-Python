# Fonctionnalités de X-Filamenta-Python

POUR PHASE 4 (1er partie)

## Installation & Déploiement

- Script "Wizard" pour installation facile.
  - Détection de l'architecture (Multi-hébergeurs ex. cPanel + Docker + VPS sous linux)
  - Détection des dépendances + versions
  - Configuration initiale
    - DB : SQLite / MySQL / PostgreSQL (SQLite nom par défaut = (Par défaut : `x-filamenta_python.db`))
      - Option : installation d'une bd d'exemple
      - Option : installation d'une sauvegarde si meme db que la sauvegarde
    - Création du compte administarteur
      - Nom de l'administarteur (Obligatoire)
      - Surnom (Optionel)
      - Mot de passe (Obligatoire avec 8 caractères avec majuscule et symbole)
      - Adresse courriel (Obligatoire)
      - Inferface EN ou FR (Sélection par défaut)
      - Theme Clair / Sombre (Sélection par défaut)
  - 1er page du Wizard = Sélectionner votre langue en anglais et francais.
  - Gestion des dépendances automatique si herbergeur accepte les commandes shell

## Sécurité & Accès

- Page "index" par défaut si aucun utilisateur de connecté.
  - Aucune autre page accessible
- Systeme d'authentification
  - Connexion sécurisé avec nom d'utilisateur et mot de passe chiffrés
  - Systeme 2FA
- Gestions des roles
  - Espace membre
    - Consultation des autres pages
  - Espace administrateur
    - Gestions des utilisateurs
    - Statistique système, modification globale
- Sécurisation globale, Protection contre les injections SQL et validation stricte des entrées.

## Esapce administrateur

- Tableau de board admin
- Gestions des utilisateur
  - Liste complète des membres inscrits.
    - Attribution/Révocation des droits administrateur.
    - Suppression d'utilisateurs.
- Détection des mise à jour (Git)
- Script d'update et de migration (Git pull) directement dans l'interface
- Affichage du numéro de version app installé et notification si nouvelle mise a jour
- Accès toujours sécurisé
- Script d'installation de theme + extensions + langues (a inclure mais pas encore développé)
- Script de sauvegarde app + DB
- Historique d'administration
  - Suivi détaillé des ajouts (Qui, Quand, Quoi) dans une page dédiée ET tableau des 5 dernières ligne dans le tableau de bord admin.
- Définition d'un thème par défaut pour tous les nouveaux utilisateurs et visiteurs.
- Définition du langage par défaut pour tous les nouveaux utilisateurs et visiteurs.

## Mobilité & Accessibilité

- **Design Responsive Intégral** : Navigation optimisée pour mobiles, tablettes et ordinateurs de bureau.
- **Grilles Adaptatives** : Réorganisation automatique des tableaux, KPI et graphiques selon la taille de l'écran.
- **Navigation Tactile** : Menus et onglets défilables horizontalement sur petits écrans.
- **Tableaux Fluides** : Support du défilement horizontal pour les données larges sur mobile.
- **Interface Épurée** : Suppression des éléments superflus sur petit écran pour maximiser l'espace de travail.

## Pages & Navigation

### Index (Public)

- Détection de première utilisation (redirection vers installation).
