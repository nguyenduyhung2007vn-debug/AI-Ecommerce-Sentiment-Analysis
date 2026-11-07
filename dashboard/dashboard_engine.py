import streamlit as st
import dashboard.pages.prediction as p1
import dashboard.pages.business_insights as p2
import dashboard.pages.aspects_features as p3_to_p20

def render_selected_page(selected_page_name, ai_model, df_data, precomputed_metrics):
    """Điều phối nội dung và truyền bộ số liệu precomputed_metrics"""
    if selected_page_name == "💻 Real-time Prediction Engine (Dự báo sắc thái)":
        p1.render_page_one_prediction(ai_model)
    elif selected_page_name == "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)":
        p2.render_page_two_dashboard(df_data, precomputed_metrics)
    else:
        # Truyền số liệu tính sẵn cho phân hệ 18 trang lượng hóa khía cạnh
        p3_to_p20.render_dynamic_feature_page(selected_page_name, df_data, precomputed_metrics)
