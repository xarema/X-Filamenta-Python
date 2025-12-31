# 📋 PHASE 3 — PLAN VALIDÉ ET ADAPTÉ

**Date:** 2025-12-30T00:35:00+01:00  
**Basé sur:** Réponses utilisateur validées  
**Durée:** 20 jours (5 sprints)  
**Status:** ✅ APPROUVÉ — DÉMARRAGE IMMÉDIAT

---

## ✅ CHOIX UTILISATEUR VALIDÉS

### Scope Global
- ✅ Tous les 5 sprints
- ✅ Ordre: Sprint 1 → 2 → 3 → 4 → 5
- ✅ v1.0.0 feature-complete

### Détails par Sprint

**Sprint 1 (CRUD Admin) — 5 jours:**
- Delete: Soft delete + Option admin (choix modal)
- Email: Checkbox optionnel lors création user
- Roles: Admin/User uniquement (simple)

**Sprint 2 (Profil User) — 4 jours:**
- Avatar: NON (Gravatar uniquement)
- Username: Modifiable (frontend)
- Champ custom: "Nom complet" personnalisable
- Activity log: Frontend + DB (table UserActivity)

**Sprint 3 (API REST) — 4 jours:**
- Scope v1.0: Read-only (GET endpoints)
- Scope v1.1+: Write (POST/PUT/DELETE)
- Auth: API keys + JWT (les deux)

**Sprint 4 (Search/Export) — 3 jours:**
- Search: SQLite FTS5 (recommandé pour multi-DB)
- Export: CSV + JSON + PDF

**Sprint 5 (Tests/Docs) — 4 jours:**
- Tests e2e: Playwright (recommandé moderne)
- Docs: Markdown + PDF + HTML navigable

---

## 📊 PROPOSITIONS TECHNIQUES

### Q6: Activity Log Storage

**Je recommande: Option B (Table DB)**

**Raison:**
- ✅ Plus sécurisé (ACL, encryption)
- ✅ Requêtable (filtres, pagination)
- ✅ Scalable (indexes, archivage)
- ✅ Intégré (relations User)

**Structure proposée:**
```python
class UserActivity(db.Model):
    id: int
    user_id: int (FK User)
    action: str  # "login", "password_change", "2fa_enable", etc.
    ip_address: str
    user_agent: str
    metadata: JSON  # Détails additionnels
    created_at: datetime
```

**Alternative (fichiers log):**
- ❌ Moins sécurisé (accès filesystem)
- ❌ Difficile à requêter
- ✅ Plus simple (pas de migration)

**Ton choix:** Table DB ou fichiers log ?

---

### Q9 (Sprint 4): Full-text Search Engine

**Je recommande: Option A (SQLite FTS5)**

**Raison:**
- ✅ Intégré SQLite (pas de dépendance)
- ✅ Compatible multi-DB (fallback simple)
- ✅ Performant (< 100k records)
- ✅ Simple à implémenter

**Comparaison:**

| Engine | Complexité | Performance | Multi-DB | Recommandé |
|--------|------------|-------------|----------|------------|
| SQLite FTS5 | Simple | Bon | ✅ Oui | ⭐⭐⭐ |
| PostgreSQL FTS | Moyen | Excellent | ❌ PostgreSQL only | ⭐⭐ |
| Elasticsearch | Complexe | Excellent | ✅ Oui | ⭐ (overkill) |

**Ton choix:** SQLite FTS5, PostgreSQL FTS, ou Elasticsearch ?

---

### Q9 (Sprint 5): Tests e2e Framework

**Je recommande: Option A (Playwright)**

**Raison:**
- ✅ Moderne (Microsoft, 2020+)
- ✅ Multi-browser (Chrome, Firefox, Safari)
- ✅ Fast & reliable
- ✅ Auto-wait (pas de sleep)
- ✅ Bon avec HTMX

**Comparaison:**

| Framework | Vitesse | Stabilité | HTMX Support | Recommandé |
|-----------|---------|-----------|--------------|------------|
| Playwright | Excellent | Excellent | ✅ Oui | ⭐⭐⭐ |
| Selenium | Moyen | Moyen | ✅ Oui | ⭐⭐ |
| Cypress | Bon | Bon | ⚠️ Limité | ⭐ |

**Ton choix:** Playwright, Selenium, ou autre ?

---

## 🚀 ORDRE D'EXÉCUTION OPTIMISÉ

### Sprint 1: CRUD Admin (5 jours)
**Priorité:** ⭐⭐⭐ HAUTE  
**Dépendances:** Aucune  
**Démarrage:** IMMÉDIAT

**Livrables:**
- CRUD Users (create, edit, delete avec modal)
- CRUD Content (create, edit, delete)
- AdminService centralisé
- 25+ tests

---

### Sprint 2: Profil User (4 jours)
**Priorité:** ⭐⭐⭐ HAUTE  
**Dépendances:** Migration user.full_name + UserActivity table

**Livrables:**
- Page profil (/profile)
- Edit profil (email, username, full_name)
- Change password
- Activity log (dernières 20 actions)
- 30+ tests

---

### Sprint 3: API REST (4 jours)
**Priorité:** ⭐⭐ MOYENNE  
**Dépendances:** Migration APIKey table

**Livrables:**
- API v1 read-only (GET /api/v1/users, /api/v1/content)
- API keys + JWT auth
- Swagger/OpenAPI docs
- Rate limiting API
- 30+ tests

---

### Sprint 4: Search/Export (3 jours)
**Priorité:** ⭐⭐ MOYENNE  
**Dépendances:** SQLite FTS5 setup (si choisi)

**Livrables:**
- Full-text search (users, content)
- Export CSV/JSON/PDF
- SearchService + ExportService
- 20+ tests

---

### Sprint 5: Tests e2e + Docs (4 jours)
**Priorité:** ⭐⭐⭐ HAUTE  
**Dépendances:** Playwright installé

**Livrables:**
- Tests e2e (wizard, auth, admin, profile)
- Fixtures complètes (admin_user, etc.)
- User guide (MD + PDF + HTML)
- Admin guide
- FAQ (30+ questions)
- README final

---

## 📅 TIMELINE PHASE 3

```
Semaine 1 (Jours 1-5):  Sprint 1 (CRUD Admin)
Semaine 2 (Jours 6-9):  Sprint 2 (Profil User)
Semaine 3 (Jours 10-13): Sprint 3 (API REST)
Semaine 3 (Jours 14-16): Sprint 4 (Search/Export)
Semaine 4 (Jours 17-20): Sprint 5 (Tests e2e + Docs)
```

**Date début:** 2025-12-30  
**Date fin estimée:** 2026-01-18  
**Résultat:** v1.0.0 feature-complete

---

## ❓ QUESTIONS FINALES AVANT DÉMARRAGE

**Réponds aux 3 propositions:**

1. **Activity log storage:**
   - A) Table DB (UserActivity) ⭐ RECOMMANDÉ
   - B) Fichiers log

2. **Full-text search:**
   - A) SQLite FTS5 ⭐ RECOMMANDÉ
   - B) PostgreSQL FTS
   - C) Elasticsearch

3. **Tests e2e framework:**
   - A) Playwright ⭐ RECOMMANDÉ
   - B) Selenium
   - C) Pas de tests e2e

---

## 🚀 APRÈS TES RÉPONSES

**Je commence IMMÉDIATEMENT Sprint 1:**
1. Créer fichiers backend (routes, services)
2. Créer templates frontend
3. Créer migrations
4. Créer tests
5. Valider avec toi

---

**Fichier:** docs/PHASE3_PLAN_VALIDATED.md  
**Status:** ✅ APPROUVÉ — EN ATTENTE 3 RÉPONSES FINALES

