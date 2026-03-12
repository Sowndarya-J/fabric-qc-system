import json
import os

import pandas as pd
import streamlit as st

from theme import apply_dark_theme
from utils import (
    create_dashboard_summary_pdf,
    delete_inspection,
    init_db,
    load_users,
    read_inspections,
    save_users,
)

apply_dark_theme()

st.title("Admin Dashboard")
init_db()

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("Only Admin can access this page.")
    st.stop()

st.subheader("User Management")
users = load_users()

with st.expander("Create New User"):
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["operator", "admin"], index=0)

    if st.button("Create User"):
        if not new_user or not new_pass:
            st.warning("Username and password required.")
        elif new_user in users:
            st.error("User already exists.")
        else:
            users[new_user] = {"password": new_pass, "role": new_role}
            save_users(users)
            st.success(f"Created user: {new_user} ({new_role})")
            st.rerun()

with st.expander("View All Users"):
    st.table(pd.DataFrame([{"Username": k, "Role": v["role"]} for k, v in users.items()]))

st.subheader("Inspection Database")
df = read_inspections(limit=1000)

if df.empty:
    st.info("No inspection records yet.")
    st.stop()

df["dt"] = pd.to_datetime(df["dt"], errors="coerce")
df = df.dropna(subset=["dt"])
df["date"] = df["dt"].dt.date

for col in [
    "source",
    "defects_json",
    "batch_no",
    "fabric_type",
    "shift",
    "machine_id",
    "inspection_id",
    "severity_score",
    "avg_confidence",
]:
    if col not in df.columns:
        df[col] = ""

def safe_load_defects(value):
    try:
        if value is None or str(value).strip() == "":
            return {}
        return json.loads(value)
    except Exception:
        return {}

all_defects = set()
for item in df["defects_json"].tolist():
    d = safe_load_defects(item)
    for k in d.keys():
        all_defects.add(k)
all_defects = sorted(list(all_defects))

st.subheader("Search & Filter")

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = st.date_input("Date range", value=(min_date, max_date))
with c2:
    selected_user = st.selectbox("Operator", ["All"] + sorted(df["user"].astype(str).unique().tolist()))
with c3:
    selected_status = st.selectbox("Pass/Reject", ["All"] + sorted(df["quality_status"].astype(str).unique().tolist()))
with c4:
    selected_source = st.selectbox("Source", ["All"] + sorted(df["source"].astype(str).unique().tolist()))
with c5:
    selected_defect = st.selectbox("Defect Type", ["All"] + all_defects)
with c6:
    batch_values = sorted([x for x in df["batch_no"].astype(str).unique().tolist() if x.strip()])
    selected_batch = st.selectbox("Batch", ["All"] + batch_values)
with c7:
    conf_filter = st.selectbox("Confidence Level", ["All", "Low (<0.5)", "Medium (0.5-0.8)", "High (>0.8)"])

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

if selected_user != "All":
    filtered = filtered[filtered["user"].astype(str) == selected_user]
if selected_status != "All":
    filtered = filtered[filtered["quality_status"].astype(str) == selected_status]
if selected_source != "All":
    filtered = filtered[filtered["source"].astype(str) == selected_source]
if selected_batch != "All":
    filtered = filtered[filtered["batch_no"].astype(str) == selected_batch]

if selected_defect != "All":
    def has_defect(x):
        d = safe_load_defects(x)
        return selected_defect in d and d[selected_defect] > 0
    filtered = filtered[filtered["defects_json"].apply(has_defect)]

if conf_filter == "Low (<0.5)":
    filtered = filtered[pd.to_numeric(filtered["avg_confidence"], errors="coerce") < 0.5]
elif conf_filter == "Medium (0.5-0.8)":
    confs = pd.to_numeric(filtered["avg_confidence"], errors="coerce")
    filtered = filtered[(confs >= 0.5) & (confs <= 0.8)]
elif conf_filter == "High (>0.8)":
    filtered = filtered[pd.to_numeric(filtered["avg_confidence"], errors="coerce") > 0.8]

st.info(f"Filtered records: {len(filtered)}")
st.dataframe(filtered.drop(columns=["date"], errors="ignore"), use_container_width=True)

st.download_button(
    "Download Filtered CSV",
    data=filtered.drop(columns=["date"], errors="ignore").to_csv(index=False).encode("utf-8"),
    file_name="filtered_inspections.csv",
    mime="text/csv",
)

pdf_path = create_dashboard_summary_pdf(filtered)
with open(pdf_path, "rb") as f:
    st.download_button("Download Dashboard PDF Summary", data=f, file_name="dashboard_summary.pdf", mime="application/pdf")

st.subheader("Preview Saved Images")
if len(filtered) > 0:
    selected_id = st.selectbox("Select Inspection ID to preview", filtered["id"].tolist())
    row = filtered[filtered["id"] == selected_id].iloc[0]
    orig_path = str(row.get("orig_path", ""))
    ann_path = str(row.get("ann_path", ""))

    cp1, cp2 = st.columns(2)
    with cp1:
        st.subheader("Original Image")
        if orig_path and os.path.exists(orig_path):
            st.image(orig_path, width=420)
        else:
            st.warning("Original image file not found.")
    with cp2:
        st.subheader("Annotated Image")
        if ann_path and os.path.exists(ann_path):
            st.image(ann_path, width=420)
        else:
            st.warning("Annotated image file not found.")

st.subheader("Analytics Dashboard")

total_inspections = len(filtered)
total_defects = int(filtered["total_defects"].sum()) if "total_defects" in filtered.columns else 0
avg_defects = float(filtered["total_defects"].mean()) if total_inspections > 0 else 0.0
reject_count = int((filtered["quality_status"] == "REJECT").sum()) if "quality_status" in filtered.columns else 0
pass_count = int((filtered["quality_status"] == "PASS").sum()) if "quality_status" in filtered.columns else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Inspections", total_inspections)
m2.metric("Total Defects", total_defects)
m3.metric("Avg Defects / Fabric", f"{avg_defects:.2f}")
m4.metric("Reject Count", reject_count)

st.subheader("Defects Per Day")
if len(filtered) > 0 and "total_defects" in filtered.columns:
    per_day = filtered.groupby("date")["total_defects"].sum().reset_index().sort_values("date")
    if len(per_day) >= 2:
        chart_df = per_day.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"])
        st.line_chart(chart_df.set_index("date")["total_defects"])
    else:
        st.info("Only one date available, showing bar chart.")
        st.bar_chart(per_day.set_index("date")["total_defects"])
    with st.expander("View table: Defects Per Day"):
        per_day.columns = ["Date", "Total Defects"]
        st.dataframe(per_day, use_container_width=True)

st.subheader("PASS vs REJECT")
status_counts = pd.DataFrame({"Status": ["PASS", "REJECT"], "Count": [pass_count, reject_count]})
st.bar_chart(status_counts.set_index("Status"))
with st.expander("View table: PASS / REJECT"):
    st.dataframe(status_counts, use_container_width=True)

st.subheader("Inspections by Source")
if len(filtered) > 0:
    by_source = filtered["source"].value_counts().reset_index()
    by_source.columns = ["Source", "Count"]
    st.bar_chart(by_source.set_index("Source"))
    with st.expander("View table: Inspections by Source"):
        st.dataframe(by_source, use_container_width=True)

st.subheader("Top Defects (Count)")
agg = {}
for item in filtered["defects_json"].tolist():
    d = safe_load_defects(item)
    for k, v in d.items():
        agg[k] = agg.get(k, 0) + int(v)

if agg:
    agg_df = pd.DataFrame(sorted(agg.items(), key=lambda x: x[1], reverse=True), columns=["Defect", "Count"])
    st.bar_chart(agg_df.set_index("Defect"))
    with st.expander("View table: Top Defects"):
        st.dataframe(agg_df, use_container_width=True)
else:
    st.info("No defect type data available.")

st.subheader("Operator Performance")
if len(filtered) > 0:
    op_df = (
        filtered.groupby("user")
        .agg(
            inspections=("id", "count"),
            rejects=("quality_status", lambda s: (s == "REJECT").sum()),
            avg_defects=("total_defects", "mean"),
        )
        .reset_index()
    )
    st.bar_chart(op_df.set_index("user")[["inspections", "rejects"]])
    with st.expander("View table: Operator Performance"):
        st.dataframe(op_df, use_container_width=True)

st.subheader("Delete Inspection Record")
del_id = st.number_input("Enter inspection ID to delete", min_value=0, step=1)
if st.button("Delete Record"):
    if del_id > 0:
        delete_inspection(int(del_id))
        st.success(f"Deleted record ID {int(del_id)}")
        st.rerun()
    else:
        st.warning("Enter valid ID")
