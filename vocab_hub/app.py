from __future__ import annotations

import streamlit as st

from vocab_hub.config import APP_NAME
from vocab_hub.db.connection import init_db
from vocab_hub.services.seed import seed_data_if_empty
from vocab_hub.state import init_state, ADMIN_KEY
from vocab_hub.ui.sidebar import render_sidebar
from vocab_hub.ui.student import render_student_mode
from vocab_hub.ui.admin import render_admin_mode


def main() -> None:
    st.set_page_config(page_title=APP_NAME, layout="wide")

    init_state()
    init_db()
    seed_data_if_empty()

    mode = render_sidebar()

    st.title("📚 Faculty of Information Technology")

    if mode == "Student":
        render_student_mode()
    else:
        if not st.session_state[ADMIN_KEY]:
            st.info(
                "Please enter the admin password in the sidebar to manage courses and vocabulary."
            )
        else:
            render_admin_mode()


if __name__ == "__main__":
    main()
