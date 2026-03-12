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

from utils import (
    get_model,
    save_images,
    insert_inspection,
    init_db,
    next_inspection_id,
    calculate_severity,
    defect_recommendations,
    play_alert_sound,
    t
)

st.markdown("""
<style>
.dark-panel {
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #334155;
    color: #e5e7eb;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("📷 Mobile-Style Camera Capture")
init_db()

if not st.session_state.get("logged_in", False):
    st.warning("Please Login first.")
    st.stop()

if cv2 is None:
    st.error("OpenCV is not available.")
    st.stop()

def reset_camera_state():
    st.session_state.captured_frame_bgr = None
    st.session_state.detected_frame_bgr = None
    st.session_state.detected_counts = {}
    st.session_state.detected_total = 0
    st.session_state.detected_high = 0
    st.session_state.detected_status = "PASS"
    st.session_state.detected_avg_conf = 0.0
    st.session_state.detected_max_conf = 0.0

if "captured_frame_bgr" not in st.session_state:
    reset_camera_state()

start_camera = st.toggle("Start Camera", value=False)

m1, m2, m3, m4 = st.columns(4)
with m1:
    batch_no = st.text_input(t("batch_no"), value="")
with m2:
    fabric_type = st.selectbox(t("fabric_type"), ["Cotton", "Polyester", "Silk", "Denim", "Other"])
with m3:
    shift = st.selectbox(t("shift"), ["Morning", "Afternoon", "Night"])
with m4:
    machine_id = st.text_input(t("machine_id"), value="M-01")

confidence_threshold = st.slider(
    t("confidence_threshold"),
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

class CameraCaptureProcessor(VideoProcessorBase):
    def __init__(self):
        self.last_frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.last_frame = img.copy()
        return av.VideoFrame.from_ndarray(img, format="bgr24")

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
        video_html_attrs={"autoPlay": True, "playsInline": True, "muted": True},
    )
else:
    st.info("Turn on Start Camera to preview and capture.")

b1, b2, b3, b4 = st.columns(4)
with b1:
    capture_clicked = st.button(t("capture"), use_container_width=True)
with b2:
    detect_clicked = st.button(t("detect"), use_container_width=True)
with b3:
    retake_clicked = st.button(t("retake"), use_container_width=True)
with b4:
    save_clicked = st.button(t("save_result"), use_container_width=True)

if retake_clicked:
    reset_camera_state()
    st.rerun()

if capture_clicked:
    if not start_camera:
        st.warning("Please start the camera first.")
    elif ctx and ctx.video_processor and ctx.video_processor.last_frame is not None:
        st.session_state.captured_frame_bgr = ctx.video_processor.last_frame.copy()
        st.session_state.detected_frame_bgr = None
        st.success("✅ Frame captured.")
    else:
        st.warning("No frame available yet. Wait a few seconds and try again.")

if st.session_state.captured_frame_bgr is not None:
    st.subheader("📌 Captured Frame")
    captured_rgb = cv2.cvtColor(st.session_state.captured_frame_bgr, cv2.COLOR_BGR2RGB)
    st.image(captured_rgb, caption="Captured Frame", use_column_width=True)

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
        confs = []

        if boxes is not None and len(boxes) > 0:
            for b in boxes:
                cls_id = int(b.cls[0])
                conf = float(b.conf[0])
                confs.append(conf)
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
        st.session_state.detected_avg_conf = round(sum(confs) / len(confs), 4) if confs else 0.0
        st.session_state.detected_max_conf = round(max(confs), 4) if confs else 0.0

        if status == "REJECT":
            play_alert_sound()

        st.success("✅ Detection completed.")

if st.session_state.detected_frame_bgr is not None:
    st.subheader("🧠 Detection Result")
    detected_rgb = cv2.cvtColor(st.session_state.detected_frame_bgr, cv2.COLOR_BGR2RGB)
    st.image(detected_rgb, caption="Detected Output", use_column_width=True)

    counts = st.session_state.detected_counts
    total = st.session_state.detected_total
    status = st.session_state.detected_status
    avg_conf = st.session_state.detected_avg_conf

    severity_score, severity_label = calculate_severity(
        total, st.session_state.detected_high, avg_conf
    )
    recommendations = defect_recommendations(counts)

    if counts:
        st.table(pd.DataFrame(counts.items(), columns=["Defect", "Count"]))
    else:
        st.info("No defects detected.")

    if status == "PASS":
        st.success(f"✅ {t('quality_status')}: PASS")
    else:
        st.error(f"❌ {t('quality_status')}: REJECT")

    st.info(f"{t('severity_score')}: {severity_score} ({severity_label})")
    st.warning(f"{t('recommendations')}: {recommendations}")

if save_clicked:
    if st.session_state.captured_frame_bgr is None or st.session_state.detected_frame_bgr is None:
        st.warning("Capture and detect first before saving.")
    else:
        inspection_id = next_inspection_id()
        original_rgb = cv2.cvtColor(st.session_state.captured_frame_bgr, cv2.COLOR_BGR2RGB)
        original_pil = Image.fromarray(original_rgb)

        orig_path, ann_path = save_images(
            original_pil,
            st.session_state.detected_frame_bgr,
            prefix=f"{facing_mode}_{st.session_state.user}"
        )

        defects_json = json.dumps(st.session_state.detected_counts, ensure_ascii=False)
        severity_score, severity_label = calculate_severity(
            st.session_state.detected_total,
            st.session_state.detected_high,
            st.session_state.detected_avg_conf
        )
        recommendations = defect_recommendations(st.session_state.detected_counts)

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_inspection(
            inspection_id,
            dt,
            st.session_state.user,
            f"camera-capture-{facing_mode}",
            batch_no,
            fabric_type,
            shift,
            machine_id,
            st.session_state.detected_total,
            st.session_state.detected_high,
            st.session_state.detected_status,
            severity_score,
            severity_label,
            recommendations,
            st.session_state.detected_avg_conf,
            st.session_state.detected_max_conf,
            orig_path,
            ann_path,
            defects_json
        )

        st.success(f"✅ Result saved. Inspection ID: {inspection_id}")
