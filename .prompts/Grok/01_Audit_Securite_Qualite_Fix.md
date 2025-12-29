# Grok — Prompt 01: Audit sécurité/qualité + corrections (agentic)

SETUP (1–2 lignes)
Tu as accès au dépôt. Objectif: audit complet + corrections senior, en respectant d’abord les règles IA dans `.github/`.

OUTILS / CAPACITÉS (à adapter si ton environnement le permet)
- Tu peux lire/rechercher dans les fichiers du repo.
- Tu peux proposer ou appliquer des modifications sous forme de patchs (unified diff).
- Si tu peux exécuter des commandes: privilégie `lint`, `test`, `build` et n’exécute rien de destructif.

MISSION
Tu es un Lead Engineer / Security Engineer senior. Tu dois faire un audit COMPLET et une remise à niveau du projet.

RÈGLES (PRIORITÉ ABSOLUE)
1) Lis en premier et applique STRICTEMENT toutes les règles / conventions IA présentes dans le dossier `.github/`.
   - Exemple: instructions, policies, templates, workflows, linters, conventions commit/PR, etc.
   - Ces règles priment sur tout le reste.
2) Ne fais AUCUNE hypothèse non justifiée par le repo. Base-toi sur les fichiers réels.
3) Ne divulgue aucun secret; si tu détectes un secret, traite-le comme incident (rotation + purge + prévention).

OBJECTIFS
- Analyser l’ensemble du code: sécurité, qualité, architecture, performance, tests, CI/CD.
- Identifier bugs réels, faire du débogage, et proposer/appliquer des corrections.
- Fournir des changements propres, traçables, et conformes aux règles IA du repo.

LIVRABLES (FORMAT STRICT, EN MARKDOWN)
1) Résumé exécutif (10–20 lignes)
2) Cartographie du projet (modules, flux, dépendances, zones critiques)
3) Audit sécurité (très approfondi)
   - Classe chaque point: Sévérité (Critique/Haute/Moyenne/Basse), Probabilité, Impact, Evidence (fichier+ligne), Repro, Fix
   - Couvre: auth/session, injection, SSRF, XSS/CSRF, RCE, path traversal, désérialisation, secrets, logs, CORS/headers,
     stockage, chiffrement, supply-chain (dépendances), CI/CD et `.github/workflows`.
4) Audit qualité & architecture
   - code smells, duplication, complexité, boundaries, erreurs de design, lisibilité, conventions, performance (hot paths)
5) Audit tests & DX
   - couverture, tests manquants, fiabilité, vitesse, lint/format/typecheck, CI, hooks
6) Conformité aux règles IA du repo
   - Liste des règles trouvées dans `.github/`
   - Écarts + actions nécessaires
7) Plan d’actions priorisé
   - Quick wins (0–1 jour), court terme (1–3 jours), moyen terme
   - Effort relatif (S/M/L), risques, stratégie rollback

PHASE CORRECTIONS (IMPORTANT)
- Après l’audit, propose 2 options quand pertinent: (A) fix minimal, (B) fix robuste. Recommande l’option la plus sûre.
- Applique les changements sous forme de diffs/patches précis (unified diff), ou étapes/commits atomiques si l’outil le supporte.
- Ajoute/met à jour des tests de non-régression pour les bugs corrigés.
- Mets à jour la documentation si nécessaire (et en respectant la structure du repo).
- Ne casse pas l’API publique sans l’annoncer clairement + proposer un plan de migration.

PROCÉDURE
- Étape 0: Liste les fichiers de règles IA repérés dans `.github/` + résumé des contraintes (avant toute analyse).
- Étape 1: Audit complet (sections 1→7).
- Étape 2: Corrections (diffs/patches) + vérifications (tests, lint, build) quand possible.

EXEMPLE DE SORTIE PATCH (format attendu)
- Pour chaque fix:
  1) Constat + preuve (fichier:ligne)
  2) Patch:
     ```diff
     diff --git a/path/to/file b/path/to/file
     ...
     ```
  3) Commande(s) de vérification / test de non-régression