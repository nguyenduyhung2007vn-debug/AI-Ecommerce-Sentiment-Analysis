# =================================================================
# FILE ĐÃ SỬA LỖI THIẾU THƯ VIỆN PANDAS: dashboard/pages/business_insights.py
# Đường dẫn lưu trữ trên GitHub: dashboard/pages/business_insights.py
# =================================================================
import streamlit as st
import pandas as pd  # ĐÃ BỔ SUNG KHAI BÁO BẮT BUỘC CHỐNG LỖI NAMEERROR BIẾN PD

def render_page_two_dashboard(metrics):
    st.title("📊 Executive Business Intelligence Dashboard")
    st.write("---")
    
    # Lượng hóa chỉ số thực tế 100% dựa trên tệp dữ liệu processed nạp từ RAM
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("TOTAL FEEDBACK", f"{metrics['total_rows']} mẫu")
    with c2: st.metric("SENTIMENT SCORE (POSITIVE)", f"{metrics['pos_ratio']:.1f}%")
    with c3: st.metric("ACTIVE ISSUES (NEGATIVE)", f"{metrics['neg_count']} sự cố")
    
    st.write("---")
    st.subheader("Biểu đồ tỷ lệ phân phối cảm xúc dòng khách hàng thực tế")
    
    # Khởi tạo ma trận bảng đồ thị đồng bộ
    chart_data = pd.DataFrame({
        'Tỷ lệ %': [metrics['neg_ratio'], metrics['neu_ratio'], metrics['pos_ratio']]
    }, index=['Tiêu cực', 'Trung lập', 'Tích cực'])
    
    st.bar_chart(chart_data)
