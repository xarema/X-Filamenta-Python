# Stack UI/UX — X-Filamenta-Python

**Version:** 0.0.1-Alpha  
**Date:** 2025-12-27  
**License:** AGPL-3.0-or-later

---

## 📋 Résumé exécutif

**Stack recommandée :**

```
Flask + Jinja2 + Bootstrap 5 + CSS Variables (tokens) + Tabulator + jsPDF/autoTable
+ HTMX (interactions) + Alpine.js (UI petits comportements)
```

**Résultat :** UI simple et pro, thèmes sans casser le layout, tableaux dynamiques, export CSV/PDF.

---

## 🎯 Objectifs UI

### 1. App publique

- Design simple et clair
- Pages stables (pas de changements constants)
- SEO-friendly (rendu serveur)

### 2. Espace utilisateur

- Préférences UI (afficher/masquer texte sur boutons, thème, etc.)
- Interactions fluides sans reload complet
- Responsive et accessible

### 3. Espace admin

- UI simple et intuitive
- CRUD complets (utilisateurs, thèmes, contenu)
- DataGrids interactifs (recherche, tri, filtres, pagination)

### 4. Système de thèmes

- **Changent UNIQUEMENT :** couleurs, textes, style boutons (arrondi/carré)
- **NE changent JAMAIS :** disposition, taille des blocs, structure HTML
- Implémentation : CSS Variables (tokens)

---

## 🛠️ Stack détaillée

### 1. Rendu & composants

#### Flask + Jinja2

```python
# Avantages
✅ Rendu serveur (SEO-friendly)
✅ Contexte facile (variables disponibles dans templates)
✅ Sécurité native (escaping HTML)
✅ Simple à maintenir
```

Exemple :

```html
<!-- frontend/templates/layouts/base.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>{% block title %}Default{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}" />
  </head>
  <body>
    {% include "components/navbar.html" %} {% block content %}{% endblock %} {% include
    "components/footer.html" %}
  </body>
</html>
```

#### Bootstrap 5

```
Avantages :
✅ Base UI pro et rapide (forms, navbar, tables, modals)
✅ Grid system responsive
✅ Composants prêts à l'emploi
✅ Classe utilities (mt-3, p-2, etc.)
```

Installation :

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
  rel="stylesheet"
/>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

#### CSS Variables (Design Tokens)

```css
/* frontend/css/tokens/variables.css */

:root {
  /* Couleurs */
  --color-primary: #0d6efd;
  --color-success: #198754;
  --text-primary: #212529;
  --bg-primary: #ffffff;

  /* Typographie */
  --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto...;
  --font-size-base: 1rem;
  --h1-font-size: 2.5rem;

  /* Espacement */
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;

  /* Bordures */
  --border-radius-md: 0.375rem;
  --border-radius-full: 9999px;

  /* Transitions */
  --transition-duration: 150ms;
}

/* Thème sombre (override) */
[data-theme="dark"] {
  --color-primary: #0d6efd;
  --text-primary: #f8f9fa;
  --bg-primary: #212529;
}
```

Utilisation dans CSS :

```css
.btn-primary {
  background-color: var(--color-primary);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-duration) ease-in-out;
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
}
```

---

### 2. Tableaux dynamiques (DataGrid)

#### Tabulator

```javascript
// frontend/js/plugins/tabulator.js

function initTabulator(containerId, columns, data = [], options = {}) {
  return new Tabulator(`#${containerId}`, {
    data: data,
    columns: columns,
    layout: "fitColumns",
    pagination: "local",
    paginationSize: 25,
    responsiveLayout: "collapse",
    movableColumns: true,
    selectable: "highlight",
  });
}
```

Utilisation :

```html
<div id="myTable"></div>

<script>
  const columns = [
    { title: "ID", field: "id", width: 80 },
    { title: "Nom", field: "name" },
    { title: "Email", field: "email" },
  ];

  const data = [
    { id: 1, name: "Jean", email: "jean@example.com" },
    { id: 2, name: "Marie", email: "marie@example.com" },
  ];

  const table = initTabulator("myTable", columns, data);
</script>
```

**Fonctionnalités :**

- ✅ Recherche live
- ✅ Tri multi-colonnes
- ✅ Filtres
- ✅ Pagination
- ✅ Export CSV/PDF
- ✅ Responsive

---

### 3. Export PDF

#### jsPDF + autoTable

```javascript
// frontend/js/plugins/tabulator.js

function exportTableToPDF(table, filename = "export.pdf") {
  if (typeof jsPDF === "undefined") return;

  const data = table.getData();
  const columns = table.getColumns().map((col) => col.getDefinition().title);
  const rows = data.map((row) => table.getColumns().map((col) => row[col.getField()]));

  const { jsPDF } = window;
  const doc = new jsPDF();

  doc.autoTable({
    head: [columns],
    body: rows,
  });

  doc.save(filename);
}
```

Installation :

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>
```

---

### 4. Interactions (HTMX)

#### HTMX pour interactivité sans reload

```html
<!-- Sauvegarder une préférence sans reload -->
<button hx-post="/api/preferences/show-text" hx-target="#feedback" hx-swap="innerHTML">
  Toggle Text
</button>

<div id="feedback"></div>
```

Backend (Flask) :

```python
@app.post('/api/preferences/<pref>')
def set_preference(pref):
    value = request.json.get('value')
    # Sauvegarder en session/BD
    return f'<p>Préférence {pref} = {value}</p>'
```

---

### 5. Petits comportements UI (Alpine.js)

#### Alpine pour toggle, dropdown, modal

```javascript
// frontend/js/plugins/alpine-utils.js

function toggleComponent(property) {
  return {
    [property]: false,
    toggle() {
      this[property] = !this[property];
    },
  };
}

function dropdownComponent() {
  return {
    isOpen: false,
    toggle() {
      this.isOpen = !this.isOpen;
    },
  };
}
```

Utilisation HTML :

```html
<!-- Toggle -->
<div x-data="toggleComponent('isOpen')">
  <button @click="toggle()">Toggle</button>
  <div x-show="isOpen">Contenu caché</div>
</div>

<!-- Dropdown -->
<div x-data="dropdownComponent()">
  <button @click="toggle()">Menu</button>
  <ul x-show="isOpen">
    <li><a href="#">Option 1</a></li>
    <li><a href="#">Option 2</a></li>
  </ul>
</div>
```

---

## 📁 Structure des fichiers

```
frontend/
├── css/
│   ├── tokens/
│   │   └── variables.css           ← Design tokens (CSS vars)
│   └── main.css                    ← Styles principaux + Bootstrap
│
├── js/
│   ├── plugins/
│   │   ├── tabulator.js            ← DataGrid setup
│   │   ├── alpine-utils.js         ← Alpine.js helpers
│   │   └── htmx-utils.js           ← HTMX config
│   └── components/
│       └── (custom JS future)
│
└── templates/
    ├── layouts/
    │   └── base.html               ← Layout principal
    ├── components/
    │   ├── navbar.html             ← Navigation
    │   └── footer.html             ← Pied de page
    ├── pages/
    │   ├── index.html              ← Accueil public
    │   └── datagrid-example.html   ← Exemple DataGrid
    └── admin/
        └── dashboard.html          ← Tableau de bord admin
```

---

## 🎨 Thèmes (CSS Variables)

### Changement de thème

```html
<button @click="toggleTheme()">🌙 Thème</button>

<script>
  function toggleTheme() {
    const html = document.documentElement;
    const theme = html.getAttribute("data-theme");
    const newTheme = theme === "dark" ? "light" : "dark";

    html.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  }
</script>
```

### CSS du thème

```css
/* Thème clair (défaut) */
:root {
  --color-primary: #0d6efd;
  --text-primary: #212529;
  --bg-primary: #ffffff;
}

/* Thème sombre */
[data-theme="dark"] {
  --color-primary: #0d6efd;
  --text-primary: #f8f9fa;
  --bg-primary: #212529;
}
```

**Points clés :**

- ✅ SEULES les couleurs changent
- ✅ Pas de changement de layout
- ✅ Pas de changement de taille des blocs
- ✅ Stocké en localStorage (persiste)

---

## 📊 Performance

### Optimisations

- ✅ CSS minimal (variables, utilities Bootstrap)
- ✅ JS léger (Alpine, HTMX)
- ✅ Tabulator optimisé (pagination 25 rows)
- ✅ Debounce sur recherche (300ms)
- ✅ Lazy loading images (si applicable)

### Limitations respectées

- **Tabulator :** OK jusqu'à ~1000 lignes avec pagination + debounce
- **Alpine.js :** OK pour <20 composants interactifs
- **CSS :** OK pour ~1000 lignes

---

## 🔒 Sécurité & Attribution

### Footer avec attribution (AGPL-3.0)

```html
<!-- frontend/templates/components/footer.html -->

<footer class="footer">
  <p>
    © 2025 <strong>AleGabMar</strong>. Sous licence
    <a href="https://www.gnu.org/licenses/agpl-3.0.html"> AGPL-3.0-or-later </a>.
  </p>
  <a href="#legal" data-toggle="modal">Mentions légales</a>
</footer>
```

### Modal légal

```html
<div class="modal" id="legal">
  <h5>Auteur: AleGabMar</h5>
  <p>Licence: AGPL-3.0-or-later</p>
  <p><a href="https://github.com/xarema/X-Filamenta-Python">Code source</a></p>
</div>
```

---

## ✅ Checklist implémentation

- [x] CSS Variables (tokens)
- [x] Bootstrap 5 intégré
- [x] Tabulator DataGrid
- [x] HTMX setup
- [x] Alpine.js utils
- [x] Thèmes (light/dark)
- [x] Footer avec attribution
- [x] Templates de base
- [x] Admin dashboard
- [ ] Tests de thème
- [ ] Optimisations performance
- [ ] SEO metadata

---

## 📚 Ressources

- [Bootstrap 5](https://getbootstrap.com/)
- [Tabulator](https://tabulator.info/)
- [HTMX](https://htmx.org/)
- [Alpine.js](https://alpinejs.dev/)
- [jsPDF](https://github.com/parallax/jsPDF)

---

## 🚀 Prochaines étapes

1. **Développement :** Ajouter routes Flask pour pages
2. **Thèmes :** Créer variantes de couleurs
3. **Admin CRUD :** Implémenter endpoints
4. **Tests :** Vérifier responsive + a11y
5. **Performance :** Profiler et optimiser

---

**Stack UI/UX validée et prête pour développement !** 🎉
