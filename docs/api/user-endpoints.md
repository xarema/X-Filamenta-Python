# User Profile & Preferences API

**Purpose:** API documentation for user profile and preferences endpoints  
**File:** `docs/api/user-endpoints.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Version:** 0.1.0-Beta

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

---

## Overview

Endpoints for managing user profiles, preferences, and account settings.

**Base Path:** `/users`  
**Authentication:** Required (own account or admin)  
**CSRF Protection:** Enabled on all POST/PUT/DELETE requests

---

## Endpoints

### User Profile

#### `GET /users/profile`

View current user's profile.

**Authentication:** Required

**Response:**
- `200 OK`: Profile page (HTML) with user information
  - Username
  - Email
  - Account status
  - Email verification status
  - 2FA status
  - Account created date
  - Last login

**Example:**
```http
GET /users/profile HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /users/profile`

Update user profile information.

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
email=newemail@example.com
full_name=John Doe
bio=Software developer interested in Python
```

**Updatable Fields:**
- `email` (string, format: email) - Must be unique, triggers re-verification
- `full_name` (string, optional, max 100 chars)
- `bio` (string, optional, max 500 chars)

**Response:**
- `302 Found`: Redirect to profile with success message
- `400 Bad Request`: Validation error
  - Invalid email format
  - Email already in use
  - Field too long

**Example:**
```http
POST /users/profile HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&email=john@example.com&full_name=John%20Doe
```

**Notes:**
- Changing email address triggers new verification email
- `email_verified` flag reset to `False`
- User must verify new email to maintain full access (if verification required)

---

### Password Management

#### `GET /users/change-password`

Display password change form.

**Authentication:** Required

**Response:**
- `200 OK`: Password change form

**Example:**
```http
GET /users/change-password HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /users/change-password`

Change user password.

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
current_password=OldPass123!
new_password=NewSecurePass456!
new_password_confirm=NewSecurePass456!
```

**Fields:**
- `current_password` (string, required) - Current password for verification
- `new_password` (string, required, min 8 chars) - New password
- `new_password_confirm` (string, required) - Must match new_password

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (`!@#$%^&*()_+-=[]{}|;:,.<>?`)
- Cannot be same as current password

**Response:**
- `302 Found`: Redirect to profile with success message
- `400 Bad Request`: Validation error
  - Current password incorrect
  - New password doesn't meet requirements
  - Passwords don't match

**Example:**
```http
POST /users/change-password HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&current_password=OldPass123!&new_password=NewSecurePass456!&new_password_confirm=NewSecurePass456!
```

**Security:**
- Rate limited: 5 attempts per 15 minutes
- Current password verified before change
- Password history (last 3 passwords) - optional feature
- Audit log entry created

---

### User Preferences

#### `GET /users/preferences`

View user preferences.

**Authentication:** Required

**Response:**
- `200 OK`: Preferences page with current settings
  - Theme (light/dark)
  - Language (en/fr)
  - Notification settings
  - Display preferences

**Example:**
```http
GET /users/preferences HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /users/preferences`

Update user preferences.

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
theme=dark
language=fr
notifications=true
```

**Available Preferences:**
- `theme` (string): UI theme
  - Values: `light`, `dark`, `auto`
  - Default: `light`
  
- `language` (string): Interface language
  - Values: `en`, `fr`
  - Default: `en`
  
- `notifications` (boolean): Enable notifications
  - Values: `true`, `false`
  - Default: `true`

**Response:**
- `302 Found`: Redirect to preferences with success message
- `400 Bad Request`: Invalid preference value

**Example:**
```http
POST /users/preferences HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&theme=dark&language=fr&notifications=true
```

**Notes:**
- Preferences stored in database
- Applied immediately to session
- Persisted across devices/browsers

---

### 2FA Management

#### `GET /users/2fa/setup`

Display 2FA/TOTP setup page.

**Authentication:** Required

**Response:**
- `200 OK`: 2FA setup page
  - QR code for authenticator app
  - Manual entry key
  - Backup codes (one-time display)

**Example:**
```http
GET /users/2fa/setup HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

**Setup Flow:**
1. User requests setup page
2. Server generates TOTP secret
3. QR code displayed for scanning
4. User scans with authenticator app (Google Authenticator, Authy, etc.)
5. User verifies with token
6. Backup codes generated and displayed

---

#### `POST /users/2fa/enable`

Enable 2FA after verification.

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
token=123456
```

**Fields:**
- `token` (string, required, 6 digits) - TOTP token from authenticator app

**Response:**
- `302 Found`: Redirect to profile, 2FA enabled
- `400 Bad Request`: Invalid token

**Example:**
```http
POST /users/2fa/enable HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&token=123456
```

**Security:**
- Token must be valid (30-second window)
- Backup codes generated and displayed once
- User must save backup codes securely

---

#### `POST /users/2fa/disable`

Disable 2FA (requires password confirmation).

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
password=SecurePass123!
```

**Fields:**
- `password` (string, required) - Current password for confirmation

**Response:**
- `302 Found`: Redirect to profile, 2FA disabled
- `400 Bad Request`: Incorrect password

**Example:**
```http
POST /users/2fa/disable HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&password=SecurePass123!
```

**Security:**
- Password verification required
- TOTP secret deleted
- Backup codes invalidated
- Audit log entry created

---

### Account Deletion

#### `POST /users/delete-account`

Request account deletion (soft delete).

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
password=SecurePass123!
confirm=DELETE
```

**Fields:**
- `password` (string, required) - Current password
- `confirm` (string, required) - Must be exactly `DELETE`

**Response:**
- `302 Found`: Redirect to goodbye page, account deactivated
- `400 Bad Request`: Incorrect password or confirmation

**Example:**
```http
POST /users/delete-account HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123...&password=SecurePass123!&confirm=DELETE
```

**Notes:**
- Soft delete: account marked inactive, data retained
- User logged out immediately
- Email sent confirming deletion
- Admin can reactivate if needed
- Hard delete (data purge) requires admin action

---

## Error Responses

### `400 Bad Request` - Validation Error
```json
{
  "error": "Validation failed",
  "code": 400,
  "details": {
    "email": ["Email address already in use"],
    "password": ["Password must contain at least one special character"]
  }
}
```

### `401 Unauthorized` - Not Authenticated
```json
{
  "error": "Authentication required",
  "code": 401,
  "message": "Please login to access this resource"
}
```

### `403 Forbidden` - Cannot Modify
```json
{
  "error": "Cannot modify other user's profile",
  "code": 403
}
```

### `429 Too Many Requests` - Rate Limited
```json
{
  "error": "Too many password change attempts",
  "code": 429,
  "retry_after": 900
}
```

---

## Data Models

### User Profile
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "bio": "Software developer",
  "is_active": true,
  "email_verified": true,
  "totp_enabled": false,
  "created_at": "2025-01-01T00:00:00Z",
  "last_login": "2025-12-30T12:00:00Z"
}
```

### User Preferences
```json
{
  "user_id": 1,
  "theme": "dark",
  "language": "fr",
  "notifications": true
}
```

---

## Examples

### Update Email Address

```bash
curl -X POST "http://localhost:5000/users/profile" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&email=newemail@example.com" \
  -L
```

### Change Password

```bash
curl -X POST "http://localhost:5000/users/change-password" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&current_password=OldPass123!&new_password=NewPass456!&new_password_confirm=NewPass456!" \
  -L
```

### Update Preferences

```bash
curl -X POST "http://localhost:5000/users/preferences" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&theme=dark&language=fr&notifications=true" \
  -L
```

### Enable 2FA

```bash
# 1. Get setup page (displays QR code)
curl "http://localhost:5000/users/2fa/setup" \
  -H "Cookie: session=..." \
  -L

# 2. Scan QR with authenticator app

# 3. Enable with token
curl -X POST "http://localhost:5000/users/2fa/enable" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&token=123456" \
  -L
```

---

## Related Documentation

- [Authentication API](./auth-endpoints.md)
- [Admin User Management](./admin-endpoints.md)
- [2FA Setup Guide](../guides/2fa-setup.md)

---

**Last Updated:** 2025-12-30  
**API Version:** 0.1.0-Beta

