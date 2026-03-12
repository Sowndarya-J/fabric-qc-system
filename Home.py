import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- GLOBAL DARK STYLE ----------
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background: linear-gradient(180deg,#020617 0%,#0f172a 100%);
    color:#f8fafc;
}

/* TEXT */
html,body,[class*="css"]{
    color:#f8fafc;
}

/* HEADINGS */
h1,h2,h3,h4,h5,h6{
    color:#ffffff !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background:#020617 !important;
}

section[data-testid="stSidebar"] *{
    color:#e5e7eb !important;
}

section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]{
    display:none;
}

/* INPUT BOXES */
.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div,
.stNumberInput input{
    background:#111827 !important;
    color:#ffffff !important;
    border:1px solid #334155 !important;
}

/* LABELS */
label{
    color:#f8fafc !important;
    font-weight:600;
}

/* BUTTONS */
.stButton > button{
    background:#2563eb !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    font-weight:600 !important;
}

.stButton > button:hover{
    background:#1d4ed8 !important;
}

/* TABLE */
[data-testid="stDataFrame"] *{
    color:#ffffff !important;
}

/* METRICS */
div[data-testid="stMetric"]{
    background:#111827;
    border:1px solid #334155;
    border-radius:14px;
    padding:10px;
}

/* HERO */
.hero{
    padding:30px;
    border-radius:20px;
    background:linear-gradient(135deg,#111827,#1e293b);
    border:1px solid #334155;
    margin-bottom:20px;
}

.hero-title{
    font-size:40px;
    font-weight:800;
}

.hero-sub{
    color:#cbd5e1;
    font-size:16px;
}

/* TAGS */
.tag{
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    background:#0f172a;
    border:1px solid #334155;
    color:#93c5fd;
    margin-right:8px;
}

/* CARDS */
.card{
    padding:20px;
    border-radius:16px;
    background:#111827;
    border:1px solid #334155;
    margin-bottom:10px;
}

.card h4{
    color:#ffffff;
}

.card p{
    color:#cbd5e1;
}

</style>
""", unsafe_allow_html=True)


# ---------- LANGUAGE ----------
if "lang" not in st.session_state:
    st.session_state.lang = "English"


# ---------- SIDEBAR ----------
with st.sidebar:

    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

    st.markdown("### Language")

    language = st.selectbox(
        "",
        ["English", "Tamil"],
        index=0
    )

    st.session_state.lang = language

    st.markdown("---")

    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Login",
            "Image Upload",
            "Live Webcam",
            "Model Metrics",
            "Admin Dashboard"
        ],
        icons=[
            "house",
            "key",
            "image",
            "camera-video",
            "bar-chart",
            "gear"
        ],
        default_index=0,
        styles={
            "container":{"padding":"0"},
            "icon":{"font-size":"18px"},
            "nav-link":{
                "font-size":"15px",
                "text-align":"left",
                "margin":"5px",
                "background-color":"#0f172a",
                "border-radius":"8px"
            },
            "nav-link-selected":{
                "background-color":"#2563eb",
            },
        }
    )

    st.markdown("---")

    if st.session_state.get("logged_in", False):

        user = st.session_state.get("user")
        role = st.session_state.get("role")

        st.success(f"👤 {user} ({role})")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    else:
        st.info("Please login first")


# ---------- PAGE LOADER ----------
def run_page(path):

    if not os.path.exists(path):
        st.error(f"Page not found: {path}")
        return

    try:
        with open(path,"r",encoding="utf-8") as f:
            code = f.read()

        exec(compile(code,path,"exec"),globals(),globals())

    except Exception as e:
        st.error(f"Error loading page: {path}")
        st.exception(e)


# ---------- HOME ----------
if selected == "Home":

    st.markdown("""
    <div class="hero">
    <div class="hero-title">Fabric Defect Detection System</div>
    <div class="hero-sub">
    AI powered textile inspection platform for automated defect detection,
    quality analysis and production monitoring.
    </div>

    <br>

    <span class="tag">YOLO Detection</span>
    <span class="tag">Mobile Camera</span>
    <span class="tag">Admin Analytics</span>
    <span class="tag">PDF Reports</span>
    <span class="tag">Quality Monitoring</span>

    </div>
    """,unsafe_allow_html=True)

    st.markdown("### Modules")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h4>🔐 Login</h4>
        <p>Admin and operator login with secure authentication.</p>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h4>🖼 Image Upload</h4>
        <p>Upload fabric images and detect defects instantly.</p>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h4>📷 Live Webcam</h4>
        <p>Capture fabric directly using mobile or webcam.</p>
        </div>
        """,unsafe_allow_html=True)

    d1,d2,d3 = st.columns(3)

    with d1:
        st.markdown("""
        <div class="card">
        <h4>📊 Model Metrics</h4>
        <p>View YOLO training performance metrics.</p>
        </div>
        """,unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="card">
        <h4>🛠 Admin Dashboard</h4>
        <p>Monitor inspections and view analytics.</p>
        </div>
        """,unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="card">
        <h4>📄 Reports</h4>
        <p>Generate PDF reports and email results.</p>
        </div>
        """,unsafe_allow_html=True)


# ---------- ROUTING ----------
elif selected == "Login":
    run_page("pages/1_Login.py")

elif selected == "Image Upload":
    run_page("pages/3_Image_Upload.py")

elif selected == "Live Webcam":
    run_page("pages/2_Webcam_Realtime.py")

elif selected == "Model Metrics":
    run_page("pages/5_Model_Metrics.py")

elif selected == "Admin Dashboard":
    run_page("pages/4_Admin_Dashboard.py")
