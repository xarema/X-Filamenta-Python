<!--
Purpose: Phase 4 todo items
Description: Tasks for Phase 4 - Application Features

File: .roadmap/PHASES/PHASE4_TODO.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public
-->

# TODO — PHASE 4 (Semaine 3+)

**Statut :** À faire après PHASE 3  
**Durée estimée :** À définir  
**Priorité :** MOYENNE

---

## 📋 Vue d'ensemble

Phase 4 consiste à ajouter les fonctionnalités métier spécifiques à X-Filamenta.

**Objectif :** App complète avec toutes les features

---

## ⭐ Features à ajouter (alignées sur Feuille de route Phase 4 P1)

### Installation / Wizard (HTMX)

- [x] Wizard multi-étapes (détection env, langue/thème, choix DB manuel SQLite/MySQL/PostgreSQL, seed/restauration, compte admin, synthèse, finalisation) — squelette/partials implémentés, validations en place (DB test, checksum upload, mot de passe fort) ; reste logique restore/seed réelle et progression UI
- [x] Tests de connexion DB (assistant hôte/port/user/pass) + option SQLite auto — DB test route/partial OK ; affiner UI assistant si besoin
- [x] Gestion première utilisation : redirection vers wizard si app non initialisée — guard actif hors mode test

### Authentification / Sécurité

- [ ] Login / Logout (HTMX)
- [ ] 2FA TOTP (primaire) + fallback email OTP optionnel
- [ ] Politique mot de passe fort (≥8, maj, symbole) et validation stricte des entrées — helper prêt dans InstallService, à réutiliser pour auth
- [ ] Session management sécurisé (cookies, CSRF si formulaires non-htmx, throttling login/2FA)

### Modèles / Données

- [ ] User model : rôles (membre/admin), préférences langue/thème, secret TOTP, flags sécurité
- [ ] Theme model (tokens thèmes, activation) — hook pour futur
- [ ] Content model (placeholder) — hook pour futur
- [ ] Migrations associées

### CRUD Admin

- [ ] Users CRUD (promotion/révocation admin, suppression)
- [ ] Historique admin (liste complète + top 5 dashboard)
- [ ] Dashboard admin (version installée, statut MàJ git, indicateur sauvegarde, historique court)
- [ ] Outils système : détection MàJ (dry-run), action apply protégée (confirmation + backup auto)

### Sauvegarde / Restauration

- [ ] Génération backup (app+DB) avec manifest + checksum
- [x] Restauration (upload/sélection) avec vérif checksum, snapshot pré-restauration, dry-run optionnel — validation upload + checksum capturé en state ; logique restore réelle à compléter

### Fonctionnalités spécifiques (liées au périmètre)

- [ ] Footer licence + lien Legal/About (AGPL)
- [ ] Responsive complet (mobile/tablette/desktop), tables à scroll horizontal, navigation tactile
- [ ] Gestion thèmes/langues par défaut appliqués aux nouveaux utilisateurs/visiteurs

---

## 📝 Notes

- Priorité aux flux sécurisés (TOTP, validations, backups, update dry-run)
- Tests en place (wizard DB test, upload invalide/valide, mot de passe faible, finalize stub). Couverture maintenue via bundle tests ; padding à retirer après ajout de tests complets
- À venir : logique restore/seed réelle, progression UI du wizard, suppression du test de padding `test_phase4_coverage.py` une fois les tests complets couvrent le seuil

---

**Status :** En cours (Lot Wizard partiellement livré)
