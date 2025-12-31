"""
Test script to validate ProductionConfig
Validates that production configuration is correct and secure
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("\n" + "="*70)
print(" Production Configuration Validation")
print("="*70 + "\n")

# Test 1: Import config module
print("🔍 Test 1: Importing configuration module...")
try:
    from backend.src.config import ProductionConfig, get_config
    print("   ✅ Config module imported successfully\n")
except Exception as e:
    print(f"   ❌ Failed to import config: {e}\n")
    sys.exit(1)

# Test 2: Load ProductionConfig
print("🔍 Test 2: Loading ProductionConfig...")
try:
    config = ProductionConfig()
    print("   ✅ ProductionConfig instantiated\n")
except Exception as e:
    print(f"   ❌ Failed to instantiate ProductionConfig: {e}\n")
    sys.exit(1)

# Test 3: Validate critical settings
print("🔍 Test 3: Validating critical security settings...")

checks = []

# Check DEBUG is False
if config.DEBUG is False:
    checks.append(("DEBUG = False", True))
    print("   ✅ DEBUG is False (secure)")
else:
    checks.append(("DEBUG = False", False))
    print("   ❌ DEBUG is True (INSECURE - must be False in production)")

# Check SQLALCHEMY_ECHO
if config.SQLALCHEMY_ECHO is False:
    checks.append(("SQLALCHEMY_ECHO = False", True))
    print("   ✅ SQLALCHEMY_ECHO is False (performance)")
else:
    checks.append(("SQLALCHEMY_ECHO = False", False))
    print("   ⚠️  SQLALCHEMY_ECHO is True (verbose logging)")

# Check SECRET_KEY exists and is not default
secret_key = config.SECRET_KEY
if secret_key:
    if secret_key != "dev-key-change-in-production-immediately":
        if len(secret_key) >= 32:
            checks.append(("SECRET_KEY (strong)", True))
            print(f"   ✅ SECRET_KEY is set and strong ({len(secret_key)} chars)")
        else:
            checks.append(("SECRET_KEY (strong)", False))
            print(f"   ⚠️  SECRET_KEY is short ({len(secret_key)} chars, recommended: 64+)")
    else:
        checks.append(("SECRET_KEY (not default)", False))
        print("   ❌ SECRET_KEY is default development key (INSECURE)")
else:
    checks.append(("SECRET_KEY exists", False))
    print("   ❌ SECRET_KEY is not set")

# Check DEPLOYMENT_TARGET
if config.DEPLOYMENT_TARGET == "production":
    checks.append(("DEPLOYMENT_TARGET = production", True))
    print("   ✅ DEPLOYMENT_TARGET is 'production'")
else:
    checks.append(("DEPLOYMENT_TARGET = production", False))
    print(f"   ⚠️  DEPLOYMENT_TARGET is '{config.DEPLOYMENT_TARGET}' (expected: 'production')")

# Check Session security
if config.SESSION_COOKIE_HTTPONLY is True:
    checks.append(("SESSION_COOKIE_HTTPONLY = True", True))
    print("   ✅ SESSION_COOKIE_HTTPONLY is True (XSS protection)")
else:
    checks.append(("SESSION_COOKIE_HTTPONLY = True", False))
    print("   ❌ SESSION_COOKIE_HTTPONLY is False (vulnerable to XSS)")

if config.SESSION_COOKIE_SAMESITE == "Lax":
    checks.append(("SESSION_COOKIE_SAMESITE = Lax", True))
    print("   ✅ SESSION_COOKIE_SAMESITE is 'Lax' (CSRF protection)")
else:
    checks.append(("SESSION_COOKIE_SAMESITE = Lax", False))
    print(f"   ⚠️  SESSION_COOKIE_SAMESITE is '{config.SESSION_COOKIE_SAMESITE}'")

print()

# Test 4: Database configuration
print("🔍 Test 4: Validating database configuration...")

if config.SQLALCHEMY_DATABASE_URI:
    checks.append(("Database URI configured", True))
    # Mask sensitive parts
    uri = config.SQLALCHEMY_DATABASE_URI
    if "://" in uri:
        scheme = uri.split("://")[0]
        print(f"   ✅ Database configured (type: {scheme})")
    else:
        print(f"   ✅ Database configured")

    # Check SQLAlchemy engine options
    if config.SQLALCHEMY_ENGINE_OPTIONS.get("pool_pre_ping"):
        checks.append(("Connection pool pre-ping enabled", True))
        print("   ✅ Connection pool pre-ping enabled (reliability)")

    pool_size = config.SQLALCHEMY_ENGINE_OPTIONS.get("pool_size", 0)
    if pool_size >= 10:
        checks.append(("Connection pool size adequate", True))
        print(f"   ✅ Connection pool size: {pool_size}")
    else:
        checks.append(("Connection pool size adequate", False))
        print(f"   ⚠️  Connection pool size: {pool_size} (recommended: 10+)")
else:
    checks.append(("Database URI configured", False))
    print("   ❌ Database URI not configured")

print()

# Test 5: Security headers
print("🔍 Test 5: Validating security headers configuration...")

if hasattr(config, "SECURE_HSTS_SECONDS") and config.SECURE_HSTS_SECONDS > 0:
    checks.append(("HSTS configured", True))
    print(f"   ✅ HSTS configured ({config.SECURE_HSTS_SECONDS} seconds)")
else:
    checks.append(("HSTS configured", False))
    print("   ⚠️  HSTS not configured")

print()

# Test 6: Validate production config function
print("🔍 Test 6: Testing validate_production_config()...")
try:
    ProductionConfig.validate_production_config()
    checks.append(("Production config validation passes", True))
    print("   ✅ Production config validation passed\n")
except ValueError as e:
    checks.append(("Production config validation passes", False))
    print(f"   ❌ Production config validation failed: {e}\n")

# Test 7: Test get_config function
print("🔍 Test 7: Testing get_config() function...")
try:
    prod_config = get_config("production")
    checks.append(("get_config('production') works", True))
    print("   ✅ get_config('production') returned valid config\n")
except Exception as e:
    checks.append(("get_config('production') works", False))
    print(f"   ❌ get_config('production') failed: {e}\n")

# Summary
print("="*70)
print(" Validation Summary")
print("="*70 + "\n")

passed = sum(1 for _, result in checks if result)
total = len(checks)
percentage = (passed / total * 100) if total > 0 else 0

print(f"Checks Passed: {passed}/{total} ({percentage:.1f}%)\n")

if percentage == 100:
    print("✅ ALL CHECKS PASSED - ProductionConfig is VALID")
    print("\nStatus: PRODUCTION-READY ✅")
    exit_code = 0
elif percentage >= 80:
    print("⚠️  MOST CHECKS PASSED - Minor issues detected")
    print("\nStatus: REVIEW WARNINGS ⚠️")
    print("\nRecommendation: Review warnings above before deployment")
    exit_code = 0
else:
    print("❌ MULTIPLE CHECKS FAILED - Action required")
    print("\nStatus: NOT PRODUCTION-READY ❌")
    print("\nRecommendation: Fix critical issues before deployment")
    exit_code = 1

print("\n" + "="*70 + "\n")

# Detailed recommendations
if exit_code != 0 or percentage < 100:
    print("Recommendations:\n")

    for check_name, result in checks:
        if not result:
            if "SECRET_KEY" in check_name:
                print("  - Generate strong SECRET_KEY:")
                print("    python -c \"import secrets; print(secrets.token_hex(32))\"")
            elif "DEBUG" in check_name:
                print("  - Set FLASK_DEBUG=False in .env")
            elif "Database" in check_name:
                print("  - Configure DATABASE_URL or DB_* variables in .env")
            elif "SESSION" in check_name:
                print("  - Configure session security settings in .env")

    print()

sys.exit(exit_code)

