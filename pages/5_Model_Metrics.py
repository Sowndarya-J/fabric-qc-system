import os
from pathlib import Path

import pandas as pd
import streamlit as st

from theme import apply_dark_theme

apply_dark_theme()

st.title("Model Performance Metrics")

if not st.session_state.get("logged_in", False):
    st.warning("Please Login first.")
    st.stop()

possible_paths = [
    Path("results.csv"),
    Path("./results.csv"),
    Path("data/results.csv"),
    Path("runs/detect/results.csv"),
    Path("runs/train/results.csv"),
]

results_path = None
for p in possible_paths:
    if p.exists():
        results_path = p
        break

st.markdown(
    """
    <div class="hero-box">
        <h3>YOLO Training Summary</h3>
        <p>
            This page shows training performance using values from results.csv,
            including Precision, Recall, mAP@50, and mAP@50-95.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("results.csv found:", results_path is not None)

if results_path is None:
    st.info("Put your training results.csv inside the project root folder.")
    with st.expander("View available files in current folder"):
        try:
            files_here = sorted(os.listdir("."))
            st.code("\n".join(files_here))
        except Exception as e:
            st.error(f"Could not list files: {e}")
    st.stop()

try:
    metrics_df = pd.read_csv(results_path)
except Exception as e:
    st.error(f"Failed to read {results_path}: {e}")
    st.stop()

if metrics_df.empty:
    st.error("results.csv is empty.")
    st.stop()

last_row = metrics_df.iloc[-1]

def pick(cols, default=0.0):
    for c in cols:
        if c in metrics_df.columns:
            try:
                return float(last_row[c])
            except Exception:
                return float(default)
    return float(default)

precision = pick(["metrics/precision(B)", "metrics/precision", "precision"])
recall = pick(["metrics/recall(B)", "metrics/recall", "recall"])
map50 = pick(["metrics/mAP50(B)", "metrics/mAP50", "mAP50"])
map5095 = pick(["metrics/mAP50-95(B)", "metrics/mAP50-95", "mAP50-95"])

st.subheader("Final Model Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Precision", f"{precision:.3f}")
c2.metric("Recall", f"{recall:.3f}")
c3.metric("mAP@50", f"{map50:.3f}")
c4.metric("mAP@50-95", f"{map5095:.3f}")

st.subheader("Performance Interpretation")

def performance_label(value: float) -> str:
    if value >= 0.85:
        return "Excellent"
    if value >= 0.70:
        return "Good"
    if value >= 0.50:
        return "Moderate"
    return "Needs Improvement"

note_df = pd.DataFrame(
    {
        "Metric": ["Precision", "Recall", "mAP@50", "mAP@50-95"],
        "Value": [precision, recall, map50, map5095],
        "Status": [
            performance_label(precision),
            performance_label(recall),
            performance_label(map50),
            performance_label(map5095),
        ],
    }
)
st.dataframe(note_df, use_container_width=True)

st.subheader("Training Curves")

def try_line_chart(label: str, candidates: list[str]) -> bool:
    for col in candidates:
        if col in metrics_df.columns:
            st.info(f"{label} → column used: {col}")
            st.line_chart(metrics_df[col])
            return True
    return False

found_any = False
found_any |= try_line_chart("Precision Curve", ["metrics/precision(B)", "metrics/precision", "precision"])
found_any |= try_line_chart("Recall Curve", ["metrics/recall(B)", "metrics/recall", "recall"])
found_any |= try_line_chart("mAP@50 Curve", ["metrics/mAP50(B)", "metrics/mAP50", "mAP50"])
found_any |= try_line_chart("mAP@50-95 Curve", ["metrics/mAP50-95(B)", "metrics/mAP50-95", "mAP50-95"])
found_any |= try_line_chart("Train Box Loss", ["train/box_loss", "box_loss"])
found_any |= try_line_chart("Train Class Loss", ["train/cls_loss", "cls_loss"])
found_any |= try_line_chart("Train DFL Loss", ["train/dfl_loss", "dfl_loss"])

if not found_any:
    st.warning("No known metric columns found. Check the full CSV below.")

with st.expander("Show full results.csv"):
    st.dataframe(metrics_df, use_container_width=True)

st.caption(f"Using file: {results_path}")
