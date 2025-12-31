# Scripts Utilitaires de Développement

**Dossier:** `.dev_scripts/utilities/`  
**Objectif:** Scripts PowerShell pour gérer le serveur de production en développement

---

## 📋 Scripts disponibles

### 1. `start_prod_with_logs.ps1`

**Description:** Démarre le serveur de production Waitress avec logs automatiques

**Actions:**
- ✅ Nettoie les processus Python existants
- ✅ Crée le dossier `logs/` si nécessaire
- ✅ Lance le serveur en arrière-plan
- ✅ Redirige stdout/stderr vers des fichiers de log
- ✅ Ouvre automatiquement le navigateur Edge

**Utilisation:**
```powershell
.\.dev_scripts\utilities\start_prod_with_logs.ps1
```

**Logs créés:**
- `logs/prod_server_YYYYMMDD_HHmmss.log` (stdout)
- `logs/prod_server_YYYYMMDD_HHmmss.log.err` (stderr + logs app)

---

### 2. `monitor_prod_logs.ps1`

**Description:** Affiche les logs du serveur en temps réel (tail -f)

**Actions:**
- ✅ Trouve automatiquement le dernier fichier de log
- ✅ Affiche les 50 dernières lignes
- ✅ Met à jour en temps réel (mode watch)

**Utilisation:**
```powershell
.\.dev_scripts\utilities\monitor_prod_logs.ps1
```

**Arrêt:** `Ctrl+C`

---

### 3. `stop_prod.ps1`

**Description:** Arrête proprement le serveur de production

**Actions:**
- ✅ Liste tous les processus Python actifs
- ✅ Arrête tous les processus Python
- ✅ Vérifie que le port 5000 est bien libéré

**Utilisation:**
```powershell
.\.dev_scripts\utilities\stop_prod.ps1
```

---

## 🚀 Workflow de test complet

### Démarrage
```powershell
# Terminal 1: Démarrer le serveur
.\.dev_scripts\utilities\start_prod_with_logs.ps1

# Terminal 2: Suivre les logs (optionnel)
.\.dev_scripts\utilities\monitor_prod_logs.ps1
```

### Test
- Le navigateur s'ouvre automatiquement sur `http://localhost:5000`
- Tester le wizard d'installation
- Observer les logs en temps réel dans Terminal 2

### Arrêt
```powershell
# Dans n'importe quel terminal
.\.dev_scripts\utilities\stop_prod.ps1
```

---

## 📊 Logs

**Emplacement:** `logs/`  
**Format:** `prod_server_YYYYMMDD_HHmmss.log(.err)`  
**Rotation:** Nouveau fichier à chaque démarrage

**Contenu des logs:**
- Démarrage de l'application Flask
- Configuration (sessions, cache, DB)
- Requêtes HTTP (GET/POST)
- Erreurs applicatives
- Messages Waitress

---

## 🛠️ Dépannage

### Serveur ne démarre pas
```powershell
# Vérifier les logs d'erreur
Get-Content logs\*.err | Select-Object -Last 20

# Vérifier les processus Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Nettoyer manuellement
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

### Port 5000 déjà utilisé
```powershell
# Trouver le processus utilisant le port
netstat -ano | Select-String "5000"

# Tuer le processus (remplacer PID par le numéro)
Stop-Process -Id PID -Force
```

### Environnement virtuel non activé
```powershell
# Ces scripts utilisent toujours le bon venv:
# D:\xarema\X-Filamenta-Python\.venv\Scripts\python.exe
# Pas besoin d'activer manuellement
```

---

## 📝 Notes

- **Windows uniquement** (PowerShell)
- **Pas d'émojis dans les logs** (règle projet)
- **Logs NOT versionnés** (voir `.gitignore`)
- Chemins absolus pour éviter les erreurs de path

---

**Dernière mise à jour:** 2025-12-29  
**Auteur:** AleGabMar / XAREMA  
**Licence:** AGPL-3.0-or-later

