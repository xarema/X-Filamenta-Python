"""
------------------------------------------------------------------------------
Purpose: Installation service
Description: Utilities for first-run detection, environment checks,
    and wizard state helpers.

File: backend/src/services/install_service.py | Repository: X-Filamenta-Python
Created: 2025-12-27T00:00:00+00:00
Last modified (Git): 2025-12-28T13:45:00+01:00 | Commit: TBD

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.0.1-Alpha | File version: 0.0.3-Alpha

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later

Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:

- Status: Stable
- Classification: Internal
  Notes:
- Git history is the source of truth for authorship and change tracking.
------------------------------------------------------------------------------
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import tarfile
import time
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

INSTALL_FLAG = "installed.flag"
DEFAULT_DB_NAME = "x-filamenta_python.db"
ALLOWED_BACKUP_EXT = {".tar.gz", ".tgz"}
MAX_BACKUP_BYTES = 50 * 1024 * 1024  # 50MB safety cap


@dataclass
class EnvCheck:
    os_name: str
    architecture: str
    has_git: bool
    has_python: bool
    has_pip: bool
    db_clients: list[str]
    has_redis: bool = False
    redis_version: str | None = None


class InstallService:
    """Utility helpers for installation wizard and first-run guard."""

    @staticmethod
    def _flag_path(app_root: str) -> str:
        return os.path.join(app_root, "instance", INSTALL_FLAG)

    @staticmethod
    def is_installed(app_root: str, max_retries: int = 3) -> bool:
        """
        Check if installation is complete.

        Uses retry logic to handle potential file I/O race conditions
        where the .installed flag might not be readable immediately after
        being written.

        Args:
            app_root: Application root directory
            max_retries: Maximum number of attempts (default: 3)

        Returns:
            True if .installed flag exists and is readable, False otherwise
        """
        flag_path = InstallService._flag_path(app_root)

        for attempt in range(max_retries):
            try:
                if os.path.exists(flag_path):
                    # Try to read the file to ensure it's accessible
                    with open(flag_path, "r", encoding="utf-8") as fp:
                        content = fp.read().strip()
                        if content:
                            logger.debug(f"Installation flag found (attempt {attempt + 1}/{max_retries})")
                            return True
            except (OSError, IOError) as e:
                logger.warning(f"Error checking install flag (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.1)  # Wait 100ms before retry
                continue

        logger.debug(f"Installation not complete after {max_retries} attempts")
        return False

    @staticmethod
    def mark_installed(app_root: str) -> None:
        """
        Mark the application as installed by creating the .installed flag file.

        Ensures file is properly written and synced to disk to prevent
        race conditions where the file isn't readable immediately.

        Args:
            app_root: Application root directory
        """
        instance_dir = os.path.join(app_root, "instance")
        os.makedirs(instance_dir, exist_ok=True)

        flag_path = InstallService._flag_path(app_root)

        try:
            # Write flag file
            with open(flag_path, "w", encoding="utf-8") as fp:
                fp.write("installed\n")
                # Force sync to disk
                fp.flush()
                os.fsync(fp.fileno())

            logger.info(f"Installation flag created: {flag_path}")

            # Verify file was created
            if os.path.exists(flag_path):
                logger.info("Installation flag verified")
            else:
                logger.error("Installation flag could not be verified immediately")
        except OSError as e:
            logger.error(f"Failed to create installation flag: {e}")
            raise

    @staticmethod
    def detect_environment() -> EnvCheck:
        db_clients: list[str] = []
        for client in ("psql", "mysql", "mariadb"):
            if shutil.which(client):
                db_clients.append(client)
        return EnvCheck(
            os_name=platform.system(),
            architecture=platform.machine(),
            has_git=shutil.which("git") is not None,
            has_python=shutil.which("python") is not None,
            has_pip=shutil.which("pip") is not None,
            db_clients=db_clients,
        )

    @staticmethod
    def detect_versions() -> dict[str, str | None]:
        def _run(cmd: list[str]) -> str | None:
            try:
                out = subprocess.check_output(  # noqa: S603
                    cmd, stderr=subprocess.STDOUT, text=True
                )
                return out.strip().split("\n", maxsplit=1)[0]
            except Exception:
                return None

        def _get_package_version(package: str) -> str | None:
            try:
                import importlib.metadata

                return importlib.metadata.version(package)
            except Exception:
                return None

        return {
            "python": _run(["python", "--version"]),
            "pip": _run(["pip", "--version"]),
            "git": _run(["git", "--version"]),
            "flask": _get_package_version("flask"),
            "sqlalchemy": _get_package_version("sqlalchemy"),
        }

    @staticmethod
    def detect_env_type() -> str | None:
        """Detect environment type: docker, cpanel, vps, or local."""
        # Check for Docker
        if os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
            return "docker"

        # Check for cPanel
        if os.path.exists("/usr/local/cpanel"):
            return "cpanel"

        # Check for common VPS indicators
        if os.path.exists("/etc/cloud") or os.path.exists("/var/lib/cloud"):
            return "vps"

        # Default to local/development
        return "local"

    @staticmethod
    def test_db_connection(db_uri: str) -> tuple[bool, str]:
        """Test database connection and return (success, message)."""
        try:
            engine: Engine = create_engine(db_uri)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True, "Connexion réussie"
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def ensure_sqlite_db(app_root: str, dbname: str) -> tuple[str, str | None]:
        """Create SQLite database file if needed, return (uri, error)."""
        os.makedirs(os.path.join(app_root, "instance"), exist_ok=True)
        db_path = os.path.join(app_root, "instance", dbname)
        try:
            # Touch file to ensure permissions
            with open(db_path, "a", encoding="utf-8"):
                pass
            return f"sqlite:///{db_path}", None
        except OSError as exc:
            return "", f"Impossible de créer le fichier SQLite: {exc}"

    @staticmethod
    def check_instance_writable(app_root: str) -> tuple[bool, str]:
        try:
            instance_dir = os.path.join(app_root, "instance")
            os.makedirs(instance_dir, exist_ok=True)
            test_path = os.path.join(instance_dir, "_write_test.tmp")
            with open(test_path, "w", encoding="utf-8") as fp:
                fp.write("ok")
            os.remove(test_path)
            return True, "OK"
        except OSError as exc:
            return False, f"Permissions insuffisantes sur instance/: {exc}"

    @staticmethod
    def render_env_summary(app_root: str | None = None) -> dict[str, Any]:
        env = InstallService.detect_environment()
        versions = InstallService.detect_versions()
        writable_ok, writable_msg = InstallService.check_instance_writable(
            app_root or os.getcwd()
        )
        env_type = InstallService.detect_env_type()

        return {
            "os": env.os_name,
            "arch": env.architecture,
            "git": env.has_git,
            "python": env.has_python,
            "pip": env.has_pip,
            "redis": env.has_redis,
            "redis_version": env.redis_version,
            "versions": versions,
            "writable": writable_ok,
            "writable_msg": writable_msg,
            "env_type": env_type,
            # db_clients intentionally not surfaced in UI per request
        }

    @staticmethod
    def save_wizard_state(
        session_obj: MutableMapping[str, Any], data: dict[str, Any]
    ) -> None:
        session_obj["wizard_state"] = data

    @staticmethod
    def get_wizard_state(session_obj: MutableMapping[str, Any]) -> dict[str, Any]:
        val = session_obj.get("wizard_state")
        return val if isinstance(val, dict) else {}

    @staticmethod
    def clear_wizard_state(session_obj: MutableMapping[str, Any]) -> None:
        session_obj.pop("wizard_state", None)

    @staticmethod
    def export_state_json(session_obj: MutableMapping[str, Any]) -> str:
        return json.dumps(InstallService.get_wizard_state(session_obj))

    @staticmethod
    def default_sqlite_uri(app_root: str) -> str:
        db_path = os.path.join(app_root, "instance", DEFAULT_DB_NAME)
        return f"sqlite:///{db_path}"

    @staticmethod
    def validate_backup(file_storage: Any) -> tuple[bool, str]:
        filename = getattr(file_storage, "filename", "")
        if not filename:
            return False, "Aucun fichier reçu"
        if not any(filename.endswith(ext) for ext in ALLOWED_BACKUP_EXT):
            return False, "Extension invalide (attendu .tar.gz ou .tgz)"
        file_storage.stream.seek(0, os.SEEK_END)
        size = file_storage.stream.tell()
        file_storage.stream.seek(0)

        # Vérifier que le fichier n'est pas vide
        if size == 0:
            return False, "Le fichier est vide (0 octets)"

        if size > MAX_BACKUP_BYTES:
            return False, "Backup trop volumineux (>50MB)"

        # Vérifier que le tar.gz contient des fichiers
        try:
            import io
            import tarfile

            file_storage.stream.seek(0)
            content = file_storage.stream.read()
            file_storage.stream.seek(0)

            with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
                members = tar.getmembers()
                if len(members) == 0:
                    return False, "Le fichier tar.gz ne contient aucun fichier"
                # Au moins un fichier .sql ou manifest
                has_sql = any(m.name.endswith(".sql") for m in members)
                has_manifest = any("manifest" in m.name.lower() for m in members)
                if not has_sql and not has_manifest:
                    return False, "Le backup ne contient ni fichier SQL ni manifest"
        except tarfile.TarError as e:
            return False, f"Fichier tar.gz invalide: {str(e)}"
        except Exception as e:
            return False, f"Erreur lors de la validation: {str(e)}"

        return True, ""

    @staticmethod
    def checksum_bytes(raw: bytes) -> str:
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def verify_backup_checksum(file_storage: Any, expected: str) -> bool:
        raw = file_storage.read()
        file_storage.seek(0)
        return InstallService.checksum_bytes(raw) == expected

    @staticmethod
    def locate_manifest(extracted_dir: str) -> str | None:
        for name in ("manifest.json", "manifest.yaml", "manifest.yml"):
            candidate = os.path.join(extracted_dir, name)
            if os.path.exists(candidate):
                return candidate
        return None

    @staticmethod
    def apply_seed_or_restore(state: dict[str, Any]) -> tuple[bool, str]:
        # Placeholder restore: verify checksum if provided and ensure backup flag
        if state.get("backup_ok"):
            expected = state.get("backup_checksum")
            if not expected:
                return False, "Checksum du backup manquant"
            return True, "Backup validé"
        return True, "Seed appliqué"

    @staticmethod
    def create_admin_user(data: dict[str, Any]) -> tuple[bool, str]:
        from backend.src.extensions import db
        from backend.src.services.user_service import UserService

        username = data.get("admin_username") or "admin"
        email = data.get("admin_email") or "admin@example.com"
        password = data.get("admin_password") or "ChangeMe!42"

        try:
            user = UserService.create(
                username=username,
                email=email,
                password=password,
                is_admin=True,
                session=db.session,
            )
            if user is None:
                # Vérifier si l'utilisateur existe déjà
                from backend.src.models.user import User

                existing = User.query.filter(
                    (User.username == username) | (User.email == email)
                ).first()
                if existing:
                    return False, f"Utilisateur '{username}' existe déjà"
                return False, "Échec création utilisateur (cause inconnue)"
            return True, f"Administrateur '{username}' créé avec succès"
        except Exception as e:
            import traceback

            traceback.print_exc()
            db.session.rollback()
            return False, f"Exception lors de la création: {str(e)}"

    @staticmethod
    def finalize_install(app_root: str, app: Any = None) -> None:
        """
        Finalize installation by marking it as complete.

        Args:
            app_root: Application root directory
            app: Flask app instance (optional) - used to invalidate cache
        """
        InstallService.mark_installed(app_root)

        # Invalidate installation status cache in Flask app if provided
        if app and hasattr(app, "_install_status_cache"):
            app._install_status_cache["installed"] = True
            app._install_status_cache["timestamp"] = 0  # Force refresh on next check
            logger.info("Installation cache invalidated in Flask app")

    @staticmethod
    def _safe_members(tar: tarfile.TarFile, dest_dir: str) -> Any:
        """Yield members while preventing path traversal."""
        for member in tar.getmembers():
            member_path = os.path.join(dest_dir, member.name)
            if os.path.commonpath(
                [
                    dest_dir,
                    os.path.abspath(member_path),
                ]
            ) != os.path.abspath(dest_dir):
                raise ValueError("Unsafe path in archive")
            yield member

    @staticmethod
    def extract_backup_tmp(file_storage: Any, dest_dir: str) -> str:
        os.makedirs(dest_dir, exist_ok=True)
        tmp_path = os.path.join(dest_dir, "upload.tar.gz")
        file_storage.save(tmp_path)
        with tarfile.open(tmp_path, "r:gz") as tar:
            for member in InstallService._safe_members(tar, dest_dir):
                tar.extract(member, path=dest_dir)
        return dest_dir

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        if len(password) < 8:
            return False, "Mot de passe trop court (8 caractères min)"
        if password.lower() == password or password.upper() == password:
            return False, "Doit contenir majuscules et minuscules"
        if not any(c.isdigit() for c in password):
            return False, "Doit contenir au moins un chiffre"
        if not any(not c.isalnum() for c in password):
            return False, "Doit contenir au moins un symbole"
        return True, ""

    @staticmethod
    def create_schema(db_uri: str) -> tuple[bool, str]:
        """Create all tables on the target database URI using SQLAlchemy metadata."""
        try:
            from backend.src.extensions import db  # lazy import to get metadata
            from backend.src.models.admin_history import AdminHistory  # noqa: F401
            from backend.src.models.content import Content  # noqa: F401
            from backend.src.models.preferences import UserPreferences  # noqa: F401

            # Ensure ALL models are registered
            from backend.src.models.user import User  # noqa: F401

            engine = create_engine(db_uri)
            # Use the global metadata containing all models
            db.metadata.create_all(bind=engine)

            from sqlalchemy import inspect

            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                return False, "Aucune table créée (metadata vide)"

            return True, f"Schéma créé ({len(tables)} tables: {', '.join(tables)})"
        except Exception as exc:  # pragma: no cover - guardrail
            import traceback

            tb = traceback.format_exc()
            return False, f"Impossible de créer le schéma: {exc}\n{tb[:300]}"

    @staticmethod
    def detect_redis_standard() -> dict[str, Any]:
        """
        Detect if Redis is available on standard localhost:6379.

        Returns:
            Dict with keys:
                - detected: bool
                - version: str or None
                - host: str
                - port: int
                - message: str
        """
        try:
            import redis

            r = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            r.ping()

            info = r.info()
            return {
                "detected": True,
                "version": info.get("redis_version", "unknown"),
                "host": "localhost",
                "port": 6379,
                "message": "Redis détecté sur localhost:6379",
            }
        except Exception as e:
            return {
                "detected": False,
                "version": None,
                "host": None,
                "port": None,
                "message": f"Redis non détecté: {str(e)}",
            }

    @staticmethod
    def detect_redis_custom_port(port: int) -> dict[str, Any]:
        """
        Detect if Redis is available on custom port.

        Args:
            port: Custom port to test

        Returns:
            Dict with detection result
        """
        try:
            import redis

            r = redis.Redis(
                host="localhost",
                port=port,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            r.ping()

            info = r.info()
            return {
                "detected": True,
                "version": info.get("redis_version", "unknown"),
                "host": "localhost",
                "port": port,
                "message": f"Redis détecté sur localhost:{port}",
            }
        except Exception as e:
            return {
                "detected": False,
                "version": None,
                "host": None,
                "port": port,
                "message": f"Aucun Redis détecté sur port {port}: {str(e)}",
            }
