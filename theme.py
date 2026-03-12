import streamlit as st
from theme import apply_dark_theme

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide"
)

apply_dark_theme()

st.title("Fabric Defect Detection System")

st.write(
    "AI-powered textile inspection platform for image upload detection, "
    "live webcam capture, model analytics, admin monitoring, and fabric assistant support."
)

st.markdown("### Modules")

st.write("🔐 Login")
st.write("🖼 Image Upload")
st.write("📷 Live Webcam")
st.write("📊 Model Metrics")
st.write("🛠 Admin Dashboard")
st.write("🤖 Fabric Assistant")

if st.session_state.get("logged_in", False):
    st.info(f"User: {st.session_state.get('user')} | Role: {st.session_state.get('role')}")
