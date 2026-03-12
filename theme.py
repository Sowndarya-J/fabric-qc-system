import streamlit as st


def apply_dark_theme():

    st.markdown(
        """
        <style>

        /* MAIN BACKGROUND */
        .stApp {
            background-color: #0f0f0f;
            color: white;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #000000;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* TITLES */
        h1 {
            color: #ff3b3b;
            font-weight: 700;
        }

        h2, h3 {
            color: #ff5252;
        }

        /* TEXT */
        p, label, span {
            color: #f1f1f1;
        }

        /* CARD BOX */
        .soft-box {
            background: #1c1c1c;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #ff3b3b;
            margin-bottom: 20px;
        }

        /* BUTTON */
        .stButton>button {
            background: #ff3b3b;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: bold;
            padding: 8px 20px;
        }

        .stButton>button:hover {
            background: #d90429;
        }

        /* INPUT */
        .stTextInput>div>div>input {
            background: #1c1c1c;
            color: white;
            border-radius: 8px;
        }

        /* SELECTBOX */
        .stSelectbox>div>div {
            background: #1c1c1c;
            color: white;
        }

        /* SLIDER */
        .stSlider {
            color: white;
        }

        /* TABLE */
        .dataframe {
            background: #1c1c1c;
            color: white;
        }

        /* ALERT COLORS */
        .stAlert-success {
            background: #0f5132;
            color: white;
        }

        .stAlert-error {
            background: #7f1d1d;
            color: white;
        }

        /* CHAT */
        .stChatMessage {
            background: #1c1c1c;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
