# =================================================================
# FILE ĐÃ ĐỒNG BỘ CẤU TRÚC LỒNG THƯ MỤC: dashboard/dashboard_app.py
# Đường dẫn lưu trữ trên GitHub: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# --- GIẢI PHÁP ĐỒNG BỘ ĐA TẦNG: TỰ ĐỘNG QUÉT VÀ THÊM TẤT CẢ CÁC CẤP THƯ MỤC CHA VÀO LUỒNG TÌM KIẾM ---
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path) # Thư mục dashboard
parent_dir = os.path.dirname(current_dir)        # Thư mục AI_Ecommerce_Sentiment (nếu có)
grandparent_dir = os.path.dirname(parent_dir)   # Thư mục gốc ngoài cùng hệ thống

# Đưa tất cả các biến cấp độ thư mục vào hệ thống tìm kiếm ngầm của Python
sys.path.append(current_dir)
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)

# Quét sâu thêm thư mục src lồng bên trong thư mục cha của nhóm bạn
src_nested_path = os.path.join(parent_dir, 'src')
if os.path.exists(src_nested_path):
    sys.path.append(src_nested_path)

from src.data_loader import load_binary_model, load_and_preprocess_dataframe
import src.config as config
import engine as engine_views  # Lúc này hệ thống đã nhận diện được file engine cùng cấp

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    # Nạp bộ não AI và tính toán ma trận số liệu thực tế đã lưu cache
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
