"""
Purpose: Plan Phase 2 adapté multi-environnement (cPanel, VPS, Docker, Prod)
Description: Solution cache adaptative selon environnement avec fallback

File: Analysis_reports/2025-12-29_PHASE2_MULTI_ENV_STRATEGY.md | Repository: X-Filamenta-Python
Created: 2025-12-29T17:30:00+00:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
"""

# 🚀 PHASE 2 — STRATÉGIE MULTI-ENVIRONNEMENT

**Date:** 2025-12-29  
**Problème:** Redis non compatible cPanel mutualisé  
**Solution:** Architecture cache adaptative avec fallback

---

## ⚠️ CONTRAINTES IDENTIFIÉES

### Environnements cibles
1. **cPanel Mutualisé** — Aucun Redis possible
2. **VPS** — Redis possible (SSH + root)
3. **Docker** — Redis intégré (docker-compose)
4. **Prod interne** — Redis dédié

### Limites cPanel
- ❌ Pas d'accès SSH/root
- ❌ Pas de services système personnalisés
- ❌ Ports réseau bloqués (6379)
- ✅ Python + filesystem access
- ✅ SQLite + MySQL/PostgreSQL

---

## 🎯 SOLUTION PROPOSÉE — CACHE ADAPTATIVE

### Architecture 3-Tiers

```python
Cache Backend Selection (Auto-detect):

1. REDIS (Meilleur)
   └─ Si disponible: VPS, Docker, Prod interne
   └─ Performance: ⭐⭐⭐⭐⭐
   └─ Features: Complet (sessions, rate limit, cache)

2. FILESYSTEM (Moyen)
   └─ Si Redis indisponible: cPanel, développement
   └─ Performance: ⭐⭐⭐
   └─ Features: Cache queries (pas sessions distribuées)

3. MEMORY (Basique)
   └─ Fallback ultime: test, dev local
   └─ Performance: ⭐⭐
   └─ Features: Cache volatile (perdu au restart)
```

---

## 📦 IMPLÉMENTATION PROPOSÉE

### CacheService Auto-Adaptatif

```python
# backend/src/services/cache_service.py

from enum import Enum
import os

class CacheBackend(str, Enum):
    REDIS = "redis"
    FILESYSTEM = "filesystem"
    MEMORY = "memory"

class CacheService:
    def __init__(self):
        self.backend = self._detect_backend()
        self.client = self._init_client()
    
    def _detect_backend(self) -> CacheBackend:
        """Auto-detect best cache backend available"""
        
        # Try Redis first
        if self._redis_available():
            return CacheBackend.REDIS
        
        # Fallback to filesystem (cPanel compatible)
        if self._filesystem_writable():
            return CacheBackend.FILESYSTEM
        
        # Last resort: memory
        return CacheBackend.MEMORY
    
    def _redis_available(self) -> bool:
        """Check if Redis is available"""
        try:
            import redis
            r = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True
            )
            r.ping()
            return True
        except:
            return False
    
    def _filesystem_writable(self) -> bool:
        """Check if filesystem cache directory writable"""
        cache_dir = os.getenv("CACHE_DIR", "./cache")
        try:
            os.makedirs(cache_dir, exist_ok=True)
            test_file = os.path.join(cache_dir, ".test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            return False
    
    def _init_client(self):
        """Initialize cache client based on backend"""
        if self.backend == CacheBackend.REDIS:
            return self._init_redis()
        elif self.backend == CacheBackend.FILESYSTEM:
            return self._init_filesystem()
        else:
            return self._init_memory()
```

---

## 🔧 BACKENDS DÉTAILS

### 1️⃣ Redis Backend (VPS/Docker/Prod)

**Features:**
- ✅ Sessions distribuées (multi-instances)
- ✅ Rate limiting distribué
- ✅ Cache queries avec TTL
- ✅ Pub/Sub pour invalidation
- ✅ Performance maximale

**Configuration:**
```env
CACHE_BACKEND=redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

**Tests nécessaires:**
- Connection pooling
- Failover gracieux
- Reconnection automatique

---

### 2️⃣ Filesystem Backend (cPanel Compatible)

**Features:**
- ✅ Cache queries fichiers JSON
- ✅ Sessions fichiers (Flask-Session FileSystemSessionInterface)
- ⚠️ Rate limiting fichiers (moins performant)
- ❌ Pas multi-instances (sessions non partagées)
- ⭐ Performance correcte pour petit volume

**Configuration:**
```env
CACHE_BACKEND=filesystem
CACHE_DIR=./cache
SESSION_DIR=./sessions
```

**Implementation:**
```python
import json
import time
import hashlib
from pathlib import Path

class FilesystemCache:
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get(self, key: str):
        """Get cached value"""
        file_path = self._key_to_path(key)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Check expiry
            if data["expires_at"] < time.time():
                file_path.unlink()  # Delete expired
                return None
            
            return data["value"]
        except:
            return None
    
    def set(self, key: str, value, ttl: int = 300):
        """Set cached value with TTL"""
        file_path = self._key_to_path(key)
        
        data = {
            "value": value,
            "expires_at": time.time() + ttl
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f)
    
    def _key_to_path(self, key: str) -> Path:
        """Convert cache key to filesystem path"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
```

---

### 3️⃣ Memory Backend (Fallback)

**Features:**
- ✅ Cache queries en mémoire (dict)
- ✅ Sessions en mémoire (Flask default)
- ✅ Rate limiting en mémoire
- ❌ Perdu au restart
- ❌ Pas multi-instances

**Configuration:**
```env
CACHE_BACKEND=memory
```

**Implementation:** Built-in Flask caching

---

## 🎬 PLAN IMPLÉMENTATION PHASE 2

### Sprint 2.1 — Cache Adaptatif (5 jours)

**Jour 1-2: CacheService Multi-Backend**
- [ ] Créer `CacheService` avec auto-detection backend
- [ ] Implémenter Redis backend
- [ ] Implémenter Filesystem backend (cPanel)
- [ ] Implémenter Memory backend (fallback)
- [ ] Tests multi-backend

**Jour 3-4: Integration**
- [ ] Migrer sessions vers cache adaptatif
- [ ] Migrer rate limiting vers cache
- [ ] Cache queries Settings, Users
- [ ] Décorateur `@cached(ttl=300)`

**Jour 5: Tests & Documentation**
- [ ] Tests cPanel scenario (filesystem)
- [ ] Tests VPS scenario (Redis)
- [ ] Tests Docker scenario (Redis)
- [ ] Documentation deployment par env

---

### Sprint 2.2 — Optimisations (5 jours)

**Jour 1-2: DB Optimisations**
- [ ] Indexes (admin_history, content)
- [ ] Query optimizations
- [ ] Connection pooling

**Jour 3: Frontend Optimisations**
- [ ] Flask-Compress (gzip)
- [ ] Flask-Assets (minification)

**Jour 4-5: Load Testing**
- [ ] Locust scenarios
- [ ] Benchmarks 3 backends
- [ ] Rapport performance

---

## 📊 COMPARAISON BACKENDS

| Feature | Redis | Filesystem | Memory |
|---------|-------|------------|--------|
| **Environnement** | VPS/Docker/Prod | cPanel/Tous | Dev/Test |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Sessions distribuées** | ✅ OUI | ❌ NON | ❌ NON |
| **Rate limit distribué** | ✅ OUI | ⚠️ Partiel | ❌ NON |
| **Cache queries** | ✅ OUI | ✅ OUI | ✅ OUI |
| **Persistance restart** | ✅ OUI | ✅ OUI | ❌ NON |
| **Multi-instances** | ✅ OUI | ❌ NON | ❌ NON |
| **Installation** | Requis SSH | ✅ Aucune | ✅ Aucune |
| **cPanel compatible** | ❌ NON | ✅ OUI | ✅ OUI |

---

## 🎯 RÉSUMÉ SOLUTION

**Pour chaque environnement:**

### cPanel Mutualisé
```
Backend: Filesystem
Sessions: Fichiers
Cache: Fichiers JSON
Rate Limit: Fichiers (acceptable perf)
Multi-instance: Non supporté
```

### VPS (avec SSH)
```
Backend: Redis
Sessions: Redis
Cache: Redis
Rate Limit: Redis
Multi-instance: Supporté
```

### Docker
```
Backend: Redis (docker-compose)
Sessions: Redis
Cache: Redis
Rate Limit: Redis
Multi-instance: Supporté
```

### Prod Interne
```
Backend: Redis dédié
Sessions: Redis
Cache: Redis avec réplication
Rate Limit: Redis distribué
Multi-instance: Haute disponibilité
```

---

## ✅ AVANTAGES SOLUTION

1. **Compatibilité universelle** — Fonctionne partout
2. **Auto-detection** — Pas de config manuelle
3. **Performance adaptée** — Meilleur backend disponible
4. **Fallback gracieux** — Jamais de crash
5. **Migration facile** — Upgrade cPanel → VPS transparent

---

## 📝 CONFIGURATION ENV VARS

```env
# Cache Backend (auto si non spécifié)
CACHE_BACKEND=auto  # ou: redis, filesystem, memory

# Redis (si disponible)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Filesystem (cPanel)
CACHE_DIR=./cache
SESSION_DIR=./sessions

# Feature Flags
CACHE_ENABLED=true
SESSIONS_REDIS=auto  # utilise Redis si disponible
RATE_LIMIT_STORAGE=auto  # utilise meilleur disponible
```

---

## 🚀 PROCHAINES ÉTAPES

**Validation requise:**
1. ✅ Approuver architecture multi-backend ?
2. ✅ Approuver fallback filesystem pour cPanel ?
3. ✅ Approuver auto-detection backend ?

**Si approuvé, je commence:**
- Jour 1: CacheService multi-backend
- Jour 2: Tests 3 backends
- Jour 3: Integration sessions/rate limit
- Jour 4-5: DB optimizations
- Jour 6-7: Frontend optimizations
- Jour 8-10: Load testing

**Timeline:** 10 jours (2 semaines)

---

**Attends ta validation avant de démarrer !** 🚀

