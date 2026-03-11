import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Fabric QC System", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Login", "Image Upload", "Live Webcam", "Model Metrics", "Admin Dashboard"],
        icons=["house", "key", "image", "camera-video", "bar-chart", "gear"],
        default_index=0,
    )

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

if selected == "Home":
    st.title("🏠 Fabric Defect Detection System")
    st.write("Use the sidebar to navigate between modules.")
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
