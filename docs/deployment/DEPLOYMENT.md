<!--
Purpose: General deployment guide and platform comparison
Description: Overview of all deployment options for X-Filamenta-Python

File: DEPLOYMENT.md | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Git history is the source of truth for authorship and change tracking.
-->

# Guide de déploiement — X-Filamenta-Python

L'application X-Filamenta-Python peut être déployée sur **plusieurs plateformes** avec la même base de code. Choisissez la plateforme adaptée à vos besoins.

---

## 🎯 Comparaison des plateformes

| Critère         | cPanel         | VPS/Linux                 | Docker                    | Development    |
| --------------- | -------------- | ------------------------- | ------------------------- | -------------- |
| **Difficulté**  | ⭐⭐ Facile    | ⭐⭐⭐ Moyen              | ⭐⭐ Facile               | ⭐ Très facile |
| **Coût**        | 💰 Hébergement | 💰💰 Medium               | 💰💰 Medium               | 💰 Gratuit     |
| **Scalabilité** | ⚠️ Limité      | ✅ Oui                    | ✅✅ Excellente           | N/A            |
| **Maintenance** | ✅ Minimale    | ⚠️ Modérée                | ✅ Simple                 | N/A            |
| **Performance** | ⚠️ Acceptable  | ✅ Très bonne             | ✅✅ Excellent            | Faible         |
| **Support BD**  | SQLite, MySQL  | SQLite, MySQL, PostgreSQL | SQLite, MySQL, PostgreSQL | SQLite         |
| **HTTPS**       | ✅ AutoSSL     | ✅ Let's Encrypt          | ✅ Let's Encrypt          | ⚠️ Selfie      |
| **CI/CD**       | ❌ Non         | ✅ Possible               | ✅✅ Natif                | N/A            |

---

## 📋 Sélectionner la bonne plateforme

### 🏠 **cPanel** — Le plus simple pour débuter

**Recommandé si :**

- Tu as déjà un hébergement cPanel
- Tu veux la plus simple mise en place
- Tu n'as pas besoin de scaling horizontal
- Tu veux une maintenance minimale

**Avantages :**

- Interface graphique pour tout gérer
- SSL gratuit (AutoSSL)
- Base de données MySQL intégrée
- Support des applications Python natif

**Inconvénients :**

- Moins flexible que VPS
- Difficile de scaling
- Limité en ressources

**👉 [Guide complet cPanel](DEPLOYMENT_CPANEL.md)**

---

### 🖥️ **VPS/Linux** — Le meilleur compromis

**Recommandé si :**

- Tu veux plus de contrôle
- Tu envisages de scaler
- Tu as de l'expérience Linux
- Tu veux le meilleur rapport perf/prix

**Avantages :**

- Plein contrôle du serveur
- Support PostgreSQL, MySQL, SQLite
- Facile à scaler (load balancing)
- Excellente performance
- CI/CD intégré

**Inconvénients :**

- Requiert de l'expérience Linux
- Maintenance plus complexe
- Responsable de la sécurité

**👉 [Guide complet VPS/Linux](DEPLOYMENT_VPS.md)**

---

### 🐳 **Docker** — Le plus moderne

**Recommandé si :**

- Tu veux déployer partout (cloud, local, VPS)
- Tu aimes la containerization
- Tu veux un CI/CD automatisé
- Tu envisages une architecture microservices

**Avantages :**

- Même image partout (dev = prod)
- Facile à scaler et orchestrer
- Déploiement rapide et reproductible
- Compatible avec Kubernetes
- Multi-BD supportées

**Inconvénients :**

- Courbe d'apprentissage Docker
- Overhead mémoire (conteneurs)
- Configuration initiale plus complexe

**👉 [Guide complet Docker](DEPLOYMENT_DOCKER.md)**

---

### 💻 **Development** — Pour tester en local

**Recommandé si :**

- Tu développes sur ta machine locale
- Tu veux tester avant de déployer
- Tu apprends Flask/Python

**Setup rapide :**

```bash
# 1. Cloner le projet
git clone <repo> && cd X-Filamenta-Python

# 2. Créer l'environnement
python -m venv venv
source venv/bin/activate  # ou .venv\Scripts\Activate.ps1 sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# 4. Configurer (optionnel)
cp .env.example .env
nano .env

# 5. Lancer
python -m backend.src
# Accès: http://localhost:5000
```

---

## 🚀 Roadmap de déploiement

```
Phase 1: Development (mois 1-2)
  ├─ Développement local
  ├─ Tests unitaires/intégration
  └─ Git workflow établi

Phase 2: Testing & RC (mois 2-3)
  ├─ Docker pour staging
  ├─ Tests de performance
  ├─ cPanel OU VPS (choisis un)
  └─ Version RC-1.0.0

Phase 3: Production (mois 3+)
  ├─ Déploiement en production
  ├─ Monitoring & alertes
  ├─ Backup automatisé
  └─ Version 1.0.0

Phase 4: Scaling (selon besoins)
  ├─ Load balancing
  ├─ Cache (Redis)
  ├─ CDN pour static
  └─ Architecture microservices (si besoin)
```

---

## 📊 Configuration recommandée pour la RC

```yaml
# Pour la RC (test en production)
plateforme: Docker ou VPS
base_de_donnees: MySQL
ssl: Let's Encrypt (gratuit)
sauvegarde: Quotidienne
monitoring: Prometheus + Grafana
ci_cd: GitHub Actions

# Puis pour la version 1.0.0
ajouter: PostgreSQL comme option
load_balancer: Nginx
cache: Redis
cdn: CloudFlare ou similar
```

---

## 🔄 Migration entre plateformes

### De Development vers Docker

```bash
# Même base de code!
git push
docker build -t filamenta:latest .
docker-compose up
```

### De Docker vers VPS/cPanel

```bash
# 1. Exporter la BD
docker-compose exec db mysqldump -u root -p > backup.sql

# 2. Sur VPS/cPanel: Importer
mysql -u user -p database < backup.sql

# 3. Déployer le code (même que Docker!)
# Changement: .env seulement
```

### De cPanel vers Docker

```bash
# 1. Tirer le code du cPanel
scp -r user@host:~/apps/filamenta .

# 2. Exporter la BD
ssh user@host "mysqldump -u db_user -p db_name" > backup.sql

# 3. Sur local: docker-compose up
docker-compose exec db mysql -u root -p database < backup.sql
```

---

## 🔒 Sécurité pour chaque plateforme

### Common (tous les environnements)

- [ ] Générer une FLASK_SECRET_KEY longue et aléatoire
- [ ] Utiliser HTTPS/SSL partout
- [ ] Sécuriser les credentials (ne pas versionner .env)
- [ ] Configurer les logs
- [ ] Mettre en place les backups
- [ ] Limiter l'accès (firewall, permissions)

### cPanel

- [ ] Utiliser AutoSSL (gratuit)
- [ ] Configurer les permissions des fichiers
- [ ] Utiliser un utilisateur dédié
- [ ] Monitorer via cPanel
- [ ] Backups via cPanel

### VPS

- [ ] Configurer UFW/firewall
- [ ] Certificat Let's Encrypt
- [ ] SSH key-based auth seulement
- [ ] Fail2ban pour brute-force protection
- [ ] Monitoring (Prometheus/Grafana)

### Docker

- [ ] Scanner les images pour CVE
- [ ] Utiliser des utilisateurs non-root
- [ ] Limiter les ressources
- [ ] Secrets manager pour credentials
- [ ] Logs centralisés (ELK stack)

---

## 📈 Monitoring par plateforme

### cPanel

- Logs: `/home/user/apps/filamenta/logs/`
- Via cPanel > Apache Module Handlers
- Via cPanel > Error Log

### VPS

```bash
# Logs Gunicorn
sudo journalctl -u filamenta -f

# Logs Nginx
sudo tail -f /var/log/nginx/filamenta_access.log

# Monitoring système
htop
```

### Docker

```bash
# Logs
docker-compose logs -f web

# Stats
docker stats

# Monitoring
docker-compose exec web curl localhost:8000/health
```

---

## 🆘 Support et dépannage

### Questions par plateforme ?

**cPanel :** [Guide complet cPanel](DEPLOYMENT_CPANEL.md)
**VPS :** [Guide complet VPS](DEPLOYMENT_VPS.md)
**Docker :** [Guide complet Docker](DEPLOYMENT_DOCKER.md)

### Problèmes courants

**Application ne démarre pas**

- Vérifier les logs (voir par plateforme ci-dessus)
- Vérifier FLASK_SECRET_KEY est défini
- Vérifier la BD est accessible

**BD non accessible**

- Vérifier DB_TYPE et les credentials
- Vérifier que la BD est créée
- Vérifier les permissions

**SSL/HTTPS ne marche pas**

- Vérifier le certificat est installé
- Vérifier les redirects HTTP→HTTPS
- Vérifier les headers de sécurité

---

## 🎯 Checklist pré-déploiement

### Avant TOUT déploiement

- [ ] `git status` : Tout committé
- [ ] `pytest` : Tous les tests passent
- [ ] `ruff check .` : Pas d'erreurs de linting
- [ ] `.env` : Configuré (SECRET_KEY généré)
- [ ] Dépendances : `pip install -r requirements.txt`
- [ ] BD créée et initialisée
- [ ] Logs configurés
- [ ] Backups planifiés

### Après déploiement

- [ ] Application accessible via domaine
- [ ] HTTPS/SSL fonctionne
- [ ] Logs vérifiés pour erreurs
- [ ] Monitoring en place
- [ ] Backup de la BD fait
- [ ] Test de fonctionnalités clés

---

## 📝 Résumé rapide

| Plateforme      | Startup                                                                           | Commandes clés           |
| --------------- | --------------------------------------------------------------------------------- | ------------------------ |
| **Development** | `python -m venv venv && pip install -r requirements.txt && python -m backend.src` | `pytest`, `ruff check .` |
| **cPanel**      | [Voir guide](DEPLOYMENT_CPANEL.md)                                                | SSH, puis `gunicorn`     |
| **VPS**         | [Voir guide](DEPLOYMENT_VPS.md)                                                   | `systemctl`, `nginx`     |
| **Docker**      | `docker-compose up`                                                               | `docker-compose logs -f` |

---

## 🔗 Ressources supplémentaires

- [Flask Deployment Official](https://flask.palletsprojects.com/en/latest/deploying/)
- [WSGI Standard](https://peps.python.org/pep-3333/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Docker Docs](https://docs.docker.com/)
- [Let's Encrypt](https://letsencrypt.org/)

---

## ❓ Questions fréquentes

**Q: Quel est le meilleur choix pour débuter?**
A: **Docker**. C'est le plus portable et le plus simple à maintenir.

**Q: Peut-on changer de plateforme après?**
A: **Oui!** La base de code est la même. Juste exporter la BD et rédeployer.

**Q: Combien ça coûte?**
A: Development=Gratuit, Docker=~5$/mois, VPS=~10-20$/mois, cPanel=~10-20$/mois

**Q: Puis-je utiliser PostgreSQL au lieu de MySQL?**
A: **Oui!** Supporté partout. Voir `.env` pour configuration.

---

**Choisi ta plateforme et suis le guide correspondant !** 🚀
