import streamlit as st


def apply_dark_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }

        html, body, [class*="css"] {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        h1 {
            color: #ff3b3b !important;
            font-weight: 800 !important;
        }

        h2, h3, h4, h5, h6 {
            color: #ff5a5a !important;
        }

        p, span, label, div, li {
            color: #f3f4f6 !important;
        }

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

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #9ca3af !important;
        }

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

        .soft-box {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-left: 4px solid #ff3b3b !important;
            border-radius: 14px !important;
            padding: 16px !important;
        }

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

        div[data-testid="stDataFrame"] * {
            color: #ffffff !important;
        }

        table, th, td {
            color: #ffffff !important;
        }

        details {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
        }

        summary {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        ul[role="listbox"] {
            background-color: #1a1a1a !important;
        }

        li[role="option"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        li[role="option"]:hover {
            background-color: #ff3b3b !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
