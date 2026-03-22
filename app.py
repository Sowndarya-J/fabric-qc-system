import os
import json
from datetime import datetime

import torch
torch.set_num_threads(1)

import av
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from utils import (
    load_users,
    save_users,
    check_login,
    get_role,
    get_model,
    init_db,
    insert_inspection,
    read_inspections,
    delete_inspection,
    save_images,
    build_heatmap,
    send_email_with_pdf,
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Fabric Defect Detection", layout="wide")
st.title("🧵 Fabric Defect Detection & Quality Monitoring System")

# =========================
# INIT DB
# =========================
init_db()

# =========================
# USERS
# =========================
USERS = load_users()

# =========================
# LOGIN SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        USERS = load_users()
        if check_login(u, p):
            st.session_state.logged_in = True
            st.session_state.user = u
            st.session_state.role = get_role(u)
            st.success(f"Logged in as {u} ({st.session_state.role})")
            st.rerun()
        else:
            st.error("Invalid username/password")

    st.stop()

st.info(f"✅ User: {st.session_state.user} | Role: {st.session_state.role}")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# =========================
# MODEL + CONTROLS
# =========================
model = get_model()
confidence_threshold = st.slider("Select Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

# =========================
# ADMIN: USER MANAGEMENT
# =========================
if st.session_state.role == "admin":
    st.header("👤 Admin: User Management")

    USERS = load_users()

    with st.expander("➕ Create New User", expanded=False):
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["operator", "admin"], index=0)

        if st.button("Create User"):
            if not new_user or not new_pass:
                st.warning("Username and password required.")
            elif new_user in USERS:
                st.error("User already exists. Choose different username.")
            else:
                USERS[new_user] = {"password": new_pass, "role": new_role}
                save_users(USERS)
                st.success(f"✅ User created: {new_user} ({new_role})")
                st.rerun()

    with st.expander("📋 View All Users", expanded=False):
        user_table = [{"Username": k, "Role": v["role"]} for k, v in USERS.items()]
        st.table(pd.DataFrame(user_table))

    with st.expander("🗑 Delete User", expanded=False):
        if USERS:
            del_user = st.selectbox("Select user to delete", list(USERS.keys()))
            if st.button("Delete Selected User"):
                if del_user == "admin":
                    st.error("You cannot delete the main admin.")
                else:
                    USERS.pop(del_user, None)
                    save_users(USERS)
                    st.success(f"Deleted user: {del_user}")
                    st.rerun()

# =========================
# REAL-TIME WEBCAM
# =========================
st.header("📷 Real-time Webcam Detection")

colA, colB, colC, colD = st.columns(4)
with colA:
    run_webcam = st.toggle("Start Camera", value=False)
with colB:
    # default = 320
    webcam_imgsz = st.selectbox("img size (CPU friendly)", [320, 416, 512, 640], index=0)
with colC:
    # default = 4
    webcam_every_n = st.selectbox("Run YOLO every N frames", [1, 2, 3, 4, 5], index=3)
with colD:
    cam_mode = st.selectbox("Camera", ["Back Camera", "Front Camera"], index=0)

facing_mode = "environment" if cam_mode == "Back Camera" else "user"

st.caption("📌 Mobile tip: For back camera, select 'Back Camera'. If needed, stop and start camera again.")

live_counts_placeholder = st.empty()
live_status_placeholder = st.empty()

class YOLOVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame_count = 0
        self.last_original = None
        self.last_annotated = None
        self.last_counts = {}
        self.last_total = 0
        self.last_high = 0
        self.last_status = "PASS"

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.last_original = img.copy()
        self.frame_count += 1

        out = self.last_annotated if self.last_annotated is not None else img

        if self.frame_count % int(webcam_every_n) == 0:
            res = model.predict(
                source=img,
                conf=float(confidence_threshold),
                imgsz=int(webcam_imgsz),
                verbose=False
            )
            r0 = res[0]
            boxes = r0.boxes
            names = r0.names

            counts = {}
            total = 0
            high = 0

            if boxes is not None and len(boxes) > 0:
                for b in boxes:
                    cls_id = int(b.cls[0])
                    conf = float(b.conf[0])
                    name = names[cls_id]
                    counts[name] = counts.get(name, 0) + 1
                    total += 1
                    if conf > 0.80:
                        high += 1

            if high > 0:
                status = "REJECT"
            elif total <= 2:
                status = "PASS"
            else:
                status = "REJECT"

            self.last_counts = counts
            self.last_total = total
            self.last_high = high
            self.last_status = status

            annotated = r0.plot()
            self.last_annotated = annotated
            out = annotated

        return av.VideoFrame.from_ndarray(out, format="bgr24")

ctx = None

if run_webcam:
    ctx = webrtc_streamer(
        key=f"fabric-webcam-{facing_mode}",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=YOLOVideoProcessor,
        media_stream_constraints={
            "video": {
                "facingMode": {"ideal": facing_mode},
                "width": {"ideal": 1280},
                "height": {"ideal": 720},
            },
            "audio": False,
        },
        rtc_configuration={
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                {"urls": ["stun:stun1.l.google.com:19302"]},
            ]
        },
        async_processing=True,
        video_html_attrs={
            "autoPlay": True,
            "playsInline": True,
            "muted": True,
        },
    )
else:
    st.info("Turn ON **Start Camera** to begin real-time detection.")

if ctx and ctx.video_processor:
    vp = ctx.video_processor
    counts = vp.last_counts
    total = vp.last_total
    status = vp.last_status

    live_counts_placeholder.subheader("🧾 Live Defect Count")
    if counts:
        live_counts_placeholder.table(pd.DataFrame(counts.items(), columns=["Defect", "Count"]))
    else:
        live_counts_placeholder.info("No defects detected in current frames.")

    if status == "PASS":
        live_status_placeholder.success(f"✅ LIVE QUALITY: PASS (Total defects: {total})")
    else:
        live_status_placeholder.error(f"❌ LIVE QUALITY: REJECT (Total defects: {total})")

    st.divider()
    st.subheader("💾 Save Camera Snapshot to History")

    if st.button("📌 Save Current Frame"):
        if vp.last_original is None or vp.last_annotated is None:
            st.warning("No frame available yet. Wait a few seconds after starting camera.")
        else:
            original_rgb = cv2.cvtColor(vp.last_original, cv2.COLOR_BGR2RGB)
            original_pil = Image.fromarray(original_rgb)

            orig_path, ann_path = save_images(
                original_pil,
                vp.last_annotated,
                prefix=f"{facing_mode}_{st.session_state.user}"
            )

            defects_json = json.dumps(vp.last_counts, ensure_ascii=False)

            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_inspection(
                dt,
                st.session_state.user,
                f"webcam-{facing_mode}",
                vp.last_total,
                vp.last_high,
                vp.last_status,
                orig_path,
                ann_path,
                defects_json
            )

            st.success("✅ Saved snapshot to history!")
            st.write(orig_path)
            st.write(ann_path)

st.warning("⚠️ Mobile camera works best on HTTPS. Render gives HTTPS, so allow camera permission in browser.")

# =========================
# IMAGE UPLOAD DETECTION
# =========================
st.header("🖼️ Image Upload Detection")

uploaded_file = st.file_uploader("Upload Fabric Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=500)

    if st.button("Detect Defects (Image)"):
        results = model(image, conf=confidence_threshold)
        result = results[0]
        result_image = result.plot()

        st.image(result_image, caption="Detected Defects", width=500)

        boxes = result.boxes
        names = result.names

        defect_data = []
        defect_count = {}
        total_defects = 0
        high_defects = 0
        quality_status = "PASS"
        defects_json = "{}"

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                defect_name = names[cls_id]

                if conf > 0.80:
                    severity = "High"
                elif conf > 0.50:
                    severity = "Medium"
                else:
                    severity = "Low"

                total_defects += 1
                defect_count[defect_name] = defect_count.get(defect_name, 0) + 1
                defect_data.append([defect_name, round(conf * 100, 2), severity])

            defects_json = json.dumps(defect_count, ensure_ascii=False)

            st.subheader("📋 Defect Details")
            df = pd.DataFrame(defect_data, columns=["Defect Type", "Confidence (%)", "Severity"])
            st.table(df)

            st.subheader("📊 Defect Distribution Chart")
            fig = plt.figure(figsize=(4, 4))
            plt.pie(defect_count.values(), labels=defect_count.keys(), autopct="%1.1f%%")
            plt.title("Defect Distribution")
            st.pyplot(fig)

            st.subheader("🏭 Quality Decision")
            high_defects = sum(1 for d in defect_data if d[2] == "High")

            if high_defects > 0:
                quality_status = "REJECT"
                st.error("❌ QUALITY STATUS: REJECT (High Severity Defect Found)")
            elif total_defects <= 2:
                quality_status = "PASS"
                st.success("✅ QUALITY STATUS: PASS")
            else:
                quality_status = "REJECT"
                st.warning("⚠️ QUALITY STATUS: REJECT (Too Many Defects)")

            st.subheader("🔥 Defect Heatmap")
            xyxy = boxes.xyxy.cpu().numpy()
            heat_color = build_heatmap(result_image.shape, xyxy)
            overlay = cv2.addWeighted(result_image, 0.7, heat_color, 0.3, 0)
            st.image(overlay, caption="Heatmap Overlay", width=500)

        else:
            df = pd.DataFrame([["No Defects", 0, "-"]], columns=["Defect Type", "Confidence (%)", "Severity"])
            st.success("🎉 No Defects Found — PERFECT FABRIC")
            quality_status = "PASS"
            total_defects = 0
            high_defects = 0
            defects_json = json.dumps({}, ensure_ascii=False)

        orig_path, ann_path = save_images(image, result_image, prefix=st.session_state.user)
        st.success(f"Saved images:\n{orig_path}\n{ann_path}")

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_inspection(
            dt,
            st.session_state.user,
            "image-upload",
            total_defects,
            high_defects,
            quality_status,
            orig_path,
            ann_path,
            defects_json
        )

        pdf_path = "Fabric_Report.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Fabric Defect Detection Report", styles["Heading1"]))
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph(f"Date: {dt}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Inspector: {st.session_state.user}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Confidence Threshold: {confidence_threshold}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Quality Status: {quality_status}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        data = [["Defect Type", "Confidence (%)", "Severity"]] + df.values.tolist()
        table = Table(data)
        table.setStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))

        temp_image_path = "detected_image.jpg"
        Image.fromarray(result_image).save(temp_image_path)
        elements.append(RLImage(temp_image_path, width=4 * inch, height=3 * inch))

        doc.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download PDF Report",
                data=f,
                file_name="Fabric_Report.pdf",
                mime="application/pdf"
            )

        st.subheader("📧 Email PDF Report (Gmail)")
        with st.expander("Send report via Email", expanded=False):
            sender_email = st.text_input(
                "Sender Gmail",
                value=st.secrets.get("SENDER_EMAIL", ""),
                placeholder="yourgmail@gmail.com"
            )
            app_password = st.text_input(
                "Gmail App Password",
                value=st.secrets.get("APP_PASSWORD", ""),
                type="password",
                placeholder="16-character app password"
            )
            receiver_email = st.text_input("Receiver Email", placeholder="receiver@gmail.com")
            email_subject = st.text_input("Email Subject", value="Fabric Defect Detection Report")
            email_body = st.text_area(
                "Email Message",
                value=f"Hi,\n\nPlease find attached the Fabric Defect Detection Report.\n\nInspector: {st.session_state.user}\nDate: {dt}\nQuality Status: {quality_status}\n\nThanks."
            )

            if st.button("📨 Send Email"):
                try:
                    if not sender_email or not app_password or not receiver_email:
                        st.warning("Please fill sender, app password, and receiver email.")
                    else:
                        send_email_with_pdf(
                            sender_email=sender_email.strip(),
                            app_password=app_password.strip(),
                            receiver_email=receiver_email.strip(),
                            subject=email_subject.strip(),
                            body=email_body,
                            pdf_path=pdf_path
                        )
                        st.success("✅ Email sent successfully!")
                except Exception as e:
                    st.error(f"❌ Email failed: {e}")

# =========================
# ADMIN DASHBOARD
# =========================
if st.session_state.role == "admin":
    st.header("🛠 Admin Dashboard")
    db_df = read_inspections(limit=300)

    st.subheader("📦 Database Records")
    st.dataframe(db_df)

    st.download_button(
        "⬇️ Download DB Export (CSV)",
        data=db_df.to_csv(index=False).encode("utf-8"),
        file_name="inspections_export.csv",
        mime="text/csv",
    )

    st.subheader("🗑 Delete a Record")
    del_id = st.number_input("Enter ID to delete", min_value=0, step=1)
    if st.button("Delete Record"):
        if del_id > 0:
            delete_inspection(int(del_id))
            st.success(f"Deleted record ID {int(del_id)}")
            st.rerun()
        else:
            st.warning("Enter valid ID")

# =========================
# TRAINING METRICS
# =========================
st.header("📊 Model Performance Metrics (Training)")
st.write("results.csv found:", os.path.exists("results.csv"))

if os.path.exists("results.csv"):
    metrics_df = pd.read_csv("results.csv")
    last_row = metrics_df.iloc[-1]

    def pick(cols, default=0.0):
        for c in cols:
            if c in metrics_df.columns:
                return float(last_row[c])
        return float(default)

    precision = pick(["metrics/precision(B)", "metrics/precision", "precision"])
    recall = pick(["metrics/recall(B)", "metrics/recall", "recall"])
    map50 = pick(["metrics/mAP50(B)", "metrics/mAP50", "mAP50"])
    map5095 = pick(["metrics/mAP50-95(B)", "metrics/mAP50-95", "mAP50-95"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Precision", f"{precision:.3f}")
    c2.metric("Recall", f"{recall:.3f}")
    c3.metric("mAP@50", f"{map50:.3f}")
    c4.metric("mAP@50-95", f"{map5095:.3f}")

    with st.expander("Show full results.csv"):
        st.dataframe(metrics_df)
else:
    st.info("📌 Place your training results.csv in this folder to display metrics.")
