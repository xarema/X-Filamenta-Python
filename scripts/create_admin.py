"""
Script pour créer un utilisateur admin pour X-Filamenta-Python

Usage:
    python scripts/create_admin.py
"""

import sys
from pathlib import Path

# Ajouter le dossier racine au path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from backend.src.app import create_app
from backend.src.services.user_service import UserService


def create_admin_user():
    """Crée un utilisateur administrateur"""
    app = create_app()

    with app.app_context():
        # Importer db et créer les tables si nécessaire
        from backend.src.extensions import db

        # Créer toutes les tables si elles n'existent pas
        print("📦 Vérification de la base de données...")
        db.create_all()
        print("✅ Tables de base de données prêtes")
        print()

        user_service = UserService()

        # Vérifier si l'admin existe déjà
        existing = user_service.get_by_username("admin")
        if existing:
            print("❌ L'utilisateur 'admin' existe déjà")
            print(f"   Email: {existing.email}")
            print(f"   Admin: {existing.is_admin}")
            print(f"   Actif: {existing.is_active}")
            return

        # Créer l'utilisateur admin
        try:
            user = user_service.create(
                username="admin",
                email="admin@example.com",
                password="Admin123!",  # noqa: S106
                is_admin=True,
            )

            print("✅ Utilisateur admin créé avec succès!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Admin: {user.is_admin}")
            print(f"   ID: {user.id}")
            print()
            print("🔐 Credentials de connexion:")
            print("   URL: http://localhost:5000/auth/login")
            print("   Username: admin")
            print("   Password: Admin123!")

        except Exception as e:
            print(f"❌ Erreur lors de la création: {e}")
            raise


if __name__ == "__main__":
    create_admin_user()
