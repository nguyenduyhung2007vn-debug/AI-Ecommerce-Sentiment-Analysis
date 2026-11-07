# =================================================================
# FILE ĐÃ ĐỒNG BỘ TỐC ĐỘ: dashboard/engine.py
# Đường dẫn lưu trữ trên GitHub: dashboard/engine.py
# =================================================================
import streamlit as st

# SỬA LỖI GỐC: XÓA CHỮ 'dashboard.' ĐỂ PYTHON TÌM FILE TRONG THƯ MỤC CÙNG CẤP PAGES
import pages.prediction as p1
import pages.business_insights as p2
import pages.aspects_features as p3_to_p20

def render_selected_page(selected_page_name, ai_model, df_data, precomputed_metrics):
    """Điều phối và kết xuất nội dung chính xác cho trang được chọn từ Sidebar"""
    if selected_page_name == "💻 Real-time Prediction Engine (Dự báo sắc thái)":
        p1.render_page_one_prediction(ai_model)
    elif selected_page_name == "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)":
        p2.render_page_two_dashboard(df_data, precomputed_metrics)
    else:
        # Các trang từ 3 đến 20 được render động qua module lượng hóa thuộc tính nâng cao
        p3_to_p20.render_dynamic_feature_page(selected_page_name, df_data, precomputed_metrics)

