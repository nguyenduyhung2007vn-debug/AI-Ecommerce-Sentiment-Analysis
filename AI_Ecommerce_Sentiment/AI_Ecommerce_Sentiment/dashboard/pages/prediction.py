
# Vị trí: dashboard/pages/prediction.py

import streamlit as st
import pandas as pd
import tempfile
import os

# Kiểm tra thư viện nhận diện giọng nói
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    sr = None
    SPEECH_AVAILABLE = False

# Kiểm tra thư viện xử lý âm thanh
try:
    from pydub import AudioSegment
    AUDIO_AVAILABLE = True
except ImportError:
    AudioSegment = None
    AUDIO_AVAILABLE = False

from src.pipeline import convert_text_to_feature_matrix
import src.config as config


def transcribe_voice(video_path):
    if not SPEECH_AVAILABLE or not AUDIO_AVAILABLE:
        return ""

    r = sr.Recognizer()
    wav_p = None

    try:
        audio = AudioSegment.from_file(video_path)

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as tmp:
            wav_p = tmp.name

        audio.export(wav_p, format="wav")

        with sr.AudioFile(wav_p) as source:
            audio_data = r.record(source)

        return r.recognize_google(
            audio_data,
            language="vi-VN"
        )

    except Exception as e:
        st.error(f"Không thể trích xuất lời thoại: {e}")
        return ""

    finally:
        if wav_p and os.path.exists(wav_p):
            os.remove(wav_p)


def render_page_one_prediction(ai_model_object):

    st.title("💻 Real-time Prediction Engine")

    input_mode = st.radio(
        "Đầu vào dữ liệu:",
        [
            "Nhập văn bản chữ viết thô",
            "Tải file Video Review (.mp4)"
        ]
    )

    text_input = ""

    # ---------------------------------
    # CHẾ ĐỘ 1: DỰ ĐOÁN TỪ VĂN BẢN
    # ---------------------------------

    if input_mode == "Nhập văn bản chữ viết thô":

        text_input = st.text_area(
            "Nhập review khách hàng:",
            placeholder="Ví dụ: Sách rất đẹp, đóng gói cẩn thận, giao hàng nhanh..."
        )

    # ---------------------------------
    # CHẾ ĐỘ 2: NHẬN DIỆN TỪ VIDEO
    # ---------------------------------

    else:

        if not SPEECH_AVAILABLE or not AUDIO_AVAILABLE:

            st.warning(
                "Chức năng nhận diện giọng nói/video hiện chưa khả dụng. "
                "Bạn vẫn có thể sử dụng chế độ dự đoán bằng văn bản."
            )

        else:

            v_file = st.file_uploader(
                "Thả video vào đây:",
                type=["mp4"]
            )

            if v_file:

                video_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp4"
                    ) as t:
                        t.write(v_file.getbuffer())
                        video_path = t.name

                    with st.spinner("AI đang trích xuất lời thoại..."):
                        text_input = transcribe_voice(video_path)

                    if text_input:
                        st.info(f"AI trích xuất lời thoại: {text_input}")
                    else:
                        st.warning(
                            "Không nhận diện được lời thoại trong video."
                        )

                finally:
                    if video_path and os.path.exists(video_path):
                        os.remove(video_path)

    # ---------------------------------
    # DỰ ĐOÁN CẢM XÚC
    # ---------------------------------

    if st.button("KÍCH HOẠT DỰ BÁO AI", type="primary"):

        if not text_input or not text_input.strip():

            st.warning("Vui lòng nhập nội dung đánh giá hoặc cung cấp video hợp lệ.")

        else:

            try:
                vector = convert_text_to_feature_matrix(text_input)

                df_predict = pd.DataFrame(
                    [vector],
                    columns=config.FEATURE_COLUMNS
                )

                pred_class = int(
                    ai_model_object.predict(df_predict)[0]
                )

                st.subheader("Kết quả phân tích cảm xúc")

                # Xác suất dự đoán theo đúng thứ tự classes của model
                if hasattr(ai_model_object, "predict_proba"):

                    probs = ai_model_object.predict_proba(df_predict)[0]
                    classes = list(ai_model_object.classes_)

                    labels = {
                        0: "Tiêu cực",
                        1: "Trung lập",
                        2: "Tích cực"
                    }

                    probability_text = " | ".join(
                        f"{labels.get(int(cls), str(cls))}: {prob * 100:.1f}%"
                        for cls, prob in zip(classes, probs)
                    )

                    st.write(f"📊 Xác suất: {probability_text}")

                if pred_class == 0:
                    st.error("🚨 SẮC THÁI TIÊU CỰC (NEGATIVE)")

                elif pred_class == 1:
                    st.warning("😐 SẮC THÁI TRUNG LẬP (NEUTRAL)")

                elif pred_class == 2:
                    st.success("🎉 SẮC THÁI TÍCH CỰC (POSITIVE)")

                else:
                    st.info(f"Kết quả dự đoán: {pred_class}")

            except Exception as e:
                st.error(f"Lỗi khi dự đoán: {e}")
