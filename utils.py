import os
import io
import json
import math
import wave
import base64
import sqlite3
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime
from uuid import uuid4

try:
    import cv2
except Exception:
    cv2 = None

import numpy as np
from PIL import Image
import pandas as pd
import qrcode
import streamlit as st

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

USERS_FILE = "users.json"
DB_PATH = "fabric_inspections.db"
SAVE_DIR = Path("saved_inspections")
SAVE_DIR.mkdir(exist_ok=True)


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2)


def check_login(username: str, password: str) -> bool:
    """Check if username and password are valid."""
    users = load_users()
    if username in users and users[username].get("password") == password:
        return True
    return False


def get_role(username: str) -> str:
    """Get the role of a user."""
    users = load_users()
    if username in users:
        return users[username].get("role", "user")
    return "user"


@st.cache_resource
def get_model():
    """Load YOLO model. Uses best.pt if available, falls back to yolov8n.pt"""
    try:
        from ultralytics import YOLO
        
        # Try loading custom trained model
        if os.path.exists("best.pt"):
            print("Loading custom model: best.pt")
            return YOLO("best.pt")
        
        # Fallback to pre-trained model
        print("best.pt not found, loading pre-trained yolov8n.pt")
        if os.path.exists("yolov8n.pt"):
            return YOLO("yolov8n.pt")
        
        # Download if neither exists
        print("Downloading yolov8n model...")
        return YOLO("yolov8n.pt")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        raise Exception(f"Failed to load YOLO model: {str(e)}")



def _column_exists(cur, table_name, column_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cur.fetchall()]
    return column_name in cols


def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inspection_id TEXT,
        dt TEXT,
        user TEXT,
        source TEXT,
        batch_no TEXT,
        fabric_type TEXT,
        shift TEXT,
        machine_id TEXT,
        total_defects INTEGER,
        high_severity INTEGER,
        quality_status TEXT,
        severity_score REAL,
        severity_label TEXT,
        recommendations TEXT,
        avg_confidence REAL,
        max_confidence REAL,
        orig_path TEXT,
        ann_path TEXT,
        defects_json TEXT
    )
    """)

    new_cols = {
        "inspection_id": "TEXT",
        "batch_no": "TEXT",
        "fabric_type": "TEXT",
        "shift": "TEXT",
        "machine_id": "TEXT",
        "severity_score": "REAL",
        "severity_label": "TEXT",
        "recommendations": "TEXT",
        "avg_confidence": "REAL",
        "max_confidence": "REAL",
        "defects_json": "TEXT",
        "source": "TEXT",
    }

    for col, dtype in new_cols.items():
        if not _column_exists(cur, "inspections", col):
            cur.execute(f"ALTER TABLE inspections ADD COLUMN {col} {dtype}")

    con.commit()
    con.close()


def next_inspection_id():
    now = datetime.now().strftime("%Y%m%d")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM inspections WHERE inspection_id LIKE ?", (f"FQC-{now}-%",))
    count = cur.fetchone()[0] + 1
    con.close()
    return f"FQC-{now}-{count:03d}"


def insert_inspection(
    inspection_id,
    dt,
    user,
    source,
    batch_no,
    fabric_type,
    shift,
    machine_id,
    total,
    high,
    status,
    severity_score,
    severity_label,
    recommendations,
    avg_confidence,
    max_confidence,
    orig_path,
    ann_path,
    defects_json
):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    INSERT INTO inspections (
        inspection_id, dt, user, source, batch_no, fabric_type, shift, machine_id,
        total_defects, high_severity, quality_status, severity_score, severity_label,
        recommendations, avg_confidence, max_confidence, orig_path, ann_path, defects_json
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inspection_id, dt, user, source, batch_no, fabric_type, shift, machine_id,
        total, high, status, severity_score, severity_label, recommendations,
        avg_confidence, max_confidence, orig_path, ann_path, defects_json
    ))
    con.commit()
    con.close()


def read_inspections(limit=500):
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT * FROM inspections ORDER BY id DESC LIMIT {int(limit)}",
        con
    )
    con.close()
    return df


def delete_inspection(row_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM inspections WHERE id=?", (row_id,))
    con.commit()
    con.close()


def save_images(original_pil: Image.Image, annotated_bgr: np.ndarray, prefix: str):
    if cv2 is None:
        raise RuntimeError("OpenCV is not available on this system.")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{prefix}_{ts}"

    original_path = SAVE_DIR / f"{base}_original.jpg"
    annotated_path = SAVE_DIR / f"{base}_annotated.jpg"

    original_pil.save(original_path)
    cv2.imwrite(str(annotated_path), annotated_bgr)

    return str(original_path), str(annotated_path)


def build_heatmap(img_shape, boxes_xyxy):
    if cv2 is None:
        raise RuntimeError("OpenCV is not available on this system.")

    h, w = img_shape[:2]
    heat = np.zeros((h, w), dtype=np.float32)

    for (x1, y1, x2, y2) in boxes_xyxy:
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)
        if x2 > x1 and y2 > y1:
            heat[y1:y2, x1:x2] += 1.0

    heat = cv2.GaussianBlur(heat, (0, 0), sigmaX=25, sigmaY=25)
    heat_norm = cv2.normalize(heat, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heat_color = cv2.applyColorMap(heat_norm, cv2.COLORMAP_JET)
    return heat_color


def calculate_severity(total_defects, high_defects, avg_conf):
    score = min(100, (total_defects * 12) + (high_defects * 20) + (avg_conf * 20))
    if score < 30:
        label = "Good"
    elif score < 60:
        label = "Moderate"
    else:
        label = "Poor"
    return round(score, 2), label


def defect_recommendations(defect_count: dict):
    recs = []
    defect_keys = [k.lower() for k in defect_count.keys()]

    if any("oil" in k or "stain" in k for k in defect_keys):
        recs.append("Check machine oil leakage and clean fabric path.")
    if any("hole" in k for k in defect_keys):
        recs.append("Inspect needle damage and mechanical puncture points.")
    if any("crack" in k for k in defect_keys):
        recs.append("Check fabric tension and handling process.")
    if any("knot" in k for k in defect_keys):
        recs.append("Inspect yarn joining and threading quality.")
    if not recs:
        recs.append("No action needed. Fabric quality is acceptable.")

    return " | ".join(recs)


def play_alert_sound(level: str = "high"):
    if level == "medium":
        volume = 0.55
        repeats = 2
        duration = 0.20
        gap = 0.06
    else:
        volume = 0.85
        repeats = 3
        duration = 0.22
        gap = 0.05

    sr = 22050
    freq = 1200.0

    def tone_bytes(seconds: float, vol: float):
        n = int(sr * seconds)
        audio = bytearray()
        for i in range(n):
            sample = int(vol * 32767 * math.sin(2 * math.pi * freq * i / sr))
            audio += int(sample).to_bytes(2, byteorder="little", signed=True)
        return audio

    def silence_bytes(seconds: float):
        n = int(sr * seconds)
        return bytearray(b"\x00\x00" * n)

    full_audio = bytearray()
    for i in range(repeats):
        full_audio += tone_bytes(duration, volume)
        if i < repeats - 1:
            full_audio += silence_bytes(gap)

    bio = io.BytesIO()
    with wave.open(bio, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(full_audio))

    b64 = base64.b64encode(bio.getvalue()).decode()
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True
    )


def send_email_with_pdf(sender_email: str, app_password: str, receiver_email: str,
                        subject: str, body: str, pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(pdf_path)
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)


def create_qr_image(data: str, out_path="inspection_qr.png"):
    img = qrcode.make(data)
    img.save(out_path)
    return out_path


def create_inspection_pdf(
    pdf_path,
    inspection_id,
    dt,
    inspector,
    source,
    batch_no,
    fabric_type,
    shift,
    machine_id,
    confidence_threshold,
    quality_status,
    severity_score,
    severity_label,
    recommendations,
    defect_df,
    annotated_bgr
):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    elements.append(Paragraph("Fabric Defect Detection Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Inspection ID: {inspection_id}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {dt}", styles["Normal"]))
    elements.append(Paragraph(f"Inspector: {inspector}", styles["Normal"]))
    elements.append(Paragraph(f"Source: {source}", styles["Normal"]))
    elements.append(Paragraph(f"Batch No: {batch_no}", styles["Normal"]))
    elements.append(Paragraph(f"Fabric Type: {fabric_type}", styles["Normal"]))
    elements.append(Paragraph(f"Shift: {shift}", styles["Normal"]))
    elements.append(Paragraph(f"Machine ID: {machine_id}", styles["Normal"]))
    elements.append(Paragraph(f"Confidence Threshold: {confidence_threshold}", styles["Normal"]))
    elements.append(Paragraph(f"Quality Status: {quality_status}", styles["Normal"]))
    elements.append(Paragraph(f"Severity Score: {severity_score} ({severity_label})", styles["Normal"]))
    elements.append(Paragraph(f"Recommendations: {recommendations}", styles["Normal"]))
    elements.append(Spacer(1, 0.25 * inch))

    table_data = [["Defect Type", "Confidence (%)", "Severity"]] + defect_df.values.tolist()
    table = Table(table_data)
    table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])
    elements.append(table)
    elements.append(Spacer(1, 0.25 * inch))

    temp_img = f"annotated_{uuid4().hex[:8]}.jpg"
    Image.fromarray(annotated_bgr).save(temp_img)
    elements.append(RLImage(temp_img, width=4 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.25 * inch))

    qr_path = create_qr_image(inspection_id)
    elements.append(Paragraph("Inspection QR", styles["Heading3"]))
    elements.append(RLImage(qr_path, width=1.4 * inch, height=1.4 * inch))

    doc.build(elements)

    if os.path.exists(temp_img):
        os.remove(temp_img)
    if os.path.exists(qr_path):
        os.remove(qr_path)


def create_dashboard_summary_pdf(filtered_df: pd.DataFrame, pdf_path="dashboard_summary.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    elements.append(Paragraph("Fabric QC Dashboard Summary", styles["Heading1"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    total_inspections = len(filtered_df)
    total_defects = int(filtered_df["total_defects"].sum()) if "total_defects" in filtered_df.columns else 0
    reject_count = int((filtered_df["quality_status"] == "REJECT").sum()) if "quality_status" in filtered_df.columns else 0

    summary_table = Table([
        ["Metric", "Value"],
        ["Total Inspections", str(total_inspections)],
        ["Total Defects", str(total_defects)],
        ["Reject Count", str(reject_count)],
    ])
    summary_table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25 * inch))

    preview_cols = [c for c in ["inspection_id", "dt", "user", "source", "batch_no", "fabric_type", "quality_status"] if c in filtered_df.columns]
    preview_df = filtered_df[preview_cols].head(15)

    preview_table = Table([preview_cols] + preview_df.astype(str).values.tolist())
    preview_table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ])
    elements.append(Paragraph("Top Records Preview", styles["Heading2"]))
    elements.append(preview_table)

    doc.build(elements)
    return pdf_path
