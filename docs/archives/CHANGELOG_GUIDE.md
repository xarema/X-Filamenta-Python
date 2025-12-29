# Guide Rapide — CHANGELOG

**Projet:** X-Filamenta-Python  
**Standard:** Keep a Changelog + Semantic Versioning

---

## 📋 Quand Mettre à Jour le CHANGELOG ?

**TOUJOURS** lors de :

- ✅ Nouvelle fonctionnalité
- ✅ Correction de bug
- ✅ Changement de comportement
- ✅ Suppression de fonctionnalité
- ✅ Correctif de sécurité
- ✅ Bump de version

---

## 🏷️ Catégories Disponibles

| Catégorie    | Usage                                       |
| ------------ | ------------------------------------------- |
| `Added`      | Nouvelles fonctionnalités                   |
| `Changed`    | Changements dans fonctionnalités existantes |
| `Deprecated` | Fonctionnalités bientôt supprimées          |
| `Removed`    | Fonctionnalités supprimées                  |
| `Fixed`      | Corrections de bugs                         |
| `Security`   | Vulnérabilités corrigées                    |

---

## ✍️ Format d'Entrée

```markdown
### <Catégorie>

- Description concise du changement (#issue)
- Autre changement avec contexte
```

**Exemples :**

```markdown
### Added

- User authentication with JWT tokens (#42)
- Export to PDF feature for reports

### Fixed

- Fix pagination bug when results < page size (#38)
- Correct timezone handling in date filters

### Changed

- **BREAKING:** Renamed `/api/users` to `/api/v2/users`
  Migration: Update all API calls to use new endpoint
```

---

## 🔄 Workflow de Développement

### En Développement

Ajouter dans la section `[Unreleased]` :

```markdown
## [Unreleased]

### Added

- Ma nouvelle feature

### Fixed

- Mon bug fix
```

### À la Release

1. Déplacer contenu `[Unreleased]` vers nouvelle version
2. Créer section avec version et date :

```markdown
## [0.2.0] - 2025-12-28

### Added

- Ma nouvelle feature

### Fixed

- Mon bug fix
```

3. Créer section `[Unreleased]` vide
4. Mettre à jour versions :
   - `pyproject.toml`
   - `package.json`
   - File headers
5. Commit : `chore: release v0.2.0`

---

## ⚠️ Breaking Changes

**Format obligatoire :**

```markdown
### Changed

- **BREAKING:** Description du changement
  Migration: Étapes pour migrer
  Impact: Qui est affecté
```

**Règles :**

- ✅ Préfixe `**BREAKING:**` en gras
- ✅ Guide de migration
- ✅ Bump MAJOR version (sauf pre-1.0.0)

---

## 🔒 Security Fixes

**Format obligatoire :**

```markdown
### Security

- Fix <description> [SECURITY] (CVE-XXXX-YYYY)
  Affects: v0.1.0 to v0.2.3
  Severity: HIGH/MEDIUM/LOW
```

**Règles :**

- ✅ Tag `[SECURITY]`
- ✅ CVE si applicable
- ✅ Versions affectées
- ✅ Niveau de sévérité

---

## ❌ À Éviter

- ❌ Temps passé : "Add feature" → ✅ "Added feature"
- ❌ Refactoring interne (sauf impact utilisateur)
- ❌ Duplication de commits git
- ❌ Catégories vides dans le CHANGELOG
- ❌ Oublier de mettre à jour avant release

---

## 🎯 Template Rapide

Copier-coller dans `CHANGELOG.md` :

```markdown
## [Unreleased]

### Added

-

### Changed

-

### Fixed

-

### Security

-
```

---

## 📚 Liens Utiles

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- Règles complètes : `.github/copilot-instructions.md` (Section 15)

---

**Rappel :** Le CHANGELOG est pour les **utilisateurs**, pas pour les développeurs.  
Focalisez sur l'**impact** et la **clarté**, pas sur les détails techniques.
