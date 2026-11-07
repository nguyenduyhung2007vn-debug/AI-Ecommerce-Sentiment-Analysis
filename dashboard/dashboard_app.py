# =================================================================
# KHỐI CODE 4: KHUNG ĐIỀU HƯỚNG SIDEBAR ĐỘNG CHO DANH MỤC 20 TRANG WEB
# Đường dẫn lưu trữ trên GitHub: dashboard/app.py
# =================================================================
import streamlit as st
import src.config as config
from src.data_loader import load_system_assets
import dashboard.engine as engine_views

# Áp dụng giao diện CSS Style nền tối Tech Dashboard đồng bộ thiết kế của nhóm
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    ai_engine, df_matrix = load_system_assets()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv: {e}")

# Lập trình thanh Menu điều hướng danh mục 20 trang hiển thị độc lập tại Sidebar trái
st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Chọn trang chức năng hệ thống (20 Trang):", list(config.PAGES_DICTIONARY.values()))

# Kích hoạt luồng xử lý render nội dung trang được lựa chọn thông qua Core Engine
engine_views.render_selected_page(page_selection, ai_engine, df_matrix)
