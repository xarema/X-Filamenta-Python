# Wizard d'Installation - Documentation Technique

**Version:** 0.0.2-Alpha  
**Date:** 2025-12-28  
**Statut:** Stable  

---

## Vue d'ensemble

Le wizard d'installation est un assistant multi-étapes permettant de configurer l'application X-Filamenta-Python lors de sa première utilisation. Il utilise HTMX pour une expérience utilisateur fluide sans rechargement de page.

---

## Architecture

### Composants principaux

```
frontend/templates/
├── layouts/
│   └── wizard.html                 # Layout dédié (sans navbar)
└── pages/install/
    ├── index.html                  # Page principale du wizard
    ├── done.html                   # Page de fin (succès)
    ├── error.html                  # Page d'erreur
    └── partials/
        ├── requirements.html       # Vérification prérequis
        ├── db_form.html           # Formulaire BD (tabs)
        ├── db_test.html           # Résultat test connexion
        ├── upload_form.html       # Upload backup (optionnel)
        ├── upload.html            # Validation backup
        ├── admin_form.html        # Formulaire compte admin
        └── summary.html           # Résumé avant finalisation

backend/src/
├── routes/
│   └── install.py                 # Routes du wizard
├── services/
│   └── install_service.py         # Logique métier
└── i18n/
    ├── en.json                    # Traductions anglais
    └── fr.json                    # Traductions français
```

---

## Flux du wizard

### Diagramme de flux

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GET /                                                    │
│    → Redirige vers /install/ si pas installé               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. GET /install/                                            │
│    → Affiche page choix de langue                          │
│    → Drapeaux: 🇺🇸 EN | 🇫🇷 FR                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. GET /lang/{en|fr}?start=1                               │
│    → Set session['lang'] = en|fr                           │
│    → Set session['wizard_started'] = True                  │
│    → Redirige vers /install/                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Page Welcome                                             │
│    → Message de bienvenue localisé                         │
│    → Bouton "Continuer"                                    │
│    → POST /install/step (step=requirements)                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Page Requirements                                        │
│    → Vérification système:                                 │
│      • Environnement (OS/Arch)      ✓                      │
│      • Git                          ✓/✗                    │
│      • Python                       ✓/✗                    │
│      • Pip                          ✓/✗                    │
│      • DB Clients                   ✓/⚠                    │
│    → Bouton "Continuer"                                    │
│    → POST /install/step (step=db_form)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Page Database (tabs)                                     │
│    → Tab 💾 SQLite                                          │
│      • Nom fichier BD (app.db)                             │
│    → Tab 🐬 MySQL                                           │
│      • Host, Port, Nom BD, User, Password                  │
│    → Tab 🐘 PostgreSQL                                      │
│      • Host, Port, Nom BD, User, Password                  │
│    → Bouton "Tester la connexion"                          │
│    → POST /install/step (step=db_test)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Test connexion BD                                        │
│    → InstallService.test_db_connection(db_uri)             │
│    → Si OK: Affiche bouton "Continuer"                     │
│    → Si KO: Affiche erreur + bouton "Réessayer"            │
│    → POST /install/step (step=upload_form)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Page Upload Backup (optionnel)                          │
│    → Upload fichier .tar.gz / .tgz (max 50MB)              │
│    → Bouton "Restaurer" ou "Continuer sans backup"         │
│    → POST /install/step (step=upload|admin_form)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Page Admin                                               │
│    → Formulaire compte administrateur:                     │
│      • Username (défaut: admin)                            │
│      • Email                                               │
│      • Password (min 8 char, 1 maj, 1 symbole)            │
│    → Bouton "Créer l'administrateur"                       │
│    → POST /install/step (step=admin)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. Validation password                                     │
│     → InstallService.validate_password(password)           │
│     → Si KO: Affiche erreur + reste sur formulaire         │
│     → Si OK: Continue vers Summary                         │
│     → Affiche summary.html                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. Page Summary                                            │
│     → Résumé configuration BD:                             │
│       • Type (SQLite/MySQL/PostgreSQL)                     │
│       • Paramètres (host, port, nom, user)                 │
│       • URI complète                                       │
│     → Résumé compte admin:                                 │
│       • Username                                           │
│       • Email                                              │
│       • Password (masqué)                                  │
│     → Résumé backup (si présent):                          │
│       • Nom fichier                                        │
│       • Checksum                                           │
│     → Bouton "Finaliser l'installation"                    │
│     → POST /install/step (step=finalize)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 12. Finalisation                                            │
│     → InstallService.apply_seed_or_restore(state)          │
│       • Si backup: Restore depuis fichier                  │
│       • Sinon: Seed DB (tables vides)                      │
│     → InstallService.create_admin_user(state)              │
│       • Création utilisateur admin                         │
│       • Hash password (bcrypt)                             │
│     → InstallService.finalize_install(app_root)            │
│       • Création fichier .installed                        │
│     → InstallService.clear_wizard_state(session)           │
│       • Nettoyage session                                  │
│     → Affiche done.html                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 13. Page Done                                               │
│     → Icône de succès ✓                                    │
│     → Message de confirmation                              │
│     → Bouton "Aller à la connexion"                        │
│     → Lien vers /auth/login                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 14. GET /auth/login                                         │
│     → Page de connexion                                    │
│     → Login avec credentials créés                         │
└─────────────────────────────────────────────────────────────┘
```

---

## État du wizard (session)

### Variables de session

| Clé | Type | Description |
|-----|------|-------------|
| `lang` | str | Langue sélectionnée (`en` ou `fr`) |
| `wizard_started` | bool | Wizard démarré (langue choisie) |
| `welcome_shown` | bool | Page welcome affichée |
| `requirements_checked` | bool | Page requirements validée |
| `db_type` | str | Type de BD (`sqlite`, `mysql`, `postgresql`) |
| `db_uri` | str | URI de connexion complète |
| `sqlite_dbname` | str | Nom fichier SQLite |
| `mysql_host` | str | Hôte MySQL |
| `mysql_port` | str | Port MySQL |
| `mysql_user` | str | User MySQL |
| `mysql_password` | str | Password MySQL |
| `mysql_dbname` | str | Nom BD MySQL |
| `pg_host` | str | Hôte PostgreSQL |
| `pg_port` | str | Port PostgreSQL |
| `pg_user` | str | User PostgreSQL |
| `pg_password` | str | Password PostgreSQL |
| `pg_dbname` | str | Nom BD PostgreSQL |
| `backup_ok` | bool | Backup validé |
| `backup_filename` | str | Nom fichier backup |
| `backup_checksum` | str | SHA256 checksum |
| `admin_username` | str | Username admin |
| `admin_email` | str | Email admin |
| `admin_password` | str | Password admin (temporaire) |

---

## Breadcrumb (fil d'Ariane)

### Étapes

1. **Welcome** - Page de bienvenue
2. **Requirements** - Vérification prérequis système
3. **Database** - Configuration base de données
4. **Administrator** - Création compte admin
5. **Summary** - Résumé et finalisation

### Navigation

- Chaque étape est **cliquable** (sauf Summary)
- Permet de revenir en arrière
- État conservé dans la session
- Étape active marquée par classe CSS `active`

### Implémentation

```html
<nav aria-label="Wizard steps">
  <ol class="breadcrumb justify-content-center mb-4">
    <li class="breadcrumb-item {% if condition %}active{% endif %}">
      <a href="#" hx-post="/install/step" 
         hx-vals='{"step":"welcome"}' 
         hx-target="#wizard-container">
        {{ t('wizard.steps.welcome') }}
      </a>
    </li>
    <!-- ... autres étapes ... -->
  </ol>
</nav>
```

---

## HTMX

### Stratégie

- **Target:** `#wizard-container` (unique dans la page)
- **Swap:** `innerHTML` (remplace contenu, conserve conteneur)
- **Method:** `POST /install/step`
- **Payload:** `FormData` avec champ `step`

### Avantages

- Pas de rechargement de page
- Navigation fluide
- État conservé (session backend)
- Progressive enhancement (fonctionne sans JS)

---

## Sécurité

### Protection CSRF

- Tous les formulaires incluent `{{ csrf_token() }}`
- Validation côté backend automatique (Flask-WTF)

### Validation des entrées

- **Password:**
  - Minimum 8 caractères
  - Au moins 1 majuscule
  - Au moins 1 symbole
- **Email:** Validation format email
- **DB URI:** Test connexion avant continue
- **Backup:** Validation format .tar.gz/.tgz, max 50MB

### Stockage sécurisé

- Password admin hashé avec `bcrypt` (12 rounds)
- Pas de credentials en clair dans session (temporaire uniquement)
- Session sécurisée (HTTPOnly, SameSite)

---

## Internationalisation (i18n)

### Langues supportées

- 🇺🇸 Anglais (en) - International
- 🇫🇷 Français (fr) - France

### Fonction de traduction

```python
from flask import session

def t(key: str, **kwargs) -> str:
    """Translate key with optional interpolation."""
    lang = session.get('lang', 'en')
    translations = load_translations(lang)
    text = translations.get(key, key)
    return text.format(**kwargs) if kwargs else text
```

### Utilisation dans templates

```jinja
{{ t('wizard.title') }}
{{ t('wizard.welcome.message') }}
{{ t('wizard.db.test_success') }}
```

---

## Design UI/UX

### Layout wizard

- **Header:** Simplifié, uniquement "X-Filamenta" centré
- **Navbar:** Absente (pas de distraction)
- **Footer:** Minimal (projet + version + copyright + licence)
- **Couleurs:** Thème Bootstrap 5 par défaut
- **Responsive:** Mobile-first, fonctionne sur tous écrans

### Feedback visuel

- **Checkmarks:** ✓ (vert) pour succès
- **Croix:** ✗ (rouge) pour échec
- **Warning:** ⚠ (jaune) pour avertissement
- **Badges:** Pills colorés pour statuts
- **Cards:** Shadow-sm pour profondeur
- **Boutons:** Primary pour actions principales

---

## Tests

### Tests manuels recommandés

Consultez `docs/TEST_WIZARD_REDESIGN.md` pour le guide complet.

### Tests automatisés (à implémenter)

```python
# tests/test_wizard.py
def test_wizard_language_selection(client):
    """Test selection of language."""
    # ...

def test_wizard_requirements_page(client):
    """Test requirements page displays."""
    # ...

def test_wizard_db_sqlite_config(client):
    """Test SQLite configuration."""
    # ...

def test_wizard_admin_creation(client):
    """Test admin user creation."""
    # ...

def test_wizard_finalization(client):
    """Test full wizard flow."""
    # ...
```

---

## Dépannage

### Problème: Redirection infinie

**Cause:** Fichier `.installed` présent ou logique de redirection cassée  
**Solution:**
```powershell
Remove-Item .installed -ErrorAction SilentlyContinue
```

### Problème: Bouton "Continuer" ne fonctionne pas

**Cause:** HTMX target `#wizard-container` manquant  
**Solution:** Vérifier que le conteneur existe dans le DOM

### Problème: Traductions manquantes

**Cause:** Clés non présentes dans `en.json` ou `fr.json`  
**Solution:** Vérifier fichiers i18n, ajouter clés manquantes

### Problème: Base de données ne se crée pas

**Cause:** Permissions dossier `instance/` ou drivers BD manquants  
**Solution:**
```powershell
# Vérifier dossier
New-Item -ItemType Directory -Force -Path instance

# Installer drivers
pip install pymysql psycopg2-binary
```

---

## Maintenance

### Ajout d'une nouvelle étape

1. Créer partial dans `frontend/templates/pages/install/partials/`
2. Ajouter route dans `backend/src/routes/install.py`
3. Ajouter traductions dans `backend/src/i18n/*.json`
4. Mettre à jour breadcrumb dans `index.html`
5. Tester flux complet

### Modification du design

- Modifier `frontend/templates/layouts/wizard.html` pour layout global
- Modifier partials individuels pour pages spécifiques
- Respecter Bootstrap 5 classes

---

## Références

- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTMX Documentation](https://htmx.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

**Dernière mise à jour:** 2025-12-28  
**Version documentation:** 1.0.0

