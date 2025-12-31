# Development Documentation

This directory contains documentation for developers working on X-Filamenta-Python.

## Contents

### Setup & Environment
- **[Setup Guide](../guides/01_QUICKSTART.md)** - Quick start guide for setting up the development environment
- **[Development Workflow](../contributing/README.md)** - Contribution guidelines and workflow

### Development Processes

#### Code Quality
- **Linting**: Run `make lint` or `npm run lint`
  - Python: `ruff check .`
  - JavaScript: `eslint .`
  - CSS: `stylelint "frontend/**/*.css"`
- **Formatting**: Run `make format` or `npm run fmt`
  - Python: `ruff format .`
  - JavaScript/CSS: `prettier --write .`
- **Type Checking**: Run `mypy backend/src`

#### Testing
- **Unit Tests**: `pytest backend/tests/unit/`
- **Integration Tests**: `pytest backend/tests/integration/`
- **All Tests**: `pytest` or `make test`
- **Coverage**: `pytest --cov=backend/src --cov-report=html`

#### Pre-commit Hooks
```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Development Tools

#### Scripts
- **`scripts/utils/`** - Utility scripts for common development tasks
- **`scripts/setup/`** - Setup and installation scripts
- **`scripts/hooks/`** - Git hooks for automation

#### Debugging
- **Flask Debug Mode**: Set `FLASK_ENV=development` in `.env`
- **Logging**: Configure logging level in `backend/src/config.py`
- **Database**: Use `flask shell` for interactive database queries

### Build & Deployment

#### Local Development
```bash
# Run development server
python -m backend.src

# With hot reload
flask run --debug

# Production simulation
python run_prod.py
```

#### Docker
```bash
# Build image
docker build -t x-filamenta-python .

# Run container
docker-compose up

# Stop
docker-compose down
```

### Architecture & Design

See [Architecture Documentation](../architecture/) for:
- System design
- Database schema
- API endpoints
- Authentication flow
- Caching strategy

### Troubleshooting

Common development issues and solutions:
- [Troubleshooting Guide](../troubleshooting/README.md)
- [Common Issues](../troubleshooting/common-issues.md)
- [FAQ](../troubleshooting/faq.md)

## Additional Resources

- **[Contributing Guidelines](../../CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](../../CODE_OF_CONDUCT.md)** - Community guidelines
- **[Security Policy](../../SECURITY.md)** - Security practices
- **[Changelog](../../CHANGELOG.md)** - Release history

## Questions?

- Open an issue: https://github.com/xarema/X-Filamenta-Python/issues
- Email: filamenta@xarema.com
