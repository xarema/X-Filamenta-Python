# Commandes Pour Tuer Les Serveurs

**Stocké dans:** `.github/SERVER_KILL_COMMANDS.md`

---

## PowerShell - Tuer Tous Les Serveurs Python

### Option 1: Tous les processus python.exe

```powershell
Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
```

### Option 2: Tous les processus Python (any variant)

```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue
```

### Option 3: Tuer par port (si vous connaissez le port)

```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Exemple: Si port 5000 est utilisé:
```powershell
netstat -ano | findstr :5000
# Output: TCP 127.0.0.1:5000 ... LISTENING PID=1234
taskkill /PID 1234 /F
```

### Option 4: One-liner complet (tous les serveurs)

```powershell
Get-Process python.exe, waitress -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue ; Write-Host "All servers killed"
```

---

## CMD (Command Prompt classique)

### Tuer par port 5000

```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## Bash / Linux / WSL

```bash
# Tuer tous les processus Python
pkill -f python

# Tuer par port
lsof -i :5000
kill -9 <PID>
```

---

## Verification - Confirmer que serveur est arrete

```powershell
# Verifier qu'aucun processus Python ne tourne
Get-Process python.exe -ErrorAction SilentlyContinue | Measure-Object

# Verifier le port 5000 est libre
netstat -ano | findstr :5000
# Si rien ne s'affiche = port libre OK
```

---

## Problemes Courants

### Port toujours occupe après kill

```powershell
# Wait 2 secondes et re-check
Start-Sleep -Seconds 2
netstat -ano | findstr :5000
```

### Processus "zombie"

```powershell
# Forcer plus agressif
Get-Process python.exe | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Get-Process python.exe -ErrorAction SilentlyContinue
```

---

## Quick Reference

| Commande | Usage |
|----------|-------|
| `Get-Process python.exe \| Stop-Process -Force` | Tuer tous les python.exe |
| `netstat -ano \| findstr :5000` | Voir quel processus utilise port 5000 |
| `taskkill /PID <PID> /F` | Tuer processus par PID |
| `pkill -f python` | Linux/WSL: Tuer tous les Python |

---

## Alias PowerShell (optionnel)

Ajouter a votre profil PowerShell pour rapide access:

```powershell
# $PROFILE -> Ouvrir fichier profil
function Kill-Servers {
    Get-Process python.exe, waitress -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "All servers killed"
}

# Utiliser:
# Kill-Servers
```

---

**Last Updated:** 2025-12-28
**License:** AGPL-3.0-or-later

