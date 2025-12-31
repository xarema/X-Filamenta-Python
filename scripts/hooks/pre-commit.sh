#!/bin/bash
# Pre-commit Hook for Code Quality (Bash Version)
#
# Purpose: Enforce code quality standards before commit
# Description: Runs linting, formatting, type checking, i18n validation, and tests
#
# File: scripts/hooks/pre-commit.sh | Repository: X-Filamenta-Python
# Created: 2025-12-30
# Last modified (Git): TBD | Commit: TBD
#
# Distributed by:  XAREMA | Coder:  AleGabMar
# App version: 0.0.1-Alpha | File version: 1.0.0
#
# License:  AGPL-3.0-or-later
# SPDX-License-Identifier:  AGPL-3.0-or-later
#
# Copyright (c) 2025 XAREMA. All rights reserved. 
#
# Metadata:
# - Status: Stable
# - Classification: Internal
#
# Installation:
#   ln -s ../../scripts/hooks/pre-commit.sh . git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Usage:
#   Runs automatically on 'git commit'
#   Manual test: bash scripts/hooks/pre-commit. sh

set -e

echo "🔍 Running pre-commit checks..."
echo ""

ERROR_COUNT=0

# ---- Check if venv exists ----
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found (. venv/)"
    echo "   Create it with: python -m venv .venv"
    exit 1
fi

# ---- Python Linting (Ruff) ----
echo "📝 Checking code with Ruff..."
if . venv/bin/ruff check .; then
    echo "   ✅ Ruff linting passed"
else
    echo "   ❌ Ruff linting failed"
    ((ERROR_COUNT++))
fi
echo ""

# ---- Python Formatting (Ruff) ----
echo "🎨 Checking code formatting with Ruff..."
if . venv/bin/ruff format --check .; then
    echo "   ✅ Code formatting passed"
else
    echo "   ❌ Code formatting issues found"
    echo "      Fix with: . venv/bin/ruff format ."
    ((ERROR_COUNT++))
fi
echo ""

# ---- Type Checking (Mypy) ----
echo "🔍 Running type checker (Mypy)..."
if .venv/bin/mypy backend/src; then
    echo "   ✅ Type checking passed"
else
    echo "   ❌ Type checking failed"
    ((ERROR_COUNT++))
fi
echo ""

# ---- i18n Translation Check ----
echo "🌐 Checking i18n translations..."
if .venv/bin/python scripts/utils/check_i18n.py --strict; then
    echo "   ✅ i18n validation passed"
else
    echo "   ❌ i18n validation failed"
    ((ERROR_COUNT++))
fi
echo ""

# ---- Tests (Pytest) ----
echo "🧪 Running tests (pytest)..."
if .venv/bin/pytest --quiet; then
    echo "   ✅ All tests passed"
else
    echo "   ❌ Tests failed"
    ((ERROR_COUNT++))
fi
echo ""

# ---- Summary ----
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERROR_COUNT -eq 0 ]; then
    echo "✅ All pre-commit checks passed!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "❌ $ERROR_COUNT check(s) failed"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Fix the issues above before committing."
    echo ""
    echo "⚠️  To bypass this hook (NOT RECOMMENDED):"
    echo "   git commit --no-verify -m \"message\""
    exit 1
fi