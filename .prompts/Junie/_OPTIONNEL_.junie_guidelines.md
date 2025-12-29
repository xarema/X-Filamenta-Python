# Junie Guidelines (optionnel)

Ces guidelines servent à aligner Junie sur ton repo. Ajuste si nécessaire.

Priorités absolues
- Lire et respecter toutes les règles IA/conventions situées dans `.github/` avant toute action.
- Ne pas exécuter de commandes destructives (rm -rf, wipe, delete) sans confirmation explicite.
- Ne jamais exposer de secrets. Si un secret est détecté: arrêter, documenter, proposer rotation + purge + prévention.

Qualité
- Changements petits et atomiques.
- Patches/diffs clairs.
- Ajouter tests de non-régression pour les bugs corrigés.
- Garder le repo “buildable” et la CI verte.

Sécurité
- Vérifier dépendances, workflows CI, gestion des secrets, inputs non fiables, logs, headers, CORS.