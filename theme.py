import streamlit as st


def apply_dark_theme():

    st.markdown("""
    <style>

    /* APP BACKGROUND */
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }

    html, body {
        color: #ffffff;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* TITLES */
    h1 {
        color: #ff3b3b !important;
        font-weight: 800 !important;
    }

    h2, h3, h4, h5, h6 {
        color: #ff5a5a !important;
    }

    p, span, label, div {
        color: #f3f4f6 !important;
    }

    /* INPUT BOXES */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stDateInput input {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 10px !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: #ff3b3b !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background: #d90429 !important;
        color: #ffffff !important;
    }

    /* CARDS / INFO BOX */
    .hero-box, .card-box, .soft-box {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-left: 4px solid #ff3b3b !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }

    /* DATAFRAMES */
    div[data-testid="stDataFrame"] * {
        color: #ffffff !important;
    }

    table, th, td {
        color: #ffffff !important;
    }

    /* EXPANDER */
    details {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }

    summary {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* METRICS */
    div[data-testid="stMetric"] {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* FILE UPLOADER FIX */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a !important;
        border: 1px solid #444 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }

    [data-testid="stFileUploader"] * {
        color: #ffffff !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] button {
        background-color: #ff3b3b !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* SELECT BOX DROPDOWN FIX */
    div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
        color: white !important;
    }

    ul[role="listbox"] {
        background-color: #1a1a1a !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)
