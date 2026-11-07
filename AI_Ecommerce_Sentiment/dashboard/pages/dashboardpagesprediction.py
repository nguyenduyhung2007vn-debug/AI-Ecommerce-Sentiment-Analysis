# Vị trí file: dashboard/pages/prediction.py
import streamlit as st
import pandas as pd
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
import os
from src.pipeline import convert_text_to_feature_matrix
import src.config as config

def transcribe_voice(video_path):
    r = sr.Recognizer()
    try:
        audio = AudioSegment.from_file(video_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            wav_p = tmp.name
        with sr.AudioFile(wav_p) as src:
            audio_data = r.record(src)
            return r.recognize_google(audio_data, language="vi-VN")
    except Exception:
        return ""

def render_page_one_prediction(ai_model_object):
    st.title("💻 Real-time Prediction Engine")
    input_mode = st.radio("Đầu vào dữ liệu:", ["Nhập văn bản chữ viết thô", "Tải file Video Review (.mp4)"])
    text_input = ""
    
    if input_mode == "Nhập văn bản chữ viết thô":
        text_input = st.text_area("Nhập review khách hàng:")
    else:
        v_file = st.file_uploader("Thả video vào đây:", type=["mp4"])
        if v_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t:
                t.write(v_file.read())
                text_input = transcribe_voice(t.name)
            st.info(f"AI trích xuất lời thoại: {text_input}")

    if st.button("KÍCH HOẠT DỰ BÁO AI", type="primary") and text_input:
        vector = convert_text_to_feature_matrix(text_input)
        df_predict = pd.DataFrame([vector], columns=config.FEATURE_COLUMNS)
        
        # FIX TRIỆT ĐỂ LỖI 3: Ép kiểu int cho mảng dự đoán NumPy để chống lỗi Truth Value
        pred_class = int(ai_model_object.predict(df_predict)[0])
        
        # Hiển thị xác suất phân bổ nếu thuật toán hỗ trợ tính toán toán học
        try:
            probs = ai_model_object.predict_proba(df_predict)[0]
            st.write(f"📊 Xác suất: Tiêu cực: {probs[0]*100:.1f}% | Tích cực: {probs[2]*100:.1f}%")
        except: pass

        if pred_class == 0: st.error("🚨 SẮC THÁI TIÊU CỰC (NEGATIVE)")
        elif pred_class == 1: st.warning("😐 SẮC THÁI TRUNG LẬP (NEUTRAL)")
        else: st.success("🎉 SẮC THÁI TÍCH CỰC (POSITIVE)")
