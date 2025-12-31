<!--
Purpose: Feuille de route Phase 4 - Partie 1
Description: Synthèse des fonctionnalités cibles et jalons pour la Phase 4 (partie 1).

File: .roadmap/features.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal
  Notes:
- Git history is the source of truth for authorship and change tracking.
-->

# Feuille de route — Phase 4 (Partie 1)

## Portée

- Mettre en œuvre le wizard d'installation multi-hébergeurs (cPanel/Docker/VPS) avec détection d'architecture et dépendances.
- Sécuriser l'accès initial : page index publique seule, redirection première utilisation vers installation, auth + 2FA (TOTP primaire), rôles membre/admin.
- Établir l'espace administrateur minimal : tableau de bord, gestion utilisateurs, détection MàJ git, affichage version, sauvegarde app+DB, historique admin (liste + top 5).
- Garantir réactivité et accessibilité mobile (responsive, grilles adaptatives, scroll horizontal tables).

## Jalons et livrables

### 1) Installation & Déploiement

- Wizard (page 1 langue EN/FR) avec choix DB (SQLite par défaut `x-filamenta_python.db`, MySQL, PostgreSQL) et options seed/restauration.
- Détection auto dépendances + versions ; exécution auto des installs si shell disponible.
- Sélection manuelle du moteur DB par l'utilisateur (SQLite par défaut, MySQL, PostgreSQL), assistance guidée si besoin.
- Restauration proposée lors de l'installation : seed par défaut ou restauration d'une sauvegarde existante.
- Création compte admin (nom obligatoire, surnom optionnel, mot de passe fort ≥8 avec majuscule+symbole, email obligatoire, langue par défaut, thème clair/sombre par défaut).

#### Wizard (UX détaillée)

- Étape 0 (détection) : détecter shell dispo, OS, arch, présence git/python/pip/DB clients ; afficher résumé.
- Étape 1 (langue/thème) : FR/EN, thème clair/sombre par défaut ; stocker dans session ; validations simples.
- Étape 2 (base de données) : choix manuel SQLite/MySQL/PostgreSQL ; assistant de connexion (hôte/port/user/pass/db) avec test de connexion ; option SQLite auto (`x-filamenta_python.db`).
- Étape 3 (données) : seed par défaut ou restauration d'une sauvegarde existante (upload/chemin local) ; vérif format + checksum ; dry-run de restauration si choisi.
- Étape 4 (compte admin) : nom requis, surnom optionnel, email requis, mot de passe fort (≥8, maj, symbole), préférence langue/thème ; validation côté serveur ; hachage sécurisé.
- Étape 5 (synthèse) : récap paramètres, bouton "Lancer" ; barre de progression ; logs succincts HTMX.
- Étape 6 (finalisation) : création structure DB/migrations, seed/restauration, création admin, test de santé ; redirection login.
- States/erreurs : messages clairs, possibilité de revenir aux étapes précédentes sans perdre les valeurs ; HTMX partials ciblés pour swap.

### 2) Sécurité & Accès

- Page `index` publique, tout le reste protégé si non connecté.
- Authentification sécurisée (stockage mot de passe haché, transport chiffré), 2FA TOTP primaire ; email OTP disponible en fallback optionnel.
- Validation stricte des entrées.
- Gestion des rôles : espace membre (consultation), espace admin (gestion utilisateurs, stats, paramètres globaux).

### 3) Espace administrateur

- Tableau de bord admin (widgets : 5 dernières entrées historique admin, version installée, statut MàJ git, indicateur sauvegarde).
- Gestion utilisateurs : liste, promotion/révocation admin, suppression.
- Outils système : détection MàJ (git), action d'update/migration (git pull) dans l'interface, script sauvegarde app+DB, hooks futurs pour thèmes/extensions/langues.
- Historique admin détaillé : page dédiée + top 5 dans le dashboard.
- Paramètres par défaut : thème et langue appliqués aux nouveaux utilisateurs et visiteurs.
- Mise à jour applicative : mode dry-run par défaut (vérification des commits en avance/retard), option "appliquer" protégée (confirmation + sauvegarde préalable automatique) pour un `git pull` sécurisé.

### 4) Mobilité & Accessibilité

- Responsive complet (mobiles/tablettes/desktop), grilles adaptatives, navigation tactile (onglets/menus scrollables), tables fluides (scroll horizontal), interface épurée sur petit écran.

### 5) Pages & Navigation

- Index public avec détection première utilisation → redirection vers wizard d’installation.
- Zones membres/admin accessibles uniquement après authentification et selon rôle.
- Footer : mention du type de licence + lien "Legal/About" vers la page légale (AGPL).

## Hypothèses / Contraintes

- Flask + HTMX + Bootstrap 5 ; Python 3.12 ; respect AGPL et attribution footer.
- Style/formatage : 88 colonnes pour code ; validation stricte inputs ; éviter dépendances nouvelles sauf nécessité.
- Tests attendus pour chaque changement (pytest), lint (ruff), type-check (mypy) avant livraison.

## Décisions confirmées

- 2FA : TOTP par défaut ; email OTP en secours optionnel.
- Sauvegarde/restauration : proposer restauration d'une sauvegarde existante (DB seule ou app+DB) depuis le menu admin ; vérifier format + checksum ; snapshot pré-restauration recommandé.
- Wizard : choix manuel du moteur DB par l'utilisateur (avec guidance), SQLite par défaut.
- Attribution : footer avec mention de licence + lien "Legal/About".
- Mises à jour : privilégier le dry-run ; application réelle protégée par confirmation et sauvegarde.

## Routes / Templates à créer ou adapter (Phase 4 - P1)

- Routes wizard : `GET/POST /install` avec étapes HTMX (partials par étape), protection pour éviter ré-usage après installation.
- Auth/2FA : routes login/logout, setup TOTP, vérif TOTP, email OTP fallback (optionnel) ; templates HTMX pour prompts.
- Admin : dashboard (`/admin`), gestion utilisateurs (`/admin/users` CRUD + promotion/révocation), historique admin (`/admin/history` + fragment top5), sauvegarde (`/admin/backup`), mise à jour (`/admin/update` dry-run + apply protégé).
- Pages publiques : `index` (public), redirection première utilisation vers wizard si non configuré.
- Fragments communs : footer avec licence + lien Legal/About ; composants HTMX de progression/alertes.

## Backup / Restore (format & flux)

- Format recommandé : archive compressée (.tar.gz ou .zip) contenant `app/` snapshot + dump DB (`.sql` pour MySQL/PostgreSQL ou copie `.db` pour SQLite) + manifest (`manifest.json` avec version, horodatage, checksum).
- Génération : via menu admin → crée manifest + checksum, stocke dans dossier dédié (ex: `backups/` hors static) ; log dans historique admin.
- Restauration : upload/sélection, vérif manifest + checksum, dry-run (intégrité) optionnel, snapshot pré-restauration automatique, application DB (import SQL ou remplacement fichier SQLite), restauration fichiers app si inclus.
- Sécurité : restreindre chemin d'écriture/lecture, contrôle des extensions, limiter taille upload, masquer secrets dans logs.
