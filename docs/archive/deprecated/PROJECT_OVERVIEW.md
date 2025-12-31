---
Purpose: Recommended reading order and key insights from technology stack analysis
Description: Guide to understanding the complete X-Filamenta-Python project

File: docs/PROJECT_OVERVIEW.md | Repository: X-Filamenta-Python
Created: 2025-12-29T16:55:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Public

---

# X-Filamenta-Python — Complete Project Overview

Welcome to X-Filamenta-Python! This document provides a complete overview of the project and guides you through the available documentation.

---

## 🎯 What is X-Filamenta-Python?

**A modern, secure web application** built with Flask + HTMX + Bootstrap 5, featuring:

- ✅ **Secure Authentication** with 2FA (TOTP + Backup Codes)
- ✅ **Admin Dashboard** for user and content management
- ✅ **Role-Based Access Control** (RBAC)
- ✅ **Internationalization (i18n)** — English + French
- ✅ **Installation Wizard** for first-time setup
- ✅ **Email Integration** with verification and password reset
- ✅ **Audit Logging** for admin actions

**Version:** 0.1.0-Beta  
**License:** AGPL-3.0-or-later  
**Python Version:** 3.12+

---

## 📚 Reading Order

### For Everyone (5 minutes)
1. **This file** — You are here
2. **[../README.md](../README.md)** — Project introduction and quick start

### For Developers (30 minutes)
3. **[../CONTRIBUTING.md](../CONTRIBUTING.md)** — How to contribute
4. **[SETUP.md](SETUP.md)** — Development environment setup
5. **[../docs/README.md](README.md)** — Documentation index

### For Code Contributors (1 hour)
6. **[Analysis_reports/2025-12-29_project-stack-analysis.md](../Analysis_reports/2025-12-29_project-stack-analysis.md)** — Complete technology stack
7. **[.github/copilot-instructions.md](../.github/copilot-instructions.md)** — AI coding rules
8. **[.github/user-preferences.md](../.github/user-preferences.md)** — User preferences & conventions
9. **[.github/workflow-rules.md](../.github/workflow-rules.md)** — Modification workflow

### For Maintainers (2+ hours)
10. **[../SECURITY.md](../SECURITY.md)** — Security policy
11. **[.github/incidents-history.md](../.github/incidents-history.md)** — Past incidents & lessons
12. **[.github/read-before-any-change.md](../.github/read-before-any-change.md)** — Pre-modification checklist
13. **[Architecture documentation](architecture/)** — System design (when available)

### For Researchers (Deep Dive)
- **[Analysis_reports/INDEX.md](../Analysis_reports/INDEX.md)** — All analysis reports
- **[../CHANGELOG.md](../CHANGELOG.md)** — Release history
- **[.github/git-commit-instructions.md](../.github/git-commit-instructions.md)** — Commit conventions

---

## 🏗️ Project Structure at a Glance

```
X-Filamenta-Python/
│
├── backend/                      ← Python Flask application
│   ├── src/
│   │   ├── app.py              ← Flask factory
│   │   ├── models/             ← SQLAlchemy ORM models
│   │   ├── routes/             ← Flask blueprints (auth, admin, etc.)
│   │   ├── services/           ← Business logic
│   │   ├── decorators.py       ← Permission decorators
│   │   └── i18n/              ← Translations (en.json, fr.json)
│   └── tests/                  ← Test suite
│
├── frontend/                     ← HTML + CSS + JS
│   ├── static/
│   │   ├── css/               ← Bootstrap + custom styles
│   │   ├── js/                ← HTMX utilities
│   │   └── images/            ← Application images
│   └── templates/
│       ├── layouts/           ← Base templates
│       ├── pages/             ← Page templates
│       └── admin/             ← Admin dashboard
│
├── migrations/                   ← Alembic database migrations
├── scripts/                      ← Development utilities
├── docs/                         ← Documentation
│
├── .github/                      ← GitHub configuration
│   ├── workflows/              ← GitHub Actions CI/CD
│   ├── prompts/               ← AI prompt templates
│   └── *.md                   ← Rules & instructions
│
├── Dockerfile                    ← Container definition
├── docker-compose.yml           ← Container orchestration
├── pyproject.toml              ← Python project config
├── alembic.ini                 ← Database migration config
└── README.md                   ← Project README
```

---

## 🧠 Key Architectural Concepts

### 1. **Monorepo Structure**
- Backend and frontend in single repository
- Shared configuration via environment variables
- Coordinated testing and deployment

### 2. **Flask Blueprint Organization**
```python
main_bp      → / (home, features, contact)
auth_bp      → /auth (login, register, logout, password reset)
admin_bp     → /admin (users, settings, content, logs)
install_bp   → /install (installation wizard)
```

### 3. **Service Layer Pattern**
- Routes stay thin (validation only)
- Business logic in Services
- Data access through SQLAlchemy ORM
- Easy to test in isolation

### 4. **HTMX-First Frontend**
- Dynamic updates without page reload
- Server renders HTML
- Minimal JavaScript
- Clear separation of concerns

### 5. **Security by Design**
- 2FA (TOTP + Backup codes)
- Bcrypt password hashing
- Fernet encryption for sensitive data
- Rate limiting on sensitive endpoints
- CSRF protection
- Session security

---

## 🛠️ Technology Stack (Quick Reference)

| Category | Technology | Details |
|----------|-----------|---------|
| **Language** | Python 3.12 | Modern, type-hinted |
| **Framework** | Flask 3.0 | Lightweight, modular |
| **Frontend** | HTMX 1.9 + Bootstrap 5 | Dynamic, responsive |
| **Database** | SQLite (SQLAlchemy 2.0) | Portable, ACID-compliant |
| **Authentication** | Session + 2FA | Secure, user-friendly |
| **Server** | Waitress | Production-ready WSGI |
| **Migrations** | Alembic | Version-controlled schema |
| **Testing** | pytest | Comprehensive test suite |
| **Deployment** | Docker + GitHub Actions | Container + CI/CD |

**Full analysis:** See [Analysis_reports/2025-12-29_project-stack-analysis.md](../Analysis_reports/2025-12-29_project-stack-analysis.md)

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/XAREMA/X-Filamenta-Python.git
cd X-Filamenta-Python
```

### 2. Setup Development Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### 3. Run Development Server
```powershell
.\.venv\Scripts\python.exe backend\src\app.py
# Visit http://localhost:5000
```

**Full setup guide:** See [SETUP.md](SETUP.md)

---

## 📋 Critical Rules Before Contributing

### ⚠️ MANDATORY
- ✅ Kill all Python processes before modifications
- ✅ Read [.github/read-before-any-change.md](../.github/read-before-any-change.md)
- ✅ Follow [.github/copilot-instructions.md](../.github/copilot-instructions.md)
- ✅ Use `.venv` paths (not `python` directly)
- ✅ Add file headers to all new files
- ✅ Test in dev mode THEN prod mode
- ✅ Never hardcode translations (use i18n)

### 🚫 NEVER
- ❌ Modify routes without checking incidents history
- ❌ Change design without asking first
- ❌ Create buttons without asking first
- ❌ Hardcode text (must be in JSON translations)
- ❌ Use emoji in PowerShell commands
- ❌ Store debug files at root (use `scripts/`)

---

## 🔒 Security Features

### Authentication
- Secure login with rate limiting
- Email verification
- Password reset with token expiration
- Session management with secure cookies

### 2FA (Two-Factor Authentication)
- TOTP (RFC 6238) — Time-based One-Time Password
- QR code for mobile app setup
- Backup codes for recovery access
- Backup code regeneration

### Data Protection
- Bcrypt password hashing (cost factor 12)
- Fernet symmetric encryption for sensitive fields
- HTTPS recommended for production
- CSRF protection on all forms
- SQL injection prevention (parameterized queries)

### Access Control
- Role-based access control (RBAC)
- Admin vs regular user roles
- Custom decorators for permission checks
- Audit logging of admin actions

---

## 📖 Documentation Roadmap

### Available Now
- ✅ README.md — Project overview
- ✅ CONTRIBUTING.md — Contribution guidelines
- ✅ CODE_OF_CONDUCT.md — Community standards
- ✅ SECURITY.md — Security policy
- ✅ docs/SETUP.md — Development setup
- ✅ docs/README.md — Documentation index

### In Progress (Phase 2)
- 📋 Architecture documentation
- 📋 API reference
- 📋 Database schema
- 📋 Deployment guide

### Planned
- 🔜 Video tutorials
- 🔜 Architecture diagrams
- 🔜 Advanced guides

---

## 🤝 Getting Help

### Questions?
1. Check [docs/README.md](README.md) for topic
2. Search existing issues on GitHub
3. Open a discussion or issue

### Security Issues?
See [../SECURITY.md](../SECURITY.md) for responsible disclosure

### Contributing Issues?
See [../CONTRIBUTING.md](../CONTRIBUTING.md)

### Technical Details?
Check [.github/](../.github/) documentation

---

## 📊 Project Status

| Aspect | Status | Notes |
|--------|--------|-------|
| **Core Features** | ✅ Complete | Auth, admin, i18n working |
| **Testing** | ✅ Partial | Unit tests in place |
| **Documentation** | 📈 Improving | Phase 1 cleanup complete |
| **Security** | ✅ Strong | 2FA, encryption, rate limiting |
| **Deployment** | ✅ Ready | Docker + GitHub Actions |
| **Code Quality** | ✅ High | Type hints, linting, formatting |

**Version:** 0.1.0-Beta  
**Status:** Production-ready (with caveats noted in README)

---

## 🎓 Learning Path

### Level 1: Beginner (Read These)
1. README.md
2. CONTRIBUTING.md
3. docs/SETUP.md
4. docs/QUICK_START.md (when available)

### Level 2: Intermediate (Then Read These)
5. Project_stack_analysis.md
6. Architecture documentation (when available)
7. .github/copilot-instructions.md (full)
8. .github/frontend.instructions.md (if frontend work)

### Level 3: Advanced (Deep Dives)
9. .github/python.instructions.md (full)
10. .github/workflow-rules.md (full)
11. Backend source code review
12. incidents-history.md (learn from past issues)

### Level 4: Expert (Maintenance)
13. All .github/*.md files
14. All analysis reports
15. Git commit history
16. CI/CD workflows

---

## 🎯 Common Tasks

### I want to...

**...set up development environment**
→ [docs/SETUP.md](SETUP.md)

**...understand how the project works**
→ [Analysis_reports/2025-12-29_project-stack-analysis.md](../Analysis_reports/2025-12-29_project-stack-analysis.md)

**...contribute code**
→ [../CONTRIBUTING.md](../CONTRIBUTING.md)

**...add a new feature**
→ [.github/copilot-instructions.md](../.github/copilot-instructions.md) + feature blueprint

**...fix a bug**
→ [.github/workflow-rules.md](../.github/workflow-rules.md)

**...report a security issue**
→ [../SECURITY.md](../SECURITY.md)

**...understand code rules**
→ [.github/](../.github/) documentation

**...test my changes**
→ [docs/SETUP.md](SETUP.md#testing-workflow)

---

## 📈 Next Steps

1. **Explore** the codebase
2. **Read** the relevant documentation
3. **Setup** your development environment
4. **Run** the application locally
5. **Contribute** improvements

---

## 🏆 Project Highlights

- 🔐 **Security-First** — 2FA, encryption, rate limiting
- 🌍 **Internationalized** — Multi-language support
- 📱 **Modern Frontend** — HTMX + Bootstrap 5
- 🏭 **Production-Ready** — Docker, CI/CD, monitoring
- 📚 **Well-Documented** — Comprehensive guides
- 🧪 **Well-Tested** — Pytest with coverage
- 🎯 **Clean Architecture** — MVC + Service layer
- ♻️ **Maintainable** — Type hints, linting, formatting

---

## 📞 Contact & Support

For questions or issues:
- **GitHub Issues:** https://github.com/XAREMA/X-Filamenta-Python/issues
- **GitHub Discussions:** https://github.com/XAREMA/X-Filamenta-Python/discussions
- **Security Issues:** See [../SECURITY.md](../SECURITY.md)

---

**Happy coding! Welcome to the X-Filamenta-Python project!** 🎉

---

*Last Updated: 2025-12-29*  
*Version: 0.1.0-Beta*  
*Status: Complete*

