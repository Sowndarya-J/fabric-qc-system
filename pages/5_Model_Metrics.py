import os
import pandas as pd
import streamlit as st

st.title("📊 Model Performance Metrics (Training)")

if not st.session_state.get("logged_in", False):
    st.warning("Please Login first (Go to Login page).")
    st.stop()

st.write("results.csv found:", os.path.exists("results.csv"))

if not os.path.exists("results.csv"):
    st.info("📌 Put your training results.csv inside the project root folder.")
    st.stop()

metrics_df = pd.read_csv("results.csv")

if metrics_df.empty:
    st.error("results.csv is empty.")
    st.stop()

last_row = metrics_df.iloc[-1]

def pick(cols, default=0.0):
    for c in cols:
        if c in metrics_df.columns:
            try:
                return float(last_row[c])
            except:
                return float(default)
    return float(default)

precision = pick(["metrics/precision(B)", "metrics/precision", "precision"])
recall = pick(["metrics/recall(B)", "metrics/recall", "recall"])
map50 = pick(["metrics/mAP50(B)", "metrics/mAP50", "mAP50"])
map5095 = pick(["metrics/mAP50-95(B)", "metrics/mAP50-95", "mAP50-95"])

st.subheader("✅ Last Epoch Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Precision", f"{precision:.3f}")
c2.metric("Recall", f"{recall:.3f}")
c3.metric("mAP@50", f"{map50:.3f}")
c4.metric("mAP@50-95", f"{map5095:.3f}")

with st.expander("📄 Show full results.csv"):
    st.dataframe(metrics_df, use_container_width=True)
