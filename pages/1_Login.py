import streamlit as st
from utils import load_users, t

st.markdown("""
<style>
.login-shell {
    max-width: 520px;
    margin: 0 auto;
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0,0,0,0.30);
}
.login-title {
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 8px;
}
.login-sub {
    color: #cbd5e1;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="login-shell">
    <div class="login-title">🔐 Login</div>
    <div class="login-sub">Enter your credentials to access the Fabric QC System.</div>
</div>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

users = load_users()

u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if u in users and users[u]["password"] == p:
        st.session_state.logged_in = True
        st.session_state.user = u
        st.session_state.role = users[u]["role"]
        st.success(f"Logged in as {u} ({st.session_state.role})")
        st.rerun()
    else:
        st.error("Invalid username/password")
