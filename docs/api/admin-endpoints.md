# Admin API Documentation

**Purpose:** API documentation for administrative endpoints  
**File:** `docs/api/admin-endpoints.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Version:** 0.1.0-Beta

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

---

## Overview

Administrative endpoints for user management, system settings, and monitoring.

**Base Path:** `/admin`  
**Authentication:** Required (admin role)  
**CSRF Protection:** Enabled on all POST/PUT/DELETE requests

---

## Endpoints

### Dashboard

#### `GET /admin/`

Display admin dashboard with system overview.

**Authentication:** Required (admin)

**Response:**
- `200 OK`: Dashboard HTML page
  - User statistics
  - Recent activity
  - System status
  - Quick actions

**Example:**
```http
GET /admin/ HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

### User Management

#### `GET /admin/users`

List all users with pagination and filtering.

**Authentication:** Required (admin)

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 20, max: 100)
- `search` (string, optional): Search by username or email
- `filter` (string, optional): Filter by status
  - Values: `all`, `active`, `inactive`, `unverified`, `admin`
- `sort` (string, optional): Sort field (default: `created_at`)
  - Values: `username`, `email`, `created_at`, `last_login`
- `order` (string, optional): Sort order (default: `desc`)
  - Values: `asc`, `desc`

**Response:**
- `200 OK`: User list HTML

**Example:**
```http
GET /admin/users?page=1&filter=active&sort=username&order=asc HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `GET /admin/users/{user_id}`

View detailed information for specific user.

**Authentication:** Required (admin)

**Path Parameters:**
- `user_id` (integer, required): User ID

**Response:**
- `200 OK`: User detail page
- `404 Not Found`: User not found

**Example:**
```http
GET /admin/users/5 HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /admin/users/{user_id}/toggle-active`

Activate or deactivate user account.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `user_id` (integer, required): User ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
```

**Response:**
- `302 Found`: Redirect to user list
- `400 Bad Request`: Invalid request or CSRF token
- `403 Forbidden`: Cannot deactivate own account
- `404 Not Found`: User not found

**Example:**
```http
POST /admin/users/5/toggle-active HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...
```

---

#### `POST /admin/users/{user_id}/toggle-admin`

Grant or revoke admin privileges.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `user_id` (integer, required): User ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
```

**Response:**
- `302 Found`: Redirect to user list
- `400 Bad Request`: Invalid request
- `403 Forbidden`: Cannot modify own admin status
- `404 Not Found`: User not found

**Example:**
```http
POST /admin/users/5/toggle-admin HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...
```

---

#### `POST /admin/users/{user_id}/reset-password`

Force password reset for user (sends reset email).

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `user_id` (integer, required): User ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
```

**Response:**
- `302 Found`: Redirect with success message
- `400 Bad Request`: Email not configured or user has no email
- `404 Not Found`: User not found

---

#### `DELETE /admin/users/{user_id}`

Delete user account (soft delete).

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `user_id` (integer, required): User ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
confirm=true
```

**Response:**
- `302 Found`: Redirect to user list
- `400 Bad Request`: Missing confirmation or CSRF
- `403 Forbidden`: Cannot delete own account
- `404 Not Found`: User not found

---

### Settings Management

#### `GET /admin/settings`

Display application settings page.

**Authentication:** Required (admin)

**Response:**
- `200 OK`: Settings management page
  - Email settings (SMTP)
  - Security settings (2FA, email verification)
  - Site settings (name, URL, logo)
  - Feature flags

**Example:**
```http
GET /admin/settings HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /admin/settings`

Update application settings.

**Authentication:** Required (admin)  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
smtp_host=smtp.example.com
smtp_port=587
smtp_user=user@example.com
smtp_password=...
smtp_tls_enabled=true
smtp_from_email=noreply@example.com
smtp_from_name=X-Filamenta
email_verification_required=true
email_verification_token_expiry_hours=24
password_reset_token_expiry_minutes=60
password_reset_rate_limit_per_hour=2
email_format=both
registration_enabled=false
2fa_required=true
site_name=X-Filamenta
site_url=https://example.com
logo_url=/static/logo.png
footer_text=© 2025 XAREMA
```

**Response:**
- `302 Found`: Redirect with success message
- `400 Bad Request`: Validation error

**Notes:**
- Sensitive fields (passwords) are encrypted before storage
- Email test can be performed from settings page
- Settings are cached and reloaded on update

---

### Activity Logs

#### `GET /admin/logs`

View admin activity logs.

**Authentication:** Required (admin)

**Query Parameters:**
- `page` (integer, optional): Page number
- `action` (string, optional): Filter by action type
- `user_id` (integer, optional): Filter by admin user

**Response:**
- `200 OK`: Activity log page with table

**Log Actions:**
- `user_created`
- `user_updated`
- `user_deleted`
- `user_activated`
- `user_deactivated`
- `admin_granted`
- `admin_revoked`
- `password_reset`
- `settings_updated`

---

## Security

### CSRF Protection

All POST/PUT/DELETE requests require valid CSRF token:

```html
<form method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <!-- form fields -->
</form>
```

### Rate Limiting

Admin endpoints have generous rate limits:
- General: 100 requests / minute
- Sensitive actions: 10 requests / minute

### Audit Logging

All admin actions are logged with:
- Admin user ID
- Action type
- Target (user ID, setting key, etc.)
- IP address
- User agent
- Timestamp

---

## Error Responses

### `403 Forbidden`
```json
{
  "error": "Admin access required",
  "code": 403
}
```

### `400 Bad Request`
```json
{
  "error": "Invalid CSRF token",
  "code": 400
}
```

### `404 Not Found`
```json
{
  "error": "User not found",
  "code": 404
}
```

---

## Examples

### List Active Users

```bash
curl -X GET "http://localhost:5000/admin/users?filter=active" \
  -H "Cookie: session=..." \
  -L
```

### Deactivate User

```bash
curl -X POST "http://localhost:5000/admin/users/5/toggle-active" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123..." \
  -L
```

### Update Email Settings

```bash
curl -X POST "http://localhost:5000/admin/settings" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123..." \
  -d "smtp_host=smtp.gmail.com" \
  -d "smtp_port=587" \
  -d "smtp_user=user@gmail.com" \
  -d "smtp_password=..." \
  -d "smtp_tls_enabled=true" \
  -L
```

---

## Related Documentation

- [Authentication API](./auth-endpoints.md)
- [User Profile API](./user-endpoints.md)
- [Settings Management](./settings-endpoints.md)

---

**Last Updated:** 2025-12-30  
**API Version:** 0.1.0-Beta

