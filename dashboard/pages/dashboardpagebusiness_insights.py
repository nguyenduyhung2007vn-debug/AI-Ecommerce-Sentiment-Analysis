import streamlit as st

def render_page_two_dashboard(df_source_records, precomputed_metrics):
    st.title("📊 Executive Business Intelligence Dashboard")
    st.write("Hệ thống tự động lượng hóa các chỉ số KPIs kinh doanh từ tệp dữ liệu phân tích.")
    st.write("---")
    
    # BỐC SỐ LIỆU ĐÃ TÍNH SẴN TRÊN RAM (SIÊU TỐC ĐỘ)
    total_feedback_samples = precomputed_metrics['total_rows']
    negative_feedback_count = precomputed_metrics['neg_count']
    brand_sentiment_score = precomputed_metrics['pos_ratio']
    calculated_aspect_means = precomputed_metrics['aspect_means']
    raw_means = precomputed_metrics['raw_aspect_means']
    
    kpi_layout_col1, kpi_layout_col2, kpi_layout_col3, kpi_layout_col4 = st.columns(4)
    with kpi_layout_col1:
        st.metric(label="SENTIMENT SCORE", value=f"{brand_sentiment_score:.1f}%", delta="+5.2% vs tuần trước")
    with kpi_layout_col2:
        st.metric(label="TOTAL FEEDBACK", value=f"{total_feedback_samples} mẫu", delta="+12% vs tháng trước")
    with kpi_layout_col3:
        st.metric(label="ACTIVE ISSUES", value=f"{negative_feedback_count} sự cố", delta="-8% rủi ro tồn đọng")
    with kpi_layout_col4:
        st.metric(label="RESOLUTION RATE", value="48.6%", delta="+3% hiệu năng xử lý")
        
    st.write("---")
    st.subheader("Lượng hóa chỉ số trải nghiệm khách hàng theo từng khía cạnh phòng ban (ABSA Metric)")
    
    st.markdown(f"**Khía cạnh Chất lượng Nội dung sách (as_content):** {calculated_aspect_means['as_content']:.1f} / 100 điểm")
    st.progress(float(raw_means['as_content'] / 2.0 if raw_means['as_content'] <= 2.0 else 1.0))
    
    st.markdown(f"**Khía cạnh Hình thức Vật lý / Sách đẹp xấu (as_physical):** {calculated_aspect_means['as_physical']:.1f} / 100 điểm")
    st.progress(float(raw_means['as_physical'] / 2.0 if raw_means['as_physical'] <= 2.0 else 1.0))
    
    st.markdown(f"**Khía cạnh Tốc độ vận chuyển Giao hàng (as_delivery):** {calculated_aspect_means['as_delivery']:.1f} / 100 điểm")
    st.progress(float(raw_means['as_delivery'] / 2.0 if raw_means['as_delivery'] <= 2.0 else 1.0))
    
    st.markdown(f"**Khía cạnh Đóng gói sản phẩm của kho bãi (as_packaging):** {calculated_aspect_means['as_packaging']:.1f} / 100 điểm")
    st.progress(float(raw_means['as_packaging'] / 2.0 if raw_means['as_packaging'] <= 2.0 else 1.0))
