import streamlit as st


def apply_dark_theme():

    st.markdown("""
    <style>

    /* MAIN BACKGROUND */

    .stApp {
        background: linear-gradient(135deg,#fff1f2,#ffe4e6,#fbcfe8);
        color:#3f0d12;
    }

    html, body, [class*="css"]  {
        color:#3f0d12 !important;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"]{
        background: linear-gradient(180deg,#be123c,#fb7185);
        color:white;
    }

    section[data-testid="stSidebar"] *{
        color:white !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]{
        display:none;
    }

    /* HERO CARD */

    .hero-box{
        background:linear-gradient(135deg,#f43f5e,#fb7185);
        color:white;
        padding:30px;
        border-radius:20px;
        box-shadow:0px 10px 25px rgba(0,0,0,0.15);
        margin-bottom:25px;
    }

    /* CARD MODULES */

    .card-box{
        background:#ffffffcc;
        padding:20px;
        border-radius:18px;
        box-shadow:0px 6px 18px rgba(0,0,0,0.15);
        backdrop-filter:blur(10px);
        min-height:150px;
    }

    /* INFO BOX */

    .soft-box{
        background:#fff0f3;
        padding:15px;
        border-radius:15px;
        border:1px solid #fda4af;
    }

    /* BUTTONS */

    .stButton>button{
        background:#e11d48;
        color:white;
        border-radius:10px;
        border:none;
        font-weight:600;
        padding:8px 18px;
    }

    .stButton>button:hover{
        background:#be123c;
        color:white;
    }

    /* METRICS */

    div[data-testid="stMetric"]{
        background:#fff0f3;
        border-radius:15px;
        padding:10px;
        border:1px solid #fecdd3;
    }

    /* TABLE */

    table{
        color:#3f0d12 !important;
    }

    th{
        background:#fda4af !important;
        color:#3f0d12 !important;
    }

    /* INPUT BOX */

    .stTextInput input{
        background:#fff;
        border-radius:10px;
        border:1px solid #fda4af;
    }

    /* CHAT */

    .stChatMessage{
        background:#fff0f3;
        border-radius:12px;
    }

    </style>
    """, unsafe_allow_html=True)
