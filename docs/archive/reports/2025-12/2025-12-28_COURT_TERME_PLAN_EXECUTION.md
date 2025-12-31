# Court Terme — Audit + Plan d'Exécution (Jours 2–3)

**Date :** 2025-12-28 18:00 UTC+1  
**Scope :** Amélioration sécurité (headers), qualité code (docstrings, type hints), tests  
**Status :** 📋 Planification + Exécution

---

## 🎯 OBJECTIFS COURT TERME

### CT-1 : Security Headers (CSP, X-Frame-Options)
- Ajouter Content-Security-Policy
- Ajouter X-Frame-Options: DENY
- Ajouter X-Content-Type-Options: nosniff
- Ajouter Strict-Transport-Security (prod)
- Impact sécurité : **HIGH** ⭐⭐⭐

### CT-2 : Tests + Linting Validation
- Exécuter tests complets (`pytest -q`)
- Vérifier linting (`ruff check .`)
- Vérifier type checking (`mypy backend/src`)
- Améliorer tests existants (couverture +5%)
- Impact qualité : **MEDIUM** ⭐⭐

### CT-3 : Docstrings + Type Hints
- Ajouter docstrings (20+ fonctions publiques)
- Compléter type hints (signatures)
- Impact maintenabilité : **HIGH** ⭐⭐⭐

---

## 📊 ANALYSE PRÉ-EXÉCUTION

### Fichiers à Modifier

#### CT-1 : Security Headers
- `backend/src/app.py` — Flask app factory (ajouter middleware/headers)
- Alternative : Créer `backend/src/middleware.py` (clean separation)

#### CT-2 : Tests
- `backend/tests/**/*.py` — Exécuter sans modifications
- Vérifier avec ruff + mypy

#### CT-3 : Docstrings + Type Hints
- `backend/src/services/*.py` — 8 services (docstrings manquantes)
- `backend/src/routes/*.py` — 10 routes (docstrings inégales)
- `backend/src/models/*.py` — 4 models (type hints partiels)

---

## 🔐 CT-1 : SECURITY HEADERS — PLAN DÉTAILLÉ

### Approche 1 (Recommandée) : Middleware Séparé

**Avantage :** Séparation des concerns, réutilisable, testable

```python
# backend/src/middleware.py
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data: https:; font-src 'self' cdn.jsdelivr.net; connect-src 'self' https://cdn.jsdelivr.net"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if app.config.get('ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

**Intégration dans `app.py` :**
```python
app.after_request(add_security_headers)
```

### Headers à Ajouter

| Header | Valeur | Raison |
|--------|--------|--------|
| CSP | default-src 'self' + whitelist | XSS protection |
| X-Frame-Options | DENY | Clickjacking protection |
| X-Content-Type-Options | nosniff | MIME sniffing prevention |
| X-XSS-Protection | 1; mode=block | XSS legacy browser support |
| HSTS | max-age=31536000 (prod only) | Force HTTPS |

---

## 🧪 CT-2 : TESTS + LINTING — PLAN DÉTAILLÉ

### Commandes à Exécuter

```powershell
# Tests
pytest -q --disable-warnings --maxfail=1 --cov=backend/src --cov-report=term-missing

# Linting
ruff check . --select=E,W,F
ruff format --check .

# Type checking
mypy backend/src

# Frontend
npm run lint
npm run fmt -- --check
```

### Amélioration Tests Existants (C3)

**Stratégie :** Améliorer couverture tests existants (+5%) sans ajouter de nouvelles suites

Fichiers test à améliorer :
- `test_auth.py` — Ajouter edge cases
- `test_csrf.py` — Améliorer couverture
- `test_admin.py` — Compléter scenarios
- `test_install_wizard.py` — Vérifier coverage

---

## 📝 CT-3 : DOCSTRINGS + TYPE HINTS — PLAN DÉTAILLÉ

### Fichiers Services à Documenter (8)

```
✅ user_service.py       — 15+ functions (partielles)
✅ csrf_service.py       — 5 functions (incomplètes)
✅ totp_service.py       — 10 functions (partielles)
✅ i18n_service.py       — 3 functions
✅ content_service.py    — 10 functions
✅ preferences_service.py — 5 functions
✅ install_service.py    — 15+ functions
✅ rate_limiter.py       — 4 functions
```

### Format Docstring Standard

```python
def example_function(param1: str, param2: int = 0) -> dict[str, Any]:
    """
    Brief description (one line).
    
    Longer description if needed (optional).
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default 0)
        
    Returns:
        dict with keys 'status', 'data', 'error'
        
    Raises:
        ValueError: If param1 is empty
        InvalidUserError: If user not found
        
    Example:
        >>> result = example_function("test", 42)
        >>> assert result['status'] == 'success'
    """
    # Implementation
```

### Type Hints à Compléter

Fichiers models (type hints partiels) :
- `models/user.py` — Attributs SQLAlchemy + methods
- `models/content.py` — Attributs + relationships
- `models/preferences.py` — Attributs + defaults
- `models/admin_history.py` — Attributs JSON

---

## ⏱️ TIMELINE EXÉCUTION

| Phase | Fichiers | Effort | Durée |
|-------|----------|--------|-------|
| **CT-1 : Security Headers** | 2 (app.py + middleware.py) | S | 1h |
| **CT-2 : Tests + Linting** | All (exécution) | M | 1.5h |
| **CT-3 : Docstrings + Types** | 12+ files | M | 2–3h |
| **TOTAL** | — | M | **4.5–5h** |

---

## ✅ VÉRIFICATIONS POST-EXÉCUTION

```powershell
# 1. Security headers présents
grep -r "Content-Security-Policy" backend/src --include="*.py"

# 2. Tests passent
pytest -q --disable-warnings

# 3. Linting OK
ruff check . --select=E,W,F

# 4. Types OK
mypy backend/src

# 5. Docstrings ajoutées
grep -r '"""' backend/src --include="*.py" | wc -l
```

---

## 📊 MÉTRIQUES AVANT/APRÈS

### Sécurité

| Métrique | Avant | Après |
|----------|-------|-------|
| Security Headers | 🟡 Absents | ✅ Présents |
| CSP Policy | ❌ Non | ✅ Oui |
| X-Frame-Options | ❌ Non | ✅ DENY |
| HSTS (prod) | ❌ Non | ✅ Oui |

### Qualité Code

| Métrique | Avant | Après |
|----------|-------|-------|
| Docstrings | 🟡 60% | ✅ 90%+ |
| Type Hints | 🟡 70% | ✅ 90%+ |
| Tests Coverage | 🟡 40–50% | ✅ 45–55% |
| Linting | 🟡 À auditer | ✅ Clean |

---

## 🚀 STATUS

**État :** 📋 Plan prêt → Exécution commence maintenant
**Prochaine étape :** CT-1 — Ajouter Security Headers

---

*Rapport généré : 2025-12-28 18:00 UTC+1*

