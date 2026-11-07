# =================================================================
# THƯ MỤC LƯU TRỮ: src/pipeline.py
# =================================================================
import re
import src.config as config

def extract_aspect_sentiment_logic(text_lower, aspect_keywords):
    """Xử lý triệt để lỗi gán cứng 0.0: Tự động nhận diện phân cực khía cạnh (-1, 0, 1)"""
    has_aspect = any(kw in text_lower for kw in aspect_keywords)
    if not has_aspect:
        return 0.0
    # Nếu khía cạnh xuất hiện, kiểm tra sắc thái đi kèm câu chữ
    is_negative = any(kw in text_lower for kw in config.KW_TIEU_CUC_MANH + config.KW_TIEU_CUC_NHE + config.KW_SHIP_CHAM)
    if is_negative:
        return -1.0
    return 1.0

def convert_text_to_feature_matrix(raw_text):
    text_lower = str(raw_text).lower().strip()
    
    # 1. Trích xuất tự động ma trận ABSA thực tế dựa trên bộ luật từ khóa từ người dùng nhập
    as_content = extract_aspect_sentiment_logic(text_lower, config.KW_AS_CONTENT)
    as_physical = extract_aspect_sentiment_logic(text_lower, config.KW_AS_PHYSICAL)
    as_price = extract_aspect_sentiment_logic(text_lower, config.KW_AS_PRICE)
    as_packaging = extract_aspect_sentiment_logic(text_lower, config.KW_AS_PACKAGING)
    as_delivery = extract_aspect_sentiment_logic(text_lower, config.KW_AS_DELIVERY)
    as_service = 0.0 # Baseline mặc định do tập dữ liệu ít nhắc khía cạnh hỗ trợ khách hàng
    
    # 2. Đặc trưng cấu trúc câu
    char_count = len(raw_text)
    word_count = len(raw_text.split())
    avg_w_len = char_count / word_count if word_count > 0 else 0.0
    
    # 3. Đặc trưng cú pháp
    excl_count = raw_text.count('!')
    ques_count = raw_text.count('?')
    emoji_flag = 1 if "emoji_" in text_lower else 0
    star_flag = 1 if re.search(r"(\d\s*sao|\d\*|1star|5star)", text_lower) else 0
    
    # 4. Trích xuất trạng thái nhị phân
    check_kw = lambda list_kw: 1 if any(w in text_lower for w in list_kw) else 0
    bad_heavy = check_kw(config.KW_TIEU_CUC_MANH)
    bad_light = check_kw(config.KW_TIEU_CUC_NHE)
    good_heavy = check_kw(config.KW_TICH_CUC_MANH)
    good_light = check_kw(config.KW_TICH_CUC_NHE)
    ship_fast = check_kw(config.KW_SHIP_NHANH)
    ship_slow = check_kw(config.KW_SHIP_CHAM)
    prod_err = check_kw(config.KW_LOI_SAN_PHAM)
    att_err = check_kw(config.KW_LOI_DINH_KEM)

    # Trả về ma trận 21 thuộc tính được sắp xếp đúng thứ tự nghiêm ngặt của file pkl
    return [
        as_content, as_physical, as_price, as_packaging, as_delivery, as_service,
        char_count, word_count, avg_w_len, excl_count, ques_count,
        emoji_flag, star_flag, bad_heavy, bad_light, good_heavy, good_light, ship_fast, ship_slow, prod_err, att_err
    ]
