# =================================================================
# FILE ĐÃ SỬA LỖI ĐƯỜNG DẪN MODULE: dashboard/dashboard_app.py
# Đường dẫn lưu trữ trên GitHub: dashboard/dashboard_app.py
# =================================================================
import streamlit as st
import sys
import os

# --- GIẢI PHÁP ĐỒNG BỘ TOÀN CỤC: ĐƯA CẢ THƯ MỤC GỐC VÀ THƯ MỤC DASHBOARD VÀO LUỒNG TÌM KIẾM ---
# Đoạn code này giúp Python tìm thấy cả thư mục 'src' bên ngoài và file 'engine.py' bên trong
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)  # Tìm kiếm hướng ra ngoài (cho thư mục src)
sys.path.append(current_dir) # Tìm kiếm hướng nội bộ (cho file engine.py và folder pages)

from src.data_loader import load_and_cache_system_resources
import src.config as config

# Lúc này hệ thống đã nhận diện được file engine và folder pages nội bộ
import engine as engine_views  
import pages.prediction as p1
import pages.business_insights as p2
import pages.aspects_features as p3_to_p20

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
    ai_engine, df_matrix, precomputed_metrics = load_and_cache_system_resources()
except Exception as e:
    st.error(f"Hệ thống gặp sự cố tải tài nguyên pkl/csv tốc độ cao. Chi tiết lỗi: {e}")

# Lập trình thanh Menu điều hướng danh mục 20 trang hiển thị độc lập tại Sidebar trái
st.sidebar.title("InsightPulse 📊")
st.sidebar.subheader("Hệ thống Quản trị AI - DUE")
st.sidebar.markdown("---")
page_selection = st.sidebar.radio("Chọn trang chức năng hệ thống (20 Trang):", list(config.PAGES_DICTIONARY.values()))

# Kết xuất nội dung động tức thì thông qua bộ lõi Engine
engine_views.render_selected_page(page_selection, ai_engine, df_matrix, precomputed_metrics)

