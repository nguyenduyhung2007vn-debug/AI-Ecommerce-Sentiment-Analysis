# Vị trí file: dashboard/pages/business_insights.py
import streamlit as st

def render_page_two_dashboard(metrics):
    st.title("📊 Executive Business Intelligence Dashboard")
    st.write("---")
    
    # THAY THẾ SỐ LIỆU GHI CỨNG BẰNG CHỈ SỐ ĐO LƯỜNG TOÁN HỌC THẬT 100% CỦA PHÂN PHỐI NHÃN
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("TOTAL FEEDBACK", f"{metrics['total_rows']} mẫu")
    with c2: st.metric("SENTIMENT SCORE (POSITIVE)", f"{metrics['pos_ratio']:.1f}%")
    with c3: st.metric("ACTIVE ISSUES (NEGATIVE)", f"{metrics['neg_count']} sự cố")
    
    st.write("---")
    st.subheader("Biểu đồ tỷ lệ phân phối cảm xúc dòng khách hàng thực tế")
    st.bar_chart(pd.DataFrame({
        'Tỷ lệ %': [metrics['neg_ratio'], metrics['neu_ratio'], metrics['pos_ratio']]
    }, index=['Tiêu cực', 'Trung lập', 'Tích cực']))
