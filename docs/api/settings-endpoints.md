# Settings & Configuration API

**Purpose:** API documentation for application settings management  
**File:** `docs/api/settings-endpoints.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Version:** 0.1.0-Beta

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

---

## Overview

Endpoints for managing application settings and configuration.

**Note:** Settings endpoints are typically accessed via the Admin panel (`/admin/settings`). These endpoints are documented separately for API reference.

**Base Path:** `/settings`  
**Authentication:** Required (admin only)  
**CSRF Protection:** Enabled on all POST/PUT/DELETE requests

---

## Settings Categories

### Email Settings (SMTP)

**Keys:**
- `smtp_host` - SMTP server hostname
- `smtp_port` - SMTP server port (25, 465, 587)
- `smtp_user` - SMTP username
- `smtp_password` - SMTP password (encrypted)
- `smtp_tls_enabled` - Enable TLS/STARTTLS (boolean)
- `smtp_from_email` - From email address
- `smtp_from_name` - From name

### Security Settings

**Keys:**
- `email_verification_required` - Require email verification (boolean)
- `email_verification_token_expiry_hours` - Token validity (hours)
- `password_reset_token_expiry_minutes` - Reset token validity (minutes)
- `password_reset_rate_limit_per_hour` - Max reset requests per hour
- `registration_enabled` - Allow new registrations (boolean)
- `2fa_required` - Require 2FA for all users (boolean)

### Email Templates

**Keys:**
- `email_format` - Email format (`html`, `text`, `both`)

### Site Settings

**Keys:**
- `site_name` - Application name
- `site_url` - Base URL (for email links)
- `logo_url` - Logo image path
- `footer_text` - Footer content

---

## Endpoints

### Get Setting

#### `GET /settings/{key}`

Retrieve value of specific setting.

**Authentication:** Required (admin)

**Path Parameters:**
- `key` (string, required): Setting key name

**Response:**
- `200 OK`: Setting value (JSON)
  ```json
  {
    "key": "smtp_host",
    "value": "smtp.gmail.com",
    "encrypted": false,
    "description": "SMTP server hostname"
  }
  ```
- `404 Not Found`: Setting not found

**Example:**
```http
GET /settings/smtp_host HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

**Notes:**
- Encrypted values (passwords) return masked value: `***`
- Description provided if available

---

### Get All Settings

#### `GET /settings/`

Retrieve all application settings.

**Authentication:** Required (admin)

**Query Parameters:**
- `category` (string, optional): Filter by category
  - Values: `email`, `security`, `site`, `features`

**Response:**
- `200 OK`: Settings object (JSON)
  ```json
  {
    "smtp_host": {
      "value": "smtp.gmail.com",
      "encrypted": false,
      "category": "email"
    },
    "smtp_password": {
      "value": "***",
      "encrypted": true,
      "category": "email"
    },
    "site_name": {
      "value": "X-Filamenta",
      "encrypted": false,
      "category": "site"
    }
  }
  ```

**Example:**
```http
GET /settings/?category=email HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

### Update Setting

#### `PUT /settings/{key}`

Update value of specific setting.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `key` (string, required): Setting key name

**Request Body:**
```json
{
  "value": "new-value"
}
```

**Response:**
- `200 OK`: Updated setting
  ```json
  {
    "key": "smtp_host",
    "value": "smtp.example.com",
    "updated_at": "2025-12-30T12:00:00Z"
  }
  ```
- `400 Bad Request`: Validation error
- `404 Not Found`: Setting not found

**Example:**
```http
PUT /settings/smtp_host HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/json
X-CSRFToken: abc123

{
  "value": "smtp.example.com"
}
```

---

### Update Multiple Settings

#### `PATCH /settings/`

Update multiple settings at once.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Request Body:**
```json
{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": "587",
  "smtp_tls_enabled": true,
  "site_name": "My Application"
}
```

**Response:**
- `200 OK`: Updated settings count
  ```json
  {
    "updated": 4,
    "settings": ["smtp_host", "smtp_port", "smtp_tls_enabled", "site_name"]
  }
  ```
- `400 Bad Request`: Validation errors
  ```json
  {
    "error": "Validation failed",
    "details": {
      "smtp_port": "Must be a valid port number (1-65535)"
    }
  }
  ```

**Example:**
```http
PATCH /settings/ HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/json
X-CSRFToken: abc123

{
  "smtp_host": "smtp.gmail.com",
  "smtp_port": "587"
}
```

---

### Test Email Configuration

#### `POST /settings/test-email`

Send test email to verify SMTP configuration.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Request Body:**
```json
{
  "to_email": "test@example.com"
}
```

**Response:**
- `200 OK`: Email sent successfully
  ```json
  {
    "success": true,
    "message": "Test email sent to test@example.com"
  }
  ```
- `400 Bad Request`: Email not configured
- `500 Internal Server Error`: SMTP error
  ```json
  {
    "error": "Failed to send email",
    "details": "Connection refused by SMTP server"
  }
  ```

**Example:**
```http
POST /settings/test-email HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/json
X-CSRFToken: abc123

{
  "to_email": "admin@example.com"
}
```

---

## Setting Validation Rules

### SMTP Settings

| Key | Type | Validation |
|-----|------|------------|
| `smtp_host` | string | Required, valid hostname |
| `smtp_port` | integer | 1-65535, typically 25, 465, or 587 |
| `smtp_user` | string | Optional, email format recommended |
| `smtp_password` | string | Encrypted storage, required if user set |
| `smtp_tls_enabled` | boolean | true/false |
| `smtp_from_email` | string | Required, valid email format |
| `smtp_from_name` | string | Max 100 chars |

### Security Settings

| Key | Type | Validation |
|-----|------|------------|
| `email_verification_required` | boolean | true/false |
| `email_verification_token_expiry_hours` | integer | 1-168 (1 week max) |
| `password_reset_token_expiry_minutes` | integer | 15-1440 (1 day max) |
| `password_reset_rate_limit_per_hour` | integer | 1-10 |
| `registration_enabled` | boolean | true/false |
| `2fa_required` | boolean | true/false |

### Site Settings

| Key | Type | Validation |
|-----|------|------------|
| `site_name` | string | 1-100 chars |
| `site_url` | string | Valid URL format |
| `logo_url` | string | Valid path or URL |
| `footer_text` | string | Max 500 chars, HTML allowed |

---

## Security

### Encrypted Settings

Sensitive settings are encrypted at rest using Fernet (symmetric encryption):
- `smtp_password`
- Any setting with suffix `_password` or `_secret`

**Encryption:**
- Key stored in environment variable `SETTINGS_ENCRYPTION_KEY`
- Automatic encryption on save
- Automatic decryption on read (for authorized users)
- Masked in logs and responses

### Audit Logging

All setting changes are logged:
```json
{
  "admin_id": 1,
  "action": "settings_updated",
  "details": {
    "keys": ["smtp_host", "smtp_port"],
    "old_values": {"smtp_host": "old.example.com"},
    "new_values": {"smtp_host": "new.example.com"}
  },
  "ip_address": "192.168.1.100",
  "timestamp": "2025-12-30T12:00:00Z"
}
```

**Note:** Encrypted values not included in audit logs for security.

---

## Cache Invalidation

Settings are cached for performance. Cache is automatically invalidated on update:

**Cache Keys:**
- `settings:all` - All settings
- `settings:{key}` - Individual setting

**TTL:** 300 seconds (5 minutes) for `settings:all`, indefinite for individual keys (invalidated on update)

---

## Examples

### Get All Email Settings

```bash
curl "http://localhost:5000/settings/?category=email" \
  -H "Cookie: session=..." \
  -H "Accept: application/json"
```

### Update SMTP Configuration

```bash
curl -X PATCH "http://localhost:5000/settings/" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: abc123" \
  -d '{
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "noreply@example.com",
    "smtp_password": "app-specific-password",
    "smtp_tls_enabled": true
  }'
```

### Test Email Configuration

```bash
curl -X POST "http://localhost:5000/settings/test-email" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: abc123" \
  -d '{"to_email": "admin@example.com"}'
```

### Get Single Setting

```bash
curl "http://localhost:5000/settings/site_name" \
  -H "Cookie: session=..." \
  -H "Accept: application/json"
```

---

## Configuration via Environment Variables

Some settings can be overridden by environment variables (takes precedence over database):

| Setting Key | Environment Variable |
|-------------|---------------------|
| `smtp_host` | `SMTP_HOST` |
| `smtp_port` | `SMTP_PORT` |
| `smtp_user` | `SMTP_USER` |
| `smtp_password` | `SMTP_PASSWORD` |
| `site_url` | `SITE_URL` |

**Priority:**
1. Environment variables (highest)
2. Database settings
3. Default values (lowest)

---

## Default Values

Settings with default values (if not set in database):

```python
DEFAULTS = {
    'smtp_port': 587,
    'smtp_tls_enabled': True,
    'email_verification_required': False,
    'email_verification_token_expiry_hours': 24,
    'password_reset_token_expiry_minutes': 60,
    'password_reset_rate_limit_per_hour': 2,
    'registration_enabled': True,
    '2fa_required': False,
    'email_format': 'both',
    'site_name': 'X-Filamenta',
    'footer_text': '© 2025 XAREMA'
}
```

---

## Related Documentation

- [Admin Settings Guide](../admin/settings-configuration.md)
- [Email Configuration](../deployment/email-setup.md)
- [Security Best Practices](../security/best-practices.md)

---

**Last Updated:** 2025-12-30  
**API Version:** 0.1.0-Beta

