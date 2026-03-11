import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CLEAN STYLING
# -----------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {display:none;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 2.2rem 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    border: 1px solid #e5e7eb;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.4rem;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #4b5563;
    line-height: 1.7;
}

.tag {
    display: inline-block;
    padding: 0.45rem 0.85rem;
    margin: 0.35rem 0.35rem 0 0;
    border-radius: 999px;
    background: white;
    border: 1px solid #dbeafe;
    color: #1d4ed8;
    font-size: 0.88rem;
    font-weight: 600;
}

.card {
    padding: 1.2rem;
    border-radius: 18px;
    background: white;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    min-height: 170px;
}

.card-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.45rem;
}

.card-text {
    font-size: 0.95rem;
    color: #4b5563;
    line-height: 1.65;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 750;
    color: #111827;
    margin: 1rem 0 0.8rem 0;
}

.step {
    padding: 1rem 1rem 0.9rem 1rem;
    border-radius: 16px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    min-height: 120px;
}

.step-no {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #111827;
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.3rem;
}

.step-text {
    font-size: 0.92rem;
    color: #4b5563;
    line-height: 1.6;
}

.status-box {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    margin-top: 0.6rem;
}

.sidebar-user {
    padding: 0.8rem;
    border-radius: 14px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-based Fabric Inspection")

    selected = option_menu(
        menu_title=None,
        options=["Home", "Login", "Image Upload", "Live Webcam", "Model Metrics", "Admin Dashboard"],
        icons=["house", "key", "image", "camera-video", "bar-chart", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#111827",
            },
        }
    )

    st.markdown("---")

    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user")
        role = st.session_state.get("role")
        st.markdown(
            f"""
            <div class="sidebar-user">
                <b>👤 {user}</b><br>
                <span style="color:#6b7280;">Role: {role}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    else:
        st.info("Please login to continue")

# -----------------------------
# SAFE PAGE LOADER
# -----------------------------
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

# -----------------------------
# HOME
# -----------------------------
if selected == "Home":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Fabric Defect Detection & Quality Monitoring</div>
        <div class="hero-subtitle">
            Inspect fabric quality using AI-powered defect detection from uploaded images or mobile camera capture.
            Monitor inspection history, analyze performance, and generate reports in one system.
        </div>
        <div style="margin-top:0.9rem;">
            <span class="tag">YOLO Detection</span>
            <span class="tag">Mobile Camera</span>
            <span class="tag">PDF Reports</span>
            <span class="tag">Admin Dashboard</span>
            <span class="tag">Quality Status</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Main Modules</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🔐 Login & Access</div>
            <div class="card-text">
                Secure access for Admin and Operator roles with controlled inspection workflow and user-level access.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🖼 Image Upload Detection</div>
            <div class="card-text">
                Upload a fabric image, detect visible defects, visualize output, and review the defect summary instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <div class="card-title">📷 Mobile Camera Inspection</div>
            <div class="card-text">
                Capture a frame from the phone camera, run AI detection, and save the inspection result to history.
            </div>
        </div>
        """, unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="card">
            <div class="card-title">📊 Model Metrics</div>
            <div class="card-text">
                Review training performance such as precision, recall, mAP@50, and mAP@50-95 from results.csv.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="card">
            <div class="card-title">🛠 Admin Dashboard</div>
            <div class="card-text">
                Search records, filter inspections, preview saved outputs, and analyze defect trends across inspections.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown("""
        <div class="card">
            <div class="card-title">📄 Reports & Email</div>
            <div class="card-text">
                Generate PDF reports and send inspection outputs through email for documentation and quality tracking.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("""
        <div class="step">
            <div class="step-no">1</div>
            <div class="step-title">Input Fabric</div>
            <div class="step-text">Upload an image or use the phone camera to capture the fabric surface.</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="step">
            <div class="step-no">2</div>
            <div class="step-title">Run Detection</div>
            <div class="step-text">The YOLO model scans the image and detects defects on the fabric.</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="step">
            <div class="step-no">3</div>
            <div class="step-title">Quality Decision</div>
            <div class="step-text">The system counts defects and marks the result as PASS or REJECT.</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="step">
            <div class="step-no">4</div>
            <div class="step-title">Save & Review</div>
            <div class="step-text">Store inspection results, generate reports, and review analytics later.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">System Status</div>', unsafe_allow_html=True)

    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user")
        role = st.session_state.get("role")
        st.markdown(
            f"""
            <div class="status-box">
                <b>Logged in:</b> {user} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Role:</b> {role}<br>
                Use the sidebar to continue with detection, metrics, or dashboard operations.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("""
        <div class="status-box">
            <b>Not logged in.</b><br>
            Please login first to access image upload, live camera, and admin features.
        </div>
        """, unsafe_allow_html=True)

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
