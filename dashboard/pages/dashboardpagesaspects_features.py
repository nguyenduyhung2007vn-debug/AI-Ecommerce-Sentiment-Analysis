import streamlit as st

def render_dynamic_feature_page(page_name, df_source, precomputed_metrics):
    st.title(f"🔍 Phân hệ lượng hóa chi tiết thuộc tính: {page_name}")
    st.write(f"Hệ thống khai phá tri thức toán học kinh doanh trích xuất tự động chỉ số của đặc trưng thuộc nhóm {page_name}.")
    st.write("---")
    
    # BỐC SỐ LIỆU ĐÃ TÍNH SẴN TRÊN RAM
    total_rows = precomputed_metrics['total_rows']
    mean_len_char = precomputed_metrics['mean_len_char']
    mean_len_word = precomputed_metrics['mean_len_word']
    calculated_aspect_means = precomputed_metrics['aspect_means']
    raw_means = precomputed_metrics['raw_aspect_means']
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Tổng số lượng mẫu dữ liệu quét", f"{total_rows} mẫu")
    with col2: st.metric("Độ dài ký tự trung bình văn bản thô", f"{mean_len_char:.1f} ký tự")
    with col3: st.metric("Số từ trung bình trích xuất", f"{mean_len_word:.1f} từ")
    st.write("---")
    
    st.markdown(f"**Chỉ số đo lường hiệu năng trải nghiệm khách hàng thời gian thực:** {calculated_aspect_means['as_content']:.1f} / 100 điểm")
    st.progress(float(raw_means['as_content'] / 2.0 if raw_means['as_content'] <= 2.0 else 1.0))
