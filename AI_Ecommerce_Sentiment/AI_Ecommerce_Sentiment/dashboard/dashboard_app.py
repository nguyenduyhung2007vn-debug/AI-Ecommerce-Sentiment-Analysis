
# ============================================================
# FILE: dashboard/dashboard_app.py
# INSIGHTPULSE - AI ECOMMERCE SENTIMENT ANALYSIS
# ============================================================

import streamlit as st
import sys
import os

# ------------------------------------------------------------
# 1. THIẾT LẬP ĐƯỜNG DẪN
# ------------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# ------------------------------------------------------------
# 2. IMPORT CÁC MODULE
# ------------------------------------------------------------

from src.data_loader import load_and_cache_system_resources
import src.config as config
import engine as engine_views

# ------------------------------------------------------------
# 3. GIAO DIỆN
# ------------------------------------------------------------

st.set_page_config(
    page_title="InsightPulse - AI Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #0F172A;
    color: #FFFFFF;
}

.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 8px;
    width: 100%;
    font-weight: bold;
}

.stTextArea textarea {
    background-color: #1E293B;
    color: white;
}

div[data-testid="stMetricValue"] {
    color: #06B6D4;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 4. TẢI MÔ HÌNH VÀ DỮ LIỆU
# ------------------------------------------------------------

try:
    with st.spinner("Đang tải mô hình AI và dữ liệu..."):

        ai_engine, df_matrix, precomputed_metrics = (
            load_and_cache_system_resources()
        )

except Exception as e:

    st.error("Không thể tải tài nguyên hệ thống.")

    st.exception(e)

    st.warning(
        "Kiểm tra requirements.txt, "
        "ai_sentiment_model.pkl và du_lieu_24_cols.csv."
    )

    st.stop()


# ------------------------------------------------------------
# 5. ĐIỀU HƯỚNG DASHBOARD
# ------------------------------------------------------------

PAGE_OPTIONS = [
    "💻 Real-time Prediction Engine (Dự báo đa phương thức)",
    "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)",
    "🎯 Aspect-Based Sentiment Analysis (Phân tích khía cạnh ABSA)",
    "📈 Business Intelligence (Phân tích kinh doanh)"
]

page_selection = st.sidebar.selectbox(
    "📌 CHỌN CHỨC NĂNG",
    PAGE_OPTIONS
)

# ------------------------------------------------------------
# 6. KẾT XUẤT TRANG
# ------------------------------------------------------------

try:
    engine_views.render_selected_page(
        page_selection,
        ai_engine,
        df_matrix,
        precomputed_metrics
    )

except Exception as e:
    st.error("Lỗi khi kết xuất dashboard.")
    st.exception(e)
