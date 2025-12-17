from __future__ import annotations

import streamlit as st

# Keys used across the app (kept in one place)
ADMIN_KEY = "is_admin"
COURSE_KEY = "current_course_id"

FLASH_INDEX_KEY = "flash_index"
FLASH_SHOW_DEF_KEY = "show_def"

QUIZ_INDEX_KEY = "quiz_index"
QUIZ_SCORE_KEY = "quiz_score"
QUIZ_FINISHED_KEY = "quiz_finished"
QUIZ_ANSWER_CHECKED_KEY = "quiz_answer_checked"
QUIZ_LAST_CORRECT_KEY = "quiz_last_correct"
QUIZ_ORDER_KEY = "quiz_order"
QUIZ_QUESTIONS_KEY = "quiz_questions"

SEARCH_QUERY_KEY = "search_query"

def init_state() -> None:
    defaults = {
        ADMIN_KEY: False,
        COURSE_KEY: None,
        FLASH_INDEX_KEY: 0,
        FLASH_SHOW_DEF_KEY: False,
        QUIZ_INDEX_KEY: 0,
        QUIZ_SCORE_KEY: 0,
        QUIZ_FINISHED_KEY: False,
        QUIZ_ANSWER_CHECKED_KEY: False,
        QUIZ_LAST_CORRECT_KEY: None,
        QUIZ_ORDER_KEY: None,
        QUIZ_QUESTIONS_KEY: None,
        SEARCH_QUERY_KEY: "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_learning_state() -> None:
    """Reset all student learning state (flashcards & quiz)."""
    st.session_state[FLASH_INDEX_KEY] = 0
    st.session_state[FLASH_SHOW_DEF_KEY] = False

    st.session_state[QUIZ_INDEX_KEY] = 0
    st.session_state[QUIZ_SCORE_KEY] = 0
    st.session_state[QUIZ_FINISHED_KEY] = False
    st.session_state[QUIZ_ANSWER_CHECKED_KEY] = False
    st.session_state[QUIZ_LAST_CORRECT_KEY] = None
    st.session_state[QUIZ_ORDER_KEY] = None
    st.session_state[QUIZ_QUESTIONS_KEY] = None
