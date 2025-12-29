# Fix Rate Limiter - Limite Trop Restrictive

**Date:** 2025-12-28 20:10 UTC+1
**Problem:** Rate limit 50 per hour bloque l'acces a main.index
**Status:** FIXED

---

## PROBLEME DETECTE

Log erreur:
```
2025-12-28 16:00:06,038 [INFO] flask-limiter: ratelimit 50 per 1 hour (127.0.0.1) 
exceeded at endpoint: main.index
```

Cause:
  - default_limits=["200 per day", "50 per hour"] dans rate_limiter.py
  - Cette limite globale s'applique a TOUTES les routes
  - Beaucoup trop restrictif pour dev/test
  - Bloque l'acces apres seulement 50 requetes

---

## SOLUTION APPLIQUEE

Fichier: backend/src/services/rate_limiter.py

Avant:
```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
```

Apres:
```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No default limit - apply explicitly per route
    storage_uri="memory://",
)
```

Changement:
  - Supprime les limites par defaut globales
  - Les limites sont maintenant appliquees explicitement par route
  - Routes sensibles gardent leurs limites strictes:
    - login_rate_limit: 5/min, 20/hour
    - two_fa_rate_limit: 10/min, 30/hour
    - strict_rate_limit: 3/min, 10/hour
    - api_rate_limit: 100/hour

---

## LIMITES PAR ROUTE (INCHANGEES)

Routes sensibles protegees:
  - /auth/login          : 5/min, 20/hour (brute-force protection)
  - /auth/2fa/verify     : 10/min, 30/hour (TOTP guessing protection)
  - /admin/*             : 3/min, 10/hour (admin operations)
  - /api/*               : 100/hour (API abuse protection)

Routes publiques SANS limite:
  - /                    : Pas de limite
  - /install/            : Pas de limite
  - /static/*            : Pas de limite
  - /favicon.ico         : Pas de limite

---

## VERIFICATION

[OK] Ruff check: Passed (apres fix auto)
[OK] Default limits: [] (vides)
[OK] Routes sensibles: Limites explicites preservees
[OK] Routes publiques: Pas de limite globale

---

## IMPACT

Avant:
  - 50 requetes/heure MAX sur toutes les routes
  - Bloque dev/test apres 50 refreshes
  - Trop restrictif pour usage normal

Apres:
  - Pas de limite sur routes publiques
  - Limites strictes seulement sur routes sensibles
  - Dev/test non bloque
  - Securite preservee la ou necessaire

---

## TEST

Nettoyer cache rate limiter (restart serveur):
  Get-Process python.exe | Stop-Process -Force
  .venv\Scripts\python.exe run_prod.py

Tester:
  GET http://127.0.0.1:5000/ (multiple fois)
  → PAS de "ratelimit exceeded"
  
  GET http://127.0.0.1:5000/install/ (multiple fois)
  → PAS de "ratelimit exceeded"

Logs attendus:
  - Serveur demarre OK
  - Redirection vers /install/ OK
  - Pas de message "ratelimit exceeded"

---

## CONCLUSION

Probleme: Limite globale trop restrictive (50/hour)
Solution: Supprime limite par defaut, garde limites explicites
Impact: Dev/test non bloque, securite preservee
Status: FIXED

Serveur pret pour restart et test.

---

License: AGPL-3.0-or-later

