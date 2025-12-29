"""
------------------------------------------------------------------------------
Purpose: Language switch routes
Description: Set language in session and redirect back.

File: backend/src/routes/lang.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): TBD | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.1-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Draft
- Classification: Public

Notes:
- Simple language switcher endpoint
- Stores language in session
- Supports FR and EN
- Redirects back to referrer
------------------------------------------------------------------------------
"""

from typing import Any

from flask import Blueprint, redirect, request, session, url_for

from backend.src.services.i18n_service import SUPPORTED_LANGS
from backend.src.services.install_service import InstallService

lang_bp = Blueprint("lang", __name__, url_prefix="/lang")


@lang_bp.route("/<code>")
def set_language(code: str) -> Any:
    if code not in SUPPORTED_LANGS:
        code = "en"
    session["lang"] = code

    # Si start=1 en paramètre, c'est le début du wizard
    if request.args.get("start") == "1":
        # Réinitialiser tout l'état du wizard pour éviter les boucles et le saut d'étapes
        InstallService.clear_wizard_state(session)
        session.pop("wizard_started", None)
        # Forcer le démarrage sur l'étape de bienvenue
        session["wizard_state"] = {"step": "welcome"}
        session["wizard_started"] = True
        session.modified = True

    referrer = request.headers.get("Referer")
    if referrer:
        return redirect(referrer)
    return redirect(url_for("main.index"))
