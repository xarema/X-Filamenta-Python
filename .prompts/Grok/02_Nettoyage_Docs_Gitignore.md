# Grok — Prompt 02: Nettoyage repo + docs + .gitignore (agentic)

SETUP (1–2 lignes)
Tu as accès au dépôt. Objectif: remettre le repo au carré (docs, suppression temp safe, .gitignore) en respectant `.github/`.

OUTILS / CAPACITÉS
- Lire/rechercher fichiers, proposer/appliquer patchs.
- Si exécution possible: vérifier `status`, `lint`, `test`, `build` après changements.

MISSION
Tu es un Maintainer senior (DX + architecture de repo). Tu dois NETTOYER et ORGANISER le dépôt pour qu’il soit cohérent, maintenable, et conforme.

RÈGLES (PRIORITÉ ABSOLUE)
1) Lis d’abord et applique STRICTEMENT toutes les règles IA dans `.github/`. Elles priment sur tout.
2) Ne supprime jamais un fichier sans justification (pourquoi, impact, récupération).
3) Ne casse pas le build ni la CI: toute modification de structure implique MAJ des imports/paths/scripts/pipelines.
4) Si tu hésites sur une suppression: préfère “gitignore + doc” plutôt que supprimer.

OBJECTIFS
1) Organisation propre du repo
   - Proposer une arborescence cible réaliste et adaptée au projet
   - Déplacer la documentation au bon endroit (souvent `/docs`), uniformiser (README/CONTRIBUTING/CHANGELOG, etc.)
2) Nettoyage
   - Identifier et supprimer uniquement les fichiers temporaires/artefacts non essentiels (caches, build outputs, logs locaux)
3) `.gitignore` (CRITIQUE)
   - Mettre à jour tous les `.gitignore` nécessaires (racine + sous-projets)
   - Couvrir: OS, IDE, langages/outils du projet, build artefacts, logs, env files, secrets, reports
   - Ajouter sections/commentaires clairs
4) Cohérence docs
   - Corriger liens relatifs après déplacements
   - Vérifier que README décrit setup/dev/tests/build/lint/CI
5) CI/CD & scripts
   - Vérifier `.github/workflows` + scripts (package.json, makefile, etc.) et corriger chemins
   - Améliorations légères (pre-commit/lint-staged/format) UNIQUEMENT si autorisées par les règles IA

LIVRABLES (FORMAT STRICT, EN MARKDOWN)
A) Diagnostic actuel (liste des problèmes)
B) Plan de nettoyage (étapes ordonnées + justification + impact)
C) Changements appliqués
   - Fichiers déplacés: ancien → nouveau
   - Fichiers supprimés: liste + raison
   - Patch/diff proposé pour `.gitignore` (et sous `.gitignore` si monorepo)
D) Vérifications
   - Commandes à exécuter (tests, lint, build)
   - Checklist repo clean

PROCÉDURE
- Étape 0: Lire les règles IA dans `.github/` et les résumer.
- Étape 1: Proposer arborescence cible.
- Étape 2: Appliquer nettoyage étape par étape (diffs/patches).
- Étape 3: Vérifier et corriger ce qui casse (tests/CI/scripts).

EXEMPLE DE SORTIE (déplacements + patch)
- Déplacements: `ancien → nouveau`
- Patch `.gitignore` en unified diff
- Checklist de validation (commandes)