# =================================================================
# FILE ĐÃ ĐỒNG BỘ ĐƯỜNG DẪN INTERN: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# Luồng ánh xạ dứt điểm bài toán ModuleNotFoundError
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path) # Thư mục dashboard
parent_dir = os.path.dirname(current_dir)        # Thư mục cha

sys.path.append(current_dir)
sys.path.append(parent_dir)

# Quét sâu thư mục gốc ngoài cùng của Git để nhận diện module src
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from src.data_loader import load_binary_model, load_and_preprocess_dataframe
import src.config as config
import engine as engine_views  # Nhận diện file engine cùng cấp phân hệ

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    ai_engine = load_binary_model()
    df_matrix, precomputed_metrics = load_and_preprocess_dataframe()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv: {e}")

st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Lựa chọn các trang chức năng:", list(config.PAGES_DICTIONARY.values()))

engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)
