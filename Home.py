import os
import streamlit as st
from streamlit_option_menu import option_menu
from theme import apply_dark_theme

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_dark_theme()

# Hide default Streamlit multipage navigation
st.markdown("""
<style>
section[data-testid="stSidebarNav"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

    st.markdown("---")

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
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#000000"
            },
            "icon": {
                "font-size": "18px",
                "color": "#ff3b3b"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px",
                "border-radius": "8px",
                "background-color": "#111111",
                "color": "#ffffff",
            },
            "nav-link-selected": {
                "background-color": "#ff3b3b",
                "color": "white",
            },
        },
    )

    st.markdown("---")

    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user")
        role = st.session_state.get("role")

        st.success(f"👤 {user} ({role})")

        if st.button("Logout", use_container_width=True, key="sidebar_logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    else:
        st.info("Please login first")


# ---------------- PAGE LOADER ---------------- #

def run_page(path: str):
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


# ---------------- PAGE ROUTING ---------------- #

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
