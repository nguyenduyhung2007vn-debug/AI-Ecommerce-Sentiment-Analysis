# =================================================================
# FILE ĐÃ SỬA DỨT ĐIỂM LỖI CÚ PHÁP: dashboard/dashboard_app.py
# Đường dẫn lưu trữ trên GitHub: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# Đường dẫn động giúp hệ thống tìm kiếm thông suốt các thư mục con
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)

# ĐÃ VÁ LỖI CÚ PHÁP: Gọi đúng hàm import sạch sẽ của Python
from src.data_loader import load_binary_model, load_and_preprocess_dataframe
import src.config as config
import engine as engine_views  # Gọi bộ lõi điều phối cùng cấp

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    # Nạp tài nguyên mô hình và tính toán ma trận số liệu thực tế từ RAM
    ai_engine = load_binary_model()
    df_matrix, precomputed_metrics = load_and_preprocess_dataframe()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv: {e}")

st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Lựa chọn các trang chức năng:", list(config.PAGES_DICTIONARY.values()))

# Truyền bộ số liệu sạch xuống cho tầng giao diện
engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)

