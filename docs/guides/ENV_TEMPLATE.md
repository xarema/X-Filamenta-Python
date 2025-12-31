---
Purpose: Environment variables template for X-Filamenta-Python
Description: Complete .env template with all configuration options

File: docs/guides/ENV_TEMPLATE.md | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified: 2025-12-30

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public
---

# Environment Variables Template

This file provides a complete template for the `.env` configuration file used by X-Filamenta-Python.

**Instructions:**
1. Copy this file to your project root as `.env`
2. Replace placeholder values with your actual configuration
3. **Never commit `.env` to version control**

---

## Core Application Settings

```bash
# =============================================================================
# CORE APPLICATION
# =============================================================================

# Flask Environment (production, development, testing)
FLASK_ENV=production

# Secret key for session encryption (MUST be changed!)
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here-change-this-value

# Application name
APP_NAME="X-Filamenta"

# Debug mode (NEVER enable in production!)
FLASK_DEBUG=False
```

---

## Database Configuration

```bash
# =============================================================================
# DATABASE
# =============================================================================

# SQLite (Default - for development/small deployments)
DATABASE_URL=sqlite:///instance/x-filamenta_python.db

# PostgreSQL (Recommended for production)
# DATABASE_URL=postgresql://username:password@localhost:5432/x_filamenta

# MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/x_filamenta

# Database pool settings (optional)
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
SQLALCHEMY_POOL_RECYCLE=3600
```

---

## Cache Configuration

```bash
# =============================================================================
# CACHE
# =============================================================================

# Cache type (filesystem, redis, memcached)
CACHE_TYPE=filesystem

# Filesystem cache (if CACHE_TYPE=filesystem)
CACHE_DIR=instance/cache
CACHE_DEFAULT_TIMEOUT=300

# Redis cache (if CACHE_TYPE=redis)
# CACHE_TYPE=redis
# CACHE_REDIS_HOST=localhost
# CACHE_REDIS_PORT=6379
# CACHE_REDIS_DB=0
# CACHE_REDIS_PASSWORD=
# CACHE_KEY_PREFIX=x-filamenta:
```

---

## Session Configuration

```bash
# =============================================================================
# SESSIONS
# =============================================================================

# Session type (filesystem, redis)
SESSION_TYPE=filesystem

# Session cookie settings
SESSION_COOKIE_NAME=x_filamenta_session
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_DOMAIN=
SESSION_PERMANENT=True
PERMANENT_SESSION_LIFETIME=3600

# Filesystem sessions (if SESSION_TYPE=filesystem)
SESSION_FILE_DIR=instance/flask_session

# Redis sessions (if SESSION_TYPE=redis)
# SESSION_REDIS=redis://localhost:6379/1
```

---

## Email Configuration

```bash
# =============================================================================
# EMAIL
# =============================================================================

# Email server settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False

# Email credentials
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password

# Sender information
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
MAIL_SENDER_NAME="X-Filamenta"

# Email verification
EMAIL_VERIFICATION_REQUIRED=True
EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS=24

# Password reset
PASSWORD_RESET_TOKEN_EXPIRY_MINUTES=60
PASSWORD_RESET_RATE_LIMIT_PER_HOUR=2
```

---

## Security Settings

```bash
# =============================================================================
# SECURITY
# =============================================================================

# CSRF Protection
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
WTF_CSRF_SSL_STRICT=True

# Content Security Policy
CONTENT_SECURITY_POLICY="default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data: cdn.jsdelivr.net"

# Rate limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=memory://
# Or with Redis:
# RATELIMIT_STORAGE_URL=redis://localhost:6379/2

# 2FA Settings
TWO_FACTOR_REQUIRED=False
TWO_FACTOR_ISSUER_NAME="X-Filamenta"

# Password policy
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=True
PASSWORD_REQUIRE_LOWERCASE=True
PASSWORD_REQUIRE_DIGITS=True
PASSWORD_REQUIRE_SPECIAL=True

# Account lockout
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=1800
```

---

## File Upload Settings

```bash
# =============================================================================
# FILE UPLOADS
# =============================================================================

# Upload folder
UPLOAD_FOLDER=instance/uploads

# Maximum file size (in bytes, 16MB default)
MAX_CONTENT_LENGTH=16777216

# Allowed extensions
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,txt,zip,tar,gz

# Backup file extensions
BACKUP_ALLOWED_EXTENSIONS=tar,gz,tar.gz,sql,db,sqlite,zip
```

---

## Logging Configuration

```bash
# =============================================================================
# LOGGING
# =============================================================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log file path
LOG_FILE=logs/app.log

# Log format
LOG_FORMAT="%(asctime)s [%(levelname)s] %(name)s: %(message)s"

# Log rotation
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
```

---

## Application Features

```bash
# =============================================================================
# FEATURES
# =============================================================================

# Registration
REGISTRATION_ENABLED=True
REGISTRATION_REQUIRE_APPROVAL=False

# User roles
DEFAULT_USER_ROLE=user
AVAILABLE_ROLES=admin,user,moderator

# Content management
CONTENT_MODERATION_ENABLED=True
CONTENT_AUTO_PUBLISH=False

# Comments
COMMENTS_ENABLED=True
COMMENTS_REQUIRE_APPROVAL=True
```

---

## Internationalization

```bash
# =============================================================================
# I18N
# =============================================================================

# Available languages
LANGUAGES=en,fr,es,de,it

# Default language
DEFAULT_LANGUAGE=en

# Timezone
TIMEZONE=UTC
```

---

## Development Settings

```bash
# =============================================================================
# DEVELOPMENT (for development environment only)
# =============================================================================

# Database echo (show SQL queries)
# SQLALCHEMY_ECHO=False

# Template auto-reload
# TEMPLATES_AUTO_RELOAD=True

# Explain template loading
# EXPLAIN_TEMPLATE_LOADING=False

# Preserve context on exception
# PRESERVE_CONTEXT_ON_EXCEPTION=False
```

---

## Server Configuration

```bash
# =============================================================================
# SERVER
# =============================================================================

# Host and port
HOST=0.0.0.0
PORT=5000

# Workers (for production)
WORKERS=4
THREADS=2

# Timeout
TIMEOUT=30

# Keep alive
KEEPALIVE=5
```

---

## Production Settings (cPanel/VPS)

```bash
# =============================================================================
# PRODUCTION
# =============================================================================

# Server name
SERVER_NAME=yourdomain.com

# Preferred URL scheme
PREFERRED_URL_SCHEME=https

# Trust proxy headers
PROXY_FIX_ENABLED=True
PROXY_FIX_X_FOR=1
PROXY_FIX_X_PROTO=1
PROXY_FIX_X_HOST=1
PROXY_FIX_X_PORT=1
PROXY_FIX_X_PREFIX=1

# Asset pipeline
ASSETS_DEBUG=False
ASSETS_AUTO_BUILD=True
```

---

## Backup Configuration

```bash
# =============================================================================
# BACKUPS
# =============================================================================

# Backup directory
BACKUP_DIR=instance/backups

# Automatic backup schedule
BACKUP_ENABLED=True
BACKUP_INTERVAL_HOURS=24

# Backup retention
BACKUP_RETENTION_DAYS=30
BACKUP_MAX_BACKUPS=10
```

---

## External Services (Optional)

```bash
# =============================================================================
# EXTERNAL SERVICES
# =============================================================================

# Google Analytics
# GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X

# Sentry error tracking
# SENTRY_DSN=https://xxx@sentry.io/xxx

# CDN
# CDN_DOMAIN=cdn.yourdomain.com
# CDN_HTTPS=True
```

---

## Environment-Specific Examples

### Development `.env`

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///instance/dev.db
CACHE_TYPE=filesystem
SESSION_TYPE=filesystem
MAIL_SERVER=localhost
MAIL_PORT=1025
EMAIL_VERIFICATION_REQUIRED=False
RATELIMIT_ENABLED=False
LOG_LEVEL=DEBUG
```

### Production `.env` (cPanel)

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-with-secrets.token_hex>
DATABASE_URL=sqlite:///instance/x-filamenta_python.db
CACHE_TYPE=filesystem
SESSION_TYPE=filesystem
SESSION_COOKIE_SECURE=True
MAIL_SERVER=smtp.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=<your-password>
EMAIL_VERIFICATION_REQUIRED=True
RATELIMIT_ENABLED=True
SERVER_NAME=yourdomain.com
PREFERRED_URL_SCHEME=https
LOG_LEVEL=WARNING
```

### Production `.env` (VPS with Redis)

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-with-secrets.token_hex>
DATABASE_URL=postgresql://xfilamenta:password@localhost/x_filamenta
CACHE_TYPE=redis
CACHE_REDIS_HOST=localhost
CACHE_REDIS_PORT=6379
SESSION_TYPE=redis
SESSION_REDIS=redis://localhost:6379/1
SESSION_COOKIE_SECURE=True
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=<app-password>
EMAIL_VERIFICATION_REQUIRED=True
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=redis://localhost:6379/2
SERVER_NAME=yourdomain.com
PREFERRED_URL_SCHEME=https
WORKERS=4
LOG_LEVEL=INFO
```

---

## Security Best Practices

**DO:**
- ✅ Generate unique SECRET_KEY for each environment
- ✅ Use strong database passwords
- ✅ Enable HTTPS in production
- ✅ Set SESSION_COOKIE_SECURE=True in production
- ✅ Use environment-specific .env files
- ✅ Regularly rotate secrets and passwords

**DON'T:**
- ❌ Never commit .env files to version control
- ❌ Never use debug mode in production
- ❌ Never use default SECRET_KEY
- ❌ Never expose sensitive credentials
- ❌ Never share .env files between environments

---

## Generating Secure Values

### SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Database Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Random Password

```bash
python -c "import secrets; import string; chars = string.ascii_letters + string.digits + string.punctuation; print(''.join(secrets.choice(chars) for _ in range(32)))"
```

---

## Validation

After creating your `.env` file, validate it:

```bash
# Check if all required variables are set
python scripts/validate_env.py

# Test configuration
python -c "from backend.src.config import Config; print('Config OK' if Config.SECRET_KEY != 'dev' else 'WARNING: Using default secret')"
```

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-12-30  
**See Also:** `docs/guides/DEPLOYMENT.md`

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

