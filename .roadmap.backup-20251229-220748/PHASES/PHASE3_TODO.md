# TODO — PHASE 3 (Database & Models)

**Statut :** En cours  
**Durée estimée :** 3-4 jours  
**Priorité :** HAUTE  
**Commencé:** 2025-12-27

---

## 📋 Vue d'ensemble

Phase 3 consiste à créer les modèles de base de données, les migrations, et connecter l'application à une vraie base de données avec des données réelles.

**Objectif :** Application avec persistence de données réelle (SQLite → PostgreSQL ready)

---

## 🎯 JOUR 1 - Database Models (3-4 heures)

### Task 1: Créer User Model

**Durée:** 1h

- [ ] Modèle User avec SQLAlchemy
- [ ] Champs: id, username, email, password_hash, is_admin, is_active, created_at
- [ ] Relations et contraintes
- [ ] Méthodes: set_password, check_password

Files:

- [ ] `backend/src/models/user.py`

### Task 2: Créer Preferences Model

**Durée:** 45 min

- [ ] Modèle UserPreferences
- [ ] Champs: id, user_id, theme, language, notifications
- [ ] Relation avec User (one-to-one)

Files:

- [ ] `backend/src/models/preferences.py`

### Task 3: Créer Content Model

**Durée:** 1h

- [ ] Modèle Content
- [ ] Champs: id, title, body, author_id, type, status, created_at, updated_at
- [ ] Relations avec User

Files:

- [ ] `backend/src/models/content.py`

### Task 4: Initialiser Alembic (Migrations)

**Durée:** 45 min

- [ ] Installer Alembic
- [ ] Configurer env.py
- [ ] Créer première migration
- [ ] Tester migration up/down

Files:

- [ ] `migrations/` (dossier Alembic)
- [ ] `migrations/env.py`
- [ ] `migrations/versions/001_initial.py`

---

## 🎯 JOUR 2 - Services & Repository Layer (3-4 heures)

### Task 5: Refactorer UserService avec DB

**Durée:** 1h30

- [ ] Remplacer mock par requêtes DB
- [ ] CRUD operations (Create, Read, Update, Delete)
- [ ] get_by_id, get_by_email, create, update
- [ ] Intégrer avec User model

Files:

- [ ] Modifier `backend/src/services/user_service.py`

### Task 6: Créer PreferencesService

**Durée:** 1h

- [ ] Service pour gérer les préférences
- [ ] get_preferences, update_preference
- [ ] Sauvegarder en DB

Files:

- [ ] `backend/src/services/preferences_service.py`

### Task 7: Créer ContentService

**Durée:** 1h

- [ ] Service pour gérer le contenu
- [ ] CRUD operations
- [ ] Pagination, filtres

Files:

- [ ] `backend/src/services/content_service.py`

### Task 8: Seed Data (Données initiales)

**Durée:** 30 min

- [ ] Script pour créer utilisateurs par défaut
- [ ] Admin user avec mot de passe
- [ ] Contenu de démonstration

Files:

- [ ] `scripts/seed_db.py`

---

## 🎯 JOUR 3 - Integration & Polish (2-3 heures)

### Task 9: Connecter Routes aux Services

**Durée:** 1h30

- [ ] Modifier admin routes pour utiliser DB
- [ ] Modifier API endpoints pour sauvegarder en DB
- [ ] Tester toutes les routes

Files:

- [ ] Modifier `backend/src/routes/admin.py`
- [ ] Modifier `backend/src/routes/api.py`

### Task 10: Tester avec Vraies Données

**Durée:** 1h

- [ ] Tests unitaires pour models
- [ ] Tests d'intégration pour services
- [ ] Tests end-to-end

Files:

- [ ] `backend/tests/test_models.py`
- [ ] `backend/tests/test_services.py`

### Task 11: PostgreSQL Configuration

**Durée:** 30 min

- [ ] Configurer DATABASE_URL pour PostgreSQL
- [ ] Tester migrations sur PostgreSQL
- [ ] Documentation de déploiement

Files:

- [ ] Modifier `backend/src/config.py`
- [ ] Créer `docs/DATABASE.md`

### Task 12: Documentation

**Durée:** 30 min

- [ ] Documenter les modèles
- [ ] Documenter les migrations
- [ ] Mettre à jour README

Files:

- [ ] `docs/MODELS.md`
- [ ] Mettre à jour `backend/README.md`

---

## 📊 Checklist Rapide

### Jour 1 - Models

- [ ] Task 1: User Model
- [ ] Task 2: Preferences Model
- [ ] Task 3: Content Model
- [ ] Task 4: Alembic migrations

### Jour 2 - Services

- [ ] Task 5: UserService avec DB
- [ ] Task 6: PreferencesService
- [ ] Task 7: ContentService
- [ ] Task 8: Seed data

### Jour 3 - Integration

- [ ] Task 9: Connecter routes
- [ ] Task 10: Tests complets
- [ ] Task 11: PostgreSQL config
- [ ] Task 12: Documentation

---

## 🎯 Bonus (si temps)

- [ ] Session management avec Flask-Session
- [ ] Cache avec Flask-Caching
- [ ] Soft delete pour les modèles
- [ ] Audit trail (created_by, updated_by)

---

## 📝 Notes Importantes

1. **Database:** SQLite en dev, PostgreSQL en production
2. **Migrations:** Utiliser Alembic pour versionner le schéma
3. **Passwords:** JAMAIS en clair, toujours hashés (bcrypt)
4. **Tests:** Tester avec DB en mémoire (SQLite :memory:)
5. **Transactions:** Utiliser db.session.commit() avec try/except

---

## 🚀 Commandes Utiles

```bash
# Installer Alembic
pip install alembic

# Initialiser Alembic
alembic init migrations

# Créer migration
alembic revision --autogenerate -m "Initial migration"

# Appliquer migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Seed database
python scripts/seed_db.py
```

---

## 📚 Références

- SQLAlchemy: https://docs.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- `backend/README.md` - Backend structure

---

**Last Updated:** 2025-12-27
**Status:** READY TO START 🚀
