import streamlit as st
import pandas as pd
from src.pipeline import convert_text_to_feature_matrix
import src.config as config

def render_page_one_prediction(ai_model_object):
    st.title("💻 Real-time Prediction Engine - Phân hệ Dự báo") # 📝 [Feature 1]
    st.write("Nhập văn bản phản hồi thô của khách hàng để kích hoạt Pipeline AI dự báo sắc thái cảm xúc.") # 📝 [Feature 2]
    st.write("---") # 📝 [Feature 3]
    input_text = st.text_area("Nhập nội dung review thô tại đây:", height=120, placeholder="Nhập câu test...") # 📝 [Feature 4]

    col1, col2 = st.columns(2)
    with col1: submit_btn = st.button("KÍCH HOẠT DỰ BÁO AI", type="primary") # 📝 [Feature 5]
    with col2: clear_btn = st.button("XÓA DỮ LIỆU") # 📝 [Feature 6]

    if submit_btn and input_text.strip() != "":
        vector = convert_text_to_feature_matrix(input_text)
        df_predict = pd.DataFrame([vector], columns=config.FEATURE_COLUMNS)
        pred = ai_model_object.predict(df_predict)
        st.write("---") # 📝 [Feature 7]
        if pred == 0: st.error("🚨 SẮC THÁI TIÊU CỰC") # 📝 [Feature 8]
        elif pred == 1: st.warning("😐 SẮC THÁI TRUNG LẬP")
        else: st.success("🎉 SẮC THÁI TÍCH CỰC")
