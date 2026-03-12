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

        h2, h3, h4, h5, h6 {
            color: #ff5a5a !important;
        }

        p, span, label, div, li {
            color: #f3f4f6 !important;
        }

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            background: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
            border-radius: 10px !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #9ca3af !important;
        }

        /* Dropdown popup */
        ul[role="listbox"] {
            background-color: #1a1a1a !important;
            border: 1px solid #444 !important;
        }

        li[role="option"] {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }

        li[role="option"]:hover {
            background-color: #ff3b3b !important;
            color: #ffffff !important;
        }

        /* Buttons */
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

        /* Boxes */
        .hero-box, .card-box, .soft-box {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-left: 4px solid #ff3b3b !important;
            border-radius: 14px !important;
            padding: 16px !important;
        }

        /* Dataframe / table */
        div[data-testid="stDataFrame"] * {
            color: #ffffff !important;
        }

        table, th, td {
            color: #ffffff !important;
        }

        /* Expander */
        details {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
        }

        summary {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* Metrics */
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
        </style>
        """,
        unsafe_allow_html=True,
    )
