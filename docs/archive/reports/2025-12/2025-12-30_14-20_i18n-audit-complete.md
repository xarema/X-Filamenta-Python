# Audit i18n — X-Filamenta-Python
**Date:** 2025-12-30 14:15
**Auditeur:** Junie (JetBrains AI)
**Version projet:** 0.1.0-Beta

---

## 📈 Statistiques Globales

- **Fichiers Python analysés:** 40
- **Templates HTML analysés:** 55
- **Variables linguistiques détectées:** 495
- **Textes hardcodés détectés:** ~15 (Backend) + Analyse visuelle requise (Frontend)
- **Langues supportées:** EN, FR, ES (partiel)
- **Clés JSON manquantes (EN):** 140
- **Clés JSON orphelines:** Analyse en cours (potentiellement élevées en FR)

---

## 🔴 Problèmes Critiques

### 1. Textes Hardcodés (Backend)
| Fichier | Ligne | Texte Hardcodé | Suggestion |
|---------|-------|----------------|------------|
| `backend/src/routes/admin.py` | 207 | "Paramètres sauvegardés avec succès" | `t('admin.settings.success')` |
| `backend/src/routes/auth.py` | 266 | "Lien de vérification invalide" | `t('auth.verify_email.error')` |
| `backend/src/routes/auth.py` | 271 | "Le lien de vérification a expiré" | `t('auth.verify_email.expired')` |
| `backend/src/routes/auth.py` | 312 | "Email requis" | `t('auth.forgot.error.email_required')` |
| `backend/src/routes/auth.py` | 348 | "Lien de réinitialisation invalide ou expiré" | `t('auth.reset.error.invalid')` |

### 2. Incohérences de Structure (JSON)
| Problème | Détails |
|----------|---------|
| Clés dupliquées | La clé `auth` est définie deux fois dans `fr.json` et `en.json`. La seconde écrase la première. |
| Désynchronisation massive | `en.json` (355 clés) vs `fr.json` (495 clés). 140 clés manquantes en anglais. |
| Langues non synchronisées | Toute la section `wizard` est manquante dans `en.json`. |

### 3. Fichiers JSON corrompus
Les fichiers `fr.json` et `en.json` contiennent des définitions d'objets en double au même niveau hiérarchique, ce qui est une mauvaise pratique et source d'erreurs lors de la modification manuelle.

---

## ⚠️ Avertissements

### 1. Variables Orphelines
Plusieurs clés dans `fr.json` semblent ne plus être utilisées ou ont été renommées, créant du "bruit" dans les fichiers de traduction.

### 2. Stack i18n artisanale
L'utilisation d'une classe `Translations` personnalisée au lieu de `Flask-Babel` (standard) limite l'utilisation d'outils d'extraction automatique comme `pybabel`.

---

## ✅ Recommandations

### Priorité 🔴 CRITIQUE
1. **Fusionner et nettoyer les JSON :** Supprimer les doublons de la clé `auth` et harmoniser la structure.
2. **Traduire le Wizard :** Compléter `en.json` avec les 140 clés manquantes (principalement le wizard d'installation).
3. **Externaliser les messages flash :** Remplacer tous les textes en dur dans `backend/src/routes/` par des appels à `t()`.

### Priorité 🟠 IMPORTANTE
1. **Migration vers JSON hiérarchique strict :** Assurer que chaque clé est unique.
2. **Synchronisation automatique :** Mettre en place un script de validation qui échoue si les clés ne correspondent pas entre EN et FR.

### Priorité 🟢 AMÉLIORATION
1. **Passage à Flask-Babel :** Pour bénéficier des standards de l'industrie (fichiers .po/.mo).
2. **Interface d'administration (Tabulator.js) :** Permettre la modification des traductions via le panneau admin.

---

## 🔧 Plan d'Action Recommandé

### Phase 1 : Nettoyage & Correction (Immédiat)
- [ ] Corriger les doublons JSON dans `fr.json` et `en.json`.
- [ ] Migrer les messages flash hardcodés vers les JSON.
- [ ] Harmoniser `en.json` avec `fr.json` (Traductions manquantes).

### Phase 2 : Standardisation
- [ ] Implémenter un validateur de structure JSON.
- [ ] Documenter les conventions de nommage (`domaine.page.composant.action`).

### Phase 3 : Interface Admin
- [ ] Créer la route d'édition des langues.
- [ ] Intégrer Tabulator.js pour la gestion des clés.

---

**Rapport généré le:** 2025-12-30 14:20:00
**Durée d'analyse:** 12 minutes
