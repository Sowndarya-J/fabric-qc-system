import os
import streamlit as st
from streamlit_option_menu import option_menu
from utils import t

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {display:none;}

.stApp {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    color: #e5e7eb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 2rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #111827 0%, #1e293b 60%, #0f172a 100%);
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0,0,0,0.30);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.4rem;
}

.hero-sub {
    font-size: 1rem;
    color: #cbd5e1;
    line-height: 1.7;
}

.tag {
    display: inline-block;
    padding: 0.45rem 0.85rem;
    margin: 0.5rem 0.4rem 0 0;
    border-radius: 999px;
    background: #0f172a;
    border: 1px solid #334155;
    color: #93c5fd;
    font-size: 0.86rem;
    font-weight: 600;
}

.card {
    padding: 1rem;
    border-radius: 18px;
    background: #111827;
    border: 1px solid #334155;
    box-shadow: 0 6px 18px rgba(0,0,0,0.20);
    min-height: 155px;
    color: #e5e7eb;
}

.card h4 {
    margin-bottom: 0.45rem;
    color: #f8fafc;
}

.card p {
    color: #cbd5e1;
    font-size: 0.94rem;
    line-height: 1.6;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 1rem 0 0.8rem 0;
}

.step {
    padding: 1rem;
    border-radius: 16px;
    background: #0f172a;
    border: 1px solid #334155;
    min-height: 120px;
}

.step-no {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #2563eb;
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: #f8fafc;
}

.step-text {
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.6;
    margin-top: 0.25rem;
}

.status-box {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: #111827;
    border: 1px solid #334155;
    color: #e5e7eb;
}

div[data-testid="stSidebar"] {
    background: #020617;
}

div[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "English"

with st.sidebar:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

    st.selectbox(t("language"), ["English", "Tamil"], key="lang")

    selected = option_menu(
        menu_title=None,
        options=[t("home"), t("login"), t("image_upload"), t("live_webcam"), t("model_metrics"), t("admin_dashboard")],
        icons=["house", "key", "image", "camera-video", "bar-chart", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#020617"},
            "icon": {"font-size": "18px", "color": "#93c5fd"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "10px",
                "background-color": "#0f172a",
                "color": "#e5e7eb",
            },
            "nav-link-selected": {
                "background-color": "#1d4ed8",
                "color": "white",
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
        st.info("Please login to continue")

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

if selected == t("home"):
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Fabric Defect Detection & Quality Monitoring</div>
        <div class="hero-sub">
            Premium AI-based textile inspection platform for image upload, mobile camera capture,
            quality scoring, recommendations, analytics dashboard, PDF reports, and operator tracking.
        </div>
        <div>
            <span class="tag">YOLO Detection</span>
            <span class="tag">Mobile Camera</span>
            <span class="tag">Severity Score</span>
            <span class="tag">Auto Reports</span>
            <span class="tag">Admin Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Core Modules</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
            <h4>🔐 Login & Access</h4>
            <p>Admin and Operator login with role-based access for quality control workflow.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
            <h4>🖼 Image Upload Detection</h4>
            <p>Upload a fabric image, detect defects, calculate severity, and export PDF report.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
            <h4>📷 Mobile Camera Capture</h4>
            <p>Capture fabric using back/front camera, detect defects, and save results instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("""
        <div class="card">
            <h4>📊 Model Metrics</h4>
            <p>Review training performance using Precision, Recall, mAP@50, and mAP@50-95.</p>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("""
        <div class="card">
            <h4>🛠 Admin Dashboard</h4>
            <p>Filter inspections, preview saved images, and track operator-level performance.</p>
        </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown("""
        <div class="card">
            <h4>📄 Reports & Alerts</h4>
            <p>Generate QR-coded PDF reports and send auto-email alerts for reject cases.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("""
        <div class="step">
            <div class="step-no">1</div>
            <div class="step-title">Input Fabric</div>
            <div class="step-text">Upload image or capture from mobile camera.</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="step">
            <div class="step-no">2</div>
            <div class="step-title">Run AI Detection</div>
            <div class="step-text">YOLO finds defect regions and confidence values.</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="step">
            <div class="step-no">3</div>
            <div class="step-title">Quality Decision</div>
            <div class="step-text">System marks fabric as PASS or REJECT with severity score.</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown("""
        <div class="step">
            <div class="step-no">4</div>
            <div class="step-title">Save & Analyze</div>
            <div class="step-text">Store inspection history and review analytics later.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">System Status</div>', unsafe_allow_html=True)
    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user")
        role = st.session_state.get("role")
        st.markdown(
            f"""
            <div class="status-box">
                <b>Logged in:</b> {user} &nbsp; | &nbsp; <b>Role:</b> {role}<br>
                Use the sidebar to continue with inspection, metrics, or dashboard operations.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("""
        <div class="status-box">
            <b>Not logged in.</b><br>
            Please login first to access image upload, camera, model metrics, and admin features.
        </div>
        """, unsafe_allow_html=True)

elif selected == t("login"):
    run_page("pages/1_Login.py")
elif selected == t("image_upload"):
    run_page("pages/3_Image_Upload.py")
elif selected == t("live_webcam"):
    run_page("pages/2_Webcam_Realtime.py")
elif selected == t("model_metrics"):
    run_page("pages/5_Model_Metrics.py")
elif selected == t("admin_dashboard"):
    run_page("pages/4_Admin_Dashboard.py")
