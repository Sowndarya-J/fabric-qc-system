import streamlit as st


def apply_dark_theme():
    st.markdown(
        """
        <style>

        /* App background */
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }

        html, body {
            color: #ffffff;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Titles */
        h1 {
            color: #ff3b3b !important;
            font-weight: 800 !important;
        }

        h2, h3, h4 {
            color: #ff5a5a !important;
        }

        p, span, label, div {
            color: #f3f4f6 !important;
        }

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input {
            background: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
            border-radius: 10px !important;
        }

        /* Dropdown SELECT box */
        div[data-baseweb="select"] > div {
            background-color: #1a1a1a !important;
            color: white !important;
            border: 1px solid #444 !important;
        }

        /* Dropdown menu items */
        ul[role="listbox"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        li[role="option"] {
            background-color: #1a1a1a !important;
            color: white !important;
        }

        li[role="option"]:hover {
            background-color: #333333 !important;
        }

        /* Buttons */
        .stButton > button {
            background: #ff3b3b !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }

        .stButton > button:hover {
            background: #d90429 !important;
        }

        /* Download button FIX */
        button[kind="secondary"] {
            background-color: #ff3b3b !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }

        button[kind="secondary"]:hover {
            background-color: #d90429 !important;
        }

        /* Dataframe */
        div[data-testid="stDataFrame"] * {
            color: white !important;
        }

        table, th, td {
            color: white !important;
        }

        /* Expander */
        details {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
        }

        summary {
            color: white !important;
            font-weight: 700 !important;
        }

        /* Metric boxes */
        div[data-testid="stMetric"] {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricValue"] {
            color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
