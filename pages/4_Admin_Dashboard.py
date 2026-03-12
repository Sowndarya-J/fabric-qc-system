import os
import json
import streamlit as st
import pandas as pd

from utils import read_inspections, delete_inspection, load_users, save_users, init_db

st.title("🛠 Admin Dashboard")

# -----------------------------
# PAGE STYLES
# -----------------------------
st.markdown("""
<style>
.metric-card {
    padding: 16px;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    margin-bottom: 8px;
}

.metric-title {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 12px;
}

.soft-note {
    padding: 12px 14px;
    border-radius: 14px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    color: #475569;
    font-size: 14px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# INIT DB
# -----------------------------
init_db()

# -----------------------------
# AUTH CHECK
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.warning("Please Login first (Go to Login page).")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("❌ Only Admin can access this page.")
    st.stop()

# -----------------------------
# USER MANAGEMENT
# -----------------------------
st.markdown('<div class="section-title">👤 User Management</div>', unsafe_allow_html=True)

USERS = load_users()

with st.expander("➕ Create New User", expanded=False):
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["operator", "admin"], index=0)

    if st.button("Create User"):
        if not new_user or not new_pass:
            st.warning("Username and password required.")
        elif new_user in USERS:
            st.error("User already exists.")
        else:
            USERS[new_user] = {"password": new_pass, "role": new_role}
            save_users(USERS)
            st.success(f"✅ Created user: {new_user} ({new_role})")
            st.rerun()

with st.expander("📋 View All Users", expanded=False):
    user_table = [{"Username": k, "Role": v["role"]} for k, v in USERS.items()]
    st.table(pd.DataFrame(user_table))

with st.expander("🗑 Delete User", expanded=False):
    if USERS:
        del_user = st.selectbox("Select user to delete", list(USERS.keys()))
        if st.button("Delete Selected User"):
            if del_user == "admin":
                st.error("You cannot delete the main admin.")
            else:
                USERS.pop(del_user, None)
                save_users(USERS)
                st.success(f"Deleted user: {del_user}")
                st.rerun()

# -----------------------------
# LOAD DATABASE
# -----------------------------
st.markdown('<div class="section-title">📦 Inspection Database</div>', unsafe_allow_html=True)

db_df = read_inspections(limit=800)

if db_df.empty:
    st.info("No inspection records yet.")
    st.stop()

db_df["dt"] = pd.to_datetime(db_df["dt"], errors="coerce")
db_df = db_df.dropna(subset=["dt"])
db_df["date"] = db_df["dt"].dt.date

if "source" not in db_df.columns:
    db_df["source"] = "unknown"

if "defects_json" not in db_df.columns:
    db_df["defects_json"] = "{}"

# -----------------------------
# SAFE DEFECT JSON PARSER
# -----------------------------
def safe_load_defects(value):
    try:
        if value is None or str(value).strip() == "":
            return {}
        return json.loads(value)
    except Exception:
        return {}

all_defects = set()
for item in db_df["defects_json"].tolist():
    d = safe_load_defects(item)
    for k in d.keys():
        all_defects.add(k)

all_defects = sorted(list(all_defects))

# -----------------------------
# SEARCH & FILTER
# -----------------------------
st.markdown('<div class="section-title">🔎 Search & Filter</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    min_date = db_df["date"].min()
    max_date = db_df["date"].max()
    date_range = st.date_input("Date range", value=(min_date, max_date))

with c2:
    users_list = ["All"] + sorted(db_df["user"].astype(str).unique().tolist())
    selected_user = st.selectbox("Operator", users_list)

with c3:
    status_list = ["All"] + sorted(db_df["quality_status"].astype(str).unique().tolist())
    selected_status = st.selectbox("Pass/Reject", status_list)

with c4:
    source_list = ["All"] + sorted(db_df["source"].astype(str).unique().tolist())
    selected_source = st.selectbox("Source", source_list)

with c5:
    defect_list = ["All"] + all_defects
    selected_defect = st.selectbox("Defect Type", defect_list)

filtered = db_df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
else:
    filtered = filtered[filtered["date"] == date_range]

if selected_user != "All":
    filtered = filtered[filtered["user"].astype(str) == selected_user]

if selected_status != "All":
    filtered = filtered[filtered["quality_status"].astype(str) == selected_status]

if selected_source != "All":
    filtered = filtered[filtered["source"].astype(str) == selected_source]

if selected_defect != "All":
    def has_defect(x):
        d = safe_load_defects(x)
        return selected_defect in d and d[selected_defect] > 0
    filtered = filtered[filtered["defects_json"].apply(has_defect)]

st.markdown(
    f'<div class="soft-note">Filtered records: <b>{len(filtered)}</b></div>',
    unsafe_allow_html=True
)

show_df = filtered.drop(columns=["date"], errors="ignore")
st.dataframe(show_df, use_container_width=True)

st.download_button(
    "⬇️ Download Filtered CSV",
    data=show_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_inspections.csv",
    mime="text/csv",
)

# -----------------------------
# PREVIEW IMAGES
# -----------------------------
st.markdown('<div class="section-title">🖼 Preview Saved Images</div>', unsafe_allow_html=True)

if len(filtered) > 0:
    ids = filtered["id"].tolist()
    selected_id = st.selectbox("Select Inspection ID to preview", ids)

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

    d1, d2 = st.columns(2)
    with d1:
        if orig_path and os.path.exists(orig_path):
            with open(orig_path, "rb") as f:
                st.download_button(
                    "Download Original",
                    data=f,
                    file_name=os.path.basename(orig_path),
                    mime="image/jpeg"
                )

    with d2:
        if ann_path and os.path.exists(ann_path):
            with open(ann_path, "rb") as f:
                st.download_button(
                    "Download Annotated",
                    data=f,
                    file_name=os.path.basename(ann_path),
                    mime="image/jpeg"
                )
else:
    st.info("No rows after filter. Adjust filters to preview images.")

# -----------------------------
# ANALYTICS DASHBOARD
# -----------------------------
st.markdown('<div class="section-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)

total_inspections = len(filtered)
total_defects = int(filtered["total_defects"].sum()) if "total_defects" in filtered.columns else 0
avg_defects = float(filtered["total_defects"].mean()) if total_inspections > 0 else 0.0
reject_count = int((filtered["quality_status"] == "REJECT").sum()) if "quality_status" in filtered.columns else 0
pass_count = int((filtered["quality_status"] == "PASS").sum()) if "quality_status" in filtered.columns else 0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Total Inspections</div><div class="metric-value">{total_inspections}</div></div>',
        unsafe_allow_html=True
    )
with m2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Total Defects</div><div class="metric-value">{total_defects}</div></div>',
        unsafe_allow_html=True
    )
with m3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Avg Defects / Fabric</div><div class="metric-value">{avg_defects:.2f}</div></div>',
        unsafe_allow_html=True
    )
with m4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Reject Count</div><div class="metric-value">{reject_count}</div></div>',
        unsafe_allow_html=True
    )

# -----------------------------
# DEFECTS PER DAY
# -----------------------------
st.subheader("📅 Defects Per Day")

if "total_defects" in filtered.columns and len(filtered) > 0:
    per_day = (
        filtered.groupby("date")["total_defects"]
        .sum()
        .reset_index()
        .sort_values("date")
    )

    per_day_display = per_day.copy()
    per_day_display.columns = ["Date", "Total Defects"]

    if len(per_day) >= 2:
        chart_df = per_day.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"])
        chart_df = chart_df.set_index("date")
        st.line_chart(chart_df["total_defects"])
    else:
        st.info("Only one date is available, so bar chart is shown instead of line chart.")
        bar_df = per_day.copy().set_index("date")
        st.bar_chart(bar_df["total_defects"])

    with st.expander("View table: Defects Per Day", expanded=False):
        st.dataframe(per_day_display, use_container_width=True)
else:
    st.info("No daily defect data available.")

# -----------------------------
# PASS VS REJECT
# -----------------------------
st.subheader("✅ PASS vs ❌ REJECT")

status_counts = pd.DataFrame({
    "Status": ["PASS", "REJECT"],
    "Count": [pass_count, reject_count]
})

st.bar_chart(status_counts.set_index("Status"))

with st.expander("View table: PASS / REJECT", expanded=False):
    st.dataframe(status_counts, use_container_width=True)

# -----------------------------
# INSPECTIONS BY SOURCE
# -----------------------------
st.subheader("📸 Inspections by Source")

if "source" in filtered.columns and len(filtered) > 0:
    by_source = filtered["source"].value_counts().reset_index()
    by_source.columns = ["Source", "Count"]

    st.bar_chart(by_source.set_index("Source"))

    with st.expander("View table: Inspections by Source", expanded=False):
        st.dataframe(by_source, use_container_width=True)
else:
    st.info("No source data available.")

# -----------------------------
# MOST COMMON DEFECT + TOP DEFECTS
# -----------------------------
st.subheader("⭐ Most Common Defect Type")

agg = {}
for item in filtered["defects_json"].tolist():
    d = safe_load_defects(item)
    for k, v in d.items():
        agg[k] = agg.get(k, 0) + int(v)

if len(agg) == 0:
    st.info("No defect type data available yet. Save some inspections first.")
else:
    most_common = max(agg.items(), key=lambda x: x[1])
    st.success(f"Most common defect: **{most_common[0]}** (Total: {most_common[1]})")

    st.subheader("📊 Top Defects (Count)")
    agg_df = pd.DataFrame(
        sorted(agg.items(), key=lambda x: x[1], reverse=True),
        columns=["Defect", "Count"]
    )

    st.bar_chart(agg_df.set_index("Defect"))

    with st.expander("View table: Top Defects", expanded=False):
        st.dataframe(agg_df, use_container_width=True)

# -----------------------------
# DELETE RECORD
# -----------------------------
st.subheader("🗑 Delete Inspection Record")
del_id = st.number_input("Enter inspection ID to delete", min_value=0, step=1)

if st.button("Delete Record"):
    if del_id > 0:
        delete_inspection(int(del_id))
        st.success(f"Deleted record ID {int(del_id)}")
        st.rerun()
    else:
        st.warning("Enter valid ID")
