# =================================================================
# KHỐI CODE 1: CẤU HÌNH ĐẶC TRƯNG MÔ HÌNH VÀ DANH MỤC 20 TRANG WEB
# Đường dẫn lưu trữ trên GitHub: src/config.py
# =================================================================

MODEL_FILE = 'ai_sentiment_model.pkl'
DATA_FILE = 'du_lieu_24_cols.csv'

# Hệ thống từ khóa lọc nhị phân trích xuất thuộc tính (Feature Engineering)
KW_TIEU_CUC_MANH = ["lừa đảo", "cẩu thả", "rách", "nát", "bể gáy", "rụng", "bùng", "gian dối"]
KW_TIEU_CUC_NHE = ["chán", "cũ", "dơ", "móp", "bụi", "mờ", "nhỏ", "ngắn", "tệ", "thất vọng", "kém"]
KW_TICH_CUC_MANH = ["tuyệt vời", "xuất sắc", "xịn", "cực kì hài lòng", "cực kỳ hài lòng", "quá đẹp"]
KW_TICH_CUC_NHE = ["tốt", "ok", "được", "ổn", "đẹp", "thơm", "rẻ", "hài lòng", "ưng ý"]
KW_SHIP_NHANH = ["giao nhanh", "ship nhanh", "thần tốc", "siêu tốc", "giao hàng nhanh", "nhanh chóng"]
KW_SHIP_CHAM = ["trễ", "delay", "lâu", "ngâm hàng", "đợi dài cổ", "giao chậm", "ship chậm"]
KW_LOI_SAN_PHAM = ["thiếu trang", "in lỗi", "mất trang", "lặp đoạn", "trùng ý", "lỗi in", "trang trắng"]
KW_LOI_DINH_KEM = ["thiếu cd", "ko có cd", "không có cd", "qr ko hoạt động", "ko có quà", "thiếu quà"]

# ĐÃ ĐỒNG BỘ ĐÚNG MA TRẬN PHIÊN BẢN CỦA TỆP PKL GỐC
FEATURE_COLUMNS = [
    'as_content', 'as_physical', 'as_price', 'as_packaging', 'as_delivery', 'as_service',
    'review_len_char', 'review_len_word', 'avg_word_length', 'exclamation_count', 'question_count',
    'contains_emoji_text', 'mention_star_rating', 'kw_tieu_cuc_manh', 'kw_tieu_cuc_nhe',
    'kw_tich_cuc_manh', 'kw_tich_cuc_nhe', 'kw_ship_nhanh', 'kw_ship_cham', 'kw_loi_san_pham', 'kw_loi_dinh_kem'
]

PAGES_DICTIONARY = {
    "PAGE 1": "💻 Real-time Prediction Engine (Dự báo sắc thái)",
    "PAGE 2": "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)",
    "PAGE 3": "📚 Content Quality Insights (Khía cạnh Nội dung)",
    "PAGE 4": "📦 Physical & Printing Quality (Khía cạnh Vật lý)",
    "PAGE 5": "💰 Pricing & Commercial Strategy (Khía cạnh Giá cả)",
    "PAGE 6": "🎁 Packaging & Warehouse Logistics (Khía cạnh Đóng gói)",
    "PAGE 7": "🚚 Delivery Speed & Logistics (Khía cạnh Vận chuyển)",
    "PAGE 8": "📞 Customer Service Experience (Khía cạnh Hỗ trợ)",
    "PAGE 9": "📏 Text Length Characteristics (Đặc trưng Độ dài câu)",
    "PAGE 10": "❓ Customer Inquiries & Questions (Đặc trưng Dấu hỏi)",
    "PAGE 11": "⚠️ Emotional Punctuation Intensity (Đặc trưng Dấu chấm cảm)",
    "PAGE 12": "💬 Emoji Sentiment Representation (Đặc trưng Emoji văn bản)",
    "PAGE 13": "⭐ Star Rating Mention Matrix (Đặc trưng Nhắc sao)",
    "PAGE 14": "🚨 Critical Operational Risk Alert (Từ khóa Tiêu cực mạnh)",
    "PAGE 15": "📉 Minor Customer Complaints (Từ khóa Tiêu cực nhẹ)",
    "PAGE 16": "🏆 Elite Customer Satisfaction (Từ khóa Tích cực mạnh)",
    "PAGE 17": "✨ General Positive Feedback (Từ khóa Tích cực nhẹ)",
    "PAGE 18": "🚀 Hyper-Speed Logistics Impact (Từ khóa Ship nhanh)",
    "PAGE 19": "🐢 Delayed Logistics Bottlenecks (Từ khóa Ship chậm)",
    "PAGE 20": "⚙️ System Error & Bug Diagnostics (Từ khóa Lỗi sản phẩm)"
}

