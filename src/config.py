# ============================================================
# src/config.py - Cấu hình đường dẫn, đặc trưng, từ khóa
# ============================================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def find_file(name, subdirs=("", "models", "data")):
    """Tìm file ở thư mục gốc dự án (và thư mục cha / thư mục chạy)."""
    for root in (BASE_DIR, BASE_DIR.parent, Path.cwd()):
        for sub in subdirs:
            p = root / sub / name
            if p.exists():
                return p
    return BASE_DIR / name


MODEL_FILE = find_file("ai_sentiment_model.pkl")
DATA_FILE = find_file("du_lieu_24_cols.csv")
ASPECT_MODEL_FILE = find_file("aspect_model.pkl")

# Mã hóa cột as_* trong CSV thực tế (KHÁC với README cũ -1/0/1): 0 = tiêu cực hoặc không nhắc, 1 = trung lập, 2 = tích cực
ASPECT_CODES = {0: "Tiêu cực / không nhắc", 1: "Trung lập", 2: "Tích cực"}

LABELS = {0: "Tiêu cực", 1: "Trung lập", 2: "Tích cực"}
LABEL_COLORS = {"Tiêu cực": "#EF4444", "Trung lập": "#F59E0B", "Tích cực": "#10B981"}

# ---------- Từ khóa cho 8 đặc trưng kw_* (giữ nguyên) ----------
KW_TIEU_CUC_MANH = ["lừa đảo", "cẩu thả", "rách", "nát", "bể gáy", "rụng", "bùng", "gian dối"]
KW_TIEU_CUC_NHE = ["chán", "cũ", "dơ", "móp", "bụi", "mờ", "nhỏ", "ngắn", "tệ", "thất vọng", "kém"]
KW_TICH_CUC_MANH = ["tuyệt vời", "xuất sắc", "xịn", "cực kì hài lòng", "cực kỳ hài lòng", "quá đẹp"]
KW_TICH_CUC_NHE = ["tốt", "ok", "được", "ổn", "đẹp", "thơm", "rẻ", "hài lòng", "ưng ý"]
KW_SHIP_NHANH = ["giao nhanh", "ship nhanh", "thần tốc", "siêu tốc", "giao hàng nhanh", "nhanh chóng"]
KW_SHIP_CHAM = ["trễ", "delay", "lâu", "ngâm hàng", "đợi dài cổ", "giao chậm", "ship chậm"]
KW_LOI_SAN_PHAM = ["thiếu trang", "in lỗi", "mất trang", "lặp đoạn", "trùng ý", "lỗi in", "trang trắng"]
KW_LOI_DINH_KEM = ["thiếu cd", "ko có cd", "không có cd", "qr ko hoạt động", "ko có quà", "thiếu quà"]

# ---------- Từ khóa nhận diện khía cạnh ----------
KW_AS_CONTENT = ["nội dung", "cốt truyện", "kiến thức", "tác giả", "ý nghĩa", "triết lý", "chữ viết", "dịch"]
KW_AS_PHYSICAL = ["bìa", "giấy", "mực", "đẹp", "mới", "gáy sách", "đóng gáy", "bọc", "ngoại hình", "vật lý", "gáy", "trang sách"]
KW_AS_PRICE = ["giá", "rẻ", "đắt", "tốn tiền", "kinh tế", "sale", "voucher", "khuyến mãi", "xu"]
KW_AS_PACKAGING = ["đóng gói", "bọc hàng", "hộp", "chống sốc", "ni lông", "cẩn thận", "thùng"]
KW_AS_DELIVERY = ["giao hàng", "shipper", "giao nhanh", "giao chậm", "ship", "vận chuyển", "bưu tá", "giao trễ", "nhận hàng"]
KW_AS_SERVICE = ["shop", "tư vấn", "nhân viên", "hỗ trợ", "phản hồi", "đổi trả", "bảo hành", "chăm sóc", "cskh"]

# Từ bổ sung CHỈ dùng để xác định phân cực của khía cạnh (không ảnh hưởng đặc trưng kw_*)
EXTRA_POSITIVE = ["cẩn thận", "chắc chắn", "nhiệt tình", "nhanh", "đúng hẹn", "chu đáo", "thân thiện", "kỹ"]
EXTRA_NEGATIVE = ["chậm", "trầy", "hư", "hỏng", "sai", "thiếu", "ẩm", "mốc", "nhàu", "cong", "bung", "chưa nhận", "không phản hồi", "không trả lời", "không hỗ trợ"]

ASPECT_KEYWORDS = {
    "as_content": KW_AS_CONTENT, "as_physical": KW_AS_PHYSICAL, "as_price": KW_AS_PRICE,
    "as_packaging": KW_AS_PACKAGING, "as_delivery": KW_AS_DELIVERY, "as_service": KW_AS_SERVICE,
}
ASPECT_NAMES = {
    "as_content": "Nội dung", "as_physical": "Tình trạng vật lý", "as_price": "Giá cả",
    "as_packaging": "Đóng gói", "as_delivery": "Giao hàng", "as_service": "Dịch vụ",
}

FEATURE_COLUMNS = [
    "as_content", "as_physical", "as_price", "as_packaging", "as_delivery", "as_service",
    "review_len_char", "review_len_word", "avg_word_length", "exclamation_count", "question_count",
    "contains_emoji_text", "mention_star_rating", "kw_tieu_cuc_manh", "kw_tieu_cuc_nhe",
    "kw_tich_cuc_manh", "kw_tich_cuc_nhe", "kw_ship_nhanh", "kw_ship_cham", "kw_loi_san_pham", "kw_loi_dinh_kem",
]
FEATURE_DESC = {
    "as_content": "Khía cạnh nội dung (0/1/2)", "as_physical": "Khía cạnh vật lý (0/1/2)",
    "as_price": "Khía cạnh giá (0/1/2)", "as_packaging": "Khía cạnh đóng gói (0/1/2)",
    "as_delivery": "Khía cạnh giao hàng (0/1/2)", "as_service": "Khía cạnh dịch vụ (0/1/2)",
    "review_len_char": "Số ký tự", "review_len_word": "Số từ", "avg_word_length": "Độ dài từ trung bình",
    "exclamation_count": "Số dấu !", "question_count": "Số dấu ?", "contains_emoji_text": "Có emoji",
    "mention_star_rating": "Nhắc số sao", "kw_tieu_cuc_manh": "Từ tiêu cực mạnh", "kw_tieu_cuc_nhe": "Từ tiêu cực nhẹ",
    "kw_tich_cuc_manh": "Từ tích cực mạnh", "kw_tich_cuc_nhe": "Từ tích cực nhẹ", "kw_ship_nhanh": "Giao nhanh",
    "kw_ship_cham": "Giao chậm", "kw_loi_san_pham": "Lỗi sản phẩm", "kw_loi_dinh_kem": "Lỗi đi kèm",
}
KEYWORD_GROUPS = {
    "kw_tieu_cuc_manh": KW_TIEU_CUC_MANH, "kw_tieu_cuc_nhe": KW_TIEU_CUC_NHE,
    "kw_tich_cuc_manh": KW_TICH_CUC_MANH, "kw_tich_cuc_nhe": KW_TICH_CUC_NHE,
    "kw_ship_nhanh": KW_SHIP_NHANH, "kw_ship_cham": KW_SHIP_CHAM,
    "kw_loi_san_pham": KW_LOI_SAN_PHAM, "kw_loi_dinh_kem": KW_LOI_DINH_KEM,
}
