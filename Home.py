import os
import streamlit as st
from streamlit_option_menu import option_menu

from theme import apply_dark_theme

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dark_theme()

if "lang" not in st.session_state:
    st.session_state.lang = "English"

with st.sidebar:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

    st.markdown("### Language")
    st.session_state.lang = st.selectbox(
        "Select Language",
        ["English", "Tamil"],
        index=0 if st.session_state.lang == "English" else 1,
        label_visibility="collapsed",
    )

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
            "container": {"padding": "0!important"},
            "icon": {"font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background-color": "#e11d48",
                "color": "white",
            },
        },
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


def run_page(path: str) -> None:
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


if selected == "Home":
    st.title("Fabric Defect Detection System")

    st.write("AI-powered textile inspection platform.")

    st.markdown("""
### Modules

- 🔐 Login
- 🖼 Image Upload Detection
- 📷 Live Webcam Detection
- 📊 Model Metrics
- 🛠 Admin Dashboard
- 🤖 Fabric Assistant

### Features

- YOLO Fabric Defect Detection
- Mobile Camera Capture
- Quality Status
- PDF Report Generation
- Admin Analytics
- Fabric Question Assistant
""")

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
