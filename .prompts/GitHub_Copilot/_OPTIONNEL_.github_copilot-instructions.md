# .github/copilot-instructions.md (optionnel)

## Règles prioritaires
- Lis et respecte toutes les règles IA et conventions situées dans `.github/` (y compris celles-ci).
- Ne propose pas de suppression de fichiers sans justification claire.
- Ne jamais introduire de secrets dans le code, les logs, ou la CI.

## Style de sortie
- Pour les changements: fournir un patch `diff --git` (unified diff).
- Pour la sécurité: toujours inclure fichier+ligne, sévérité, repro, fix.

## Vérifications
- Après modifications: proposer les commandes `lint`, `test`, `build` adaptées au repo.