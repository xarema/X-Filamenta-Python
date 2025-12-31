"""
Commande Flask CLI pour créer un utilisateur admin

Usage:
    flask create-admin
"""

import click
from flask import current_app
from flask.cli import with_appcontext

from backend.src.extensions import db
from backend.src.models.user import User


@click.command("create-admin")
@click.option("--username", default="admin", help="Nom d'utilisateur admin")
@click.option("--email", default="admin@xarema.local", help="Email admin")
@click.option("--password", default="Admin123!", help="Mot de passe admin")
@with_appcontext
def create_admin_command(username, email, password):
    """Créer un utilisateur administrateur"""

    # Vérifier si un admin existe déjà
    existing_admin = User.query.filter_by(username=username).first()

    if existing_admin:
        click.echo(f"✓ L'utilisateur '{username}' existe déjà.")
        click.echo(f"  Email: {existing_admin.email}")
        click.echo(f"  Active: {existing_admin.is_active}")
        click.echo(f"  Admin: {existing_admin.is_admin}")
        return

    # Créer un nouvel utilisateur admin
    admin = User(
        username=username,
        email=email,
        is_admin=True,
        is_active=True,
        role="admin",
    )
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    click.echo()
    click.echo("✓ Utilisateur admin créé avec succès !")
    click.echo(f"  Username: {admin.username}")
    click.echo(f"  Email: {admin.email}")
    click.echo(f"  Password: {password}")
    click.echo()
    click.echo("⚠️  IMPORTANT: Changez le mot de passe après la première connexion!")
    click.echo()


def init_app(app):
    """Enregistrer la commande dans l'app Flask"""
    app.cli.add_command(create_admin_command)

