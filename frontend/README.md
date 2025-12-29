"""
5. `static/css/custom.css` — Styles personnalisés
4. `static/css/tokens.css` — Variables CSS
3. `pages/index.html` — Accueil
2. `components/navbar.html` — Barre de navigation
1. `layouts/base.html` — Structure parente

## Fichiers à créer

```
npm run format
npm run lint
# Vérifier CSS/JS

npm install
# Bootstrap 5 est dans requirements (node_modules)
```bash

## Setup

  ```
  export function initSearch(selector) { ... }
  // static/js/modules/search.js
  ```js
- Si custom JS : isoler dans un module
- Comportements HTMX préférés aux custom JS
- Modules ES6 (pas de variables globales)

### JavaScript

- Custom CSS uniquement quand nécessaire
- Utiliser Bootstrap en priorité (`@apply` ou classes Tailwind-like)
  ```
  }
    --font-family-base: 'Segoe UI', sans-serif;
    --spacing-xs: 0.25rem;
    --color-primary: #0d6efd;
  :root {
  ```css
- **Variables CSS** (`static/css/tokens.css`)

### CSS

  ```
  -->
    Contexte: items, page_info
    Swap: outerHTML
    Target: #items-list
    Endpoint: GET /api/items?page=2
    Fragment HTMX: paginated-list.html
  <!-- 
  ```html
- Commenter le fragment :
- Fichier : `frontend/templates/fragments/` ou dans le dossier `components/`

Quand une route Flask retourne un **fragment Jinja2** pour HTMX :

### HTMX Fragments

   - Pas de structure HTML parente (confiée au layout)
   - Contenu spécifique à la route
   - Héritage de layout : `{% extends "layouts/base.html" %}`
3. **Pages** (`pages/`)

     ```
     -->
       Contexte attendu: user, menu_items
       Usage: {% include 'components/navbar.html' with context %}
       Composant: navbar.html
     <!-- 
     ```html
   - Commenter l'usage :
   - Doivent être idempotents
   - Fragments réutilisables
2. **Components** (`components/`)

   - Bloc `{% block content %}` pour l'héritage
   - Imports Bootstrap, CSS custom, HTMX
   - Navigation globale, footer
   - Structure HTML parente
1. **Base layout** (`layouts/base.html`)

### Templates (Jinja2)

## Conventions

```
    └── fonts/        # Polices personnalisées
    ├── images/       # Images et icônes
    ├── js/           # Modules JavaScript (ES6)
    ├── css/          # Feuilles de style custom (variables CSS, composants custom)
└── static/           # Ressources statiques
│   └── pages/        # Pages complètes (héritent des layouts)
│   ├── components/   # Fragments réutilisables (navbar, sidebar, pagination, etc.)
│   ├── layouts/      # Mise en page parente (base.html, auth_layout.html, etc.)
├── templates/         # Modèles Jinja2 serveur
frontend/
```

## Structure

# Frontend

"""
Frontend README — HTMX + Bootstrap 5 UI structure

