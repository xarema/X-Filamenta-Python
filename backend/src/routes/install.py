"""
------------------------------------------------------------------------------
Purpose: Installation wizard routes
Description: Flask Blueprint handling multi-step HTMX installation wizard.

File: backend/src/routes/install.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): 2025-12-28T13:30:00+01:00 | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.3-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal

Notes:
- Multi-step installation wizard
- Database configuration
- Admin user setup
- Support for SQLite, MySQL, PostgreSQL
- HTMX-based progressive enhancement
- One-time setup token for security
------------------------------------------------------------------------------
"""

from __future__ import annotations

import os
from typing import Any

from flask import Blueprint, current_app, redirect, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.src.extensions import db
from backend.src.services.install_service import InstallService
from backend.src.utils import i18n

install = Blueprint("install", __name__, url_prefix="/install")


@install.before_request
def block_if_installed() -> Any:
    # In tests, bypass the installation guard to allow wizard steps
    if current_app and (
        current_app.config.get("TESTING") or os.environ.get("PYTEST_CURRENT_TEST")
    ):
        return None

    # Permettre verify-db même après installation (pour déboguer)
    from flask import request

    if request.endpoint == "install.verify_db":
        return None

    # Get app_root correctly (handle both / and \ path separators)
    app_root = os.path.dirname(os.path.dirname(os.path.dirname(install.root_path)))

    if InstallService.is_installed(app_root):
        return redirect("/")
    return None


@install.route("/", methods=["GET"])
def install_index() -> str:
    app_root = os.path.abspath(os.path.join(install.root_path, "..", "..", ".."))

    state = InstallService.get_wizard_state(session)
    wizard_started = session.get("wizard_started")

    # Si le wizard n'a pas démarré, on affiche la sélection de langue
    if not wizard_started and not state:
        env_summary = InstallService.render_env_summary(app_root)
        return render_template(
            "pages/install/index.html",
            env=env_summary,
            state={},
            step="language",
            session=session,
        )

    # Wizard démarré (langue choisie) : s'assurer d'un step par défaut
    if not wizard_started:
        session["wizard_started"] = True
    if not state:
        state = {"step": "welcome"}
        InstallService.save_wizard_state(session, state)

    env_summary = InstallService.render_env_summary(app_root)
    step = state.get("step") or "welcome"

    return render_template(
        "pages/install/index.html",
        env=env_summary,
        state=state,
        step=step,
        session=session,
    )


@install.route("/step", methods=["POST"])
def install_step() -> Any:
    payload: dict[str, Any] = request.form.to_dict()
    state = InstallService.get_wizard_state(session)
    state.update(payload)
    # Mémoriser l'étape courante pour le breadcrumb
    state["step"] = payload.get("step") or "db_form"
    InstallService.save_wizard_state(session, state)

    # IMPORTANT: Activer le breadcrumb dès qu'on arrive à step
    session["wizard_started"] = True
    session.modified = True

    step = state.get("step") or "db_form"
    current_app.logger.info(f"WIZARD STEP: {step}")
    app_root = os.path.abspath(os.path.join(install.root_path, "..", "..", ".."))

    # Determine current active tab from state or payload
    active_tab = state.get("db_type") or payload.get("db_type") or "sqlite"

    # Toujours retourner la page complète (pas de HTMX)
    def render_full_page(extra_context: dict[str, Any] | None = None) -> str:
        env_summary = InstallService.render_env_summary(app_root)
        ctx = {
            "state": state,
            "env": env_summary,
            "session": session,
            "step": step,
            "t": i18n.t,  # Fonction de traduction
        }
        if extra_context:
            ctx.update(extra_context)
        return render_template("pages/install/index.html", **ctx)

    if step == "welcome":
        # Reset to welcome step (but keep language)
        return render_full_page()

    if step == "requirements":
        # Detect Redis availability
        redis_detection = InstallService.detect_redis_standard()

        # Store in state for next steps
        state["redis_available"] = redis_detection.get("detected", False)
        state["redis_version"] = redis_detection.get("version")

        return render_full_page({"redis_detection": redis_detection})

    if step == "db_form":
        db_uri = state.get("db_uri") or InstallService.default_sqlite_uri(app_root)
        return render_full_page({"db_uri": db_uri, "active_tab": active_tab})

    if step == "db_test":
        db_uri = None
        error_msg = None
        # Obtenir app_root correctement (compatible Windows et Linux)
        app_root = os.path.abspath(os.path.join(install.root_path, "..", "..", ".."))

        if "sqlite_dbname" in payload or active_tab == "sqlite":
            dbname = payload.get(
                "sqlite_dbname", state.get("sqlite_dbname") or "x-filamenta_python.db"
            )
            uri, err = InstallService.ensure_sqlite_db(app_root, dbname)
            if err:
                error_msg = err
            else:
                db_uri = uri
            state.update({"db_type": "sqlite", "sqlite_dbname": dbname})

        elif payload.get("db_type") == "mysql":
            host = payload.get("mysql_host", state.get("mysql_host") or "localhost")
            port = payload.get("mysql_port", state.get("mysql_port") or "3306")
            user = payload.get("mysql_user", state.get("mysql_user") or "root")
            password = payload.get("mysql_password", state.get("mysql_password") or "")
            dbname = payload.get("mysql_dbname", state.get("mysql_dbname") or "myapp")
            db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
            state.update(
                {
                    "db_type": "mysql",
                    "mysql_host": host,
                    "mysql_port": port,
                    "mysql_user": user,
                    "mysql_password": password,
                    "mysql_dbname": dbname,
                }
            )

        elif payload.get("db_type") == "postgresql":
            host = payload.get("pg_host", state.get("pg_host") or "localhost")
            port = payload.get("pg_port", state.get("pg_port") or "5432")
            user = payload.get("pg_user", state.get("pg_user") or "postgres")
            password = payload.get("pg_password", state.get("pg_password") or "")
            dbname = payload.get("pg_dbname", state.get("pg_dbname") or "myapp")
            db_uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            state.update(
                {
                    "db_type": "postgresql",
                    "pg_host": host,
                    "pg_port": port,
                    "pg_user": user,
                    "pg_password": password,
                    "pg_dbname": dbname,
                }
            )

        if not db_uri and not error_msg:
            app_root_fallback = os.path.abspath(
                os.path.join(install.root_path, "..", "..", "..")
            )
            db_uri = state.get("db_uri") or InstallService.default_sqlite_uri(
                app_root_fallback
            )

        ok = False
        test_msg = ""
        if not error_msg and db_uri:
            ok, test_msg = InstallService.test_db_connection(db_uri)
            if ok:
                schema_ok, schema_msg = InstallService.create_schema(db_uri)
                ok = ok and schema_ok
                if not schema_ok:
                    error_msg = schema_msg
        else:
            test_msg = error_msg or "URI manquante"

        state["db_uri"] = db_uri
        InstallService.save_wizard_state(session, state)
        return render_full_page(
            {
                "ok": ok,
                "db_uri": db_uri,
                "error": error_msg or (None if ok else test_msg),
            }
        )

    if step == "upload_form":
        return render_full_page()

    if step == "upload":
        file = request.files.get("backup")
        ok, msg = (
            InstallService.validate_backup(file)
            if file
            else (
                False,
                "Aucun fichier reçu",
            )
        )
        if ok and file:
            checksum = InstallService.checksum_bytes(file.read())
            file.seek(0)
            state["backup_checksum"] = checksum
            state["backup_filename"] = file.filename
        state["backup_ok"] = ok
        InstallService.save_wizard_state(session, state)
        return render_full_page({"ok": ok, "message": msg})

    if step == "remove_backup":
        # Supprimer les informations de backup de l'état
        state.pop("backup_ok", None)
        state.pop("backup_checksum", None)
        state.pop("backup_filename", None)
        InstallService.save_wizard_state(session, state)
        return render_full_page()

    if step == "admin_form":
        return render_full_page()

    if step == "admin":
        valid, err = InstallService.validate_password(state.get("admin_password", ""))
        if not valid:
            return (
                render_full_page({"error": err}),
                400,
            )
        return render_full_page()

    if step == "cache_config":
        # Get Redis detection result from state
        redis_available = state.get("redis_available", False)
        redis_version = state.get("redis_version")

        # Default cache backend based on detection
        default_backend = "redis" if redis_available else "filesystem"

        return render_full_page(
            {
                "redis_available": redis_available,
                "redis_version": redis_version,
                "default_backend": default_backend,
                "cache_backend": state.get("cache_backend", default_backend),
                "redis_host": state.get("redis_host", "localhost"),
                "redis_port": state.get("redis_port", "6379"),
                "redis_password": state.get("redis_password", ""),
                "redis_db": state.get("redis_db", "0"),
            }
        )

    if step == "cache_test":
        # Save cache configuration to state
        cache_backend = payload.get("cache_backend", "filesystem")
        state["cache_backend"] = cache_backend

        if cache_backend == "redis":
            # Save Redis configuration
            redis_host = payload.get("redis_host", "localhost")
            redis_port = int(payload.get("redis_port", 6379))
            redis_password = payload.get("redis_password", "")
            redis_db = int(payload.get("redis_db", 0))

            state.update(
                {
                    "redis_host": redis_host,
                    "redis_port": redis_port,
                    "redis_password": redis_password,
                    "redis_db": redis_db,
                }
            )

            # Test Redis connection (simple ping)
            from backend.src.services.cache_service import CacheService

            cache_svc = CacheService()

            success, message, info = cache_svc.test_redis_connection(
                host=redis_host,
                port=redis_port,
                password=redis_password or None,
                db=redis_db,
            )

            if not success:
                # Connection failed, fallback to filesystem
                state["cache_backend"] = "filesystem"
                state["cache_test_failed"] = True
                state["cache_test_error"] = message

                return render_full_page(
                    {
                        "test_failed": True,
                        "error_message": message,
                        "fallback": "filesystem",
                    }
                )

            # Connection successful
            state["cache_test_success"] = True
            state["cache_test_info"] = info

            return render_full_page({"test_success": True, "redis_info": info})
        else:
            # Filesystem backend, no test needed
            state["cache_backend"] = "filesystem"
            return render_full_page({"test_success": True, "backend": "filesystem"})

    if step == "summary":
        return render_full_page()

    if step == "finalize":
        app_root = os.path.abspath(os.path.join(install.root_path, "..", "..", ".."))
        errors_list = []

        db_uri = state.get("db_uri")
        if not db_uri:
            errors_list.append("URI de base de données manquante")
        else:
            try:
                # Ensure all models are loaded in metadata
                from backend.src.models.admin_history import AdminHistory  # noqa: F401
                from backend.src.models.content import Content  # noqa: F401
                from backend.src.models.preferences import UserPreferences  # noqa: F401
                from backend.src.models.user import User  # noqa: F401

                # 2. Créer le moteur pour l'URI cible
                engine = create_engine(db_uri)

                # 3. Créer les tables physiquement
                current_app.logger.info(
                    f"Creating tables with metadata: {db.metadata.tables.keys()}"
                )
                db.metadata.create_all(bind=engine)

                # 4. Créer une session dédiée pour les opérations d'install
                Session = sessionmaker(bind=engine)
                install_session = Session()

                try:
                    # Étape 1: Restaurer backup ou appliquer seeds
                    ok_restore, msg_restore = InstallService.apply_seed_or_restore(
                        state
                    )
                    if not ok_restore:
                        errors_list.append(f"Restauration backup: {msg_restore}")

                    # Étape 2: Créer l'administrateur avec CETTE session
                    from backend.src.services.user_service import UserService

                    username = state.get("admin_username") or "admin"
                    email = state.get("admin_email") or "admin@example.com"
                    password = state.get("admin_password") or "ChangeMe!42"

                    admin = UserService.create(
                        username=username,
                        email=email,
                        password=password,
                        is_admin=True,
                        session=install_session,
                    )

                    if not admin:
                        # Vérifier si déjà présent
                        existing = (
                            install_session.query(User)
                            .filter((User.username == username) | (User.email == email))
                            .first()
                        )
                        if not existing:
                            errors_list.append("Échec de création de l'administrateur")

                    if not errors_list:
                        install_session.commit()
                except Exception as op_err:
                    install_session.rollback()
                    import traceback

                    errors_list.append(f"Erreur opérationnelle: {str(op_err)}")
                    current_app.logger.error(
                        f"Install operations error: {traceback.format_exc()}"
                    )
                finally:
                    install_session.close()

                # 5. Si tout est OK, configurer l'application pour le futur
                if not errors_list:
                    current_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
                    db.session.remove()
                    db.session.configure(bind=engine)

                    # Sauvegarder la DB URI dans .env pour les redémarrages futurs
                    env_file = os.path.join(app_root, ".env")
                    try:
                        # Normalize path (avoid Windows escaping issues)
                        db_uri_normalized = db_uri.replace("\\", "/")

                        # Read current .env file
                        env_content = ""
                        if os.path.exists(env_file):
                            with open(env_file, encoding="utf-8") as f:
                                env_content = f.read()

                        # Remove all existing SQLALCHEMY_DATABASE_URI lines
                        import re

                        lines = env_content.split("\n")
                        new_lines = []
                        found_db_uri = False

                        for line in lines:
                            # Skip existing SQLALCHEMY_DATABASE_URI lines
                            if re.match(r"^\s*#?\s*SQLALCHEMY_DATABASE_URI\s*=", line):
                                if not found_db_uri:
                                    # Add new value
                                    new_lines.append(
                                        f"SQLALCHEMY_DATABASE_URI={db_uri_normalized}"
                                    )
                                    found_db_uri = True
                                # Ignorer les autres occurrences (ne pas les ajouter)
                            else:
                                new_lines.append(line)

                        # Si aucune ligne SQLALCHEMY_DATABASE_URI n'existait, l'ajouter
                        if not found_db_uri:
                            new_lines.append("")
                            new_lines.append(
                                "# Database URI set by installation wizard"
                            )
                            new_lines.append(
                                f"SQLALCHEMY_DATABASE_URI={db_uri_normalized}"
                            )

                        env_content = "\n".join(new_lines)

                        # Écrire le fichier .env
                        with open(env_file, "w", encoding="utf-8") as f:
                            f.write(env_content)

                        current_app.logger.info(
                            f"Database URI saved to .env: {db_uri_normalized}"
                        )
                    except Exception as e:
                        current_app.logger.warning(
                            f"Failed to save DB URI to .env: {e}"
                        )

            except Exception as e:
                import traceback

                errors_list.append(f"Erreur configuration base de données: {str(e)}")
                current_app.logger.error(
                    f"Finalize DB config error: {traceback.format_exc()}"
                )

        # Vérifier les erreurs accumulées
        if errors_list:
            error_details = " | ".join(errors_list)
            return (
                render_full_page(
                    {
                        "error_content": (
                            f"<div class='alert alert-danger'>{error_details}</div>"
                        ),
                        "error": error_details,
                    }
                ),
                500,
            )

        # Finalisation réussie !
        # CRITICAL FIX: Mark as installed BEFORE rendering done page
        # This prevents redirect loop when user navigates after installation
        InstallService.finalize_install(app_root, app=current_app)

        # Clear wizard session data to prevent conflicts
        session.pop("wizard_started", None)
        session.pop("wizard_state", None)
        session.modified = True

        # Afficher la page done avec tous les détails
        env_summary = InstallService.render_env_summary(app_root)
        return render_template(
            "pages/install/index.html",
            state=state,
            session=session,
            step="done",
            env=env_summary,
        )

    return render_template("pages/install/step.html", step=step, state=state)


@install.route("/verify-db", methods=["GET"])
def verify_db() -> str:
    """Affiche les données de la base de données pour vérification"""
    from sqlalchemy import inspect, text

    from backend.src.extensions import db

    try:
        # Vérifier la connexion
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        # Inspector pour lister les tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Compter les enregistrements dans chaque table
        table_counts = {}
        for table in tables:
            # SEC-01: Valider que le nom de table est alphanumérique (sécurité)
            if not table.replace("_", "").isalnum():
                current_app.logger.warning(f"Skipping invalid table name: {table}")
                continue
            with db.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))  # noqa: S608
                count = result.scalar()
                table_counts[table] = count

        # Récupérer les utilisateurs
        users_data = []
        if "users" in tables:
            with db.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT id, username, email, is_admin, created_at FROM users")
                )
                for row in result:
                    users_data.append(
                        {
                            "id": row[0],
                            "username": row[1],
                            "email": row[2],
                            "is_admin": row[3],
                            "created_at": row[4],
                        }
                    )

        return render_template(
            "pages/install/verify_db.html",
            db_uri=str(db.engine.url),
            tables=tables,
            table_counts=table_counts,
            users=users_data,
            db_connected=True,
        )
    except Exception as e:
        return render_template(
            "pages/install/verify_db.html", db_connected=False, error=str(e)
        )
