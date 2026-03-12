import streamlit as st


def apply_dark_theme():
    st.markdown(
        """
        <style>

        /* MAIN BACKGROUND */
        .stApp {
            background: linear-gradient(135deg,#eef2ff,#e0f2fe);
            color: #111827;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background: #1e293b;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* TITLES */
        h1 {
            color: #1e293b;
            font-weight: 700;
        }

        h2, h3 {
            color: #334155;
        }

        /* CARDS */
        .soft-box {
            background: white;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        /* BUTTONS */
        .stButton>button {
            background: #6366f1;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 8px 18px;
            font-weight: 600;
        }

        .stButton>button:hover {
            background: #4f46e5;
        }

        /* TABLE */
        .dataframe {
            border-radius: 10px;
            border: 1px solid #e5e7eb;
        }

        /* INPUT */
        .stTextInput>div>div>input {
            border-radius: 8px;
        }

        /* SLIDER */
        .stSlider {
            padding-top: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
