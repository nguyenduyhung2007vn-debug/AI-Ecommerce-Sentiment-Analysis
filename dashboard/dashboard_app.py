# =================================================================
# FILE ĐÃ TỐI ƯU TỐC ĐỘ: dashboard/app.py
# ĐỒNG BỘ LUỒNG GỌI TÀI NGUYÊN TỐC ĐỘ CAO QUA CORE ENGINE
# =================================================================
import streamlit as st
import src.config as config
from src.data_loader import load_and_cache_system_resources  # Gọi hàm hợp nhất tốc độ cao
import dashboard.engine as engine_views

# Khởi tạo cấu hình giao diện nền tối Tech Dashboard diện rộng (Wide Layout)
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #FFFFFF; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1E293B; color: white; }
    div[data-testid="stMetricValue"] { color: #06B6D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    # Kích hoạt nạp bộ não AI và ma trận dữ liệu trực tiếp từ thanh RAM máy chủ đám mây
    ai_engine, df_matrix = load_and_cache_system_resources()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv tốc độ cao. Chi tiết lỗi: {e}")

# Lập trình thanh Menu điều hướng danh mục 20 trang hiển thị độc lập tại Sidebar trái
st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Chọn trang chức năng hệ thống (20 Trang):", list(config.PAGES_DICTIONARY.values()))

# Kết xuất nội dung động tức thì thông qua bộ lõi Engine
engine_views.render_selected_page(page_selection, ai_engine, df_matrix)
