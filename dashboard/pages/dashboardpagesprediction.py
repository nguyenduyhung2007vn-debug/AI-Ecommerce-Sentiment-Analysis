# =================================================================
# =================================================================
import streamlit as st
import pandas as pd
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
import os
from src.pipeline import convert_text_to_feature_matrix
import src.config as config

def transcribe_video_voice_to_text(video_file_path):
    """Hàm tách âm thanh từ video và chuyển giọng nói Tiếng Việt sang chữ bằng API siêu nhẹ"""
    r = sr.Recognizer()
    
    # 1. Trích xuất âm thanh từ Video và chuyển đổi sang định dạng .wav chuẩn toán học
    audio = AudioSegment.from_file(video_file_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio.export(temp_wav.name, format="wav")
        wav_path = temp_wav.name
        
    # 2. Sử dụng API nhận diện giọng nói Tiếng Việt thời gian thực
    with sr.AudioFile(wav_path) as source:
        audio_data = r.record(source)
        try:
            # Ép cấu hình nhận diện ngôn ngữ Tiếng Việt (vi-VN)
            text_result = r.recognize_google(audio_data, language="vi-VN")
            return text_result
        except sr.UnknownValueError:
            return "Không thể nhận diện được giọng nói trong video (Âm thanh quá nhỏ hoặc bị nhiễu)."
        except sr.RequestError as e:
            return f"Lỗi kết nối máy chủ API nhận diện: {e}"
        finally:
            # Dọn dẹp file tạm trên ổ cứng máy chủ sau khi xử lý xong
            if os.path.exists(wav_path):
                os.remove(wav_path)

def render_page_one_prediction(ai_model_object):
    st.title("💻 Multimodal AI Sentiment Engine - Dự báo đa phương thức")
    st.write("Hệ thống hỗ trợ phân tích sắc thái thời gian thực thông qua Chữ viết HOẶC File Video Review.")
    st.write("---")
    
    # Lựa chọn phương thức nhập liệu
    input_mode = st.radio("Lựa chọn phương thức nhập liệu đầu vào:", ["Nhập văn bản chữ viết thô", "Tải file Video Review (.mp4, .mov)"])
    
    final_text_to_analyze = ""
    
    # CHẾ ĐỘ 1: NHẬP CHỮ TRUYỀN THỐNG
    if input_mode == "Nhập văn bản chữ viết thô":
        final_text_to_analyze = st.text_area(
            "Nhập nội dung đánh giá của khách hàng tại đây:", height=120,
            placeholder="Ví dụ: Sách bọc quá cẩu thả, rách gáy rồi. Thất vọng cực kỳ!"
        )
    
    # CHẾ ĐỘ 2: TẢI FILE VIDEO (KHÔNG BỊ TREO MẠNG)
    else:
        uploaded_video = st.file_uploader("Kéo thả file Video Review của khách hàng vào đây:", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            st.video(uploaded_video)
            
            with st.spinner("⏳ Hệ thống AI đang xử lý âm thanh và trích xuất lời thoại trong Video..."):
                # Ghi tạm file video đầu vào
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                    temp_file.write(uploaded_video.read())
                    temp_video_path = temp_file.name
                
                # Gọi hàm dịch Speech-to-Text API siêu tốc
                final_text_to_analyze = transcribe_video_voice_to_text(temp_video_path)
                
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                    
                st.info(f"📝 **Văn bản AI trích xuất từ Video:** {final_text_to_analyze}")

    # NÚT LỆNH DỰ BÁO CHUNG CHO PIPELINE AI
    if st.button("KÍCH HOẠT PIPELINE AI DỰ BÁO SẮC THÁI", type="primary"):
        if final_text_to_analyze.strip() == "" or "Không thể nhận diện" in final_text_to_analyze or "Lỗi kết nối" in final_text_to_analyze:
            st.warning("Hệ thống trống dữ liệu đầu vào văn bản hợp lệ để dự báo ma trận!")
        else:
            # Truyền chuỗi chữ vào layer trích xuất ma trận 21 cột của nhóm
            feature_vector = convert_text_to_feature_matrix(final_text_to_analyze)
            df_predict_input = pd.DataFrame([feature_vector], columns=config.FEATURE_COLUMNS)
            
            # Bộ não Random Forest thực hiện lệnh phân loại
            predicted_class = ai_model_object.predict(df_predict_input)
            
            st.write("---")
            st.markdown("### 🔔 Kết quả dự báo sắc thái cảm xúc sau Pipeline:")
            
            if predicted_class == 0:
                st.error("🚨 **SẮC THÁI TIÊU CỰC (NEGATIVE)** — Lời thoại hoặc chữ viết mang tâm lý phàn nàn lỗi vận hành!")
            elif predicted_class == 1:
                st.warning("😐 **SẮC THÁI TRUNG LẬP (NEUTRAL)** — Đánh giá mang tính thảo luận chung chung hệ thống")
            else:
                st.success("🎉 **SẮC THÁI TÍCH CỰC (POSITIVE)** — Khách hàng bày tỏ sự hài lòng, tăng trưởng ROI kinh doanh!")
