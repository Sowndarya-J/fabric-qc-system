import os
import streamlit as st
from streamlit_option_menu import option_menu
from theme import apply_dark_theme

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_dark_theme()

# Hide default Streamlit navigation
st.markdown("""
<style>

/* Hide sidebar navigation */
[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stSidebarNav"] {
    display: none;
}

/* Remove Streamlit header */
header {
    visibility: hidden;
}

/* Remove large padding */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* Reduce vertical spacing */
div[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

/* Top navigation container */
.top-nav-wrap {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #000000;
    padding: 0.2rem 0.5rem;
    border-bottom: 1px solid #222;
    margin-bottom: 0.3rem;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None


# ---------------- TOP NAV ---------------- #

st.markdown('<div class="top-nav-wrap">', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "Login",
        "Image Upload",
        "Live Webcam",
        "Model Metrics",
        "Admin Dashboard",
        "Fabric Assistant",
    ],
    icons=[
        "house",
        "key",
        "image",
        "camera-video",
        "bar-chart",
        "gear",
        "robot",
    ],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#000000",
        },
        "icon": {
            "font-size": "16px",
            "color": "#ff3b3b",
        },
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "2px",
            "padding": "8px",
            "border-radius": "6px",
            "background-color": "#111111",
            "color": "#ffffff",
        },
        "nav-link-selected": {
            "background-color": "#ff3b3b",
            "color": "white",
        },
    },
)

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HEADER ---------------- #

left, right = st.columns([4, 1])

with left:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

with right:
    if st.session_state.logged_in:
        st.success(f"{st.session_state.user} ({st.session_state.role})")

        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    else:
        st.info("Not logged in")


# ---------------- PAGE LOADER ---------------- #

def run_page(path):
    if not os.path.exists(path):
        st.error(f"Page not found: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        exec(compile(code, path, "exec"), globals(), globals())

    except Exception as e:
        st.error(f"Error loading page: {path}")
        st.exception(e)


# ---------------- HOME PAGE ---------------- #

if selected == "Home":

    st.markdown("""
    <div class="hero-box">
        <h1>Fabric Defect Detection System</h1>
        <p>
        AI-powered textile inspection platform for image upload detection,
        live webcam capture, model analytics, admin monitoring,
        and fabric assistant support.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Modules")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card-box">
        <h4>🔐 Login</h4>
        <p>Admin and operator login with secure access control.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card-box">
        <h4>🖼 Image Upload</h4>
        <p>Upload fabric images and detect defects instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card-box">
        <h4>📷 Live Webcam</h4>
        <p>Capture fabric directly using webcam or mobile camera.</p>
        </div>
        """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("""
        <div class="card-box">
        <h4>📊 Model Metrics</h4>
        <p>View training results such as precision, recall and mAP.</p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="card-box">
        <h4>🛠 Admin Dashboard</h4>
        <p>Monitor inspections, defects, trends and operator performance.</p>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="card-box">
        <h4>🤖 Fabric Assistant</h4>
        <p>Ask fabric-related questions using a ChatGPT-style layout.</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------- ROUTING ---------------- #

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

elif selected == "Fabric Assistant":
    run_page("pages/7_Fabric_Assistant.py")
