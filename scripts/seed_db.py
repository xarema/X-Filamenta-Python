"""
------------------------------------------------------------------------------
Purpose: Database seed script
Description: Populate database with initial/demo data

File: scripts/seed_db.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Internal

Usage:
    python scripts/seed_db.py
------------------------------------------------------------------------------
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.src.app import create_app
from backend.src.services.content_service import ContentService
from backend.src.services.user_service import UserService


def seed_users():
    """Create default users"""
    print("📝 Creating users...")

    # Admin user
    admin = UserService.create(
        username="admin",
        email="admin@xarema.com",
        password=os.getenv("SEED_ADMIN_PASSWORD", "ChangeMe!42"),
        is_admin=True,
    )

    if admin:
        print(f"  ✅ Admin user created: {admin.username}")
    else:
        print("  ⚠️  Admin user already exists or creation failed")

    # Guest user
    guest = UserService.create(
        username="guest",
        email="guest@xarema.com",
        password=os.getenv("SEED_GUEST_PASSWORD", "ChangeMe!42"),
        is_admin=False,
    )

    if guest:
        print(f"  ✅ Guest user created: {guest.username}")
    else:
        print("  ⚠️  Guest user already exists or creation failed")

    # Demo user
    demo = UserService.create(
        username="demo",
        email="demo@xarema.com",
        password=os.getenv("SEED_DEMO_PASSWORD", "ChangeMe!42"),
        is_admin=False,
    )

    if demo:
        print(f"  ✅ Demo user created: {demo.username}")
    else:
        print("  ⚠️  Demo user already exists or creation failed")

    return admin, guest, demo


def seed_content(admin_user, demo_user):
    """Create demo content"""
    print("\n📄 Creating content...")

    # Create posts
    posts = [
        {
            "title": "Bienvenue sur X-Filamenta-Python",
            "body": """Ceci est le premier article de démonstration.

X-Filamenta-Python est une application web moderne construite avec Flask,
Bootstrap 5, HTMX et Alpine.js.

Cette plateforme offre:
- Une architecture modulaire
- Un design moderne
- Une base solide pour vos projets""",
            "author_id": admin_user.id if admin_user else 1,
            "content_type": "post",
            "status": "published",
        },
        {
            "title": "Guide de démarrage rapide",
            "body": """Ce guide vous aidera à démarrer avec X-Filamenta-Python.

## Installation

1. Cloner le repository
2. Installer les dépendances: `pip install -r requirements.txt`
3. Configurer .env
4. Lancer l'application: `flask run`

## Fonctionnalités

- Dashboard administrateur
- Gestion des utilisateurs
- Système de préférences
- Notifications en temps réel
- Et bien plus!

Consultez la documentation pour plus d'informations.""",
            "author_id": admin_user.id if admin_user else 1,
            "content_type": "post",
            "status": "published",
        },
        {
            "title": "Article de test (brouillon)",
            "body": """Ceci est un brouillon qui n'est pas encore publié.

Il contient du contenu de test pour vérifier le système de statuts.""",
            "author_id": demo_user.id if demo_user else 2,
            "content_type": "post",
            "status": "draft",
        },
    ]

    for post_data in posts:
        content = ContentService.create(**post_data)
        if content:
            print(f"  ✅ Content created: {content.title} (status: {content.status})")
        else:
            print(f"  ⚠️  Failed to create content: {post_data['title']}")

    # Create a page
    page = ContentService.create(
        title="À propos de nous",
        body="""# À propos de X-Filamenta-Python

X-Filamenta-Python est un projet open-source conçu pour fournir une base
solide pour les applications web modernes.

## Mission
Offrir une fondation robuste et extensible pour les développeurs, avec des
choix technologiques modernes.

## Vision
Favoriser l'adoption de pratiques modernes et de frameworks qui permettent
aux développeurs de construire rapidement des applications de qualité.
""",
        author_id=admin_user.id if admin_user else 1,
        content_type="page",
        status="published",
    )

    if page:
        print(f"  ✅ Page created: {page.title}")


def main():
    """Main seed function"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║                                                        ║")
    print("║         🌱 SEEDING DATABASE - X-Filamenta-Python       ║")
    print("║                                                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")

    # Create app
    app = create_app()

    with app.app_context():
        # Seed users
        admin, guest, demo = seed_users()

        # Seed content
        seed_content(admin, demo)

        print("\n✅ Database seeded successfully!")
        print("\n📋 Default credentials:")
        print("  Admin:")
        print("    Username: admin")
        print("    Password: admin123")
        print("\n  Guest:")
        print("    Username: guest")
        print("    Password: guest123")
        print("\n⚠️  IMPORTANT: Change default passwords in production!\n")


if __name__ == "__main__":
    main()
