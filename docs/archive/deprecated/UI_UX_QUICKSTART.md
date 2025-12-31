# Guide rapide UI/UX — X-Filamenta-Python

**Version:** 0.0.1-Alpha  
**Date:** 2025-12-27

---

## 📁 Structure du projet UI

```
frontend/
├── css/tokens/variables.css    ← Définir les couleurs, espacements, etc.
├── css/main.css               ← Styles Bootstrap + customs
├── js/plugins/
│   ├── tabulator.js           ← DataGrid
│   ├── alpine-utils.js        ← Petits comportements (toggle, dropdown)
│   └── htmx-utils.js          ← Interactions sans reload
└── templates/
    ├── layouts/base.html      ← Layout principal
    ├── components/            ← Réutilisables (navbar, footer)
    ├── pages/                 ← Pages publiques
    └── admin/                 ← Pages admin
```

---

## 🎨 Créer une nouvelle page

### 1. Créer le fichier template

```html
<!-- frontend/templates/pages/my-page.html -->
{% extends "layouts/base.html" %} {% block title %}Mon titre - X-Filamenta{% endblock %}
{% block content %}
<div class="container py-4">
  <h1>Ma page</h1>
  <p>Contenu ici</p>
</div>
{% endblock %}
```

### 2. Ajouter la route Flask

```python
# backend/src/routes/__init__.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/my-page')
def my_page():
    return render_template('pages/my-page.html')
```

### 3. Enregistrer le blueprint

```python
# backend/src/app.py
from backend.src.routes import main

def create_app(config=None):
    # ...
    app.register_blueprint(main)
    return app
```

---

## 🎨 Changer les couleurs (thème)

### 1. Éditer les variables CSS

```css
/* frontend/css/tokens/variables.css */

:root {
  --color-primary: #0d6efd;        ← Changer cette couleur
  --color-success: #198754;
  --text-primary: #212529;
  /* ... */
}
```

### 2. Ajouter un thème alternatif

```css
[data-theme="custom-blue"] {
  --color-primary: #1e90ff;        ← Nouvelle couleur primaire
  --color-success: #00aa00;        ← Nouvelle couleur succès
  --text-primary: #1a1a2e;
}
```

### 3. Changer le thème en JS

```javascript
document.documentElement.setAttribute("data-theme", "custom-blue");
localStorage.setItem("theme", "custom-blue");
```

---

## 📊 Créer un DataGrid (Tabulator)

### 1. Préparer les données

```python
# backend/src/routes/__init__.py
@main.route('/users')
def users():
    users_list = [
        {'id': 1, 'name': 'Jean', 'email': 'jean@example.com'},
        {'id': 2, 'name': 'Marie', 'email': 'marie@example.com'},
    ]
    return render_template('pages/users.html', users=users_list)
```

### 2. Créer le template

```html
<!-- frontend/templates/pages/users.html -->
{% extends "layouts/base.html" %} {% block content %}
<div class="container py-4">
  <h1>Utilisateurs</h1>

  <!-- Barre de recherche -->
  <input
    type="text"
    id="searchInput"
    class="form-control mb-3"
    placeholder="Rechercher..."
  />

  <!-- Boutons export -->
  <div class="mb-3">
    <button class="btn btn-success" id="exportCSV">📥 CSV</button>
    <button class="btn btn-danger" id="exportPDF">📕 PDF</button>
  </div>

  <!-- Table -->
  <div id="usersTable"></div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const columns = [
      { title: 'ID', field: 'id', width: 80 },
      { title: 'Nom', field: 'name' },
      { title: 'Email', field: 'email' },
    ];

    const data = {{ users | tojson }};  ← Passer les données Flask

    window.table = initTabulator('usersTable', columns, data);

    // Recherche
    document.getElementById('searchInput').addEventListener('input', debounce(function(e) {
      filterTableBySearch(window.table, e.target.value);
    }, 300));

    // Export
    document.getElementById('exportCSV').onclick = () =>
      exportTableToCSV(window.table, 'users.csv');

    document.getElementById('exportPDF').onclick = () =>
      exportTableToPDF(window.table, 'users.pdf');
  });
</script>
{% endblock %}
```

---

## 🔘 Ajouter une interaction (Toggle/Dropdown/Modal)

### Toggle

```html
<div x-data="toggleComponent('isOpen')">
  <button @click="toggle()" class="btn btn-primary">
    {{ isOpen ? 'Masquer' : 'Afficher' }}
  </button>
  <div x-show="isOpen" class="mt-3">
    <p>Contenu caché</p>
  </div>
</div>
```

### Dropdown

```html
<div x-data="dropdownComponent()">
  <button class="btn btn-primary" @click="toggle()">Menu ▼</button>
  <ul class="dropdown-menu" x-show="isOpen">
    <li><a href="#">Option 1</a></li>
    <li><a href="#">Option 2</a></li>
  </ul>
</div>
```

### Modal

```html
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
  Ouvrir Modal
</button>

<div class="modal fade" id="myModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Titre</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p>Contenu...</p>
      </div>
    </div>
  </div>
</div>
```

---

## 📝 Interaction sans reload (HTMX)

### 1. Template

```html
<form hx-post="/api/save-preference" hx-target="#feedback" hx-swap="innerHTML">
  <label> <input type="checkbox" name="show_text" /> Afficher texte </label>

  <button type="submit" class="btn btn-primary">Enregistrer</button>
</form>

<div id="feedback"></div>
```

### 2. Route Flask

```python
@main.post('/api/save-preference')
def save_preference():
    show_text = request.form.get('show_text') == 'on'
    # Sauvegarder la préférence
    return '<p class="alert alert-success">✓ Enregistré!</p>'
```

---

## 🎯 Bonnes pratiques

### ✅ DO

- Utiliser CSS Variables pour les couleurs
- Nommer les classes : `.btn-primary`, `.card`, `.table`
- Utiliser Bootstrap utilities : `mt-3`, `p-4`, `text-center`
- Structurer templates avec `{% extends %}` et `{% include %}`
- Débouncer les recherches (300ms minimum)

### ❌ DON'T

- Hardcoder des couleurs (#0d6efd au lieu de var(--color-primary))
- Mélanger inline styles et CSS
- Créer trop de classes CSS custom
- Changer le layout pour les thèmes (seulement couleurs!)
- Charger de gros datasets sans pagination

---

## 🧪 Tester localement

```bash
# 1. Activer l'env virtuel
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Démarrer Flask
python -m backend.src

# 4. Ouvrir le navigateur
# http://localhost:5000
```

---

## 📊 Exemples rapides

### Bouton avec couleur primaire

```html
<button class="btn btn-primary">Cliquez-moi</button>
```

### Carte (Card)

```html
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Titre</h5>
    <p class="card-text">Texte...</p>
    <a href="#" class="btn btn-primary">Action</a>
  </div>
</div>
```

### Alerte

```html
<div class="alert alert-success">✓ Succès!</div>

<div class="alert alert-danger">✗ Erreur!</div>
```

### Formulaire

```html
<form>
  <div class="mb-3">
    <label for="name" class="form-label">Nom</label>
    <input type="text" class="form-control" id="name" name="name" />
  </div>

  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email" name="email" />
  </div>

  <button type="submit" class="btn btn-primary">Envoyer</button>
</form>
```

---

## 📚 Ressources rapides

- **Couleurs :** Éditer `frontend/css/tokens/variables.css`
- **Bootstrap :** https://getbootstrap.com/docs/5.3/
- **HTMX :** https://htmx.org/reference/
- **Alpine :** https://alpinejs.dev/
- **Tabulator :** https://tabulator.info/docs/5.4

---

## 🚀 Prochaines étapes

1. Tester la page d'accueil
2. Créer une page CRUD (admin)
3. Ajouter un DataGrid
4. Tester les thèmes (light/dark)
5. Optimiser les performances

---

**Besoin d'aide ?** Consulter `docs/UI_UX_STACK.md` pour plus de détails ! 🎉
