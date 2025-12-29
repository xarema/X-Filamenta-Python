"""
Script pour appliquer la migration User 2FA manuellement
"""

import sys
from pathlib import Path

# Ajouter le dossier racine au path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from backend.src.app import create_app
from backend.src.extensions import db

print("🔧 Application migration User 2FA...")
print()

app = create_app()

with app.app_context():
    # Créer toutes les tables si elles n'existent pas
    print("📦 Vérification/création des tables...")
    db.create_all()
    print("✅ Tables prêtes")
    print()

    # Vérifier si la colonne role existe déjà
    print("🔍 Vérification des colonnes existantes...")
    result = db.session.execute(db.text("PRAGMA table_info(users)"))
    columns = [row[1] for row in result]

    if "role" in columns:
        print("✅ Migration déjà appliquée (colonne 'role' existe)")
        print()
        print("📊 Champs 2FA disponibles:")
        print("   - role")
        print("   - totp_secret")
        print("   - totp_enabled")
        print("   - backup_codes")
        print("   - last_login")
        print("   - last_login_ip")
        print("   - login_attempts")
        print("   - locked_until")
        print("   - email_verified")
        print("   - email_verification_token")
    else:
        print("❌ Les nouvelles colonnes ne sont pas présentes")
        print("   → Utilisez db.create_all() qui créera la table avec tous les champs")
        print()
        print(
            "💡 Conseil: Supprimez instance/app.db et relancez scripts/create_admin.py"
        )
