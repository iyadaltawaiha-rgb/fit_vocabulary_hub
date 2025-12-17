from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from ..db.courses_repo import get_courses_dict_name_to_id
from ..db.vocab_repo import add_vocab_item, _normalize_difficulty

@dataclass
class ImportStats:
    imported_count: int = 0
    skipped_missing_course: int = 0
    skipped_missing_fields: int = 0

def import_vocab_from_excel(df: pd.DataFrame) -> ImportStats:
    """
    Import vocabulary from a dataframe representing the 'vocabulary' sheet.
    Required columns: course_name, term_en, definition_en, definition_ar.
    Optional: term_ar, example_en, difficulty, category.
    """
    name_to_id = get_courses_dict_name_to_id()
    stats = ImportStats()

    for _, row in df.iterrows():
        course_name = str(row.get("course_name", "")).strip()
        if not course_name:
            continue

        course_id = name_to_id.get(course_name)
        if not course_id:
            stats.skipped_missing_course += 1
            continue

        term_en = str(row.get("term_en", "")).strip()
        definition_en = str(row.get("definition_en", "")).strip()
        definition_ar = str(row.get("definition_ar", "")).strip()

        if not term_en or not definition_en or not definition_ar:
            stats.skipped_missing_fields += 1
            continue

        term_ar = str(row.get("term_ar", "") or "").strip()
        example_en = str(row.get("example_en", "") or "").strip()
        difficulty_raw = row.get("difficulty", 1)
        category = str(row.get("category", "") or "").strip()

        add_vocab_item(
            course_id=course_id,
            term_en=term_en,
            term_ar=term_ar,
            definition_en=definition_en,
            definition_ar=definition_ar,
            example_en=example_en,
            difficulty=_normalize_difficulty(difficulty_raw),
            category=category,
        )
        stats.imported_count += 1

    return stats
