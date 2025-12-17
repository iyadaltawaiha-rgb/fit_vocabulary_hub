from __future__ import annotations

import sqlite3
from typing import List

from .connection import get_connection

def _normalize_difficulty(value) -> int:
    """Ensure difficulty is always between 1 and 3."""
    try:
        v = int(value)
    except Exception:
        v = 1
    return max(1, min(3, v))

def add_vocab_item(
    course_id: int,
    term_en: str,
    term_ar: str = "",
    definition_en: str = "",
    definition_ar: str = "",
    example_en: str = "",
    difficulty: int = 1,
    category: str = "",
) -> None:
    term_en = (term_en or "").strip()
    term_ar = (term_ar or "").strip()
    definition_en = (definition_en or "").strip()
    definition_ar = (definition_ar or "").strip()
    example_en = (example_en or "").strip()
    category = (category or "").strip()
    difficulty = _normalize_difficulty(difficulty)

    if not term_en or not definition_en or not definition_ar:
        return

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO vocab_items (
                course_id, term_en, term_ar, definition_en, definition_ar,
                example_en, difficulty, category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                course_id,
                term_en,
                term_ar,
                definition_en,
                definition_ar,
                example_en,
                difficulty,
                category,
            ),
        )

def update_vocab_item(
    item_id: int,
    term_en: str,
    term_ar: str = "",
    definition_en: str = "",
    definition_ar: str = "",
    example_en: str = "",
    difficulty: int = 1,
    category: str = "",
) -> bool:
    term_en = (term_en or "").strip()
    term_ar = (term_ar or "").strip()
    definition_en = (definition_en or "").strip()
    definition_ar = (definition_ar or "").strip()
    example_en = (example_en or "").strip()
    category = (category or "").strip()
    difficulty = _normalize_difficulty(difficulty)

    if not term_en or not definition_en or not definition_ar:
        return False

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE vocab_items
            SET term_en = ?, term_ar = ?, definition_en = ?, definition_ar = ?,
                example_en = ?, difficulty = ?, category = ?
            WHERE id = ?
            """,
            (
                term_en,
                term_ar,
                definition_en,
                definition_ar,
                example_en,
                difficulty,
                category,
                item_id,
            ),
        )
        return cur.rowcount > 0

def delete_vocab_item(item_id: int) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM vocab_items WHERE id = ?", (item_id,))

def get_vocab_for_course(course_id: int) -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM vocab_items
            WHERE course_id = ?
            ORDER BY term_en
            """,
            (course_id,),
        )
        return cur.fetchall()

def filter_vocab(vocab_rows: List[sqlite3.Row], query: str) -> List[sqlite3.Row]:
    query = (query or "").strip().lower()
    if not query:
        return list(vocab_rows)

    filtered = []
    for w in vocab_rows:
        if (
            query in str(w["term_en"]).lower()
            or query in str(w["term_ar"] or "").lower()
            or query in str(w["definition_en"] or "").lower()
            or query in str(w["definition_ar"] or "").lower()
        ):
            filtered.append(w)
    return filtered
