import json
from datetime import datetime

import av

try:
    import cv2
except Exception:
    cv2 = None

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

from utils import get_model, save_images, insert_inspection, init_db

st.title("📷 Mobile-Style Camera Capture")

init_db()

if not st.session_state.get("logged_in", False):
    st.warning("Please Login first (Go to Login page).")
    st.stop()

if cv2 is None:
    st.error("OpenCV is not available on this system.")
    st.stop()

# -----------------------------
# SESSION STATE
# -----------------------------
def reset_camera_state():
    st.session_state.captured_frame_bgr = None
    st.session_state.detected_frame_bgr = None
    st.session_state.detected_counts = {}
    st.session_state.detected_total = 0
    st.session_state.detected_high = 0
    st.session_state.detected_status = "PASS"

if "captured_frame_bgr" not in st.session_state:
    reset_camera_state()

# -----------------------------
# CONTROLS
# -----------------------------
start_camera = st.toggle("Start Camera", value=False)

confidence_threshold = st.slider(
    "Confidence Threshold",
    min_value=0.30,
    max_value=1.00,
    value=0.60,
    step=0.05
)

c1, c2 = st.columns(2)
with c1:
    cam_mode = st.selectbox("Camera", ["Back Camera", "Front Camera"], index=0)
with c2:
    webcam_imgsz = st.selectbox("Detection Image Size", [320, 416, 512, 640], index=0)

facing_mode = "environment" if cam_mode == "Back Camera" else "user"

st.caption("📌 Mobile tip: choose Back Camera for fabric inspection. Use Chrome and allow camera permission.")

# -----------------------------
# VIDEO PROCESSOR
# -----------------------------
class CameraCaptureProcessor(VideoProcessorBase):
    def __init__(self):
        self.last_frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.last_frame = img.copy()
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# -----------------------------
# CAMERA PREVIEW
# -----------------------------
ctx = None

if start_camera:
    ctx = webrtc_streamer(
        key=f"mobile-capture-{facing_mode}",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=CameraCaptureProcessor,
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
    st.info("Turn on **Start Camera** to preview and capture a frame.")

# -----------------------------
# ACTION BUTTONS
# -----------------------------
b1, b2, b3, b4 = st.columns(4)

with b1:
    capture_clicked = st.button("📸 Capture", use_container_width=True)

with b2:
    detect_clicked = st.button("🔍 Detect", use_container_width=True)

with b3:
    retake_clicked = st.button("🔄 Retake", use_container_width=True)

with b4:
    save_clicked = st.button("💾 Save Result", use_container_width=True)

# -----------------------------
# RETAKE
# -----------------------------
if retake_clicked:
    reset_camera_state()
    st.rerun()

# -----------------------------
# CAPTURE FRAME
# -----------------------------
if capture_clicked:
    if not start_camera:
        st.warning("Please start the camera first.")
    elif ctx and ctx.video_processor and ctx.video_processor.last_frame is not None:
        st.session_state.captured_frame_bgr = ctx.video_processor.last_frame.copy()
        st.session_state.detected_frame_bgr = None
        st.session_state.detected_counts = {}
        st.session_state.detected_total = 0
        st.session_state.detected_high = 0
        st.session_state.detected_status = "PASS"
        st.success("✅ Frame captured.")
    else:
        st.warning("No frame available yet. Wait a few seconds and try again.")

# -----------------------------
# SHOW CAPTURED FRAME
# -----------------------------
if st.session_state.captured_frame_bgr is not None:
    st.subheader("📌 Captured Frame")
    captured_rgb = cv2.cvtColor(st.session_state.captured_frame_bgr, cv2.COLOR_BGR2RGB)
    st.image(captured_rgb, caption="Captured Frame", use_column_width=True)

# -----------------------------
# RUN DETECTION
# -----------------------------
if detect_clicked:
    if st.session_state.captured_frame_bgr is None:
        st.warning("Please capture a frame first.")
    else:
        model = get_model()

        res = model.predict(
            source=st.session_state.captured_frame_bgr,
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

        st.session_state.detected_frame_bgr = r0.plot()
        st.session_state.detected_counts = counts
        st.session_state.detected_total = total
        st.session_state.detected_high = high
        st.session_state.detected_status = status

        st.success("✅ Detection completed.")

# -----------------------------
# SHOW DETECTION RESULT
# -----------------------------
if st.session_state.detected_frame_bgr is not None:
    st.subheader("🧠 Detection Result")

    detected_rgb = cv2.cvtColor(st.session_state.detected_frame_bgr, cv2.COLOR_BGR2RGB)
    st.image(detected_rgb, caption="Detected Output", use_column_width=True)

    counts = st.session_state.detected_counts
    total = st.session_state.detected_total
    status = st.session_state.detected_status

    if counts:
        st.subheader("🧾 Defect Count")
        st.table(pd.DataFrame(counts.items(), columns=["Defect", "Count"]))
    else:
        st.info("No defects detected.")

    if status == "PASS":
        st.success(f"✅ QUALITY STATUS: PASS (Total defects: {total})")
    else:
        st.error(f"❌ QUALITY STATUS: REJECT (Total defects: {total})")

# -----------------------------
# SAVE RESULT
# -----------------------------
if save_clicked:
    if st.session_state.captured_frame_bgr is None or st.session_state.detected_frame_bgr is None:
        st.warning("Capture and detect first before saving.")
    else:
        original_rgb = cv2.cvtColor(st.session_state.captured_frame_bgr, cv2.COLOR_BGR2RGB)
        original_pil = Image.fromarray(original_rgb)

        orig_path, ann_path = save_images(
            original_pil,
            st.session_state.detected_frame_bgr,
            prefix=f"{facing_mode}_{st.session_state.user}"
        )

        defects_json = json.dumps(st.session_state.detected_counts, ensure_ascii=False)

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_inspection(
            dt,
            st.session_state.user,
            f"camera-capture-{facing_mode}",
            st.session_state.detected_total,
            st.session_state.detected_high,
            st.session_state.detected_status,
            orig_path,
            ann_path,
            defects_json
        )

        st.success("✅ Result saved to history.")
        st.write(orig_path)
        st.write(ann_path)

st.warning("⚠️ Mobile camera works best on HTTPS and Chrome browser.")
