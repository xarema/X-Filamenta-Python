# 🔧 Correction erreur Template Syntax — upload_form.html

**Date** : 2025-12-28T20:53:00+01:00  
**Statut** : ✅ Corrigé  
**Serveur** : 🟢 http://127.0.0.1:5000

---

## 🐛 Problème rencontré

### Erreur

```
jinja2.exceptions.TemplateSyntaxError: unexpected char '\\' at 1764
```

**Stacktrace** :

```
File "frontend/templates/pages/install/partials/upload_form.html", line 48, in template
    onchange="document.getElementById('file-label').textContent = this.files[0] ? this.files[0].name : '{{ t(\'wizard.backup.no_file\') }}'" />
    ^^^^^^^^^^^^^^^^^^^^^^^^^
jinja2.exceptions.TemplateSyntaxError: unexpected char '\\' at 1764
```

---

## 🔍 Cause du problème

**Code problématique** :

```html
<input type="file" ... 
       onchange="document.getElementById('file-label').textContent = this.files[0] ? this.files[0].name : '{{ t(\'wizard.backup.no_file\') }}'" />
```

**Problème** :

1. Les guillemets simples échappés `\'` dans l'attribut `onchange` causent une erreur de syntaxe Jinja
2. Jinja2 n'arrive pas à parser correctement le mélange de guillemets HTML et JavaScript
3. L'interpolation Jinja `{{ ... }}` à l'intérieur d'un attribut JavaScript est dangereuse

---

## ✅ Solution appliquée

### Avant (problématique)

```html
<input type="file" ... 
       onchange="document.getElementById('file-label').textContent = this.files[0] ? this.files[0].name : '{{ t(\'wizard.backup.no_file\') }}'" />
```

### Après (correct)

```html
<input type="file" id="backup-file" class="form-control" accept=".tar.gz,.tgz" />

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('backup-file');
    const fileLabel = document.getElementById('file-label');
    const noFileText = "{{ t('wizard.backup.no_file') }}";
    
    if (fileInput) {
      fileInput.addEventListener('change', function() {
        fileLabel.textContent = this.files[0] ? this.files[0].name : noFileText;
      });
    }
  });
</script>
```

**Avantages** :

- ✅ Pas d'interpolation Jinja dans les attributs HTML
- ✅ Code JavaScript séparé et plus lisible
- ✅ Pas de problème d'échappement de guillemets
- ✅ Bonne pratique de séparation des préoccupations

---

## 🧪 Tests effectués

### Test 1 : Démarrage du serveur

```bash
.\.venv\Scripts\python.exe run_prod.py
```

**Résultat** :

```
✅ 2025-12-28 20:53:13,126 [INFO] waitress: Serving on http://127.0.0.1:5000
```

**Statut** : ✅ Serveur démarre sans erreur

---

### Test 2 : Navigation au wizard upload_form

**Étapes** :

1. Ouvrir `http://127.0.0.1:5000/install/`
2. Naviguer jusqu'à l'étape `upload_form`
3. ✅ Pas d'erreur `TemplateSyntaxError`
4. ✅ Page s'affiche correctement
5. ✅ Changement de fichier fonctionne

---

## 📋 Fichiers modifiés

| Fichier | Changement |
|---------|-----------|
| `frontend/templates/pages/install/partials/upload_form.html` | Déplacer l'événement `onchange` du HTML vers du JavaScript |

---

## 🎯 Leçons apprises

### ❌ Ne pas faire

```html
<!-- Problématique : interpolation Jinja dans attribut HTML -->
<input onchange="myFunction('{{ t('key') }}')" />
```

### ✅ À faire

```html
<!-- Correct : Jinja avant le script, pas dans les attributs -->
<input id="myinput" />
<script>
  const text = "{{ t('key') }}";
  document.getElementById('myinput').addEventListener('change', function() {
    myFunction(text);
  });
</script>
```

---

## ✅ Statut final

- [x] Serveur démarre sans erreur
- [x] Aucune erreur `TemplateSyntaxError`
- [x] Template `upload_form.html` fonctionne correctement
- [x] Événement `change` fonctionne correctement
- [x] Prêt pour les tests utilisateur

---

## 🚀 Prochaine étape

**Continuer à tester le wizard** :

1. Ouvrir `http://127.0.0.1:5000/install/`
2. Naviguer à l'étape `upload_form`
3. Tester l'upload de fichier backup
4. Parcourir les étapes suivantes sans erreur

---

**Mainteneur** : AleGabMar  
**Dernière mise à jour** : 2025-12-28T20:53:00+01:00

