import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Fabric QC System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM STYLE
# -----------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {display:none;}

.main-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 8px;
}

.sub-title {
    font-size: 18px;
    color: #9aa0a6;
    margin-bottom: 18px;
}

.hero-box {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: white;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    margin-bottom: 18px;
}

.info-chip {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    color: white;
    font-size: 14px;
    margin-right: 8px;
    margin-top: 6px;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: #111827;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    min-height: 150px;
}

.card h4 {
    margin-top: 0;
    margin-bottom: 8px;
    font-size: 20px;
}

.card p {
    color: #d1d5db;
    font-size: 14px;
    line-height: 1.6;
}

.small-card {
    padding: 18px;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    min-height: 120px;
}

.small-card h5 {
    margin: 0 0 6px 0;
    font-size: 18px;
}

.small-card p {
    margin: 0;
    color: #4b5563;
    font-size: 14px;
}

.status-box {
    padding: 18px;
    border-radius: 16px;
    background: #ecfeff;
    border: 1px solid #a5f3fc;
    margin-top: 10px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 14px;
}

.footer-box {
    padding: 18px;
    border-radius: 18px;
    background: #0f172a;
    color: white;
    margin-top: 18px;
}

div[data-testid="stMetric"] {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    padding: 12px;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 🧵 Fabric QC System")
    st.caption("AI-Based Fabric Quality Inspection")

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
        st.success(f"👤 {user} ({role})")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    else:
        st.warning("Not logged in")

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
# HOME PAGE
# -----------------------------
if selected == "Home":
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">🧵 Fabric Defect Detection & Quality Monitoring System</div>
        <div class="sub-title">
            Smart textile inspection using AI-powered YOLO detection for image upload, mobile camera capture,
            analytics dashboard, PDF reporting, and quality decision support.
        </div>
        <span class="info-chip">⚡ Real-Time Detection</span>
        <span class="info-chip">📷 Mobile Camera Support</span>
        <span class="info-chip">📄 PDF Reports</span>
        <span class="info-chip">🛠 Admin Dashboard</span>
        <span class="info-chip">🤖 YOLO AI Model</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Detection Type", "YOLO Model")
    with c2:
        st.metric("Inspection Modes", "2")
    with c3:
        st.metric("User Roles", "Admin / Operator")
    with c4:
        st.metric("Output", "PASS / REJECT")

    st.markdown('<div class="section-title">🔥 Core Modules</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="card">
            <h4>🔐 Login & Role Management</h4>
            <p>
                Secure login for Admin and Operator users. Admin can manage users,
                monitor records, and control inspection workflow.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="card">
            <h4>🖼 Image Upload Detection</h4>
            <p>
                Upload a fabric image and instantly detect defects, visualize bounding boxes,
                view severity, and generate inspection reports.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with a3:
        st.markdown("""
        <div class="card">
            <h4>📷 Live / Mobile Camera Inspection</h4>
            <p>
                Capture fabric directly using front or back mobile camera,
                run AI detection, and save the inspection result to history.
            </p>
        </div>
        """, unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        <div class="card">
            <h4>📊 Model Metrics</h4>
            <p>
                Track precision, recall, mAP@50, and mAP@50-95 using your training
                results file and monitor overall model quality.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div class="card">
            <h4>🛠 Admin Dashboard</h4>
            <p>
                Search inspection history, filter by user/date/source/defect,
                preview saved images, and analyze plant-level quality trends.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with b3:
        st.markdown("""
        <div class="card">
            <h4>📄 Reports & Email</h4>
            <p>
                Export professional PDF inspection reports and send them directly
                via email for documentation and quality control review.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚙️ How the System Works</div>', unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown("""
        <div class="small-card">
            <h5>1. Capture / Upload</h5>
            <p>Take a photo from camera or upload a fabric image into the system.</p>
        </div>
        """, unsafe_allow_html=True)
    with w2:
        st.markdown("""
        <div class="small-card">
            <h5>2. AI Detection</h5>
            <p>YOLO model scans the fabric and identifies visible defect regions.</p>
        </div>
        """, unsafe_allow_html=True)
    with w3:
        st.markdown("""
        <div class="small-card">
            <h5>3. Quality Decision</h5>
            <p>The system counts defects and marks the fabric as PASS or REJECT.</p>
        </div>
        """, unsafe_allow_html=True)
    with w4:
        st.markdown("""
        <div class="small-card">
            <h5>4. Save & Analyze</h5>
            <p>Store inspection history, preview results, and review analytics later.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📌 Current System Status</div>', unsafe_allow_html=True)

    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user")
        role = st.session_state.get("role")
        st.markdown(f"""
        <div class="status-box">
            <b>System Ready:</b> Logged in as <b>{user}</b> with role <b>{role}</b>.<br>
            You can now open modules from the sidebar and start inspection.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-box">
            <b>System Ready:</b> Please login first to access image upload, live camera,
            model metrics, and admin dashboard features.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-box">
        <b>Project Objective:</b><br>
        To automate fabric defect inspection using AI and help textile industries improve
        quality control, reduce manual error, and generate faster inspection reports.
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
