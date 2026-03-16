import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from PIL import Image

from theme import apply_dark_theme
from utils import (
    build_heatmap,
    calculate_severity,
    create_inspection_pdf,
    defect_recommendations,
    get_model,
    init_db,
    insert_inspection,
    next_inspection_id,
    play_alert_sound,
    save_images,
    send_email_with_pdf,
)

try:
    import cv2
except Exception:
    cv2 = None

apply_dark_theme()

st.title("Image Upload Detection")
init_db()

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

if cv2 is None:
    st.error("OpenCV is not available.")
    st.stop()

confidence_threshold = st.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.40,
    step=0.05,
)

st.write(f"Selected Confidence Threshold: {confidence_threshold:.2f}")

uploaded_file = st.file_uploader("Upload Fabric Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=500)

    if st.button("Detect", use_container_width=True):
        model = get_model()
        results = model(image, conf=confidence_threshold)
        result = results[0]
        result_image = result.plot()

        st.image(result_image, caption="Detected Defects", width=500)

        boxes = result.boxes
        names = result.names

        defect_data = []
        defect_count = {}
        confidences = []
        total_defects = 0
        quality_status = "PASS"
        high_defects = 0

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                confidences.append(conf)
                defect_name = names[cls_id]

                if conf > 0.80:
                    severity = "High"
                elif conf > 0.60:
                    severity = "Medium"
                else:
                    severity = "Low"

                total_defects += 1
                defect_count[defect_name] = defect_count.get(defect_name, 0) + 1
                defect_data.append([defect_name, round(conf * 100, 2), severity])

            df = pd.DataFrame(defect_data, columns=["Defect Type", "Confidence (%)", "Severity"])
            st.table(df)

            fig = plt.figure(figsize=(4, 4))
            plt.pie(defect_count.values(), labels=defect_count.keys(), autopct="%1.1f%%")
            plt.title("Defect Distribution")
            st.pyplot(fig)

            high_defects = sum(1 for d in defect_data if d[2] == "High")
            if high_defects > 0:
                quality_status = "REJECT"
            elif total_defects <= 2:
                quality_status = "PASS"
            else:
                quality_status = "REJECT"

            xyxy = boxes.xyxy.cpu().numpy()
            heat_color = build_heatmap(result_image.shape, xyxy)
            overlay = cv2.addWeighted(result_image, 0.7, heat_color, 0.3, 0)
            st.image(overlay, caption="Heatmap Overlay", width=500)
        else:
            df = pd.DataFrame([["No Defects", 0, "-"]], columns=["Defect Type", "Confidence (%)", "Severity"])
            st.success("No Defects Found — PERFECT FABRIC")
            defect_count = {}

        avg_conf = round(sum(confidences) / len(confidences), 4) if confidences else 0.0
        max_conf = round(max(confidences), 4) if confidences else 0.0
        severity_score, severity_label = calculate_severity(total_defects, high_defects, avg_conf)
        recommendations = defect_recommendations(defect_count)
        inspection_id = next_inspection_id()

        if quality_status == "REJECT":
            st.error("Quality Status: REJECT")
            play_alert_sound("high")
        else:
            st.success("Quality Status: PASS")

        st.markdown(
            f"""
            <div class="soft-box">
                <b>Inspection ID:</b> {inspection_id}<br>
                <b>Severity Score:</b> {severity_score} ({severity_label})<br>
                <b>Recommendations:</b> {recommendations}
            </div>
            """,
            unsafe_allow_html=True,
        )

        defects_json = json.dumps(defect_count, ensure_ascii=False)
        orig_path, ann_path = save_images(image, result_image, prefix=st.session_state.user)

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_inspection(
            inspection_id,
            dt,
            st.session_state.user,
            "image",
            "",
            "",
            "",
            "",
            total_defects,
            high_defects,
            quality_status,
            severity_score,
            severity_label,
            recommendations,
            avg_conf,
            max_conf,
            orig_path,
            ann_path,
            defects_json,
        )

        pdf_path = f"{inspection_id}_report.pdf"
        create_inspection_pdf(
            pdf_path=pdf_path,
            inspection_id=inspection_id,
            dt=dt,
            inspector=st.session_state.user,
            source="Image Upload",
            batch_no="",
            fabric_type="",
            shift="",
            machine_id="",
            confidence_threshold=confidence_threshold,
            quality_status=quality_status,
            severity_score=severity_score,
            severity_label=severity_label,
            recommendations=recommendations,
            defect_df=df,
            annotated_bgr=result_image,
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                data=f,
                file_name=pdf_path,
                mime="application/pdf",
            )

        with st.expander("Email Report", expanded=False):
            sender_email = st.text_input("Sender Gmail", value=st.secrets.get("SENDER_EMAIL", ""))
            app_password = st.text_input(
                "Gmail App Password",
                value=st.secrets.get("APP_PASSWORD", ""),
                type="password",
            )
            receiver_email = st.text_input("Receiver Email", value=st.secrets.get("RECEIVER_EMAIL", ""))

            if st.button("Send Email", use_container_width=True):
                try:
                    send_email_with_pdf(
                        sender_email=sender_email.strip(),
                        app_password=app_password.strip(),
                        receiver_email=receiver_email.strip(),
                        subject=f"Fabric Report - {inspection_id}",
                        body=(
                            f"Inspection ID: {inspection_id}\n"
                            f"Status: {quality_status}\n"
                            f"Recommendations: {recommendations}"
                        ),
                        pdf_path=pdf_path,
                    )
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"Email failed: {e}")
