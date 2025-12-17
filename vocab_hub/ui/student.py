from __future__ import annotations

import random
import sqlite3
from typing import List

import streamlit as st

from ..db.courses_repo import get_courses
from ..db.vocab_repo import get_vocab_for_course, filter_vocab
from ..services.quiz import build_quiz_questions
from ..state import (
    COURSE_KEY,
    SEARCH_QUERY_KEY,
    FLASH_INDEX_KEY,
    FLASH_SHOW_DEF_KEY,
    QUIZ_INDEX_KEY,
    QUIZ_SCORE_KEY,
    QUIZ_FINISHED_KEY,
    QUIZ_ANSWER_CHECKED_KEY,
    QUIZ_LAST_CORRECT_KEY,
    QUIZ_QUESTIONS_KEY,
    reset_learning_state,
)

def _render_flashcards(vocab: List[sqlite3.Row]) -> None:
    st.markdown("#### 🔁 Flashcards")

    if st.session_state[FLASH_INDEX_KEY] >= len(vocab):
        st.session_state[FLASH_INDEX_KEY] = 0

    idx = st.session_state[FLASH_INDEX_KEY]
    word = vocab[idx]

    term_en = word["term_en"] or ""
    term_ar = word["term_ar"] or ""
    category = word["category"] or ""
    difficulty = int(word["difficulty"] or 1)
    difficulty = max(1, min(3, difficulty))
    stars = "⭐" * difficulty

    cols = st.columns([2, 1])

    with cols[0]:
        st.markdown("##### Term (EN / AR)")

        card_html = f"""
        <div style="
            padding: 24px;
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            background:
                radial-gradient(circle at top left, rgba(59,130,246,0.20), transparent 55%),
                radial-gradient(circle at bottom right, rgba(236,72,153,0.20), transparent 55%),
                #0f172a;
            color: #e5e7eb;
            box-shadow: 0 18px 35px rgba(15,23,42,0.7);
        ">
          <div style="font-size: 0.75rem; text-transform: uppercase;
                      letter-spacing: .12em; opacity: .75; margin-bottom: 2px;">
            English term
          </div>
          <div style="font-size: 2.1rem; font-weight: 700; margin: 0 0 10px 0;">
            {term_en}
          </div>

          <div style="font-size: 0.75rem; text-transform: uppercase;
                      letter-spacing: .12em; opacity: .75; margin-bottom: 2px;">
            المصطلح بالعربية
          </div>
          <div style="font-size: 1.7rem; font-weight: 600; margin: 0 0 8px 0;">
            {term_ar}
          </div>

          <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top: 8px;">
            <span style="
                font-size: 0.75rem;
                padding: 4px 10px;
                border-radius: 999px;
                border: 1px solid rgba(148,163,184,0.7);
                background: rgba(15,23,42,0.8);
            ">
              Difficulty: {stars}
            </span>
            {f'<span style="font-size: 0.75rem; padding: 4px 10px; border-radius: 999px; background: rgba(59,130,246,0.25); border: 1px solid rgba(59,130,246,0.5);">{category}</span>' if category else ""}
          </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        st.write("")

        if not st.session_state[FLASH_SHOW_DEF_KEY]:
            if st.button("Show definition", key="btn_show_def"):
                st.session_state[FLASH_SHOW_DEF_KEY] = True
        else:
            st.markdown("**Definition (EN):**")
            st.write(word["definition_en"])

            st.markdown("**التعريف (عربي):**")
            st.write(word["definition_ar"])

            if word["example_en"]:
                st.markdown("**Example:**")
                st.write(word["example_en"])

    with cols[1]:
        st.markdown("##### Progress")
        st.progress((idx + 1) / len(vocab))
        st.write(f"Word {idx + 1} of {len(vocab)}")

        st.markdown("##### Your response")
        col_a, col_b = st.columns(2)

        def _next_word():
            if st.session_state[FLASH_INDEX_KEY] < len(vocab) - 1:
                st.session_state[FLASH_INDEX_KEY] += 1
            else:
                st.session_state[FLASH_INDEX_KEY] = 0
            st.session_state[FLASH_SHOW_DEF_KEY] = False

        with col_a:
            if st.button("👍 I know this", key="btn_know"):
                _next_word()

        with col_b:
            if st.button("👎 I need practice", key="btn_practice"):
                _next_word()

        if st.button("🔀 Random word", key="btn_random"):
            st.session_state[FLASH_INDEX_KEY] = random.randint(0, len(vocab) - 1)
            st.session_state[FLASH_SHOW_DEF_KEY] = False


def _render_quiz(vocab: List[sqlite3.Row]) -> None:
    st.markdown("#### 📝 Quiz")

    if not vocab:
        st.info("No vocabulary available for quiz in this course.")
        return

    # Build questions if missing or mismatched
    questions = st.session_state.get(QUIZ_QUESTIONS_KEY)
    if questions is None or len(questions) != len(vocab):
        st.session_state[QUIZ_QUESTIONS_KEY] = build_quiz_questions(vocab)
        st.session_state[QUIZ_INDEX_KEY] = 0
        st.session_state[QUIZ_SCORE_KEY] = 0
        st.session_state[QUIZ_FINISHED_KEY] = False
        st.session_state[QUIZ_ANSWER_CHECKED_KEY] = False
        st.session_state[QUIZ_LAST_CORRECT_KEY] = None
        questions = st.session_state[QUIZ_QUESTIONS_KEY]

    total_questions = len(questions)

    if st.session_state[QUIZ_FINISHED_KEY]:
        score = st.session_state[QUIZ_SCORE_KEY]
        percent = round(100 * score / total_questions) if total_questions else 0
        st.success(
            f"Quiz finished! Your score: {score} / {total_questions} ({percent}%)."
        )
        if st.button("Restart quiz"):
            reset_learning_state()
        return

    qpos = st.session_state[QUIZ_INDEX_KEY]
    if qpos >= total_questions:
        st.session_state[QUIZ_FINISHED_KEY] = True
        return

    qdata = questions[qpos]
    word = vocab[qdata["word_idx"]]
    options = qdata["options"]
    correct_term = qdata["correct"]

    st.write("")
    st.progress(qpos / total_questions)
    st.caption(f"Question {qpos + 1} of {total_questions}")

    question_html = f"""
    <div style="
        padding: 24px;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.4);
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.20), transparent 55%),
            radial-gradient(circle at bottom right, rgba(236,72,153,0.20), transparent 55%),
            #020617;
        color: #e5e7eb;
        box-shadow: 0 18px 40px rgba(15,23,42,0.75);
        margin-bottom: 16px;
    ">
      <div style="font-size: 0.8rem; text-transform: uppercase;
                  letter-spacing: .14em; opacity: .75; margin-bottom: 4px;">
        Multiple-choice question
      </div>
      <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 12px;">
        What is the correct English term for this Arabic word?
      </div>
      <div style="font-size: 2.1rem; font-weight: 700;
                  margin-bottom: 4px; direction: rtl; text-align: right;">
        {word['term_ar']}
      </div>
    </div>
    """
    st.markdown(question_html, unsafe_allow_html=True)

    selected = st.radio(
        "Choose one answer:",
        options,
        key=f"quiz_option_{qpos}",
    )

    col1, col2 = st.columns(2)
    with col1:
        check_clicked = st.button("Check answer ✅", key=f"btn_check_{qpos}")
    with col2:
        next_clicked = False
        if st.session_state[QUIZ_ANSWER_CHECKED_KEY]:
            label = "Next word ➜" if qpos < total_questions - 1 else "Finish quiz ✅"
            next_clicked = st.button(label, key=f"btn_next_{qpos}")

    if check_clicked and not st.session_state[QUIZ_ANSWER_CHECKED_KEY]:
        is_correct = selected == correct_term
        st.session_state[QUIZ_ANSWER_CHECKED_KEY] = True
        st.session_state[QUIZ_LAST_CORRECT_KEY] = is_correct
        if is_correct:
            st.session_state[QUIZ_SCORE_KEY] += 1

    if st.session_state[QUIZ_ANSWER_CHECKED_KEY]:
        if st.session_state[QUIZ_LAST_CORRECT_KEY]:
            st.success("✅ Correct! Well done.")
        else:
            st.error(f"❌ Incorrect. The correct answer is: **{correct_term}**.")

    if st.session_state[QUIZ_ANSWER_CHECKED_KEY] and next_clicked:
        if qpos < total_questions - 1:
            st.session_state[QUIZ_INDEX_KEY] += 1
            st.session_state[QUIZ_ANSWER_CHECKED_KEY] = False
            st.session_state[QUIZ_LAST_CORRECT_KEY] = None
        else:
            st.session_state[QUIZ_FINISHED_KEY] = True
            st.session_state[QUIZ_ANSWER_CHECKED_KEY] = False
            st.session_state[QUIZ_LAST_CORRECT_KEY] = None


def _render_word_list(vocab: List[sqlite3.Row]) -> None:
    st.markdown("#### 📖 Word list")
    for w in vocab:
        with st.expander(f"{w['term_en']}  |  {w['term_ar']}"):
            st.write("**Definition (EN):**", w["definition_en"])
            st.write("**التعريف (عربي):**", w["definition_ar"])
            if w["example_en"]:
                st.write("**Example:**", w["example_en"])
            if w["category"]:
                st.write("**Category:**", w["category"])
            if w["difficulty"]:
                stars = "⭐" * int(w["difficulty"])
                st.write("**Difficulty:**", stars)


def render_student_mode() -> None:
    st.subheader("Student mode")

    courses = get_courses()
    if not courses:
        st.info("No courses available yet. Please ask an admin to add some first.")
        return

    course_names = [c["name"] for c in courses]
    selected_name = st.sidebar.selectbox("Select a course", course_names)
    selected_course = next(c for c in courses if c["name"] == selected_name)
    selected_course_id = selected_course["id"]

    # reset when switching course
    if st.session_state[COURSE_KEY] != selected_course_id:
        st.session_state[COURSE_KEY] = selected_course_id
        reset_learning_state()

    search_input = st.sidebar.text_input(
        "Search vocabulary (EN/AR/definition)",
        value=st.session_state[SEARCH_QUERY_KEY],
    )
    if search_input != st.session_state[SEARCH_QUERY_KEY]:
        st.session_state[SEARCH_QUERY_KEY] = search_input
        reset_learning_state()

    view_mode = st.sidebar.radio("Learning mode", ["Flashcards", "Quiz", "Word List"])

    all_vocab = get_vocab_for_course(selected_course_id)
    vocab = filter_vocab(all_vocab, st.session_state[SEARCH_QUERY_KEY])

    st.markdown(f"### Course: {selected_course['name']}")
    if selected_course["description"]:
        st.caption(selected_course["description"])

    if not all_vocab:
        st.warning("No vocabulary added yet for this course.")
        return
    if not vocab:
        st.warning("No vocabulary matches your search in this course.")
        return

    if view_mode == "Flashcards":
        _render_flashcards(vocab)
    elif view_mode == "Quiz":
        _render_quiz(vocab)
    else:
        _render_word_list(vocab)
