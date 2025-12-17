from __future__ import annotations

import streamlit as st

from ..config import APP_NAME, get_admin_password
from ..state import ADMIN_KEY

def render_sidebar() -> str:
    """
    Render sidebar and return selected mode: "Student" or "Admin".
    Handles admin login/logout.
    """
    st.sidebar.title("Isra University-Faculty of Information Technology")
    mode = st.sidebar.radio("Mode", ["Student", "Admin"])

    if mode == "Admin":
        if not st.session_state[ADMIN_KEY]:
            st.sidebar.subheader("Admin login")
            pwd = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                if pwd == get_admin_password():
                    st.session_state[ADMIN_KEY] = True
                    st.sidebar.success("Logged in as admin.")
                else:
                    st.sidebar.error("Incorrect password.")
        else:
            st.sidebar.success("Admin mode")
            if st.sidebar.button("Logout"):
                st.session_state[ADMIN_KEY] = False

    return mode
