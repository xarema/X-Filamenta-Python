# Installation Wizard API Documentation

**Purpose:** API documentation for installation wizard endpoints  
**File:** `docs/api/installation-endpoints.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Version:** 0.1.0-Beta

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

---

## Overview

Installation wizard for first-time setup of X-Filamenta application.

**Base Path:** `/install`  
**Authentication:** Not required (wizard mode only)  
**Active:** Only when no database configured

---

## Wizard Flow

```
1. Language Selection  → /install/
2. Requirements Check  → /install/step?step=requirements
3. Database Config     → /install/step?step=db_form
4. Database Test       → /install/step?step=db_test
5. Cache Config        → /install/step?step=cache_form (optional)
6. Cache Test          → /install/step?step=cache_test (optional)
7. Backup Upload       → /install/step?step=upload_form (optional)
8. Admin Account       → /install/step?step=admin_form
9. Finalization        → /install/step?step=finalize
10. Completion         → /install/step?step=done
```

---

## Endpoints

### Language Selection

#### `GET /install/`

Display language selection page (first wizard step).

**Query Parameters:** None

**Response:**
- `200 OK`: Language selection page (HTML)
- `302 Found`: Redirect if installation already complete

**Supported Languages:**
- `en` - English
- `fr` - Français

**Example:**
```http
GET /install/ HTTP/1.1
Host: localhost:5000
```

#### `POST /install/set-language`

Set installation language preference.

**Request Body:**
```x-www-form-urlencoded
language=fr
```

**Response:**
- `302 Found`: Redirect to requirements step

---

### Requirements Check

#### `GET /install/step?step=requirements`

Display system requirements check page.

**Checks Performed:**
- Python version (≥3.9)
- Required packages installed
- Write permissions
- Database drivers available
- Cache backend availability (Redis/Filesystem)

**Response:**
- `200 OK`: Requirements page with test results

**Example:**
```http
GET /install/step?step=requirements HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From requirements page)**

Proceed to database configuration.

**Request Body:**
```x-www-form-urlencoded
step=requirements
requirements_checked=1
```

**Response:**
- `302 Found`: Redirect to `db_form` step

---

### Database Configuration

#### `GET /install/step?step=db_form`

Display database configuration form.

**Response:**
- `200 OK`: Database config form

**Form Fields:**
- `db_type`: Database type (`sqlite`, `mysql`, `postgresql`)
- SQLite:
  - `db_name`: Database filename (default: `x-filamenta_python.db`)
- MySQL/PostgreSQL:
  - `db_host`: Hostname (default: `localhost`)
  - `db_port`: Port (default: `3306` for MySQL, `5432` for PostgreSQL)
  - `db_name`: Database name
  - `db_user`: Username
  - `db_password`: Password

**Example:**
```http
GET /install/step?step=db_form HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From db_form page)**

Test database connection.

**Request Body (SQLite):**
```x-www-form-urlencoded
step=db_form
db_type=sqlite
db_name=x-filamenta_python.db
```

**Request Body (MySQL):**
```x-www-form-urlencoded
step=db_form
db_type=mysql
db_host=localhost
db_port=3306
db_name=filamenta
db_user=filamenta_user
db_password=secure_password
```

**Response:**
- `302 Found`: Redirect to `db_test` step if connection successful
- `400 Bad Request`: Form with validation errors

**Validation:**
- All required fields present
- Valid port numbers
- Database name format (SQLite: `.db` extension)

---

### Database Connection Test

#### `GET /install/step?step=db_test`

Test database connection and display results.

**Response:**
- `200 OK`: Test results page

**Tests Performed:**
- Connection test
- Create database (if not exists)
- Write permission test
- Character encoding test

**Example:**
```http
GET /install/step?step=db_test HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From db_test page)**

Proceed to cache configuration or admin account.

**Request Body:**
```x-www-form-urlencoded
step=db_test
```

**Response:**
- `302 Found`: Redirect to `cache_form` (if Redis detected) or `admin_form`

---

### Cache Configuration (Optional)

#### `GET /install/step?step=cache_form`

Display cache backend configuration form.

**Response:**
- `200 OK`: Cache config form

**Form Fields:**
- `cache_type`: Cache backend (`redis`, `filesystem`)
- Redis options:
  - `redis_host`: Hostname (default: `localhost`)
  - `redis_port`: Port (default: `6379`)
  - `redis_password`: Password (optional)
  - `redis_db`: Database number (default: `0`)

**Example:**
```http
GET /install/step?step=cache_form HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From cache_form page)**

Test cache connection.

**Request Body:**
```x-www-form-urlencoded
step=cache_form
cache_type=redis
redis_host=localhost
redis_port=6379
redis_password=
redis_db=0
```

**Response:**
- `302 Found`: Redirect to `cache_test` step

---

### Backup Upload (Optional)

#### `GET /install/step?step=upload_form`

Display backup file upload form.

**Response:**
- `200 OK`: Upload form

**Accepts:**
- `.tar.gz` backup files
- SQLite database exports

**Example:**
```http
GET /install/step?step=upload_form HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From upload_form page)**

Upload and validate backup file.

**Request Body:**
```multipart/form-data
step=upload_form
backup_file=<file data>
```

**Response:**
- `302 Found`: Redirect to `admin_form` if valid
- `400 Bad Request`: Form with validation error

**Validation:**
- File size ≤ 50 MB
- Valid `.tar.gz` format
- Contains valid SQLite database

---

### Admin Account Creation

#### `GET /install/step?step=admin_form`

Display admin account creation form.

**Response:**
- `200 OK`: Admin account form

**Form Fields:**
- `username`: Admin username (3-50 chars, alphanumeric + `_-`)
- `email`: Admin email address
- `password`: Password (min 8 chars, complexity rules)
- `password_confirm`: Password confirmation

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

**Example:**
```http
GET /install/step?step=admin_form HTTP/1.1
Host: localhost:5000
```

#### `POST /install/step`
**(From admin_form page)**

Create admin account and proceed.

**Request Body:**
```x-www-form-urlencoded
step=admin_form
username=admin
email=admin@example.com
password=SecurePass123!
password_confirm=SecurePass123!
```

**Response:**
- `302 Found`: Redirect to `finalize` step
- `400 Bad Request`: Form with validation errors

---

### Finalization

#### `GET /install/step?step=finalize`

Perform final setup steps.

**Actions Performed:**
1. Create database tables
2. Apply migrations
3. Restore backup (if uploaded)
4. Create admin user
5. Initialize default settings
6. Set installation flag

**Response:**
- `200 OK`: Finalization progress page
- `500 Internal Server Error`: Setup failed

**Example:**
```http
GET /install/step?step=finalize HTTP/1.1
Host: localhost:5000
```

---

### Completion

#### `GET /install/step?step=done`

Display installation completion page.

**Response:**
- `200 OK`: Success page with next steps

**Displays:**
- Installation summary
- Database connection details
- Admin credentials reminder
- Login link

**Example:**
```http
GET /install/step?step=done HTTP/1.1
Host: localhost:5000
```

---

## Wizard State Management

### Session Variables

The wizard stores state in Flask session:

```python
session['wizard_started'] = True
session['wizard_state'] = {
    'language': 'fr',
    'step': 'admin_form',
    'db_type': 'sqlite',
    'db_config': {...},
    'cache_type': 'filesystem',
    'backup_uploaded': False,
    'admin_created': False
}
```

### Breadcrumb Navigation

Each step displays a breadcrumb showing:
- Completed steps (✓)
- Current step (highlighted)
- Upcoming steps (disabled)

---

## Error Handling

### Common Errors

#### Database Connection Failed
```json
{
  "error": "Database connection failed",
  "details": "Could not connect to MySQL server at localhost:3306",
  "code": 400
}
```

#### Invalid Backup File
```json
{
  "error": "Invalid backup file",
  "details": "File is not a valid tar.gz archive",
  "code": 400
}
```

#### Admin User Creation Failed
```json
{
  "error": "Failed to create admin user",
  "details": "Username already exists",
  "code": 400
}
```

---

## Security Considerations

### Installation Lock

Once installation is complete:
- `/install/*` routes redirect to main application
- Installation flag stored in database
- Can only be reset by manual database modification

### Sensitive Data

- Database passwords not stored in plain text
- Session data cleared after completion
- Temporary files deleted

### Rate Limiting

Installation endpoints have lenient rate limits:
- 20 requests / minute per IP
- No lockout on failed attempts

---

## Examples

### Complete Installation Flow (cURL)

```bash
# 1. Start installation
curl -c cookies.txt "http://localhost:5000/install/"

# 2. Set language
curl -b cookies.txt -c cookies.txt -X POST \
  "http://localhost:5000/install/set-language" \
  -d "language=en"

# 3. Check requirements
curl -b cookies.txt -c cookies.txt -X POST \
  "http://localhost:5000/install/step" \
  -d "step=requirements&requirements_checked=1"

# 4. Configure database
curl -b cookies.txt -c cookies.txt -X POST \
  "http://localhost:5000/install/step" \
  -d "step=db_form&db_type=sqlite&db_name=app.db"

# 5. Create admin account
curl -b cookies.txt -c cookies.txt -X POST \
  "http://localhost:5000/install/step" \
  -d "step=admin_form&username=admin&email=admin@example.com&password=SecurePass123!&password_confirm=SecurePass123!"

# 6. Finalize
curl -b cookies.txt "http://localhost:5000/install/step?step=finalize"
```

---

## Related Documentation

- [Database Configuration](../deployment/database-setup.md)
- [Cache Configuration](../deployment/cache-setup.md)
- [Admin Guide](../admin/admin-guide.md)

---

**Last Updated:** 2025-12-30  
**API Version:** 0.1.0-Beta

