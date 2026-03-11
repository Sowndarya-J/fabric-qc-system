import os
import json
import sqlite3
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
import streamlit as st

USERS_FILE = "users.json"
DB_PATH = "fabric_inspections.db"
SAVE_DIR = Path("saved_inspections")
SAVE_DIR.mkdir(exist_ok=True)


# ---------- USERS ----------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2)


def check_login(username: str, password: str) -> bool:
    users = load_users()
    return username in users and users[username]["password"] == password


def get_role(username: str) -> str:
    users = load_users()
    return users[username]["role"]


# ---------- MODEL ----------
@st.cache_resource
def get_model():
    from ultralytics import YOLO
    return YOLO("best.pt")


# ---------- DATABASE ----------
def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT,
        user TEXT,
        source TEXT,
        total_defects INTEGER,
        high_severity INTEGER,
        quality_status TEXT,
        orig_path TEXT,
        ann_path TEXT,
        defects_json TEXT
    )
    """)
    con.commit()
    con.close()


def insert_inspection(dt, user, source, total, high, status, orig_path, ann_path, defects_json):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    INSERT INTO inspections
    (dt, user, source, total_defects, high_severity, quality_status, orig_path, ann_path, defects_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (dt, user, source, total, high, status, orig_path, ann_path, defects_json))
    con.commit()
    con.close()


def read_inspections(limit=300):
    import pandas as pd
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


# ---------- SAVE IMAGES ----------
def save_images(original_pil: Image.Image, annotated_bgr: np.ndarray, prefix: str):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{prefix}_{ts}"

    original_path = SAVE_DIR / f"{base}_original.jpg"
    annotated_path = SAVE_DIR / f"{base}_annotated.jpg"

    original_pil.save(original_path)
    cv2.imwrite(str(annotated_path), annotated_bgr)

    return str(original_path), str(annotated_path)


# ---------- HEATMAP ----------
def build_heatmap(img_shape, boxes_xyxy):
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


# ---------- EMAIL ----------
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
