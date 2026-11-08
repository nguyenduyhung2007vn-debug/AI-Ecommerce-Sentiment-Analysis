# ============================================================
# dashboard/dashboard_app.py - INSIGHTPULSE (điểm khởi chạy)
# Chạy: streamlit run dashboard/dashboard_app.py
# ============================================================
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

st.set_page_config(page_title="InsightPulse - AI Sentiment Analysis", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

from src.data_loader import load_context, read_csv_any
from dashboard.engine import build_navigation

st.markdown("""
<style>
.stButton>button {border-radius:8px; font-weight:bold;}
div[data-testid="stMetricValue"] {color:#06B6D4; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

try:
    with st.spinner("Đang tải mô hình AI và dữ liệu..."):
        ctx = load_context()
except Exception as e:
    st.error("Không thể tải tài nguyên hệ thống.")
    st.exception(e)
    st.warning("Kiểm tra requirements.txt và file ai_sentiment_model.pkl.")
    st.stop()

with st.sidebar:
    st.markdown("### 📊 InsightPulse")
    if ctx["df"] is None:
        st.warning("Chưa có du_lieu_24_cols.csv")
    else:
        st.caption(f"Dữ liệu: {ctx['source']} · {len(ctx['df']):,} dòng")
    up = st.file_uploader("Nạp CSV dữ liệu khác", type=["csv"], key="sidebar_csv")
    if up is not None and st.session_state.get("_csv_name") != up.name:
        st.session_state["uploaded_df"] = read_csv_any(up)
        st.session_state["_csv_name"] = up.name
        st.rerun()
    if "uploaded_df" in st.session_state and st.button("↩️ Dùng lại dữ liệu mặc định"):
        st.session_state.pop("uploaded_df")
        st.session_state.pop("_csv_name", None)
        st.rerun()

try:
    build_navigation(ctx).run()
except Exception as e:
    st.error("Lỗi khi kết xuất trang.")
    st.exception(e)
