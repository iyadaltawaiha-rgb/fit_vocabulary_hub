from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from ..config import get_db_path

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Create a SQLite connection with foreign keys enabled.
    A new connection is created per call (simple and safe for Streamlit).
    """
    path = str(db_path or get_db_path())
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db() -> None:
    """Create tables if they do not exist."""
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vocab_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                term_en TEXT NOT NULL,
                term_ar TEXT,
                definition_en TEXT,
                definition_ar TEXT,
                example_en TEXT,
                difficulty INTEGER DEFAULT 1,
                category TEXT,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
            """
        )
