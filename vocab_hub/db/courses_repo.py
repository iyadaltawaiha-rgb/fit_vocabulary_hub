from __future__ import annotations

import sqlite3
from typing import Dict, List, Optional

from .connection import get_connection

def add_course(name: str, description: str = "") -> Optional[int]:
    name = (name or "").strip()
    description = (description or "").strip()
    if not name:
        return None
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO courses (name, description) VALUES (?, ?)",
                (name, description),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None

def update_course(course_id: int, name: str, description: str = "") -> bool:
    name = (name or "").strip()
    description = (description or "").strip()
    if not name:
        return False
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE courses SET name = ?, description = ? WHERE id = ?",
                (name, description, course_id),
            )
            return cur.rowcount > 0
    except sqlite3.IntegrityError:
        return False

def delete_course(course_id: int) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM courses WHERE id = ?", (course_id,))

def get_courses() -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses ORDER BY name")
        return cur.fetchall()

def get_course_by_id(course_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        return cur.fetchone()

def get_courses_dict_id_to_name() -> Dict[int, str]:
    return {row["id"]: row["name"] for row in get_courses()}

def get_courses_dict_name_to_id() -> Dict[str, int]:
    return {row["name"]: row["id"] for row in get_courses()}
