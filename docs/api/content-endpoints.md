# Content Management API

**Purpose:** API documentation for content creation and management  
**File:** `docs/api/content-endpoints.md` | Repository: X-Filamenta-Python  
**Created:** 2025-12-30  
**Version:** 0.1.0-Beta

**License:** AGPL-3.0-or-later  
**Copyright:** © 2025 XAREMA. All rights reserved.

---

## Overview

Endpoints for creating, reading, updating, and deleting content (posts, articles, pages).

**Base Path:** `/content`  
**Authentication:** Required for create/update/delete, optional for read  
**CSRF Protection:** Enabled on all POST/PUT/DELETE requests

---

## Endpoints

### List Content

#### `GET /content/`

List all published content with pagination.

**Authentication:** Optional (public content only without auth)

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 10, max: 50)
- `type` (string, optional): Filter by content type
  - Values: `post`, `page`, `article`
- `status` (string, optional): Filter by status (admin/author only)
  - Values: `draft`, `published`, `archived`
- `author` (integer, optional): Filter by author ID
- `search` (string, optional): Search in title and body

**Response:**
- `200 OK`: Content list page with pagination

**Example:**
```http
GET /content/?page=1&type=post&per_page=20 HTTP/1.1
Host: localhost:5000
```

**Response Structure:**
```html
<!-- Paginated list of content items -->
<!-- Each item displays: title, excerpt, author, date, status -->
```

---

### View Content

#### `GET /content/{id}`

View single content item by ID.

**Authentication:** Optional (required for drafts)

**Path Parameters:**
- `id` (integer, required): Content ID

**Response:**
- `200 OK`: Content detail page
- `403 Forbidden`: Draft content (not author or admin)
- `404 Not Found`: Content not found

**Example:**
```http
GET /content/123 HTTP/1.1
Host: localhost:5000
```

**Access Rules:**
- Published content: Public access
- Draft content: Author or admin only
- Archived content: Admin only

---

### Create Content

#### `GET /content/new`

Display content creation form.

**Authentication:** Required

**Response:**
- `200 OK`: Content creation form

**Example:**
```http
GET /content/new HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `POST /content/`

Create new content item.

**Authentication:** Required  
**CSRF Protection:** Required

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
title=My New Post
body=<p>Content body in HTML</p>
type=post
status=draft
tags=python,flask,tutorial
```

**Fields:**
- `title` (string, required, max 200 chars) - Content title
- `body` (string, required) - Content body (HTML allowed)
- `type` (string, required) - Content type
  - Values: `post`, `page`, `article`
  - Default: `post`
- `status` (string, optional) - Publication status
  - Values: `draft`, `published`
  - Default: `draft`
- `tags` (string, optional) - Comma-separated tags

**Response:**
- `302 Found`: Redirect to created content
- `400 Bad Request`: Validation error

**Validation:**
- Title required and not empty
- Body required (min 10 chars)
- Type must be valid value
- Tags: max 10 tags, each max 30 chars

**Example:**
```http
POST /content/ HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123&title=Flask%20Tutorial&body=%3Cp%3ELearn%20Flask%3C%2Fp%3E&type=post&status=draft
```

**Notes:**
- Author automatically set to current user
- Created timestamp set automatically
- Slug generated from title (URL-friendly)

---

### Edit Content

#### `GET /content/{id}/edit`

Display content edit form.

**Authentication:** Required (author or admin)

**Path Parameters:**
- `id` (integer, required): Content ID

**Response:**
- `200 OK`: Content edit form pre-filled
- `403 Forbidden`: Not author or admin
- `404 Not Found`: Content not found

**Example:**
```http
GET /content/123/edit HTTP/1.1
Host: localhost:5000
Cookie: session=...
```

---

#### `PUT /content/{id}`

Update existing content.

**Authentication:** Required (author or admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `id` (integer, required): Content ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
title=Updated Title
body=<p>Updated content</p>
status=published
tags=python,flask
```

**Updatable Fields:**
- `title` (string, optional)
- `body` (string, optional)
- `status` (string, optional)
- `tags` (string, optional)

**Response:**
- `302 Found`: Redirect to updated content
- `400 Bad Request`: Validation error
- `403 Forbidden`: Not authorized
- `404 Not Found`: Content not found

**Example:**
```http
PUT /content/123 HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123&title=Updated%20Title&status=published
```

**Notes:**
- Updated timestamp automatically set
- Slug regenerated if title changed
- Version history maintained (optional feature)

---

### Delete Content

#### `DELETE /content/{id}`

Delete content item (soft delete).

**Authentication:** Required (author or admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `id` (integer, required): Content ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
confirm=true
```

**Response:**
- `302 Found`: Redirect to content list
- `400 Bad Request`: Missing confirmation
- `403 Forbidden`: Not authorized
- `404 Not Found`: Content not found

**Example:**
```http
DELETE /content/123 HTTP/1.1
Host: localhost:5000
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

csrf_token=abc123&confirm=true
```

**Notes:**
- Soft delete: status changed to `archived`
- Can be restored by admin
- Hard delete requires admin action

---

### Publish/Unpublish Content

#### `POST /content/{id}/publish`

Publish draft content.

**Authentication:** Required (author or admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `id` (integer, required): Content ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
```

**Response:**
- `302 Found`: Redirect to published content
- `400 Bad Request`: Already published
- `403 Forbidden`: Not authorized

---

#### `POST /content/{id}/unpublish`

Unpublish (revert to draft).

**Authentication:** Required (author or admin)  
**CSRF Protection:** Required

**Path Parameters:**
- `id` (integer, required): Content ID

**Request Body:**
```x-www-form-urlencoded
csrf_token=...
```

**Response:**
- `302 Found`: Redirect to draft content
- `400 Bad Request`: Already draft
- `403 Forbidden`: Not authorized

---

## Data Models

### Content Item
```json
{
  "id": 123,
  "title": "My First Post",
  "body": "<p>Content goes here</p>",
  "excerpt": "Content goes here...",
  "slug": "my-first-post",
  "type": "post",
  "status": "published",
  "author": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "tags": ["python", "flask", "tutorial"],
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z",
  "published_at": "2025-12-30T11:00:00Z"
}
```

---

## Error Responses

### `400 Bad Request`
```json
{
  "error": "Validation failed",
  "code": 400,
  "details": {
    "title": ["Title is required"],
    "body": ["Body must be at least 10 characters"]
  }
}
```

### `403 Forbidden`
```json
{
  "error": "Not authorized to edit this content",
  "code": 403
}
```

### `404 Not Found`
```json
{
  "error": "Content not found",
  "code": 404
}
```

---

## Examples

### Create New Post

```bash
curl -X POST "http://localhost:5000/content/" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&title=Flask%20Tutorial&body=%3Cp%3ELearn%20Flask%3C%2Fp%3E&type=post&status=draft&tags=python,flask" \
  -L
```

### Update Content

```bash
curl -X PUT "http://localhost:5000/content/123" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&title=Updated%20Title&status=published" \
  -L
```

### Delete Content

```bash
curl -X DELETE "http://localhost:5000/content/123" \
  -H "Cookie: session=..." \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "csrf_token=abc123&confirm=true" \
  -L
```

### List Posts

```bash
curl "http://localhost:5000/content/?type=post&status=published&page=1"
```

---

## Security

### Input Sanitization

- **HTML Content:** Sanitized with Bleach library
  - Allowed tags: `<p>`, `<a>`, `<b>`, `<i>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<br>`, `<code>`, `<pre>`
  - Allowed attributes: `href` (on `<a>`), `class`, `id`
  - Dangerous tags/attributes stripped

### XSS Protection

- All user input escaped by default
- HTML content sanitized before storage
- CSP headers prevent inline scripts

### Access Control

| Action | Public | Author | Admin |
|--------|--------|--------|-------|
| View Published | ✓ | ✓ | ✓ |
| View Draft | ✗ | ✓ | ✓ |
| Create | ✗ | ✓ | ✓ |
| Edit Own | ✗ | ✓ | ✓ |
| Edit Others | ✗ | ✗ | ✓ |
| Delete Own | ✗ | ✓ | ✓ |
| Delete Others | ✗ | ✗ | ✓ |

---

## Related Documentation

- [Admin Content Management](./admin-endpoints.md)
- [Content Editor Guide](../guides/content-editor.md)
- [Markdown Support](../guides/markdown-guide.md)

---

**Last Updated:** 2025-12-30  
**API Version:** 0.1.0-Beta

