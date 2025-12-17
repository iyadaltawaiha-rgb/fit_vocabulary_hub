from __future__ import annotations

import pandas as pd
import streamlit as st

from ..db.courses_repo import add_course, update_course, delete_course, get_courses
from ..db.vocab_repo import add_vocab_item, update_vocab_item, delete_vocab_item, get_vocab_for_course
from ..services.importer import import_vocab_from_excel
from ..utils import rerun_app

def _courses_tab() -> None:
    st.markdown("### Manage courses")

    st.markdown("#### Add a new course")
    with st.form("add_course_form"):
        c_name = st.text_input("Course name *")
        c_desc = st.text_area("Course description (optional)")
        submitted = st.form_submit_button("Add course")
        if submitted:
            if not c_name.strip():
                st.error("Course name is required.")
            else:
                new_id = add_course(c_name, c_desc)
                if new_id is None:
                    st.warning("Course name is required and must be unique.")
                else:
                    st.success(f"Course '{c_name}' added successfully.")
                    rerun_app()

    st.markdown("---")
    st.markdown("#### Existing courses (click to edit)")
    courses = get_courses()
    if not courses:
        st.info("No courses found.")
        return

    for c in courses:
        with st.expander(f"{c['name']} (ID {c['id']})"):
            with st.form(f"edit_course_{c['id']}"):
                new_name = st.text_input("Course name *", value=c["name"])
                new_desc = st.text_area(
                    "Course description (optional)",
                    value=c["description"] or "",
                )
                col1, col2 = st.columns(2)
                with col1:
                    save = st.form_submit_button("Save changes")
                with col2:
                    delete = st.form_submit_button("Delete course")

                if save:
                    ok = update_course(c["id"], new_name, new_desc)
                    if ok:
                        st.success("Course updated.")
                        rerun_app()
                    else:
                        st.error("Update failed. Name is required and must be unique.")
                elif delete:
                    delete_course(c["id"])
                    st.warning(f"Course '{c['name']}' and its vocabulary were deleted.")
                    rerun_app()

def _vocab_tab() -> None:
    st.markdown("### Manage vocabulary")

    courses = get_courses()
    if not courses:
        st.info("Please add at least one course first.")
        return

    course_names = [c["name"] for c in courses]
    selected_name = st.selectbox("Select course", course_names)
    selected_course = next(c for c in courses if c["name"] == selected_name)
    selected_course_id = selected_course["id"]

    st.markdown(f"#### Add vocabulary to: {selected_course['name']}")
    with st.form("add_vocab_form"):
        term_en = st.text_input("Term (English) *")
        term_ar = st.text_input("Term (Arabic)")
        definition_en = st.text_area("Definition (English) *")
        definition_ar = st.text_area("التعريف (عربي) *")
        example_en = st.text_area("Example sentence (English)")
        difficulty = st.slider("Difficulty", 1, 3, 1)
        category = st.text_input("Category (e.g., Metric, Concept, Algorithm)")

        submitted_v = st.form_submit_button("Add vocabulary item")
        if submitted_v:
            if not term_en.strip() or not definition_en.strip() or not definition_ar.strip():
                st.error("English term and both definitions are required.")
            else:
                add_vocab_item(
                    selected_course_id,
                    term_en,
                    term_ar,
                    definition_en,
                    definition_ar,
                    example_en,
                    difficulty,
                    category,
                )
                st.success(f"Vocabulary '{term_en}' added to {selected_course['name']}.")
                rerun_app()

    st.markdown("---")
    st.markdown(f"#### Existing vocabulary for {selected_course['name']} (click to edit)")
    vocab = get_vocab_for_course(selected_course_id)
    if not vocab:
        st.info("No vocabulary yet for this course.")
        return

    for w in vocab:
        with st.expander(f"{w['term_en']} | {w['term_ar']}"):
            with st.form(f"edit_vocab_{w['id']}"):
                new_term_en = st.text_input("Term (English) *", value=w["term_en"])
                new_term_ar = st.text_input("Term (Arabic)", value=w["term_ar"] or "")
                new_def_en = st.text_area("Definition (English) *", value=w["definition_en"] or "")
                new_def_ar = st.text_area("التعريف (عربي) *", value=w["definition_ar"] or "")
                new_example = st.text_area("Example sentence (English)", value=w["example_en"] or "")
                new_difficulty = st.slider(
                    "Difficulty", 1, 3, int(w["difficulty"] or 1),
                    key=f"diff_{w['id']}",
                )
                new_category = st.text_input("Category", value=w["category"] or "")

                col1, col2 = st.columns(2)
                with col1:
                    save_v = st.form_submit_button("Save changes")
                with col2:
                    delete_v = st.form_submit_button("Delete")

                if save_v:
                    if not new_term_en.strip() or not new_def_en.strip() or not new_def_ar.strip():
                        st.error("English term and both definitions are required.")
                    else:
                        ok = update_vocab_item(
                            w["id"],
                            new_term_en,
                            new_term_ar,
                            new_def_en,
                            new_def_ar,
                            new_example,
                            new_difficulty,
                            new_category,
                        )
                        if ok:
                            st.success("Vocabulary updated.")
                            rerun_app()
                        else:
                            st.error("Update failed. Check required fields.")
                elif delete_v:
                    delete_vocab_item(w["id"])
                    st.warning(f"Deleted '{w['term_en']}'.")
                    rerun_app()

def _bulk_tab() -> None:
    st.markdown("### 📥 Bulk import vocabulary from Excel files")
    st.info(
        "Use an Excel file with a sheet named **'vocabulary'** and at least "
        "these columns: course_name, term_en, definition_en, definition_ar.\n\n"
        "Optional columns: term_ar, example_en, difficulty (1–3), category."
    )

    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    if uploaded_file is None:
        return

    try:
        df = pd.read_excel(uploaded_file, sheet_name="vocabulary")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return

    stats = import_vocab_from_excel(df)
    st.success(f"Imported {stats.imported_count} vocabulary items successfully.")
    if stats.skipped_missing_course:
        st.warning(
            f"Skipped {stats.skipped_missing_course} rows (course_name not found in DB)."
        )
    if stats.skipped_missing_fields:
        st.warning(
            f"Skipped {stats.skipped_missing_fields} rows (missing required fields)."
        )

def render_admin_mode() -> None:
    st.subheader("Admin mode")

    tab_courses, tab_vocab, tab_files = st.tabs(
        ["Courses", "Vocabulary", "Bulk Import (Excel files)"]
    )

    with tab_courses:
        _courses_tab()
    with tab_vocab:
        _vocab_tab()
    with tab_files:
        _bulk_tab()
