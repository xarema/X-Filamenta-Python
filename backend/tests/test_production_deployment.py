#!/usr/bin/env python
"""
Test script for production deployment validation
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_app_creation():
    """Test that Flask app can be created successfully"""
    print("Testing Flask app creation...")
    try:
        from backend.src.app import create_app
        app = create_app()
        assert app is not None
        assert app.name == "backend.src"
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create Flask app: {e}")
        return False

def test_config_import():
    """Test that configuration modules can be imported"""
    print("\nTesting config import...")
    try:
        from backend.src.config import Config, ProductionConfig, DevelopmentConfig
        assert Config is not None
        assert ProductionConfig is not None
        assert DevelopmentConfig is not None
        print("✅ Configuration modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        return False

def test_production_validation():
    """Test ProductionConfig validation"""
    print("\nTesting ProductionConfig validation...")
    try:
        from backend.src.config import ProductionConfig

        # Set required environment variables for testing
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = 'False'
        os.environ['FLASK_SECRET_KEY'] = 'a7f3c5e9b1d4f8a2c6e1f4b9d2a5c8e1f7a3b6d9c2e5f8b1a4d7c0e3f6a9b2'

        result = ProductionConfig.validate_production_config()

        print(f"  Validation result: {result['valid']}")
        if result['errors']:
            print(f"  Errors: {result['errors']}")
        if result['warnings']:
            print(f"  Warnings: {result['warnings']}")

        if result['valid']:
            print("✅ ProductionConfig validation passed")
            return True
        else:
            print("⚠️  ProductionConfig has errors (see above)")
            return False
    except Exception as e:
        print(f"❌ Failed to validate config: {e}")
        return False

def test_database_uri_building():
    """Test that database URI is built correctly"""
    print("\nTesting database URI construction...")
    try:
        from backend.src.config import _build_database_uri

        # Test with SQLite (default)
        os.environ.pop('SQLALCHEMY_DATABASE_URI', None)
        os.environ['DB_TYPE'] = 'sqlite'
        uri = _build_database_uri()
        assert 'sqlite' in uri.lower()
        print(f"  SQLite URI: {uri[:50]}...")

        # Test with PostgreSQL
        os.environ['DB_TYPE'] = 'postgresql'
        os.environ['DB_USER'] = 'testuser'
        os.environ['DB_PASSWORD'] = 'testpass'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'testdb'
        uri = _build_database_uri()
        assert 'postgresql' in uri.lower()
        print(f"  PostgreSQL URI: {uri[:50]}...")

        print("✅ Database URI construction works correctly")
        return True
    except Exception as e:
        print(f"❌ Failed to build database URI: {e}")
        return False

def test_env_file_loaded():
    """Test that .env files can be loaded"""
    print("\nTesting .env file loading...")
    try:
        from dotenv import load_dotenv

        env_path = Path(__file__).parent.parent / ".env.production"
        if env_path.exists():
            load_dotenv(env_path)
            secret_key = os.getenv('FLASK_SECRET_KEY')
            db_type = os.getenv('DB_TYPE')

            if secret_key and db_type:
                print(f"  Loaded FLASK_SECRET_KEY: {secret_key[:16]}...")
                print(f"  Loaded DB_TYPE: {db_type}")
                print("✅ .env.production loaded successfully")
                return True
            else:
                print("❌ .env.production missing required variables")
                return False
        else:
            print("❌ .env.production not found")
            return False
    except Exception as e:
        print(f"❌ Failed to load .env: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("PRODUCTION DEPLOYMENT VALIDATION TESTS")
    print("=" * 80)

    tests = [
        test_app_creation,
        test_config_import,
        test_database_uri_building,
        test_env_file_loaded,
        test_production_validation,
    ]

    results = []
    for test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"❌ Unexpected error in {test_func.__name__}: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print("=" * 80)

    if all(results):
        print("\n✅ ALL TESTS PASSED - READY FOR DEPLOYMENT")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed - FIX BEFORE DEPLOYMENT")
        return 1

if __name__ == "__main__":
    sys.exit(main())

