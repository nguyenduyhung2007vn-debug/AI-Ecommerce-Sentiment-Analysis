# =================================================================
# KHỐI CODE 2: TẦNG PIPELINE TRÍCH XUẤT MA TRẬN ĐẶC TRƯNG SỐ HỌC
# Đường dẫn lưu trữ trên GitHub: src/pipeline.py
# =================================================================
import re
import src.config as config

def evaluate_keyword(text_data, kw_list):
    for kw in kw_list:
        if kw in text_data: return 1
    return 0

def convert_text_to_feature_matrix(raw_text):
    text_lower = str(raw_text).lower().strip()
    
    # 1. Trích xuất đặc trưng độ dài
    char_count = len(raw_text)
    word_count = len(raw_text.split())
    avg_w_len = char_count / word_count if word_count > 0 else 0.0
    
    # 2. Trích xuất đặc trưng cú pháp
    excl_count = raw_text.count('!')
    ques_count = raw_text.count('?')
    emoji_flag = 1 if "emoji_" in text_lower else 0
    star_flag = 1 if re.search(r"(\d\s*sao|\d\*|1star|5star)", text_lower) else 0
    
    # 3. Trích xuất từ khóa vận hành
    bad_heavy = evaluate_keyword(text_lower, config.KW_TIEU_CUC_MANH)
    bad_light = evaluate_keyword(text_lower, config.KW_TIEU_CUC_NHE)
    good_heavy = evaluate_keyword(text_lower, config.KW_TICH_CUC_MANH)
    good_light = evaluate_keyword(text_lower, config.KW_TICH_CUC_NHE)
    ship_fast = evaluate_keyword(text_lower, config.KW_SHIP_NHANH)
    ship_slow = evaluate_keyword(text_lower, config.KW_SHIP_CHAM)
    prod_err = evaluate_keyword(text_lower, config.KW_LOI_SAN_PHAM)
    att_err = evaluate_keyword(text_lower, config.KW_LOI_DINH_KEM)
    
    # Mặc định các khía cạnh gốc bằng 0.0 đối với câu review mới tự do bên ngoài
    as_content, as_physical, as_price, as_packaging, as_delivery, as_service = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # ĐÃ ĐỒNG BỘ ĐÚNG THỨ TỰ MA TRẬN ĐẦU VÀO PKL (6 cột khía cạnh lên đầu)
    return [
        as_content, as_physical, as_price, as_packaging, as_delivery, as_service,
        char_count, word_count, avg_w_len, excl_count, ques_count,
        emoji_flag, star_flag, bad_heavy, bad_light, good_heavy, good_light, ship_fast, ship_slow, prod_err, att_err
    ]
