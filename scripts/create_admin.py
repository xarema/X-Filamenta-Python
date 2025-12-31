"""
Script pour créer un utilisateur admin initial

Usage:
    python scripts/create_admin.py
"""

import os
import sys
from pathlib import Path

# Configuration du path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Import après configuration du path
from backend.src.app import create_app
from backend.src.extensions import db
from backend.src.models.user import User


def create_admin_user():
    """Créer un utilisateur admin par défaut"""
    app = create_app()

    with app.app_context():
        # Vérifier si un admin existe déjà
        existing_admin = User.query.filter_by(username="admin").first()

        if existing_admin:
            print("✓ Un utilisateur admin existe déjà.")
            print(f"  Username: {existing_admin.username}")
            print(f"  Email: {existing_admin.email}")
            print(f"  Active: {existing_admin.is_active}")
            return

        # Créer un nouvel utilisateur admin
        admin = User(
            username="admin",
            email="admin@xarema.local",
            is_admin=True,
            is_active=True,
            role="admin",
        )
        admin.set_password("Admin123!")  # Mot de passe temporaire à changer

        db.session.add(admin)
        db.session.commit()

        print("✓ Utilisateur admin créé avec succès !")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Password: Admin123! (À CHANGER IMMÉDIATEMENT)")
        print()
        print("⚠️  IMPORTANT: Changez le mot de passe après la première connexion!")


if __name__ == "__main__":
    create_admin_user()

