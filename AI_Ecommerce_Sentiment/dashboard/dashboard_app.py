# =================================================================
# THƯ MỤC LƯU TRỮ: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# Giải quyết triệt để lỗi ModuleNotFoundError: Ép luồng tìm kiếm nhận diện thư mục gốc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_and_cache_system_resources = lambda: (load_binary_model(), load_and_preprocess_dataframe()[0], load_and_preprocess_dataframe()[1])
from src.data_loader import load_binary_model, load_and_preprocess_dataframe
import src.config as config
import dashboard.engine as engine_views

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    ai_engine, df_matrix, precomputed_metrics = load_binary_model(), load_and_preprocess_dataframe()[0], load_and_preprocess_dataframe()[1]
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên: {e}")

st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Lựa chọn các trang chức năng:", list(config.PAGES_DICTIONARY.values()))

engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)
