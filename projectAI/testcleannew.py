import json
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# 1. Đọc file JSON từ ổ D
file_path = r"D:\projectAI\test_clean.json"

try:
  with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  df = pd.DataFrame(data)
  print("Đã đọc thành công dữ liệu!")
except Exception as e:
  print(f"Lỗi đọc file: {e}")

# --- BƯỚC 1: XỬ LÝ KHUYẾT THIẾU CÁC CỘT KHÍA CẠNH (ASPECTS) ---
aspect_cols = [
    "as_content",
    "as_physical",
    "as_price",
    "as_packaging",
    "as_delivery",
    "as_service",
]
for col in aspect_cols:
  if col in df.columns:
    df[col] = df[col].fillna(0.0).astype(float)
  else:
    df[col] = 0.0

# --- BƯỚC 2: ĐỊNH NGHĨA DANH SÁCH TỪ KHÓA ---
kw_tieu_cuc_manh_list = [
    "lừa đảo",
    "cẩu thả",
    "rách",
    "nát",
    "bể gáy",
    "rụng",
    "bùng",
    "gian dối",
]
kw_tieu_cuc_nhe_list = [
    "chán",
    "cũ",
    "dơ",
    "móp",
    "bụi",
    "mờ",
    "nhỏ",
    "ngắn",
    "tệ",
    "thất vọng",
    "kém",
]
kw_tich_cuc_manh_list = [
    "tuyệt vời",
    "xuất sắc",
    "xịn",
    "cực kì hài lòng",
    "cực kỳ hài lòng",
    "quá đẹp",
]
kw_tich_cuc_nhe_list = [
    "tốt",
    "ok",
    "được",
    "ổn",
    "đẹp",
    "thơm",
    "rẻ",
    "hài lòng",
    "ưng ý",
]
kw_ship_nhanh_list = [
    "giao nhanh",
    "ship nhanh",
    "thần tốc",
    "siêu tốc",
    "giao hàng nhanh",
    "nhanh chóng",
]
kw_ship_cham_list = [
    "trễ",
    "delay",
    "lâu",
    "ngâm hàng",
    "đợi dài cổ",
    "giao chậm",
    "ship chậm",
]
kw_loi_san_pham_list = [
    "thiếu trang",
    "in lỗi",
    "mất trang",
    "lặp đoạn",
    "trùng ý",
    "lỗi in",
    "trang trắng",
]
kw_loi_dinh_kem_list = [
    "thiếu cd",
    "ko có cd",
    "không có cd",
    "qr ko hoạt động",
    "ko có quà",
    "thiếu quà",
]


def check_kw(text, kw_list):
  for kw in kw_list:
    if kw in text:
      return 1
  return 0


# --- BƯỚC 3: HÀM TRÍCH XUẤT 21 ĐẶC TRƯNG ---
def extract_21_features(df_in):
  df_feat = df_in.copy()
  content_str = df_feat["content"].astype(str).fillna("")

  # 1-3. Đặc trưng độ dài
  df_feat["review_len_char"] = content_str.apply(len)
  df_feat["review_len_word"] = content_str.apply(lambda x: len(x.split()))
  df_feat["avg_word_length"] = content_str.apply(
      lambda x: float(np.mean([len(w) for w in x.split()]))
      if len(x.split()) > 0
      else 0.0
  )

  # 4-7. Đặc trưng cú pháp & ký hiệu
  df_feat["exclamation_count"] = content_str.apply(lambda x: x.count("!"))
  df_feat["question_count"] = content_str.apply(lambda x: x.count("?"))
  df_feat["contains_emoji_text"] = content_str.apply(
      lambda x: 1 if "emoji_" in x.lower() else 0
  )

  star_pattern = r"(\d\s*sao|\d\*|1star|5star)"
  df_feat["mention_star_rating"] = content_str.apply(
      lambda x: 1 if re.search(star_pattern, x.lower()) else 0
  )

  # 8-15. Đặc trưng nhóm từ khóa
  content_lower = content_str.str.lower()
  df_feat["kw_tieu_cuc_manh"] = content_lower.apply(
      lambda x: check_kw(x, kw_tieu_cuc_manh_list)
  )
  df_feat["kw_tieu_cuc_nhe"] = content_lower.apply(
      lambda x: check_kw(x, kw_tieu_cuc_nhe_list)
  )
  df_feat["kw_tich_cuc_manh"] = content_lower.apply(
      lambda x: check_kw(x, kw_tich_cuc_manh_list)
  )
  df_feat["kw_tich_cuc_nhe"] = content_lower.apply(
      lambda x: check_kw(x, kw_tich_cuc_nhe_list)
  )

  df_feat["kw_ship_nhanh"] = content_lower.apply(
      lambda x: check_kw(x, kw_ship_nhanh_list)
  )
  df_feat["kw_ship_cham"] = content_lower.apply(
      lambda x: check_kw(x, kw_ship_cham_list)
  )

  df_feat["kw_loi_san_pham"] = content_lower.apply(
      lambda x: check_kw(x, kw_loi_san_pham_list)
  )
  df_feat["kw_loi_dinh_kem"] = content_lower.apply(
      lambda x: check_kw(x, kw_loi_dinh_kem_list)
  )

  return df_feat


# Thực thi trích xuất
df_full = extract_21_features(df)

feature_cols = [
    "review_len_char",
    "review_len_word",
    "avg_word_length",
    "exclamation_count",
    "question_count",
    "contains_emoji_text",
    "mention_star_rating",
    "kw_tieu_cuc_manh",
    "kw_tieu_cuc_nhe",
    "kw_tich_cuc_manh",
    "kw_tich_cuc_nhe",
    "kw_ship_nhanh",
    "kw_ship_cham",
    "kw_loi_san_pham",
    "kw_loi_dinh_kem",
    "as_content",
    "as_physical",
    "as_price",
    "as_packaging",
    "as_delivery",
    "as_service",
]

# --- BƯỚC 4: HUẤN LUYỆN MÔ HÌNH RANDOM FOREST ---
df_model = df_full.dropna(subset=["sentiment_llm"]).copy()
df_model["sentiment_llm"] = df_model["sentiment_llm"].astype(int)

X = df_model[feature_cols]
y = df_model["sentiment_llm"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200, max_depth=12, random_state=42, class_weight="balanced"
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n=== KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH VỚI 21 ĐẶC TRƯNG ===")
print("Độ chính xác (Accuracy):", round(accuracy_score(y_test, y_pred), 4))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Xuất file CSV hoàn chỉnh
output_csv = r"D:\projectAI\tiki_reviews_21_features.csv"
df_full.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"Đã xuất file thành công tại: {output_csv}")