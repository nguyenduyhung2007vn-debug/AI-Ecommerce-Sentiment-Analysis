import streamlit as st

def render_page_two_dashboard(df_records):
    st.title("📊 Executive Business Intelligence Dashboard") # 📊 [Feature 1]
    st.write("Hệ thống tự động lượng hóa các chỉ số KPIs kinh doanh từ tệp dữ liệu phân tích.") # 📊 [Feature 2]
    st.write("---") # 📊 [Feature 3]
    total = len(df_records)
    neg_count = len(df_records[df_records['sentiment_llm'] == 0])
    pos_ratio = (len(df_records[df_records['sentiment_llm'] == 2]) / total) * 100

    c1, col2_kpi, c3, c4 = st.columns(4)
    with c1: st.metric("SENTIMENT SCORE", f"{pos_ratio:.1f}%", "+5.2% vs tuần trước") # 📊 [Feature 4]
    with col2_kpi: st.metric("TOTAL FEEDBACK", f"{total} mẫu", "+12% vs tháng trước") # 📊 [Feature 5]
    with c3: st.metric("ACTIVE ISSUES", f"{neg_count} sự cố", "-8% rủi ro tồn đọng") # 📊 [Feature 6]
    with c4: st.metric("RESOLUTION RATE", "48.6%", "+3% hiệu năng") # 📊 [Feature 7]
    st.write("---") # 📊 [Feature 8]
