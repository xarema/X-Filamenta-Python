# Guide Déploiement avec Cache — X-Filamenta

**Version:** 0.1.0-Beta  
**Date:** 2025-12-29  
**Auteur:** AleGabMar

---

## 📋 Table des Matières

1. [Aperçu](#aperçu)
2. [Configuration par Environnement](#configuration-par-environnement)
3. [Installation Redis](#installation-redis)
4. [Configuration Cache](#configuration-cache)
5. [Vérification Performance](#vérification-performance)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Aperçu

X-Filamenta supporte **3 backends de cache** qui s'auto-détectent :

| Backend | Usage | Performance | Environnement |
|---------|-------|-------------|---------------|
| **Redis** | Production optimal | ⭐⭐⭐⭐⭐ | VPS, Docker |
| **Filesystem** | cPanel/Shared | ⭐⭐⭐ | Hébergement mutualisé |
| **Memory** | Development | ⭐⭐ | Local uniquement |

**Auto-détection :**
- Le wizard teste Redis au démarrage
- Fallback automatique vers Filesystem si Redis indisponible
- Configuration modifiable dans Admin > Cache

---

## 🌍 Configuration par Environnement

### 1️⃣ Développement Local

**Backend:** Memory (par défaut)

```bash
# .env
FLASK_DEBUG=True
# Pas de Redis nécessaire
```

**Caractéristiques :**
- Cache en RAM (perdu au redémarrage)
- Pas de configuration requise
- Idéal pour développement

---

### 2️⃣ cPanel / Hébergement Mutualisé

**Backend:** Filesystem (ou Redis si disponible)

#### Option A: Filesystem (par défaut)

```bash
# .env
DEPLOYMENT_TARGET=cpanel

# Cache automatiquement en instance/cache/
```

**Avantages :**
- ✅ Fonctionne partout (aucune dépendance)
- ✅ Pas de configuration Redis
- ✅ Performance acceptable (< 100 utilisateurs)

**Performance :**
- ~3-5ms par opération cache
- Bon pour sites moyens trafic

#### Option B: Redis (si hébergeur le propose)

Certains hébergeurs cPanel proposent Redis :
- **LiteSpeed Redis** (via configuration panel)
- **Redis Cloud** (module cPanel)

**Configuration :**

1. Activer Redis dans cPanel
2. Noter host/port/password (souvent panel → Redis)
3. Configurer dans wizard ou Admin > Cache

```bash
# Configuration Redis cPanel typique
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<fourni par hébergeur>
REDIS_DB=0
```

**Documentation hébergeur :**
- Hostinger: https://support.hostinger.com/en/articles/redis
- SiteGround: Panel → Speed → Redis
- A2 Hosting: cPanel → Redis Manager

---

### 3️⃣ VPS (Linux)

**Backend:** Redis (recommandé)

#### Installation Redis

**Ubuntu/Debian :**
```bash
sudo apt update
sudo apt install redis-server -y

# Vérifier statut
sudo systemctl status redis-server

# Démarrer si nécessaire
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**CentOS/RHEL :**
```bash
sudo yum install redis -y
sudo systemctl start redis
sudo systemctl enable redis
```

#### Sécurisation Redis

**Fichier:** `/etc/redis/redis.conf`

```conf
# Bind localhost uniquement (pas d'accès externe)
bind 127.0.0.1 ::1

# Mot de passe (recommandé production)
requirepass VotreMdpSecureIci123!

# Persistence (optionnel, pour sessions)
save 900 1
save 300 10
```

**Redémarrer :**
```bash
sudo systemctl restart redis-server
```

#### Configuration X-Filamenta

```bash
# .env
DEPLOYMENT_TARGET=vps

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=VotreMdpSecureIci123!
REDIS_DB=0
```

**Vérifier connexion :**
```bash
redis-cli ping
# PONG

# Avec password
redis-cli -a VotreMdpSecureIci123! ping
```

---

### 4️⃣ Docker

**Backend:** Redis (container séparé)

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass YourPassword123!
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

**Variables environnement :**
```bash
# .env
DEPLOYMENT_TARGET=docker

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=YourPassword123!
REDIS_DB=0
```

---

## ⚙️ Configuration Cache

### Via Installation Wizard

**Étape 2 - Prérequis :**
- Auto-détection Redis
- Affiche version si trouvé

**Étape 6 - Configuration Cache :**

1. **Si Redis détecté :**
   - ✅ Redis recommandé (pré-sélectionné)
   - Option Filesystem disponible

2. **Si Redis non détecté :**
   - ✅ Filesystem par défaut
   - Option configuration Redis manuelle :
     - Host (localhost)
     - Port (6379)
     - Password (optionnel)
     - Database (0-15)

3. **Test connexion :**
   - Simple: Ping Redis
   - Avancé: Write/Read test

4. **Fallback automatique :**
   - Si test échoue → Filesystem

### Via Admin Panel

**Admin > Cache :**

- Voir backend actuel
- Statistiques cache
- Test connexion Redis
- Clear cache
- Changer configuration

---

## 📊 Vérification Performance

### 1. Test Cache Manuel

**Script Python :**
```python
from backend.src.services.cache_service import cache_service

# Test get/set
cache_service.set('test_key', 'test_value', ttl=60)
value = cache_service.get('test_key')
print(f"Cache works: {value == 'test_value'}")

# Infos
info = cache_service.get_info()
print(f"Backend: {info['backend']}")
```

### 2. Load Test

**Exécuter :**
```bash
# Démarrer serveur prod
.\.venv\Scripts\python.exe run_prod.py

# Autre terminal
.\.venv\Scripts\python.exe .dev_scripts\test_scripts\load_test.py http://localhost:5000 100 10
```

**Résultats attendus :**

| Métrique | Sans cache | Avec cache | Amélioration |
|----------|------------|------------|--------------|
| P50 | 80ms | 25ms | -69% |
| P95 | 250ms | 60ms | -76% |
| Req/sec | 50 | 120 | +140% |

### 3. Vérifier Cache Hit Rate

**Logs Flask :**
```bash
# Activer debug cache
SQLALCHEMY_ECHO=True

# Observer queries répétées
# Avec cache: 1 query
# Sans cache: N queries (N+1 problem)
```

---

## 🔧 Troubleshooting

### Redis ne démarre pas

**Vérifier status :**
```bash
sudo systemctl status redis-server
```

**Logs :**
```bash
sudo tail -f /var/log/redis/redis-server.log
```

**Port déjà utilisé :**
```bash
sudo netstat -tulpn | grep 6379
# Tuer processus
sudo kill <PID>
```

### Connection Refused

**Firewall :**
```bash
# Ubuntu UFW
sudo ufw allow 6379/tcp

# CentOS firewalld
sudo firewall-cmd --add-port=6379/tcp --permanent
sudo firewall-cmd --reload
```

**Bind address :**
```conf
# /etc/redis/redis.conf
bind 127.0.0.1 ::1  # Localhost uniquement
# OU
bind 0.0.0.0  # Tous (DANGER: sécuriser avec password!)
```

### Permission Denied

**User Redis :**
```bash
sudo chown -R redis:redis /var/lib/redis
sudo chmod 750 /var/lib/redis
```

### Cache ne fonctionne pas

**Vérifier backend :**
```python
from backend.src.services.cache_service import cache_service
print(cache_service.backend)  # Doit être REDIS
```

**Force Filesystem :**
```bash
# .env
CACHE_TYPE=filesystem
```

**Clear cache :**
```bash
# Admin > Cache > Clear All
# OU
redis-cli FLUSHDB
```

---

## 📈 Optimisations Avancées

### Redis Persistence

**RDB (snapshots) :**
```conf
save 900 1    # Snapshot si 1 change en 15min
save 300 10   # Snapshot si 10 changes en 5min
save 60 10000 # Snapshot si 10k changes en 1min
```

**AOF (append-only) :**
```conf
appendonly yes
appendfsync everysec  # Sync toutes les secondes
```

### Redis Memory Limit

```conf
maxmemory 256mb
maxmemory-policy allkeys-lru  # Éviction LRU
```

### Monitoring Redis

**redis-cli :**
```bash
redis-cli INFO stats
redis-cli INFO memory
redis-cli MONITOR  # Real-time commands
```

**Outils externes :**
- RedisInsight (GUI officiel)
- redis-commander (web UI)

---

## ✅ Checklist Production

- [ ] Redis installé et sécurisé (password)
- [ ] Firewall configuré (localhost ou VPN)
- [ ] Persistence activée (RDB ou AOF)
- [ ] Memory limit configuré
- [ ] Monitoring actif
- [ ] Backup Redis configuré
- [ ] Tests load validés (> 100 req/sec)
- [ ] Cache hit rate > 85%

---

**Documentation:** docs/deployment_cache.md  
**Support:** https://github.com/XAREMA/X-Filamenta-Python/issues  
**Version:** 0.1.0-Beta

