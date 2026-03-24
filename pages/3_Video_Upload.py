import json
import time
from datetime import datetime, timezone

import cv2
import pandas as pd
import streamlit as st
from PIL import Image

from live_sync import push_live_status, set_operator_offline, upload_live_frame
from utils import get_model, insert_inspection, save_images

st.title("🎞️ Video Detection")

if not st.session_state.get("logged_in", False):
    st.warning("Please Login first (Go to Login page).")
    st.stop()

# Video mode default values
st.session_state.machine_id = "VIDEO_TEST"
st.session_state.batch_no = "SIMULATION"

st.info("🎬 Simulation Mode (Video Upload) — Operator details are auto-assigned")

model = get_model()

# ---------- Session state ----------
defaults = {
    "video_last_original": None,
    "video_last_annotated": None,
    "video_last_counts": {},
    "video_last_total": 0,
    "video_last_high": 0,
    "video_last_status": "PASS",
    "video_last_avg_conf": 0.0,
    "video_last_max_conf": 0.0,
    "video_last_snapshot_upload_ts": 0.0,
    "video_last_status_push_ts": 0.0,
    "video_last_live_snapshot_url": "",
    "video_processed_once": False,
    "video_last_saved_orig": "",
    "video_last_saved_ann": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def send_live_update(
    operator_name,
    machine_id,
    batch_no,
    input_mode,
    quality_status,
    total_defects,
    high_severity,
    avg_confidence,
    max_confidence,
    defects_json,
    is_online=True,
    snapshot_path="",
    force=False,
):
    now_ts = time.time()

    if not force and (now_ts - st.session_state.video_last_status_push_ts < 2):
        return

    payload = {
        "operator_id": operator_name,
        "operator_name": operator_name,
        "machine_id": machine_id or "",
        "batch_no": batch_no or "",
        "camera_mode": input_mode,
        "quality_status": quality_status or "PASS",
        "total_defects": int(total_defects or 0),
        "high_severity": int(high_severity or 0),
        "avg_confidence": float(avg_confidence or 0.0),
        "max_confidence": float(max_confidence or 0.0),
        "defects_json": defects_json if isinstance(defects_json, dict) else {},
        "snapshot_path": snapshot_path or "",
        "source": "video-file",
        "is_online": bool(is_online),
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

    push_live_status(payload)
    st.session_state.video_last_status_push_ts = now_ts


def analyze_result(res):
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
            name = names[cls_id]

            counts[name] = counts.get(name, 0) + 1
            total += 1
            confs.append(conf)

            if conf > 0.80:
                high += 1

    if high > 0:
        status = "REJECT"
    elif total <= 2:
        status = "PASS"
    else:
        status = "REJECT"

    avg_conf = round(sum(confs) / len(confs), 4) if confs else 0.0
    max_conf = round(max(confs), 4) if confs else 0.0
    annotated = r0.plot()

    return counts, total, high, status, avg_conf, max_conf, annotated


def upload_snapshot_if_needed(image_bgr, operator_id):
    now_ts = time.time()
    current_url = st.session_state.get("video_last_live_snapshot_url", "")

    if image_bgr is not None and (now_ts - st.session_state.video_last_snapshot_upload_ts >= 3):
        rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        snapshot_url = upload_live_frame(pil_img, operator_id)

        if snapshot_url:
            st.session_state.video_last_live_snapshot_url = snapshot_url
            st.session_state.video_last_snapshot_upload_ts = now_ts
            current_url = snapshot_url

    return current_url


def save_current_detected_video_frame():
    if st.session_state.video_last_original is None or st.session_state.video_last_annotated is None:
        st.warning("No detected video frame available to save.")
        return

    original_rgb = cv2.cvtColor(st.session_state.video_last_original, cv2.COLOR_BGR2RGB)
    original_pil = Image.fromarray(original_rgb)

    orig_path, ann_path = save_images(
        original_pil,
        st.session_state.video_last_annotated,
        prefix=f"video_{st.session_state.user}"
    )

    defects_json_str = json.dumps(st.session_state.video_last_counts, ensure_ascii=False)

    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_inspection(
        dt,
        st.session_state.user,
        "video-file",
        st.session_state.video_last_total,
        st.session_state.video_last_high,
        st.session_state.video_last_status,
        orig_path,
        ann_path,
        defects_json_str
    )

    send_live_update(
        operator_name=st.session_state.user,
        machine_id=st.session_state.machine_id,
        batch_no=st.session_state.batch_no,
        input_mode="Video File",
        quality_status=st.session_state.video_last_status,
        total_defects=st.session_state.video_last_total,
        high_severity=st.session_state.video_last_high,
        avg_confidence=st.session_state.video_last_avg_conf,
        max_confidence=st.session_state.video_last_max_conf,
        defects_json=st.session_state.video_last_counts,
        is_online=True,
        snapshot_path=st.session_state.get("video_last_live_snapshot_url", ""),
        force=True,
    )

    st.session_state.video_last_saved_orig = orig_path
    st.session_state.video_last_saved_ann = ann_path
    st.success("✅ Detected video frame saved successfully!")
    st.write(orig_path)
    st.write(ann_path)


confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
imgsz = st.selectbox("img size", [320, 416, 512, 640], index=0)
every_n = st.selectbox("Run YOLO every N frames", [1, 2, 3, 4, 5], index=2)

uploaded_video = st.file_uploader("Upload fabric video", type=["mp4", "avi", "mov", "mkv"])

frame_placeholder = st.empty()
live_counts_placeholder = st.empty()
live_status_placeholder = st.empty()

if uploaded_video is None:
    set_operator_offline(st.session_state.user)
    st.session_state.video_processed_once = False
    st.info("Upload a video file to start detection.")
else:
    temp_video_path = f"temp_{uploaded_video.name}"

    with open(temp_video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.video(temp_video_path)

    col1, col2 = st.columns(2)
    process_video = col1.button("▶️ Process Video")
    auto_save_latest = col2.button("💾 Save Latest Detected Frame")

    if process_video:
        send_live_update(
            operator_name=st.session_state.user,
            machine_id=st.session_state.machine_id,
            batch_no=st.session_state.batch_no,
            input_mode="Video File",
            quality_status="PASS",
            total_defects=0,
            high_severity=0,
            avg_confidence=0.0,
            max_confidence=0.0,
            defects_json={},
            is_online=True,
            force=True,
        )

        cap = cv2.VideoCapture(temp_video_path)
        frame_count = 0
        st.session_state.video_processed_once = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            st.session_state.video_last_original = frame.copy()

            if frame_count % int(every_n) != 0:
                continue

            res = model.predict(
                source=frame,
                conf=float(confidence_threshold),
                imgsz=int(imgsz),
                verbose=False
            )

            counts, total, high, status, avg_conf, max_conf, annotated = analyze_result(res)

            st.session_state.video_last_counts = counts
            st.session_state.video_last_total = total
            st.session_state.video_last_high = high
            st.session_state.video_last_status = status
            st.session_state.video_last_avg_conf = avg_conf
            st.session_state.video_last_max_conf = max_conf
            st.session_state.video_last_annotated = annotated
            st.session_state.video_processed_once = True

            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(
                annotated_rgb,
                caption="Processed Video View",
                use_container_width=True
            )

            live_snapshot_url = upload_snapshot_if_needed(annotated, st.session_state.user)

            send_live_update(
                operator_name=st.session_state.user,
                machine_id=st.session_state.machine_id,
                batch_no=st.session_state.batch_no,
                input_mode="Video File",
                quality_status=status,
                total_defects=total,
                high_severity=high,
                avg_confidence=avg_conf,
                max_confidence=max_conf,
                defects_json=counts,
                is_online=True,
                snapshot_path=live_snapshot_url,
            )

            live_counts_placeholder.subheader("🧾 Live Defect Count")
            if counts:
                live_counts_placeholder.table(
                    pd.DataFrame(counts.items(), columns=["Defect", "Count"])
                )
            else:
                live_counts_placeholder.info("No defects detected in current frames.")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Defects", total)
            c2.metric("High Severity", high)
            c3.metric("Avg Confidence", f"{avg_conf * 100:.1f}%")
            c4.metric("Max Confidence", f"{max_conf * 100:.1f}%")

            if status == "PASS":
                live_status_placeholder.success(f"✅ LIVE QUALITY: PASS (Total defects: {total})")
            else:
                live_status_placeholder.error(f"❌ LIVE QUALITY: REJECT (Total defects: {total})")

            time.sleep(0.03)

        cap.release()
        st.success("✅ Video processing completed. Latest detected frame is ready to save.")

    if auto_save_latest:
        if not st.session_state.video_processed_once:
            st.warning("Please process the video first.")
        else:
            save_current_detected_video_frame()

    st.divider()
    st.subheader("💾 Save Current Video Frame")

    if st.button("📌 Save Current Video Frame"):
        if not st.session_state.video_processed_once:
            st.warning("Please process the video first.")
        else:
            save_current_detected_video_frame()

    if st.session_state.video_last_saved_orig and st.session_state.video_last_saved_ann:
        st.info("Latest saved result")
        st.write(st.session_state.video_last_saved_orig)
        st.write(st.session_state.video_last_saved_ann)