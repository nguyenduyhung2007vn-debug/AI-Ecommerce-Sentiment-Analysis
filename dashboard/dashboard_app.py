import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_and_cache_system_resources
import src.config as config
import dashboard.engine as engine_views

try:
    # Nạp thêm biến precomputed_metrics chứa số liệu đã tính toán sẵn từ RAM
    ai_engine, df_matrix, precomputed_metrics = load_and_cache_system_resources()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv tốc độ cao. Chi tiết lỗi: {e}")

st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Chọn trang chức năng hệ thống (20 Trang):", list(config.PAGES_DICTIONARY.values()))

# Truyền bộ số liệu precomputed_metrics vào bộ lõi điều hướng
engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)
