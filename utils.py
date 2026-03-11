import os
import json
import sqlite3
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

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2)

@st.cache_resource
def get_model():
    from ultralytics import YOLO
    return YOLO("best.pt")

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
    df = pd.read_sql_query(f"SELECT * FROM inspections ORDER BY id DESC LIMIT {limit}", con)
    con.close()
    return df

def delete_inspection(row_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM inspections WHERE id=?", (row_id,))
    con.commit()
    con.close()

def save_images(original_pil: Image.Image, annotated_bgr: np.ndarray, prefix: str):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{prefix}_{ts}"
    original_path = SAVE_DIR / f"{base}_original.jpg"
    annotated_path = SAVE_DIR / f"{base}_annotated.jpg"
    original_pil.save(original_path)
    cv2.imwrite(str(annotated_path), annotated_bgr)
    return str(original_path), str(annotated_path)
