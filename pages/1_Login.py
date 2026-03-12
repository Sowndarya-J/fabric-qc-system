import streamlit as st
from theme import apply_dark_theme
from utils import load_users

apply_dark_theme()

st.title("🔐 Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

USERS = load_users()

u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if u in USERS and USERS[u]["password"] == p:
        st.session_state.logged_in = True
        st.session_state.user = u
        st.session_state.role = USERS[u]["role"]
        st.success(f"Logged in as {u} ({st.session_state.role})")
        st.rerun()
    else:
        st.error("Invalid username/password")

if st.session_state.logged_in:
    st.info(f"✅ User: {st.session_state.user} | Role: {st.session_state.role}")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()
