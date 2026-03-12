import streamlit as st


def apply_dark_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #0f172a;
            color: #f8fafc;
        }

        html, body, [class*="css"] {
            color: #f8fafc !important;
        }

        h1, h2, h3, h4, h5, h6,
        p, span, div, label, li {
            color: #f8fafc !important;
        }

        section[data-testid="stSidebar"] {
            background: #020617 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #e5e7eb !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
            display: none;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stDateInput input {
            background: #111827 !important;
            color: #ffffff !important;
            border: 1px solid #334155 !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #94a3b8 !important;
        }

        label, .stSelectbox label, .stSlider label, .stFileUploader label,
        .stDateInput label, .stNumberInput label, .stTextInput label,
        .stTextArea label {
            color: #f8fafc !important;
            font-weight: 600 !important;
        }

        .stButton > button {
            background: #2563eb !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .stButton > button:hover {
            background: #1d4ed8 !important;
        }

        div[data-testid="stMetric"] {
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            padding: 10px !important;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }

        div[data-testid="stDataFrame"] * {
            color: #f8fafc !important;
        }

        table, th, td {
            color: #f8fafc !important;
        }

        details {
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 6px !important;
        }

        summary {
            color: #f8fafc !important;
            font-weight: 600 !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px !important;
        }

        code {
            color: #93c5fd !important;
        }

        .hero-box {
            padding: 24px;
            border-radius: 20px;
            background: linear-gradient(135deg, #111827, #1e293b);
            border: 1px solid #334155;
            margin-bottom: 18px;
        }

        .card-box {
            padding: 18px;
            border-radius: 16px;
            background: #111827;
            border: 1px solid #334155;
            min-height: 140px;
            margin-bottom: 10px;
        }

        .soft-box {
            padding: 14px;
            border-radius: 14px;
            background: #111827;
            border: 1px solid #334155;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
