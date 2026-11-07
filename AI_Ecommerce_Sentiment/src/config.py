# =================================================================
# THƯ MỤC LƯU TRỮ: src/config.py
# =================================================================
import os

# Định vị đường dẫn động hệ thống để chạy không bao giờ lỗi trên Thonny Windows
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_FILE = os.path.join(BASE_DIR, 'models', 'ai_sentiment_model.pkl')
DATA_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'reviews_processed.csv')

# Nếu chưa có thư mục data processed, dùng file gốc ngoài cùng để làm baseline
if not os.path.exists(DATA_FILE):
    DATA_FILE = os.path.join(BASE_DIR, 'du_lieu_24_cols.csv')

# Hệ thống từ khóa bóc tách đặc trưng ngữ nghĩa và khía cạnh (ABSA)
KW_TIEU_CUC_MANH = ["lừa đảo", "cẩu thả", "rách", "nát", "bể gáy", "rụng", "bùng", "gian dối"]
KW_TIEU_CUC_NHE = ["chán", "cũ", "dơ", "móp", "bụi", "mờ", "nhỏ", "ngắn", "tệ", "thất vọng", "kém"]
KW_TICH_CUC_MANH = ["tuyệt vời", "xuất sắc", "xịn", "cực kì hài lòng", "cực kỳ hài lòng", "quá đẹp"]
KW_TICH_CUC_NHE = ["tốt", "ok", "được", "ổn", "đẹp", "thơm", "rẻ", "hài lòng", "ưng ý"]
KW_SHIP_NHANH = ["giao nhanh", "ship nhanh", "thần tốc", "siêu tốc", "giao hàng nhanh", "nhanh chóng"]
KW_SHIP_CHAM = ["trễ", "delay", "lâu", "ngâm hàng", "đợi dài cổ", "giao chậm", "ship chậm"]
KW_LOI_SAN_PHAM = ["thiếu trang", "in lỗi", "mất trang", "lặp đoạn", "trùng ý", "lỗi in", "trang trắng"]
KW_LOI_DINH_KEM = ["thiếu cd", "ko có cd", "không có cd", "qr ko hoạt động", "ko có quà", "thiếu quà"]

# Từ khóa ánh xạ khía cạnh ABSA thực tế
KW_AS_CONTENT = ["nội dung", "cốt truyện", "kiến thức", "tác giả", "ý nghĩa", "triết lý", "chữ viết", "dịch"]
KW_AS_PHYSICAL = ["bìa", "giấy", "mực", "đẹp", "mới", "gáy sách", "đóng gáy", "bọc", "ngoại hình", "vật lý"]
KW_AS_PRICE = ["giá", "rẻ", "đắt", "tốn tiền", "kinh tế", "sale", "voucher", "khuyến mãi", "xu"]
KW_AS_PACKAGING = ["đóng gói", "bọc hàng", "hộp", "chống sốc", "ni lông", "cẩn thận", "thùng"]
KW_AS_DELIVERY = ["giao hàng", "shipper", "giao nhanh", "giao chậm", "ship", "vận chuyển", "bưu tá"]

FEATURE_COLUMNS = [
    'as_content', 'as_physical', 'as_price', 'as_packaging', 'as_delivery', 'as_service',
    'review_len_char', 'review_len_word', 'avg_word_length', 'exclamation_count', 'question_count',
    'contains_emoji_text', 'mention_star_rating', 'kw_tieu_cuc_manh', 'kw_tieu_cuc_nhe',
    'kw_tich_cuc_manh', 'kw_tich_cuc_nhe', 'kw_ship_nhanh', 'kw_ship_cham', 'kw_loi_san_pham', 'kw_loi_dinh_kem'
]

PAGES_DICTIONARY = {
    "PAGE 1": "💻 Real-time Prediction Engine (Dự báo đa phương thức)",
    "PAGE 2": "📊 Executive Analytics Dashboard (Tổng quan vĩ mô)",
    "PAGE 3": "🎯 Aspect-Based Sentiment Analysis (Phân tích khía cạnh ABSA)",
    "PAGE 4": "💡 Business Intelligence (Tri thức cải tiến hành động)"
}
