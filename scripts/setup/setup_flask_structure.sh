#!/bin/bash
# Setup Flask Project Structure
# 
# Purpose: Create recommended directory structure for Flask + HTMX project
# Description: Generates folders, __init__.py files, and basic templates
#
# File: scripts/setup/setup_flask_structure.sh | Repository: X-Filamenta-Python
# Created: 2025-12-30
# Last modified (Git): TBD | Commit: TBD
#
# Distributed by:  XAREMA | Coder:  AleGabMar
# App version: 0.0.1-Alpha | File version: 1.0.0
#
# License: AGPL-3.0-or-later
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (c) 2025 XAREMA.  All rights reserved. 
#
# Metadata:
# - Status: Stable
# - Classification: Internal
#
# Usage:
#   bash scripts/setup/setup_flask_structure.sh

set -e

echo "🏗️  Creating Flask Project Structure..."

# Core application structure
mkdir -p backend/src/{templates,static/{css,js,img},models,routes,services,utils}

# Templates organization
mkdir -p backend/src/templates/{components,layouts,pages,partials}

# Testing
mkdir -p tests/{unit,integration,functional}

# Documentation
mkdir -p docs/{architecture,api,guides,development}

# Scripts and tools
mkdir -p scripts/{setup,utils,hooks}

# Config
mkdir -p config

# Logs (local only, in . gitignore)
mkdir -p logs

# Instance (database, uploads - in .gitignore)
mkdir -p instance

# Create __init__.py files
touch backend/src/__init__.py
touch backend/src/models/__init__.py
touch backend/src/routes/__init__.py
touch backend/src/services/__init__.py
touch backend/src/utils/__init__. py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/functional/__init__.py

# Create basic app factory
cat > backend/src/__init__.py << 'EOF'
"""
Flask Application Factory

Purpose: Create and configure Flask application
File: backend/src/__init__.py | Repository: X-Filamenta-Python

License: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved. 
"""
from flask import Flask


def create_app(config_name:  str = "development") -> Flask:
    """
    Create and configure Flask application. 
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    from backend.src.config import config
    app.config.from_object(config[config_name])
    
    # Register blueprints
    from backend. src.routes. main import bp as main_bp
    app. register_blueprint(main_bp)
    
    return app
EOF

# Create main routes
mkdir -p backend/src/routes
cat > backend/src/routes/main.py << 'EOF'
"""
Main Routes Blueprint

Purpose: Main application routes
File: backend/src/routes/main.py | Repository: X-Filamenta-Python

License: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved. 
"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage route."""
    return render_template('pages/index.html')
EOF

# Create config file
cat > backend/src/config.py << 'EOF'
"""
Flask Configuration

Purpose: Application configuration classes
File: backend/src/config.py | Repository: X-Filamenta-Python

License:  AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.
"""
import os
from pathlib import Path

basedir = Path(__file__).parent.parent.parent. absolute()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "instance" / "app.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    pass


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development':  DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
EOF

# Create base template
cat > backend/src/templates/layouts/base.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap. bundle.min.js"></script>
    
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
EOF

# Create index page
cat > backend/src/templates/pages/index.html << 'EOF'
{% extends 'layouts/base.html' %}

{% block title %}Home - Flask App{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12 text-center">
        <h1>Welcome to Flask + HTMX</h1>
        <p class="lead">Your project structure is ready! </p>
        <hr class="my-4">
        <p>Start building your application. </p>
    </div>
</div>
{% endblock %}
EOF

# Create navbar component
cat > backend/src/templates/components/navbar.html << 'EOF'
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Flask App</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('main.index') }}">Home</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
EOF

# Create footer component
cat > backend/src/templates/components/footer.html << 'EOF'
<footer class="mt-5 py-3 bg-light">
    <div class="container text-center">
        <p class="text-muted mb-0">© 2025 XAREMA. Licensed under AGPL-3.0-or-later.</p>
    </div>
</footer>
EOF

# Create CSS
cat > backend/src/static/css/main.css << 'EOF'
/* Main Stylesheet */
: root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
}

body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}
EOF

# Create JS
cat > backend/src/static/js/main.js << 'EOF'
// Main JavaScript
console.log('Flask + HTMX app loaded');

// HTMX event listeners
document.body.addEventListener('htmx:afterSwap', function(event) {
    console.log('HTMX swap completed');
});
EOF

# Create . env. example
cat > . env.example << 'EOF'
# Flask Configuration
FLASK_APP=backend. src
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///instance/app.db

# Debug
DEBUG=True
EOF

# Create . flaskenv
cat > . flaskenv << 'EOF'
FLASK_APP=backend.src
FLASK_ENV=development
EOF

# Create .editorconfig
cat > .editorconfig << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4

[*.{html,css,js}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
EOF

# Create app.py entry point
cat > app.py << 'EOF'
"""
Flask Application Entry Point

Purpose: Development server entry point
File: app.py | Repository: X-Filamenta-Python

License:  AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.
"""
from backend.src import create_app

app = create_app('development')

if __name__ == '__main__':
    app. run(debug=True, host='0.0.0.0', port=5000)
EOF

echo ""
echo "✅ Flask project structure created successfully!"
echo ""
echo "📋 Next steps:"
echo "  1. Create virtual environment:  python -m venv . venv"
echo "  2. Activate it:"
echo "     - Linux/Mac: source .venv/bin/activate"
echo "     - Windows PowerShell: .\\. venv\\Scripts\\Activate.ps1"
echo "  3. Install dependencies: pip install -r requirements.txt"
echo "  4. Copy . env.example to .env and configure"
echo "  5. Run the app:"
echo "     - Development: python app.py"
echo "     - Production: python run_prod. py"
echo ""
echo "📚 Documentation:  docs/"
echo "🧪 Tests: tests/"
echo "🛠️  Scripts: scripts/"