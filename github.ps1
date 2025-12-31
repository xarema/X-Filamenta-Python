@"
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔍 ANALYSE ET PUSH GITHUB - X-Filamenta-Python" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# ÉTAPE 1:  VÉRIFICATION DES FICHIERS CRITIQUES
# ============================================================================
Write-Host "1️⃣ VÉRIFICATION DES FICHIERS CRITIQUES" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

`$criticalFiles = @(
    "package.json",
    "package-lock.json",
    ". github/workflows/ci.yml",
    "requirements.txt",
    "requirements-dev.txt"
)

`$missingFiles = @()
foreach (`$file in `$criticalFiles) {
    if (Test-Path `$file) {
        Write-Host "  ✅ `$file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ `$file MANQUANT!" -ForegroundColor Red
        `$missingFiles += `$file
    }
}

if (`$missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️ ATTENTION: Fichiers critiques manquants!" -ForegroundColor Red
    Write-Host "Voulez-vous continuer quand même?  (O/N)" -ForegroundColor Yellow
    `$continue = Read-Host
    if (`$continue -ne "O") {
        Write-Host "❌ Opération annulée" -ForegroundColor Red
        exit
    }
}

Write-Host ""

# ============================================================================
# ÉTAPE 2: VALIDATION FRONTEND (npm)
# ============================================================================
Write-Host "2️⃣ VALIDATION FRONTEND (npm)" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

if (Test-Path "package.json") {
    # Vérifier la syntaxe JSON
    try {
        `$packageJson = Get-Content package.json -Raw | ConvertFrom-Json
        Write-Host "  ✅ package.json valide" -ForegroundColor Green

        # Vérifier la version Prettier
        if (`$packageJson.devDependencies.prettier) {
            Write-Host "  ✅ Prettier:  `$(`$packageJson.devDependencies.prettier)" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ❌ package.json INVALIDE!" -ForegroundColor Red
        Write-Host "  Erreur:  `$_" -ForegroundColor Red
        exit
    }

    # Vérifier package-lock.json
    if (Test-Path "package-lock. json") {
        Write-Host "  ✅ package-lock.json présent" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ package-lock. json MANQUANT (générer avec 'npm install')" -ForegroundColor Yellow
    }

    # Lancer les validations npm
    Write-Host ""
    Write-Host "  🧪 Lancement de npm run validate..." -ForegroundColor Cyan

    npm run validate 2>&1 | Out-Null

    if (`$LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Validation npm réussie" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Validation npm a des warnings" -ForegroundColor Yellow
        Write-Host "  Détails:" -ForegroundColor Gray
        npm run validate
        Write-Host ""
        Write-Host "Continuer malgré les warnings? (O/N)" -ForegroundColor Yellow
        `$continue = Read-Host
        if (`$continue -ne "O") {
            Write-Host "❌ Opération annulée" -ForegroundColor Red
            Write-Host "💡 Corrigez avec:  npm run lint: fix && npm run fmt" -ForegroundColor Cyan
            exit
        }
    }
} else {
    Write-Host "  ⚠️ Pas de package.json (frontend non configuré)" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# ÉTAPE 3: VALIDATION PYTHON
# ============================================================================
Write-Host "3️⃣ VALIDATION PYTHON" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

if (Test-Path "requirements.txt") {
    Write-Host "  ✅ requirements.txt présent" -ForegroundColor Green

    # Vérifier la syntaxe Python (fichiers . py dans backend/)
    if (Test-Path "backend") {
        `$pyFiles = Get-ChildItem -Path backend -Filter *.py -Recurse
        Write-Host "  📁 `$(`$pyFiles.Count) fichiers Python trouvés" -ForegroundColor Cyan

        # Test syntaxe Python basique
        `$pythonErrors = @()
        foreach (`$file in `$pyFiles | Select-Object -First 5) {
            python -m py_compile `$file. FullName 2>&1 | Out-Null
            if (`$LASTEXITCODE -ne 0) {
                `$pythonErrors += `$file.Name
            }
        }

        if (`$pythonErrors.Count -eq 0) {
            Write-Host "  ✅ Syntaxe Python OK (échantillon)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Erreurs Python détectées:" -ForegroundColor Red
            `$pythonErrors | ForEach-Object { Write-Host "     - `$_" -ForegroundColor Red }
            exit
        }
    }
} else {
    Write-Host "  ⚠️ requirements.txt manquant" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# ÉTAPE 4: VÉRIFICATION WORKFLOW CI/CD
# ============================================================================
Write-Host "4️⃣ VÉRIFICATION WORKFLOW CI/CD" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

if (Test-Path ".github/workflows/ci.yml") {
    `$ciContent = Get-Content . github/workflows/ci.yml -Raw

    # Vérifier les erreurs courantes
    `$issues = @()

    if (`$ciContent -match '\./\.\s+venv') {
        `$issues += "Espace dans '. /. venv' détecté (doit être '. /. venv')"
    }

    if (`$ciContent -notmatch 'package-lock\. json' -and `$ciContent -match 'cache:\s*npm') {
        `$issues += "Cache npm activé mais package-lock.json peut être manquant"
    }

    if (`$issues.Count -eq 0) {
        Write-Host "  ✅ Workflow CI/CD semble correct" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Problèmes potentiels détectés:" -ForegroundColor Yellow
        `$issues | ForEach-Object { Write-Host "     - `$_" -ForegroundColor Yellow }
        Write-Host ""
        Write-Host "Continuer malgré ces problèmes? (O/N)" -ForegroundColor Yellow
        `$continue = Read-Host
        if (`$continue -ne "O") {
            exit
        }
    }
} else {
    Write-Host "  ⚠️ Pas de workflow CI/CD configuré" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# ÉTAPE 5: STATUT GIT
# ============================================================================
Write-Host "5️⃣ STATUT GIT" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

`$status = git status --porcelain
if (`$status) {
    Write-Host "  📝 Fichiers modifiés:" -ForegroundColor Cyan
    git status --short | ForEach-Object { Write-Host "     `$_" -ForegroundColor White }

    `$fileCount = (`$status | Measure-Object).Count
    Write-Host ""
    Write-Host "  📊 Total:  `$fileCount fichier(s) modifié(s)" -ForegroundColor Cyan
} else {
    Write-Host "  ℹ️ Aucune modification à committer" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Dépôt à jour!" -ForegroundColor Green
    exit
}

Write-Host ""

# ============================================================================
# ÉTAPE 6: RÉSUMÉ ET CONFIRMATION
# ============================================================================
Write-Host "6️⃣ RÉSUMÉ" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

Write-Host "  📦 Fichiers critiques:     " -NoNewline
if (`$missingFiles.Count -eq 0) {
    Write-Host "✅ OK" -ForegroundColor Green
} else {
    Write-Host "⚠️ `$(`$missingFiles.Count) manquant(s)" -ForegroundColor Yellow
}

Write-Host "  🎨 Validation frontend:   " -NoNewline
if (Test-Path "package.json") {
    Write-Host "✅ OK" -ForegroundColor Green
} else {
    Write-Host "⚠️ Non configuré" -ForegroundColor Yellow
}

Write-Host "  🐍 Validation Python:     " -NoNewline
if (Test-Path "requirements.txt") {
    Write-Host "✅ OK" -ForegroundColor Green
} else {
    Write-Host "⚠️ Non configuré" -ForegroundColor Yellow
}

Write-Host "  ⚙️ Workflow CI/CD:         " -NoNewline
if (Test-Path ".github/workflows/ci.yml") {
    Write-Host "✅ OK" -ForegroundColor Green
} else {
    Write-Host "⚠️ Non configuré" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# ÉTAPE 7: DEMANDE DE CONFIRMATION
# ============================================================================
Write-Host "❓ Voulez-vous envoyer ces modifications sur GitHub?" -ForegroundColor Yellow
Write-Host ""
Write-Host "   [O] Oui, envoyer maintenant" -ForegroundColor Green
Write-Host "   [N] Non, annuler" -ForegroundColor Red
Write-Host "   [V] Voir les différences (git diff)" -ForegroundColor Cyan
Write-Host ""
`$choice = Read-Host "Votre choix"

if (`$choice -eq "V") {
    Write-Host ""
    Write-Host "📊 Différences:" -ForegroundColor Cyan
    git diff
    Write-Host ""
    Write-Host "Continuer avec le push? (O/N)" -ForegroundColor Yellow
    `$choice = Read-Host
}

if (`$choice -ne "O") {
    Write-Host ""
    Write-Host "❌ Opération annulée" -ForegroundColor Red
    exit
}

Write-Host ""

# ============================================================================
# ÉTAPE 8: MESSAGE DE COMMIT
# ============================================================================
Write-Host "💬 Message de commit:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   [1] fix: update CI configuration and add missing files" -ForegroundColor Cyan
Write-Host "   [2] chore: update dependencies and fix linting" -ForegroundColor Cyan
Write-Host "   [3] feat: add new frontend tooling configuration" -ForegroundColor Cyan
Write-Host "   [4] Personnalisé" -ForegroundColor Cyan
Write-Host ""
`$commitChoice = Read-Host "Votre choix (1-4)"

switch (`$commitChoice) {
    "1" { `$commitMessage = "fix: update CI configuration and add missing files" }
    "2" { `$commitMessage = "chore: update dependencies and fix linting" }
    "3" { `$commitMessage = "feat: add new frontend tooling configuration" }
    "4" {
        Write-Host ""
        `$commitMessage = Read-Host "Entrez votre message de commit"
    }
    default { `$commitMessage = "fix: update project configuration" }
}

Write-Host ""

# ============================================================================
# ÉTAPE 9: GIT ADD, COMMIT, PUSH
# ============================================================================
Write-Host "🚀 ENVOI SUR GITHUB" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Add
Write-Host "  ➕ git add..." -ForegroundColor Cyan
git add .

if (`$LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Erreur lors de git add" -ForegroundColor Red
    exit
}
Write-Host "  ✅ Fichiers ajoutés" -ForegroundColor Green

# Commit
Write-Host "  💾 git commit..." -ForegroundColor Cyan
git commit -m "`$commitMessage"

if (`$LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Erreur lors de git commit" -ForegroundColor Red
    exit
}
Write-Host "  ✅ Commit créé" -ForegroundColor Green

# Push
Write-Host "  📤 git push..." -ForegroundColor Cyan
git push origin main

if (`$LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Erreur lors de git push" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Essayez:" -ForegroundColor Yellow
    Write-Host "   git pull origin main" -ForegroundColor White
    Write-Host "   git push origin main" -ForegroundColor White
    exit
}

Write-Host "  ✅ Push réussi!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# ÉTAPE 10: RÉSULTAT FINAL
# ============================================================================
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ SUCCÈS - Code envoyé sur GitHub!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Récupérer le hash du commit
`$commitHash = git rev-parse --short HEAD

Write-Host "📋 Informations du commit:" -ForegroundColor Cyan
Write-Host "   Hash:     `$commitHash" -ForegroundColor White
Write-Host "   Message: `$commitMessage" -ForegroundColor White
Write-Host "   Branch:  main" -ForegroundColor White
Write-Host ""

Write-Host "🔗 Liens utiles:" -ForegroundColor Cyan
Write-Host "   Dépôt:   https://github.com/xarema/X-Filamenta-Python" -ForegroundColor White
Write-Host "   Commit:  https://github.com/xarema/X-Filamenta-Python/commit/`$commitHash" -ForegroundColor White
Write-Host "   Actions: https://github.com/xarema/X-Filamenta-Python/actions" -ForegroundColor White
Write-Host ""

Write-Host "⏱️ Le workflow CI/CD devrait démarrer dans quelques secondes..." -ForegroundColor Yellow
Write-Host ""

# Proposition d'ouvrir le navigateur
Write-Host "Ouvrir la page GitHub Actions?  (O/N)" -ForegroundColor Yellow
`$openBrowser = Read-Host

if (`$openBrowser -eq "O") {
    Start-Process "https://github.com/xarema/X-Filamenta-Python/actions"
}

Write-Host ""
Write-Host "✨ Terminé!" -ForegroundColor Green
Write-Host ""
"@ | Set-Content -Path "push-github.ps1" -Encoding UTF8

Write-Host "✅ Fichier push-github.ps1 créé avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Pour l'utiliser:" -ForegroundColor Cyan
Write-Host "   .\push-github.ps1" -ForegroundColor White
Write-Host ""
