import streamlit as st


def apply_dark_theme():

    st.markdown(
        """
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

        h2, h3, h4 {
            color: #ff5a5a !important;
        }

        p, span, label, div {
            color: #f3f4f6 !important;
        }

        /* INPUT BOXES */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input {
            background: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
            border-radius: 10px !important;
        }

        /* DROPDOWN SELECT BOX */
        div[data-baseweb="select"] > div {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
        }

        /* DROPDOWN MENU */
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

        /* BUTTONS */
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

        /* DOWNLOAD BUTTON */
        button[kind="secondary"] {
            background-color: #ff3b3b !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }

        button[kind="secondary"]:hover {
            background-color: #d90429 !important;
        }

        /* FILE UPLOADER BOX */
        [data-testid="stFileUploader"] {
            background-color: #1a1a1a !important;
            border: 1px solid #444 !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }

        /* TEXT INSIDE FILE UPLOADER */
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p {
            color: #ffffff !important;
        }

        /* DRAG & DROP AREA */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #1a1a1a !important;
            border: 2px dashed #444 !important;
            color: white !important;
        }

        /* BROWSE FILE BUTTON */
        [data-testid="stFileUploader"] button {
            background-color: #ff3b3b !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
        }

        /* DATAFRAME */
        div[data-testid="stDataFrame"] * {
            color: white !important;
        }

        table, th, td {
            color: white !important;
        }

        /* EXPANDER */
        details {
            background: #1a1a1a !important;
            border: 1px solid #333 !important;
            border-radius: 10px !important;
        }

        summary {
            color: white !important;
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
            color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
