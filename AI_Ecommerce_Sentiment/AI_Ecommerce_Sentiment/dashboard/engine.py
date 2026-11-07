
# ============================================================
# FILE: dashboard/engine.py
# INSIGHTPULSE - PAGE CONTROLLER
# ============================================================

import streamlit as st

import pages.prediction as p1
import pages.business_insights as p2
import pages.aspects_features as p3_to_p4


def render_selected_page(
    selected_page_name,
    ai_model,
    df_data,
    precomputed_metrics
):

    if selected_page_name == (
        "💻 Real-time Prediction Engine (Dự báo đa phương thức)"
    ):

        p1.render_page_one_prediction(ai_model)

    elif selected_page_name == (
        "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)"
    ):

        p2.render_page_two_dashboard(precomputed_metrics)

    elif selected_page_name == (
        "🎯 Aspect-Based Sentiment Analysis (Phân tích khía cạnh ABSA)"
    ):

        p3_to_p4.render_aspect_analysis_page(
            precomputed_metrics
        )

    elif selected_page_name == (
        "📈 Business Intelligence (Phân tích kinh doanh)"
    ):

        p3_to_p4.render_business_intelligence_page(
            df_data
        )

    else:

        st.error(
            f"Không tìm thấy chức năng: {selected_page_name}"
        )
