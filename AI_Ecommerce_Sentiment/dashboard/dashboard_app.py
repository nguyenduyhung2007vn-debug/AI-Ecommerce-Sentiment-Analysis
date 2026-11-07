# =================================================================
# FILE ĐÃ CHUẨN HÓA ĐƯỜNG DẪN TUYỆT ĐỐI: dashboard/dashboard_app.py
# Đường dẫn lưu trữ trên GitHub: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# --- GIẢI PHÁP TRIỆT ĐỂ: ÉP TẤT CẢ CÁC CẤP THƯ MỤC VÀO HỆ THỐNG ĐỂ PYTHON KHÔNG BỊ MẤT DẤU ---
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)  # Thư mục dashboard
parent_dir = os.path.dirname(current_dir)         # Thư mục AI_Ecommerce_Sentiment
grandparent_dir = os.path.dirname(parent_dir)     # Thư mục gốc ngoài cùng hệ thống

# Thêm tất cả các đường dẫn cha và con vào sys.path
for path in [current_dir, parent_dir, grandparent_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Thêm trực tiếp thư mục src vào tầm quét
src_path = os.path.join(parent_dir, 'src')
if os.path.exists(src_path) and src_path not in sys.path:
    sys.path.insert(0, src_path)

# Nạp tài nguyên hệ thống từ RAM sạch
from src.data_loader import load_binary_model, load_and_preprocess_dataframe
import src.config as config
import engine as engine_views  # Gọi trực tiếp bộ điều phối cùng cấp

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

# Kết xuất nội dung động tức thì thông qua bộ lõi Engine
engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)
