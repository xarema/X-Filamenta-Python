# API Documentation - X-Filamenta

**Version:** 0.1.0-Beta  
**Last Updated:** 2025-12-30  
**License:** AGPL-3.0-or-later

---

## Welcome to X-Filamenta API Documentation

This directory contains comprehensive API documentation for X-Filamenta, a Flask-based web application with HTMX and Bootstrap 5.

---

## 📁 Documentation Structure

| File | Description |
|------|-------------|
| `openapi.yaml` | OpenAPI 3.0 specification (machine-readable) |
| `admin-endpoints.md` | Admin panel endpoints documentation |
| `installation-endpoints.md` | Installation wizard endpoints |
| `auth-endpoints.md` | Authentication and authorization |
| `user-endpoints.md` | User profile and preferences |
| `content-endpoints.md` | Content management |
| `settings-endpoints.md` | Application settings |

---

## 🚀 Quick Start

### View Interactive API Docs

1. **Using Swagger UI:**
   ```bash
   # Install Swagger UI (one-time)
   npm install -g swagger-ui-express
   
   # Serve docs
   swagger-ui-serve docs/api/openapi.yaml
   ```
   
   Open: `http://localhost:8080`

2. **Using Redoc:**
   ```bash
   # Install redoc-cli (one-time)
   npm install -g redoc-cli
   
   # Generate HTML
   redoc-cli bundle docs/api/openapi.yaml
   
   # Open redoc-static.html in browser
   ```

### Base URL

- **Development:** `http://localhost:5000`
- **Production:** Configure via `SITE_URL` environment variable

---

## 🔐 Authentication

X-Filamenta uses **session-based authentication** with HTTP-only cookies.

### Login Flow

```http
POST /auth/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=admin&password=SecurePass123!
```

**Response:**
- Sets `session` cookie (HTTP-only, Secure in production)
- Redirects to dashboard or requested page

### Using Authentication

Include the session cookie in subsequent requests:

```http
GET /admin/users HTTP/1.1
Cookie: session=abc123...
```

### Logout

```http
POST /auth/logout HTTP/1.1
Cookie: session=abc123...
```

---

## 🛡️ Security

### CSRF Protection

All state-changing requests (POST/PUT/DELETE) require CSRF tokens.

**HTML Forms:**
```html
<form method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <!-- form fields -->
</form>
```

**AJAX Requests:**
```javascript
fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
  },
  body: JSON.stringify(data)
})
```

### Rate Limiting

| Endpoint Type | Limit |
|--------------|-------|
| Login attempts | 5 / 15 minutes |
| Password reset requests | 2 / hour |
| Email verification resend | 3 / hour |
| General API | 100 / minute |
| Admin actions | 50 / minute |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1672444800
```

### Security Headers

All responses include security headers:
```http
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; ...
```

---

## 📊 API Endpoints Overview

### Authentication (`/auth/*`)

- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/register` - User registration
- `GET /auth/verify-email/{token}` - Email verification
- `POST /auth/resend-verification` - Resend verification email
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password/{token}` - Reset password
- `GET /auth/2fa/setup` - Setup 2FA/TOTP
- `POST /auth/2fa/verify` - Verify 2FA token

### Admin (`/admin/*`)

- `GET /admin/` - Dashboard
- `GET /admin/users` - List users
- `GET /admin/users/{id}` - View user
- `POST /admin/users/{id}/toggle-active` - Activate/deactivate user
- `POST /admin/users/{id}/toggle-admin` - Grant/revoke admin
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/settings` - View settings
- `POST /admin/settings` - Update settings
- `GET /admin/logs` - View activity logs

### Installation (`/install/*`)

- `GET /install/` - Language selection
- `POST /install/set-language` - Set language
- `GET /install/step` - Wizard steps
- `POST /install/step` - Process step

### Users (`/users/*`)

- `GET /users/profile` - View own profile
- `POST /users/profile` - Update profile
- `GET /users/preferences` - View preferences
- `POST /users/preferences` - Update preferences
- `POST /users/change-password` - Change password

### Content (`/content/*`)

- `GET /content/` - List content
- `GET /content/{id}` - View content
- `POST /content/` - Create content
- `PUT /content/{id}` - Update content
- `DELETE /content/{id}` - Delete content

---

## 📝 Request/Response Formats

### Content Types

**Supported Request Types:**
- `application/x-www-form-urlencoded` (forms)
- `application/json` (API requests)
- `multipart/form-data` (file uploads)

**Response Types:**
- `text/html` (default for web pages)
- `application/json` (API endpoints with `Accept: application/json`)

### Standard Response Structure

#### Success (200 OK)
```html
<!-- HTML page or component -->
```

#### Created (201 Created)
```json
{
  "id": 123,
  "message": "Resource created successfully"
}
```

#### Error (400 Bad Request)
```json
{
  "error": "Validation failed",
  "code": 400,
  "details": {
    "email": ["Email address is required"],
    "password": ["Password must be at least 8 characters"]
  }
}
```

#### Error (401 Unauthorized)
```json
{
  "error": "Authentication required",
  "code": 401
}
```

#### Error (403 Forbidden)
```json
{
  "error": "Admin access required",
  "code": 403
}
```

#### Error (404 Not Found)
```json
{
  "error": "Resource not found",
  "code": 404
}
```

#### Error (429 Too Many Requests)
```json
{
  "error": "Rate limit exceeded",
  "code": 429,
  "retry_after": 60
}
```

---

## 🌍 Internationalization (i18n)

API supports multiple languages via `Accept-Language` header or session preference.

**Supported Languages:**
- `en` - English (default)
- `fr` - Français

**Request:**
```http
GET /admin/users HTTP/1.1
Accept-Language: fr
```

**Response:**
```html
<!-- French translated content -->
```

---

## 🧪 Testing

### Using cURL

```bash
# Login
curl -c cookies.txt -X POST "http://localhost:5000/auth/login" \
  -d "username=admin&password=SecurePass123!"

# Access protected resource
curl -b cookies.txt "http://localhost:5000/admin/users"

# Logout
curl -b cookies.txt -X POST "http://localhost:5000/auth/logout"
```

### Using Python Requests

```python
import requests

session = requests.Session()

# Login
response = session.post('http://localhost:5000/auth/login', data={
    'username': 'admin',
    'password': 'SecurePass123!'
})

# Access protected resource
response = session.get('http://localhost:5000/admin/users')
print(response.text)

# Logout
session.post('http://localhost:5000/auth/logout')
```

### Using Postman

1. Import `openapi.yaml` into Postman
2. Configure environment:
   - `base_url`: `http://localhost:5000`
3. Enable cookie jar for session management
4. Add pre-request script for CSRF tokens

---

## 📖 Additional Resources

### Deployment Guides
- [cPanel Deployment](../deployment/cpanel-deployment.md)
- [VPS Deployment](../deployment/vps-deployment.md)
- [Docker Deployment](../deployment/docker-deployment.md)

### Development Guides
- [Contributing Guide](../../CONTRIBUTING.md)
- [Code Style Guide](../.github/python.instructions.md)
- [Testing Guide](../testing/README.md)

### Admin Guides
- [Admin Panel Guide](../admin/admin-guide.md)
- [User Management](../admin/user-management.md)
- [Settings Configuration](../admin/settings-configuration.md)

---

## 🆘 Support

### Issues & Bug Reports
- GitHub Issues: https://github.com/XAREMA/X-Filamenta-Python/issues

### Documentation Feedback
- Submit PR with improvements
- Open issue for clarifications

### Community
- Discord: [Coming Soon]
- Forum: [Coming Soon]

---

## 📜 License

This API and documentation are licensed under **AGPL-3.0-or-later**.

**Copyright:** © 2025 XAREMA. All rights reserved.

See [LICENSE](../../LICENSE) for full license text.

---

## 🔄 Changelog

### Version 0.1.0-Beta (2025-12-30)
- Initial API documentation
- OpenAPI 3.0 specification
- Authentication endpoints documented
- Admin endpoints documented
- Installation wizard documented
- Security guidelines added
- Examples and testing guides

---

**Generated:** 2025-12-30  
**Maintainer:** XAREMA  
**Contact:** support@xarema.com

