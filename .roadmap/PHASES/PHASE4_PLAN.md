## Actions immédiates (phase 4 démarrage)

- [x] Scanner complet des templates/layouts/components pour hooks wizard/auth/admin (HTMX readiness)
- [x] Concevoir le squelette du Wizard (routes /install, services, partials HTMX, validations) avec plan de tests
- [x] Introduire hook first-run (redir / → /install si non configuré)
- [ ] Préparer la page /legal et ajuster footer si nécessaire (licence + lien Legal/About)
- [x] Définir backlog tests (pytest) lot 1 : happy path SQLite, DB invalide, mot de passe faible, restore checksum invalide, ré-usage wizard bloqué — en cours de couverture avec nouveaux tests wizard
