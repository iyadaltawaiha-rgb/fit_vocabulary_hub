from __future__ import annotations

import os
from pathlib import Path

# ---------------------------
# App-level configuration
# ---------------------------

APP_NAME = "FIT Vocabulary Hub"

def get_app_dir() -> Path:
    """
    Directory where we store user-writable data (SQLite DB, logs, etc.).
    Using a folder in the user's home directory keeps the app safe when
    packaged as an .exe.
    """
    app_dir = Path.home() / ".fit_vocabulary_hub"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def get_db_path() -> Path:
    return get_app_dir() / "vocab.db"

def get_admin_password(default: str = "admin123") -> str:
    """
    Reads admin password from:
    1) Environment variable FIT_VOCAB_ADMIN_PASSWORD
    2) Falls back to the provided default.
    """
    return os.getenv("FIT_VOCAB_ADMIN_PASSWORD", default)
