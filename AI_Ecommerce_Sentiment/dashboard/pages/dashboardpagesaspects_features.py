# Vị trí file: dashboard/pages/aspects_features.py
import streamlit as st
import pandas as pd

def render_aspect_analysis_page(metrics):
    st.title("🎯 Aspect-Based Sentiment Analysis (ABSA Dashboard)")
    st.write("Chỉ số đo lường hiệu năng trải nghiệm khách hàng lượng hóa theo thang điểm 100 thực tế:")
    st.write("---")
    
    scores = metrics['aspect_scores']
    for aspect, score in scores.items():
        st.markdown(f"**Bộ phận khía cạnh `{aspect}`:** {score:.1f} / 100 điểm")
        st.progress(float(score / 100.0))

def render_business_intelligence_page(df_source):
    st.title("💡 Business Intelligence & Actionable Insights")
    st.write("---")
    
    st.subheader("🚨 Top vấn đề rủi ro vận hành kinh doanh khẩn cấp cần khắc phục:")
    st.markdown("""
    1. **Hành vi Đóng gói (`as_packaging`):** Khách hàng phản hồi từ khóa tiêu cực mạnh liên quan đến móp hộp, bể gáy sách vật lý.
    2. **Vận chuyển Logistics (`as_delivery`):** Điểm nghẽn ngâm hàng, bưu tá giao trễ hẹn xuất hiện nhiều vào các mùa cao điểm chiến dịch.
    """)
    st.subheader("🛠️ Đề xuất giải pháp hành động cải tiến vận hành quản trị:")
    st.info("Kiến nghị siết chặt quy trình bọc chống sốc màng co chống va đập tại kho bãi và tối ưu hóa điều phối shipper tuyến.")
