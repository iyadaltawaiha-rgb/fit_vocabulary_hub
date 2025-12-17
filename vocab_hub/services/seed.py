from __future__ import annotations

from ..db.courses_repo import add_course, get_courses
from ..db.vocab_repo import add_vocab_item

def seed_data_if_empty() -> None:
    """Insert demo courses and words when DB is empty."""
    if get_courses():
        return

    ml_id = add_course(
        "Machine Learning Fundamentals",
        "Basic ML concepts: underfitting, overfitting, models, evaluation.",
    )
    ai_id = add_course(
        "Artificial Intelligence",
        "Intro to intelligent agents, search, and basic AI concepts.",
    )
    dm_id = add_course(
        "Data Mining",
        "Tasks like classification, clustering, association rules.",
    )

    if ml_id:
        add_vocab_item(
            ml_id,
            "Overfitting",
            "زيادة التخصيص",
            "When a model learns noise in the training data and performs poorly on new data.",
            "حالة يتعلم فيها النموذج الضجيج في بيانات التدريب فيضعف أداؤه على البيانات الجديدة.",
            "Our model had 99% accuracy on training data but failed on test data due to overfitting.",
            2,
            "Concept",
        )

    if ai_id:
        add_vocab_item(
            ai_id,
            "Agent",
            "الوكيل الذكي",
            "An entity that perceives its environment and acts upon it.",
            "كيان يَستشعر بيئته ويتخذ إجراءات تؤثر فيها.",
            "A robot vacuum cleaner is an intelligent agent.",
            1,
            "Basic concept",
        )

    if dm_id:
        add_vocab_item(
            dm_id,
            "Classification",
            "التصنيف",
            "The task of assigning items to one of several predefined categories.",
            "مهمة إسناد العناصر إلى واحدة من عدة فئات محددة مسبقًا.",
            "Email classification separates spam emails from non-spam.",
            1,
            "Task",
        )
