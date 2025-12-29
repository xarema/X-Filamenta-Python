# Règles obligatoires AVANT toute modification de routes

**Objectif :** Éviter de réintroduire des routes déjà défaillantes et réduire les régressions.

---
## 1) Processus obligatoire
1. **STOP processus** : tuer tous les `python.exe` avant d’éditer (voir commandes ci-dessous).
2. **Lire ce fichier** avant chaque changement de route.
3. **Consigner** toute route cassée (nom d’endpoint ou URL) et ne plus la réutiliser tant qu’un correctif n’est pas validé.
4. **Relire les règles projet** (`.github/copilot-instructions.md`, `.github/USER_PREFERENCES.md`, `.github/SERVER_KILL_COMMANDS.md`) avant de toucher au code.

---
## 2) Routes à ne plus réutiliser (historique incidents)
- (ajouter ici chaque route/endpoint problématique avec la date et le symptôme)

| Date | Route / Endpoint | Symptom | Action décidée |
|------|------------------|---------|----------------|
| (à compléter) | | | |

---
## 3) Checklist avant modification d’une route
- [ ] Processus Python arrêtés (`python.exe`).
- [ ] Ce fichier relu.
- [ ] Règles projet relues : `.github/copilot-instructions.md`, `.github/USER_PREFERENCES.md`, `.github/SERVER_KILL_COMMANDS.md`.
- [ ] Route/endpoint à modifier n’est pas listé comme cassé ci-dessus.
- [ ] Plan de changement clair (ce qui change, pourquoi, test prévu).

---
## 4) Commandes utiles (PowerShell)
```powershell
# Tuer tous les Python
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Vérifier port 5000 libre
netstat -ano | findstr :5000
```

---
## 5) Rappels essentiels
- Ne jamais réutiliser une route consignée comme défaillante sans analyse/correctif validé.
- Toujours tester après modification (lancer serveur + vérif navigateur/logs).
- Pas de changement de route sans relire les règles projet.

---
**Dernière mise à jour :** 2025-12-28

