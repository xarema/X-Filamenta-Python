# Test serveur mode dev
# Pour vérifier que l'application fonctionne

import os
import sys

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.src.app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 60)
    print("DEMARRAGE EN MODE DEV (Flask)")
    print("=" * 60)
    print("URL: http://127.0.0.1:5000/")
    print("=" * 60)

    app.run(host="127.0.0.1", port=5000, debug=True)
