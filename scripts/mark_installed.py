"""
Marquer l'installation comme complète
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier racine au path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from backend.src.services.install_service import InstallService

print("🔧 Marquage de l'installation comme complète...")
print()

app_root = str(root_dir)

# Vérifier si déjà installé
if InstallService.is_installed(app_root):
    print("✅ L'application est déjà marquée comme installée")
else:
    # Marquer comme installé
    InstallService.mark_installed(app_root)
    print("✅ Installation marquée comme complète")

# Vérifier
flag_file = os.path.join(app_root, "instance", ".installed")
print(f"\n📁 Fichier flag: {flag_file}")
print(f"   Existe: {os.path.exists(flag_file)}")

print("\n🎉 L'application ne redirigera plus vers /install")
print("   Vous pouvez maintenant accéder à /auth/login et /dashboard")
