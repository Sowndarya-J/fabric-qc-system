import os
from pathlib import Path
import pandas as pd
import streamlit as st

st.title("📊 Model Performance Metrics")

# -----------------------------
# DARK PREMIUM STYLE
# -----------------------------
st.markdown("""
<style>
.metric-shell {
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid #374151;
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    margin-bottom: 10px;
}

.metric-label {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 8px;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #f9fafb;
}

.panel {
    padding: 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid #374151;
    margin-bottom: 14px;
}

.panel-title {
    font-size: 20px;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 8px;
}

.panel-text {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.7;
}

.info-box {
    padding: 14px;
    border-radius: 14px;
    background: #111827;
    border: 1px solid #374151;
    color: #e5e7eb;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AUTH CHECK
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.warning("Please Login first (Go to Login page).")
    st.stop()

# -----------------------------
# FIND RESULTS.CSV
# -----------------------------
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

st.markdown("""
<div class="panel">
    <div class="panel-title">YOLO Training Summary</div>
    <div class="panel-text">
        This page shows the final performance of your trained model using values from <b>results.csv</b>.
        Metrics like Precision, Recall, mAP@50 and mAP@50-95 help evaluate how well your fabric defect model performs.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("results.csv found:", results_path is not None)

if results_path is None:
    st.info("📌 Put your training results.csv inside the project root folder (same level as Home.py).")

    with st.expander("📂 View available files in current folder", expanded=False):
        try:
            files_here = sorted(os.listdir("."))
            st.code("\n".join(files_here))
        except Exception as e:
            st.error(f"Could not list files: {e}")

    st.stop()

# -----------------------------
# LOAD CSV
# -----------------------------
try:
    metrics_df = pd.read_csv(results_path)
except Exception as e:
    st.error(f"Failed to read {results_path}: {e}")
    st.stop()

if metrics_df.empty:
    st.error("results.csv is empty.")
    st.stop()

last_row = metrics_df.iloc[-1]

# -----------------------------
# PICK METRICS
# -----------------------------
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

# -----------------------------
# METRIC CARDS
# -----------------------------
st.subheader("✅ Final Model Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-shell">
            <div class="metric-label">Precision</div>
            <div class="metric-number">{precision:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-shell">
            <div class="metric-label">Recall</div>
            <div class="metric-number">{recall:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-shell">
            <div class="metric-label">mAP@50</div>
            <div class="metric-number">{map50:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-shell">
            <div class="metric-label">mAP@50-95</div>
            <div class="metric-number">{map5095:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# QUICK PERFORMANCE NOTE
# -----------------------------
st.subheader("🧠 Performance Interpretation")

def performance_label(value):
    if value >= 0.85:
        return "Excellent"
    elif value >= 0.70:
        return "Good"
    elif value >= 0.50:
        return "Moderate"
    return "Needs Improvement"

note_df = pd.DataFrame({
    "Metric": ["Precision", "Recall", "mAP@50", "mAP@50-95"],
    "Value": [precision, recall, map50, map5095],
    "Status": [
        performance_label(precision),
        performance_label(recall),
        performance_label(map50),
        performance_label(map5095),
    ]
})

st.dataframe(note_df, use_container_width=True)

# -----------------------------
# TRAINING CURVES
# -----------------------------
st.subheader("📈 Training Curves")

def try_line_chart(label, candidates):
    for col in candidates:
        if col in metrics_df.columns:
            st.markdown(
                f"""
                <div class="info-box">
                    <b>{label}</b><br>
                    Column used: <code>{col}</code>
                </div>
                """,
                unsafe_allow_html=True
            )
            chart_series = metrics_df[col]
            st.line_chart(chart_series)
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

# -----------------------------
# FULL TABLE
# -----------------------------
st.subheader("📄 Full Training Results")

with st.expander("Show full results.csv", expanded=False):
    st.dataframe(metrics_df, use_container_width=True)

st.caption(f"Using file: {results_path}")
