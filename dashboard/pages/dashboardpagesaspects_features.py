import streamlit as st

def render_dynamic_feature_page(page_name, df_source):
    st.title(f"🔍 Phân hệ lượng hóa chi tiết thuộc tính: {page_name}") # 🔍 [Feature 1]
    st.write(f"Hệ thống khai phá tri thức toán học kinh doanh trích xuất tự động chỉ số của đặc trưng thuộc nhóm {page_name}.") # 🔍 [Feature 2]
    st.write("---") # 🔍 [Feature 3]
    total_rows = len(df_source)
    mean_len_char = df_source['review_len_char'].mean()
    mean_len_word = df_source['review_len_word'].mean()

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Tổng số lượng mẫu dữ liệu quét", f"{total_rows} mẫu") # 🔍 [Feature 4]
    with col2: st.metric("Độ dài ký tự trung bình văn bản thô", f"{mean_len_char:.1f} ký tự") # 🔍 [Feature 5]
    with col3: st.metric("Số từ trung bình trích xuất", f"{mean_len_word:.1f} từ") # 🔍 [Feature 6]
    st.write("---") # 🔍 [Feature 7]
    st.markdown(f"**Chỉ số đo lường hiệu năng trải nghiệm khách hàng thời gian thực:** {df_source['as_content'].mean()*50:.1f} / 100 điểm") # 🔍 [Feature 8]
    st.progress(float(df_source['as_content'].mean() / 2.0))
