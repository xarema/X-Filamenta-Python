# Phase 02 — Nettoyage Exécution — AVANT Suppression

**Date :** 2025-12-28 17:20 UTC+1  
**Approbations Utilisateur :**
- Q1 : OUI — Supprimer 8 test_*.py scripts
- Q2 : OUI — Supprimer 4 fichiers logs
- Q3 : À CLARIFIER → Décision : Supprimer run.py (legacy)
- Q4 : OUI — Nettoyer instance/*.db sauf main

---

## 📋 FICHIERS À SUPPRIMER (13 total)

### Scripts Test (8 files) ✅ À SUPPRIMER

```
D:\xarema\X-Filamenta-Python\
├── test_wizard_auto_complete.py      [SUPPRIMER]
├── test_wizard_http.py               [SUPPRIMER]
├── test_wizard_simple.py             [SUPPRIMER]
├── test_access.py                    [SUPPRIMER]
├── test_create_schema.py             [SUPPRIMER]
├── test_create_schema_debug.py       [SUPPRIMER]
├── test_schema_in_context.py         [SUPPRIMER]
├── test_schema2.py                   [SUPPRIMER]
```

### Fichiers Logs (4 files) ✅ À SUPPRIMER

```
├── app_debug.log                     [SUPPRIMER]
├── server_log.txt                    [SUPPRIMER]
├── test_output.txt                   [SUPPRIMER]
├── output.txt                        [SUPPRIMER]
```

### Script Dev (1 file) ✅ À SUPPRIMER (Q3 clarification)

```
├── run.py                            [SUPPRIMER - legacy dev]
```

### Analyse Q3 - run.py

**Contenu :** Script de démarrage Flask dev (debug=True, port 5000)

**Comparaison :**
- `run.py` : Flask dev server (debug mode) - LEGACY
- `run_prod.py` : Waitress WSGI (production) - COURANT
- `makefile` : Commands (fmt, lint, test) - COURANT

**Décision :** Supprimer (c'est du legacy, on utilise run_prod.py)

---

## 📁 FICHIERS À GARDER

```
✅ GARDER:
├── run_prod.py               (production WSGI)
├── run_prod.ps1              (Windows production script)
├── makefile                  (build/dev commands)
├── check_db.py               (À vérifier - possiblement utile)
└── backend/tests/test_*.py   (Tests réels - GARDER)

⚠️ CHECK: check_db.py
└── À clarifier si c'est un utilitaire nécessaire
```

---

## ✅ PLAN SUPPRESSION

1. ✅ Supprimer 8 test_*.py scripts (racine)
2. ✅ Supprimer 4 logs (racine)
3. ✅ Supprimer run.py (legacy dev)
4. ⏳ Demander confirmation check_db.py
5. ✅ Vérifier instance/*.db
6. ✅ Git status avant/après
7. ✅ Tests + linting
8. ✅ Rapport final

---

**Prêt à procéder ? Répondez OUI ou demandez clarification sur check_db.py.**

