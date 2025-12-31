# X-Filamenta-Python

[![CI](https://github.com/xarema/X-Filamenta-Python/actions/workflows/ci.yml/badge.svg)](https://github.com/xarema/X-Filamenta-Python/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Version](https://img.shields.io/badge/version-0.1.0--beta-orange.svg)](https://github.com/xarema/X-Filamenta-Python/releases)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Version:** 0.1.0-Beta  
**License:** AGPL-3.0-or-later  
**Distributed by:** XAREMA  
**Coder:** AleGabMar  
**Contact:** filamenta@xarema.com

---

## 🎯 About

X-Filamenta-Python is a modern web application built with: 

- **Backend:** Flask 3.0+ (Python 3.12+)
- **Frontend:** HTMX + Bootstrap 5 + Alpine.js
- **Features:** 2FA authentication, admin panel, i18n support, Redis caching
- **Database:** SQLite, MySQL, or PostgreSQL
- **Deployment:** cPanel, VPS/Linux, Docker

---

## 📚 Documentation

**Complete documentation is located in [docs/](docs/)**

### 🚀 Quick Start

- 📖 **[docs/00_START_HERE.md](docs/00_START_HERE.md)** — ⭐ Read this first!
- ⚡ **[docs/guides/01_QUICKSTART.md](docs/guides/01_QUICKSTART.md)** — 5-minute setup
- 📚 **[docs/REFERENCE.md](docs/REFERENCE.md)** — Complete reference

### 🌍 Deployment Guides

| Platform | Guide | Duration |
|----------|-------|----------|
| **cPanel** | [docs/deployment/01_CPANEL.md](docs/deployment/01_CPANEL.md) | 30 min |
| **VPS/Linux** | [docs/deployment/02_VPS_LINUX.md](docs/deployment/02_VPS_LINUX.md) | 1h |
| **Docker** | [docs/deployment/03_DOCKER.md](docs/deployment/03_DOCKER.md) | 15 min |

### 📖 Full Documentation

- **Guides** → [docs/guides/](docs/guides/)
- **Features** → [docs/features/](docs/features/)
- **Architecture** → [docs/architecture/](docs/architecture/)
- **Security** → [docs/security/](docs/security/)
- **Contributing** → [docs/contributing/](docs/contributing/)
- **Troubleshooting** → [docs/troubleshooting/](docs/troubleshooting/)

---

## ✨ Key Features

- ✅ **2FA Authentication** (TOTP with backup codes)
- ✅ **Email Verification** (with password reset)
- ✅ **Admin Panel** (user/content management, settings)
- ✅ **Multi-language** (i18n support, FR/EN)
- ✅ **Redis Caching** (with filesystem fallback)
- ✅ **Rate Limiting** (anti brute-force)
- ✅ **CSRF Protection** (all forms)
- ✅ **Responsive UI** (Bootstrap 5 + HTMX)

---

## 🚀 Quick Install

### Prerequisites

- **Python:** 3.12+
- **Node.js:** 18+
- **Git:** Latest version

### Installation (Windows PowerShell)

```powershell
# Clone repository
git clone https://github.com/xarema/X-Filamenta-Python.git
cd X-Filamenta-Python

# Create virtual environment
python -m venv .venv
. \. venv\Scripts\Activate. ps1

# Install Python dependencies
pip install -r requirements. txt
pip install -r requirements-dev.txt
pip install -e .

# Install frontend tools
npm install

# Install pre-commit hooks
pre-commit install

# Copy environment template
Copy-Item .env.example .env
# Edit .env with your configuration

# Run application
python -m backend.src
```

### Installation (Linux/macOS)

```bash
# Clone repository
git clone https://github.com/xarema/X-Filamenta-Python.git
cd X-Filamenta-Python

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# Install frontend tools
npm install

# Install pre-commit hooks
pre-commit install

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run application
python -m backend.src
```

---

## 🛠️ Development Commands

### Code Quality

```bash
# Python linting & formatting
make lint-py          # Ruff + Mypy
make fmt-py           # Auto-format with Ruff

# Frontend linting & formatting
make lint-front       # ESLint + Stylelint
make fmt-front        # Prettier

# All checks
make lint             # Lint everything
make fmt              # Format everything
```

### Testing

```bash
make test             # Run pytest with coverage
pytest -v             # Verbose mode
pytest --cov          # Coverage report
```

### Development Server

```bash
# Development mode (auto-reload, debug)
python -m backend.src

# Production mode (Waitress WSGI)
python run_prod.py    # Windows
./run_prod.sh         # Linux/macOS
```

Application runs at:  `http://127.0.0.1:5000`

---

## 📦 Project Structure

```
X-Filamenta-Python/
├── backend/
│   ├── src/                  # Source code
│   │   ├── models/           # Database models
│   │   ├── routes/           # Flask blueprints
│   │   ├── services/         # Business logic
│   │   ├── utils/            # Utilities
│   │   └── app.py            # App factory
│   └── tests/                # Tests
│       ├── unit/
│       ├── integration/
│       └── conftest.py
├── frontend/
│   ├── static/               # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/            # Jinja2 templates
│       ├── layouts/
│       ├── components/
│       └── pages/
├── scripts/                  # Utility scripts
│   ├── setup/                # Setup scripts
│   ├── utils/                # Maintenance scripts
│   └── hooks/                # Git hooks
├── docs/                     # Documentation
├── . github/                  # GitHub config + Copilot rules
├── Analysis_reports/         # Analysis reports
├── pyproject.toml            # Python config
├── package.json              # Node.js config
└── README.md
```

---

## 🔒 Security

- ✅ CSRF protection on all forms
- ✅ Rate limiting on authentication endpoints
- ✅ Password hashing with bcrypt
- ✅ 2FA with TOTP (RFC 6238)
- ✅ Secure session management
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection (auto-escaping templates)

**Security reports:** Please email security issues to [filamenta@xarema. com](mailto:filamenta@xarema.com)

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**.

**Key requirements:**
- ✅ Source code must be made available to users
- ✅ Preserve all copyright and license notices
- ✅ Document any modifications
- ✅ Provide link to original source

See [LICENSE](LICENSE) for full text.

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines: 

1. **Code of Conduct:** Be respectful and constructive
2. **Follow conventions:** See `.github/copilot-instructions.md`
3. **Add tests:** Maintain >50% coverage (target 80%)
4. **Update docs:** Document all changes
5. **Run checks:** `make lint && make test` before committing

See [docs/contributing/](docs/contributing/) for detailed guidelines.

---

## 📞 Support

For questions, issues, or contributions: 

- 📖 **Documentation:** [docs/](docs/)
- 🐛 **Bug reports:** [GitHub Issues](https://github.com/xarema/X-Filamenta-Python/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/xarema/X-Filamenta-Python/discussions)
- 📧 **Email:** [filamenta@xarema. com](mailto:filamenta@xarema.com)
- 📝 **Analysis reports:** [Analysis_reports/](Analysis_reports/)

---

## 🙏 Acknowledgments

Built with: 
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [HTMX](https://htmx.org/) — Modern web interactivity
- [Bootstrap](https://getbootstrap.com/) — CSS framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — Python ORM
- [Redis](https://redis.io/) — In-memory cache
- [Ruff](https://docs.astral.sh/ruff/) — Python linter/formatter

---

**Copyright (c) 2025 XAREMA. All rights reserved.**