from __future__ import annotations

import streamlit as st

def rerun_app() -> None:
    """Safely rerun the app across different Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
