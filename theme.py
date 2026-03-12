import streamlit as st

def apply_dark_theme():
    st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background-color: #0f0f0f;
    color: white;
}

/* TEXT COLOR */
html, body, [class*="css"]  {
    color: white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #000000 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* HIDE DEFAULT STREAMLIT PAGE NAV */
section[data-testid="stSidebarNav"] {
    display: none !important;
}

/* TITLES */
h1 {
    color: #ff3b3b !important;
    font-weight: 800;
}

h2, h3, h4 {
    color: #ff5a5a !important;
}

/* BUTTONS */
.stButton>button {
    background: #ff3b3b !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background: #d90429 !important;
}

/* TEXT INPUT */
.stTextInput input {
    background: #1a1a1a !important;
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 8px;
}

/* SELECTBOX INPUT */
div[data-baseweb="select"] > div {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 8px !important;
}

/* DROPDOWN MENU */
ul[role="listbox"] {
    background-color: #1a1a1a !important;
}

/* DROPDOWN ITEMS */
li[role="option"] {
    background-color: #1a1a1a !important;
    color: white !important;
}

/* DROPDOWN HOVER */
li[role="option"]:hover {
    background-color: #ff3b3b !important;
    color: white !important;
}

/* TABLES */
table {
    background: #1a1a1a !important;
    color: white !important;
}

/* METRIC BOX */
div[data-testid="stMetric"] {
    background: #1a1a1a !important;
    border-radius: 10px;
    border: 1px solid #333;
}

/* CHAT STYLE */
.chat-user {
    background: #111827;
    border-left: 4px solid #ff3b3b;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0 8px 80px;
}

.chat-bot {
    background: #1a1a1a;
    border-left: 4px solid #ff5a5a;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 80px 8px 0;
}

/* CARD BOX */
.soft-box {
    background: #1a1a1a;
    border-left: 4px solid #ff3b3b;
    padding: 18px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)
