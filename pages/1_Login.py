import streamlit as st

from theme import apply_dark_theme
from utils import load_users

apply_dark_theme()

st.title("Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

users = load_users()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if username in users and users[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user = username
        st.session_state.role = users[username]["role"]
        st.success("Login successful")
        st.rerun()
    else:
        st.error("Invalid username or password")
