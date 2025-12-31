"""
Purpose: Questions clarifications Phase 2 — Configuration Cache Multi-Environnement
Description: Questions détaillées avec exemples UI/UX pour validation avant implémentation Phase 2

File: Analysis_reports/2025-12-29_PHASE2_QUESTIONS_VALIDATION.md | Repository: X-Filamenta-Python
Created: 2025-12-29T18:00:00+00:00

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal
Notes:
- Questions à valider avant démarrer Phase 2
- Exemples UI/UX inclus pour chaque question
"""

# ❓ QUESTIONS CLARIFICATIONS PHASE 2 — CACHE

**Date:** 2025-12-29  
**Contexte:** Configuration cache adaptatif multi-environnement (cPanel + VPS + Docker + Prod)  
**Besoin:** LiteSpeed Redis disponible sur hébergement mutualisé cPanel

---

## 📋 QUESTIONS À VALIDER

### Q1 — Détection Redis dans Wizard

**Question:** Comment détecter LiteSpeed Redis cPanel ?

**Options:**

**A) Tester connexion Redis standard (localhost:6379)**
- Simple à implémenter
- Fonctionne pour la plupart des cas
- Peut échouer si port personnalisé

**B) Détecter LiteSpeed spécifiquement via variables env**
- Plus précis
- Complexe (dépend config hébergeur)
- Peut ne pas fonctionner sur tous hébergeurs

**C) Permettre utilisateur de saisir manuellement host/port Redis** ⭐ **RECOMMANDÉ**
- Flexible
- Utilisateur connaît sa config hébergeur
- Fonctionne partout

**Proposition UI Wizard:**

```
┌─────────────────────────────────────────────────────────┐
│ ÉTAPE 4: Configuration Cache                            │
└─────────────────────────────────────────────────────────┘

Cache Backend Détecté: Filesystem (par défaut)

Redis disponible sur votre hébergeur ?
  
  ○ Non, utiliser Filesystem (recommandé pour commencer)
  ● Oui, je veux configurer Redis maintenant
  
Si Oui:
  
  Configuration Redis:
  ┌─────────────────────────────────────────────────┐
  │ Host Redis:  [localhost                    ] │
  │ Port Redis:  [6379                         ] │
  │ Password:    [•••••••••••                  ] │ (optionnel)
  │ Database:    [0                            ] │
  └─────────────────────────────────────────────────┘
  
  [Tester Connexion]
  
  Status: ⏳ Cliquez "Tester Connexion" pour vérifier
  
  
Note: Vous pourrez activer Redis plus tard dans 
      Paramètres Admin > Cache si vous choisissez Filesystem.

[Documentation Redis cPanel ↗]

[← Retour]  [Continuer →]
```

**Réponse attendue:** A / B / C / Autre

---

### Q2 — Migration Cache Filesystem → Redis

**Question:** Faut-il migrer automatiquement les données cache lors du switch Filesystem → Redis ?

**Options:**

**A) Migration automatique (copier cache Filesystem → Redis)**
- Complexe à implémenter
- Risque d'erreurs si structures différentes
- Lent si beaucoup de données

**B) Flush cache lors du switch (recommandé)** ⭐
- Simple et sûr
- Cache se reconstruit rapidement (queries auto-cache)
- Pas de risque de corruption

**C) Laisser les 2 coexister temporairement**
- Confus pour utilisateur
- Risque incohérence données
- Compliqué à gérer

**Proposition UI Admin:**

```
┌─────────────────────────────────────────────────────────┐
│ Changer Backend Cache                                   │
└─────────────────────────────────────────────────────────┘

Backend Actuel: Filesystem

Nouveau Backend:
  ○ Filesystem
  ● Redis
  ○ Auto-détection

⚠️ ATTENTION
Changer de backend vide automatiquement le cache.
Le cache se reconstruira progressivement lors des prochaines requêtes.

Statistiques actuelles:
  - Entrées cache: 1,245
  - Taille totale: 12.3 MB
  - Hit rate: 68.5%

Ces données seront perdues. Continuer ?

[Annuler]  [Confirmer et Vider Cache]
```

**Réponse attendue:** A / B / C / Autre

---

### Q3 — Documentation Redis cPanel

**Question:** Quel niveau de détail pour la documentation Redis cPanel ?

**Options:**

**A) Guide court (5 étapes)**
- Rapide à lire
- Basique
- Peut manquer détails

**B) Guide complet avec screenshots cPanel** ⭐ **RECOMMANDÉ**
- Détaillé
- Visuel (screenshots)
- Couvre troubleshooting

**C) Guide + vidéo tutorial**
- Très complet
- Prend du temps à créer
- Peut devenir obsolète

**Proposition Contenu Guide (Option B):**

```markdown
# Activer Redis sur cPanel LiteSpeed

## Prérequis
- Hébergement cPanel avec Redis disponible
- Accès administrateur cPanel

## Étapes d'activation

### 1. Se connecter à cPanel
- URL: https://votre-domaine.com:2083
- Login avec vos identifiants hébergeur

[Screenshot: Page login cPanel]

### 2. Trouver Redis
- Dans la barre de recherche, tapez "Redis"
- Ou: Section "Software" > "Redis Manager"

[Screenshot: Recherche Redis dans cPanel]

### 3. Activer Redis
- Cliquer sur "Enable Redis"
- Noter les informations affichées:
  - Host: localhost (ou adresse IP affichée)
  - Port: 6379 (port par défaut)
  - Password: (si configuré par hébergeur)

[Screenshot: Redis activé avec credentials]

### 4. Configurer X-Filamenta
- Se connecter à votre installation X-Filamenta
- Aller dans: Admin > Paramètres > Cache
- Sélectionner "Redis" comme backend
- Saisir les credentials notés à l'étape 3
- Cliquer "Tester Connexion"
- Si OK, cliquer "Sauvegarder Configuration"

[Screenshot: Page admin cache X-Filamenta]

### 5. Vérifier le fonctionnement
- Les statistiques cache doivent afficher un hit rate
- Performance devrait s'améliorer (pages plus rapides)

## Troubleshooting

**Connexion refusée (Connection refused)**
- Vérifier que Redis est bien activé dans cPanel
- Contacter hébergeur si problème persiste

**Authentication failed**
- Vérifier le password saisi
- Certains hébergeurs n'utilisent pas de password (laisser vide)

**Port bloqué**
- Vérifier le port (peut être différent de 6379)
- Contacter support hébergeur pour confirmer port Redis

**Performance pas améliorée**
- Vérifier dans Admin > Cache que backend = Redis
- Vider le cache et laisser se reconstruire (24h)
- Vérifier hit rate > 50%

## Support
- Documentation X-Filamenta: [lien]
- Support hébergeur: [contact hébergeur]
```

**Réponse attendue:** A / B / C / Autre

---

### Q4 — UI Admin Cache Settings

**Question:** Où placer la configuration cache dans le menu Admin ?

**Options:**

**A) Dans "Paramètres Système" (existant)**
- Regroupé avec autres paramètres
- Pas de nouvelle page
- Peut être surchargé

**B) Nouvelle page "Paramètres Cache" (dédiée)** ⭐ **RECOMMANDÉ**
- Claire et organisée
- Espace pour stats cache
- Meilleure UX

**C) Dans "Paramètres Avancés" (nouvelle section)**
- Séparé du reste
- Pour utilisateurs experts
- Moins accessible

**Proposition Menu Admin (Option B):**

```
┌─────────────────────────────────────────────────────────┐
│ Menu Admin                                              │
└─────────────────────────────────────────────────────────┘

📊 Tableau de bord
👥 Utilisateurs
📧 Paramètres Couriel
🗄️  Paramètres Cache          ← NOUVELLE PAGE ICI
⚙️  Paramètres Système
🔒 Paramètres Sécurité
📋 Logs
💾 Sauvegarde
🔄 Mise à jour
```

**Proposition Page "Paramètres Cache":**

```
┌─────────────────────────────────────────────────────────┐
│ Paramètres Cache                                        │
└─────────────────────────────────────────────────────────┘

Backend Actuel: Filesystem

┌─────────────────────────────────────────────────────────┐
│ Configuration Backend                                   │
└─────────────────────────────────────────────────────────┘

Choisir Backend:
  ○ Filesystem (Compatible cPanel, performance moyenne)
  ○ Redis (Performance optimale, nécessite Redis installé)
  ● Auto-détection (Essaie Redis, sinon Filesystem)

--- Configuration Redis ---

Host:     [localhost                              ]
Port:     [6379                                   ]
Password: [•••••••••                              ] (optionnel)
Database: [0                                      ]

[Tester Connexion]

Status: ✅ Connexion Redis réussie (v7.0.0, 1.2 MB utilisé)

[Sauvegarder Configuration]

┌─────────────────────────────────────────────────────────┐
│ Statistiques Cache (7 derniers jours)                   │
└─────────────────────────────────────────────────────────┘

Hit Rate:       68.5% ████████████████░░░░░░░░
Hits:           2,705
Misses:         1,245
Total Queries:  3,950
Taille Cache:   12.3 MB
Entrées:        1,245 clés

Top 5 clés les plus accédées:
  1. settings:all (245 hits)
  2. user:123 (189 hits)
  3. content:list:page1 (156 hits)
  4. settings:smtp_host (134 hits)
  5. user:456 (98 hits)

┌─────────────────────────────────────────────────────────┐
│ Actions                                                 │
└─────────────────────────────────────────────────────────┘

[Vider le Cache Complet]
[Vider Cache Settings uniquement]
[Vider Cache Users uniquement]

⚠️ Vider le cache peut ralentir temporairement l'application
    (le cache se reconstruit progressivement)

┌─────────────────────────────────────────────────────────┐
│ Documentation                                           │
└─────────────────────────────────────────────────────────┘

[Guide Activation Redis cPanel ↗]
[Guide Migration Filesystem → Redis ↗]
[Architecture Cache ↗]
```

**Réponse attendue:** A / B / C / Autre

---

### Q5 — Stockage Config Redis

**Question:** Où stocker les credentials Redis (host, port, password) ?

**Options:**

**A) Settings table (chiffré Fernet)** ⭐ **RECOMMANDÉ**
- Sécurisé (chiffrement)
- Déjà implémenté en Phase 1
- Modifiable via UI Admin

**B) Fichier .env**
- Simple
- Moins sécurisé (texte clair)
- Pas modifiable via UI

**C) Fichier config séparé (config/cache.json)**
- Flexible
- Complexe à gérer
- Risque d'erreurs

**Proposition Settings (Option A):**

```python
# backend/src/models/settings.py - Clés ajoutées

DEFAULTS = {
    # ...existing...
    
    # Cache Configuration (NEW)
    "cache_backend": {
        "value": "auto",  # ou: redis, filesystem, memory
        "type": "enum",
        "description": "Backend cache: auto, redis, filesystem, memory",
    },
    "redis_host": {
        "value": "localhost",
        "type": "string",
        "description": "Redis server hostname (encrypted)",
    },
    "redis_port": {
        "value": "6379",
        "type": "integer",
        "description": "Redis server port",
    },
    "redis_password": {
        "value": "",
        "type": "string",
        "description": "Redis password (encrypted)",
    },
    "redis_db": {
        "value": "0",
        "type": "integer",
        "description": "Redis database number",
    },
    "cache_default_ttl": {
        "value": "300",
        "type": "integer",
        "description": "Default cache TTL in seconds (5 min)",
    },
}

# Ajout à ENCRYPTED_FIELDS
ENCRYPTED_FIELDS = [
    "smtp_password",
    "smtp_user",
    "sendgrid_api_key",
    "redis_host",      # NEW - chiffré
    "redis_password",  # NEW - chiffré
]
```

**Réponse attendue:** A / B / C / Autre

---

### Q6 — Test Connexion Redis

**Question:** Comment implémenter le test de connexion Redis (bouton "Tester Connexion") ?

**Options:**

**A) Test simple (ping)**
- Rapide
- Vérifie juste connexion
- Pas de détails

**B) Test complet (ping + info)** ⭐ **RECOMMANDÉ**
- Vérifie connexion
- Retourne version Redis, mémoire utilisée
- Utile pour debug

**C) Test avec écriture/lecture**
- Très complet
- Vérifie permissions
- Plus lent

**Proposition Implémentation (Option B):**

```python
# backend/src/routes/admin_cache.py

@admin.route("/cache/test-redis", methods=["POST"])
@require_admin
def test_redis_connection():
    """
    Test Redis connection (AJAX endpoint).
    
    Expected JSON:
        {
            "host": "localhost",
            "port": 6379,
            "password": "secret",
            "db": 0
        }
    
    Returns:
        JSON with success status, message, and Redis info
    """
    try:
        data = request.get_json()
        
        import redis
        r = redis.Redis(
            host=data.get("host", "localhost"),
            port=int(data.get("port", 6379)),
            password=data.get("password", None) or None,
            db=int(data.get("db", 0)),
            socket_connect_timeout=5,
            decode_responses=True
        )
        
        # Test ping
        r.ping()
        
        # Get info
        info = r.info()
        
        return jsonify({
            "success": True,
            "message": "✅ Connexion Redis réussie",
            "info": {
                "version": info.get("redis_version", "unknown"),
                "memory_used": f"{info.get('used_memory_human', '0')}",
                "uptime_days": info.get("uptime_in_days", 0),
                "connected_clients": info.get("connected_clients", 0)
            }
        })
        
    except redis.ConnectionError as e:
        return jsonify({
            "success": False,
            "message": f"❌ Erreur connexion: {str(e)}",
            "help": "Vérifiez que Redis est actif et accessible sur ce host/port"
        }), 200
        
    except redis.AuthenticationError:
        return jsonify({
            "success": False,
            "message": "❌ Erreur authentification: Password incorrect",
            "help": "Vérifiez le password Redis"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Erreur: {str(e)}",
            "help": "Vérifiez la configuration"
        }), 200
```

**Proposition UI Retour (AJAX):**

```javascript
// frontend/templates/admin/settings_cache.html

document.getElementById('testRedisBtn').addEventListener('click', function() {
  const btn = this;
  const resultDiv = document.getElementById('redisTestResult');
  
  // Récupérer config
  const config = {
    host: document.getElementById('redisHost').value,
    port: document.getElementById('redisPort').value,
    password: document.getElementById('redisPassword').value,
    db: document.getElementById('redisDb').value
  };
  
  // Disable button
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Test en cours...';
  
  // AJAX call
  fetch('/admin/cache/test-redis', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(config)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      resultDiv.innerHTML = `
        <div class="alert alert-success">
          <strong>${data.message}</strong><br>
          Version: ${data.info.version}<br>
          Mémoire: ${data.info.memory_used}<br>
          Uptime: ${data.info.uptime_days} jours<br>
          Clients: ${data.info.connected_clients}
        </div>
      `;
    } else {
      resultDiv.innerHTML = `
        <div class="alert alert-danger">
          <strong>${data.message}</strong><br>
          <small>${data.help}</small>
        </div>
      `;
    }
  })
  .catch(error => {
    resultDiv.innerHTML = `
      <div class="alert alert-danger">
        Erreur réseau: ${error}
      </div>
    `;
  })
  .finally(() => {
    btn.disabled = false;
    btn.innerHTML = 'Tester Connexion';
  });
});
```

**Réponse attendue:** A / B / C / Autre

---

### Q7 — Wizard Flow avec Étape Cache

**Question:** Où insérer l'étape "Configuration Cache" dans le wizard ?

**Options:**

**A) Après Base de données, avant Upload backup**
- Logique (config technique groupée)
- Utilisateur peut skip si pas Redis

**B) Après Compte admin, avant Terminé** ⭐ **RECOMMANDÉ**
- Optionnel (app fonctionne sans)
- Moins intimidant pour débutants

**C) Étape optionnelle (bouton "Avancé")**
- Pas dans flow principal
- Pour utilisateurs experts
- Peut être oublié

**Proposition Flow Wizard (Option B):**

```
Wizard Flow Complet:

1. 🌍 Sélection Langue
   └─ Choisir: Français | English | Español

2. ✅ Vérification Prérequis
   └─ Python, BD, Permissions, [Redis détecté ?]

3. 🗄️  Configuration Base de Données
   └─ Type: SQLite | MySQL | PostgreSQL
   └─ Credentials + Test connexion

4. 📦 Upload Backup (Optionnel)
   └─ Restaurer backup .tar.gz ou nouvelle install

5. 👤 Création Compte Admin
   └─ Username, Email, Password

6. 🚀 Configuration Cache (NEW - Optionnel)
   └─ Backend: Filesystem | Redis | Auto
   └─ Si Redis: Credentials + Test

7. ✅ Installation Terminée
   └─ Résumé + Lien login
```

**Proposition UI Étape Cache:**

```
┌─────────────────────────────────────────────────────────┐
│ ÉTAPE 6/7: Configuration Cache (Optionnel)              │
└─────────────────────────────────────────────────────────┘

Performance & Cache

X-Filamenta utilise un système de cache pour améliorer les
performances. Vous pouvez configurer le cache maintenant ou
plus tard dans les paramètres admin.

Backend Cache:
  ● Filesystem (Recommandé - Compatible tous hébergements)
    └─ Performance: ⭐⭐⭐
    └─ Aucune configuration requise
    
  ○ Redis (Performance optimale)
    └─ Performance: ⭐⭐⭐⭐⭐
    └─ Nécessite Redis installé sur serveur
    
  ○ Auto-détection (Essaie Redis, sinon Filesystem)


--- Configuration Redis (si sélectionné) ---

Host:     [localhost]
Port:     [6379]
Password: [        ] (optionnel)

[Tester Connexion]

Status: ⏳ Cliquez pour tester


💡 Conseil: Si vous n'êtes pas sûr, choisissez "Filesystem".
   Vous pourrez activer Redis plus tard dans Admin > Paramètres > Cache.

[Passer cette étape]  [← Retour]  [Continuer →]
```

**Réponse attendue:** A / B / C / Autre

---

### Q8 — TTL Cache par Entité

**Question:** Comment configurer les TTL (durée de vie) du cache ?

**Options:**

**A) TTL global unique (ex: 5 min pour tout)**
- Simple
- Pas flexible
- Pas optimal

**B) TTL par entité (Settings 10min, Users 5min, Content 2min)** ⭐ **RECOMMANDÉ**
- Optimal
- Flexible
- Configurable

**C) TTL dynamique (basé sur fréquence accès)**
- Très intelligent
- Complexe à implémenter
- Peut être instable

**Proposition Configuration (Option B):**

```python
# backend/src/models/settings.py

DEFAULTS = {
    # ...existing...
    
    # Cache TTL par entité (NEW)
    "cache_ttl_settings": {
        "value": "600",  # 10 minutes
        "type": "integer",
        "description": "TTL cache Settings (secondes)",
    },
    "cache_ttl_users": {
        "value": "300",  # 5 minutes
        "type": "integer",
        "description": "TTL cache Users (secondes)",
    },
    "cache_ttl_content": {
        "value": "120",  # 2 minutes
        "type": "integer",
        "description": "TTL cache Content (secondes)",
    },
    "cache_ttl_sessions": {
        "value": "3600",  # 1 heure
        "type": "integer",
        "description": "TTL cache Sessions (secondes)",
    },
}
```

**Proposition UI Admin:**

```
┌─────────────────────────────────────────────────────────┐
│ Configuration Avancée Cache                             │
└─────────────────────────────────────────────────────────┘

Durée de Vie (TTL) par Type de Données:

Settings:  [600  ] secondes (10 minutes)
           └─ Données rarement modifiées

Users:     [300  ] secondes (5 minutes)
           └─ Données modifiées occasionnellement

Content:   [120  ] secondes (2 minutes)
           └─ Données fréquemment modifiées

Sessions:  [3600 ] secondes (1 heure)
           └─ Durée connexion utilisateur

💡 Augmenter les TTL améliore les performances mais peut
   afficher des données légèrement obsolètes.

[Restaurer Défauts]  [Sauvegarder]
```

**Réponse attendue:** A / B / C / Autre

---

## 📝 RÉSUMÉ QUESTIONS

| # | Question | Recommandation |
|---|----------|----------------|
| Q1 | Détection Redis | C) Saisie manuelle |
| Q2 | Migration cache | B) Flush automatique |
| Q3 | Documentation | B) Guide complet + screenshots |
| Q4 | UI Admin | B) Page dédiée Cache |
| Q5 | Stockage config | A) Settings chiffré |
| Q6 | Test connexion | B) Ping + info Redis |
| Q7 | Étape wizard | B) Après admin, optionnel |
| Q8 | TTL cache | B) Par entité configurable |

---

## ✅ VALIDATION REQUISE

**Pour chaque question Q1-Q8, réponds:**
- ✅ **OK** — Approuve la recommandation
- 🔄 **MODIF [lettre]** — Choisis autre option (A/B/C)
- ❓ **QUESTION** — Besoin clarification

**Exemple réponse:**
```
Q1: OK
Q2: OK
Q3: MODIF A (guide court suffit)
Q4: OK
Q5: OK
Q6: MODIF A (ping simple)
Q7: QUESTION (où exactement dans flow ?)
Q8: OK
```

---

**Attends tes réponses Q1-Q8 avant de démarrer Phase 2 !** 🚀

