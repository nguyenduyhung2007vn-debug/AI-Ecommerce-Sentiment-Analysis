# =================================================================
# FILE ĐÃ CẬP NHẬT: dashboard/pages/prediction.py
# TÍCH HỢP TÍNH NĂNG CHUYỂN GIỌNG NÓI VIDEO SANG VĂN BẢN (WHISPER AI)
# =================================================================
import streamlit as st
import pandas as pd
import tempfile
import whisper
from src.pipeline import convert_text_to_feature_matrix
import src.config as config

@st.cache_resource
def load_whisper_model():
    """Tải mô hình nhận diện giọng nói OpenAI Whisper vào bộ nhớ đệm"""
    # Sử dụng bản 'tiny' hoặc 'base' để máy chạy nhanh, nhẹ, phù hợp làm demo
    return whisper.load_model("tiny")

def render_page_one_prediction(ai_model_object):
    st.title("💻 Multimodal AI Sentiment Engine - Dự báo đa phương thức")
    st.write("Hệ thống hỗ trợ phân tích sắc thái thời gian thực thông qua Chữ viết HOẶC File Video Review.")
    st.write("---")
    
    # THÀNH PHẦN LỰA CHỌN CHẾ ĐỘ ĐẦU VÀO (INPUT CHỮ HOẶC VIDEO)
    input_mode = st.radio("Lựa chọn phương thức nhập liệu đầu vào:", ["Nhập văn bản chữ viết thô", "Tải file Video Review (.mp4, .mov)"])
    
    final_text_to_analyze = ""
    
    # CHẾ ĐỘ 1: NHẬP CHỮ TRUYỀN THỐNG
    if input_mode == "Nhập văn bản chữ viết thô":
        final_text_to_analyze = st.text_area(
            "Nhập nội dung đánh giá của khách hàng tại đây:", height=120,
            placeholder="Ví dụ: Sách bọc quá cẩu thả, rách gáy rồi. Thất vọng cực kỳ!"
        )
    
    # CHẾ ĐỘ 2: TẢI FILE VIDEO (TÍNH NĂNG ĐỘT PHÁ CỦA NHÓM)
    else:
        uploaded_video = st.file_uploader("Kéo thả file Video Review của khách hàng vào đây:", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            # Hiển thị trình phát video ngay trên giao diện Web để thầy xem
            st.video(uploaded_video)
            
            with st.spinner("⏳ Hệ thống AI đang nghe và chuyển đổi giọng nói trong Video sang Văn bản..."):
                try:
                    # Nạp mô hình nhận diện giọng nói
                    whisper_engine = load_whisper_model()
                    
                    # Ghi tạm file video vào ổ cứng để AI Whisper đọc dữ liệu âm thanh
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                        temp_file.write(uploaded_video.read())
                        temp_video_path = temp_file.name
                    
                    # Tiến hành chuyển đổi Speech-to-Text (Ép cấu hình dịch sang tiếng Việt)
                    whisper_result = whisper_engine.transcribe(temp_video_path, language="vi")
                    final_text_to_analyze = whisper_result["text"]
                    
                    # Hiển thị kết quả chữ viết bóc tách từ video cho thầy xem
                    st.info(f"📝 **Văn bản AI trích xuất từ Video:** {final_text_to_analyze}")
                except Exception as e:
                    st.error(f"Lỗi xử lý âm thanh Video: {e}")

    # NÚT BẤM KÍCH HOẠT HỆ THỐNG DỰ BÁO CHUNG CHO CẢ CHỮ VÀ VIDEO
    if st.button("KÍCH HOẠT PIPELINE AI DỰ BÁO SẮC THÁI", type="primary"):
        if final_text_to_analyze.strip() == "":
            st.warning("Hệ thống trống dữ liệu đầu vào văn bản để phân tích ma trận!")
        else:
            # TRUYỀN CHỮ VÀO LAYER TRÍCH XUẤT 21 THUỘC TÍNH SẴN CÓ CỦA NHÓM
            feature_vector = convert_text_to_feature_matrix(final_text_to_analyze)
            df_predict_input = pd.DataFrame([feature_vector], columns=config.FEATURE_COLUMNS)
            
            # BỘ NÃO RANDOM FOREST TIẾN HÀNH DỰ ĐOÁN
            predicted_class = ai_model_object.predict(df_predict_input)
            
            st.write("---")
            st.markdown("### 🔔 Kết quả dự báo sắc thái cảm xúc sau Pipeline:")
            
            if predicted_class == 0:
                st.error("🚨 **SẮC THÁI TIÊU CỰC (NEGATIVE)** — Lời thoại hoặc chữ viết mang tâm lý phản nàn lỗi vận hành!")
            elif predicted_class == 1:
                st.warning("😐 **SẮC THÁI TRUNG LẬP (NEUTRAL)** — Đánh giá mang tính thảo luận chung chung hệ thống")
            else:
                st.success("🎉 **SẮC THÁI TÍCH CỰC (POSITIVE)** — Khách hàng bày tỏ sự hài lòng, tăng trưởng ROI kinh doanh!")

