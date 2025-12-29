"""
Script de démarrage de production pour X-Filamenta-Python (Windows)
Utilise Waitress comme serveur WSGI.

File: run_prod.py
"""

import os
import sys

from waitress import serve

from backend.src.app import create_app

# S'assurer que le répertoire racine est dans le path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Charger l'application
app = create_app()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000

    print("=" * 60)
    print("DEMARRAGE EN MODE PRODUCTION (Waitress)")
    print("=" * 60)
    print(f"URL: http://{host}:{port}/")
    print("Le wizard d'installation s'affichera au premier acces.")
    print("=" * 60)
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 60)

    # Lancement du serveur WSGI
    serve(app, host=host, port=port, threads=4)
