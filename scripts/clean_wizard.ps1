#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Nettoyage rapide pour recommencer le wizard
.DESCRIPTION
    Supprime tous les fichiers d'installation pour permettre de retester le wizard
#>

param(
    [switch]$Force
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NETTOYAGE WIZARD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = "D:\xarema\X-Filamenta-Python"

if (-not $Force) {
    Write-Host "ATTENTION: Cette action va supprimer:" -ForegroundColor Yellow
    Write-Host "  - Le flag d'installation" -ForegroundColor White
    Write-Host "  - Toutes les bases de donnees" -ForegroundColor White
    Write-Host "  - L'utilisateur admin cree" -ForegroundColor White
    Write-Host ""
    Write-Host "Voulez-vous continuer? (O/N): " -NoNewline -ForegroundColor Yellow
    $confirm = Read-Host

    if ($confirm -ne 'O' -and $confirm -ne 'o') {
        Write-Host "Annule." -ForegroundColor Gray
        exit 0
    }
}

Write-Host ""
Write-Host "Nettoyage en cours..." -ForegroundColor Yellow

$ItemsToDelete = @(
    "$ProjectRoot\instance\installed.flag",
    "$ProjectRoot\instance\*.db",
    "$ProjectRoot\backend\instance\installed.flag",
    "$ProjectRoot\backend\instance\*.db"
)

$DeletedCount = 0

foreach ($pattern in $ItemsToDelete) {
    $items = Get-Item $pattern -ErrorAction SilentlyContinue
    if ($items) {
        foreach ($item in $items) {
            try {
                Remove-Item $item.FullName -Force
                Write-Host "  OK Supprime: $($item.Name)" -ForegroundColor Green
                $DeletedCount++
            } catch {
                Write-Host "  ERREUR: $($item.Name) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""

if ($DeletedCount -eq 0) {
    Write-Host "OK Rien a nettoyer - deja propre!" -ForegroundColor Green
} else {
    Write-Host "OK $DeletedCount fichier(s) supprime(s)" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PRET POUR LE WIZARD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Vous pouvez maintenant lancer:" -ForegroundColor White
Write-Host "  .\scripts\test_wizard_prod.ps1" -ForegroundColor Yellow
Write-Host ""

