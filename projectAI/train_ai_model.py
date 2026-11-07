import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. TẢI TẬP DỮ LIỆU SẠCH 24 CỘT
try:
    df = pd.read_csv('du_lieu_24_cols.csv')
    print("--- 1. Tải dữ liệu 24 cột thành công ---")
except Exception as e:
    print("Lỗi: Hãy chắc chắn bạn đã đổi tên file dữ liệu thành 'du_lieu_24_cols.csv' và để chung thư mục code!")
    raise e

# 2. PHÂN TÁCH BIẾN ĐỘC LẬP (FEATURES) VÀ BIẾN MỤC TIÊU (TARGET)
# Loại bỏ 2 cột định danh văn bản thô phi số học là 'review_id' và 'content'
features_list = [
    'as_content', 'as_physical', 'as_price', 'as_packaging', 'as_delivery', 'as_service',
    'review_len_char', 'review_len_word', 'avg_word_length', 'exclamation_count', 'question_count',
    'contains_emoji_text', 'mention_star_rating', 'kw_tieu_cuc_manh', 'kw_tieu_cuc_nhe',
    'kw_tich_cuc_manh', 'kw_tich_cuc_nhe', 'kw_ship_nhanh', 'kw_ship_cham', 'kw_loi_san_pham', 'kw_loi_dinh_kem'
]

X = df[features_list]       # Ma trận đặc trưng số học đầu vào (21 thuộc tính)
y = df['sentiment_llm']     # Nhãn mục tiêu cần dự đoán (0, 1, 2)

# 3. CHIA DỮ LIỆU THÀNH TẬP TRAIN (80%) VÀ TEST (20%)
# Sử dụng stratify=y để đảm bảo tỷ lệ các nhãn (0, 1, 2) cân bằng ở cả 2 tập
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"--- 2. Phân chia dữ liệu: Train ({len(X_train)} mẫu) | Test ({len(X_test)} mẫu) ---")

# 4. KHỞI TẠO VÀ HUẤN LUYỆN MÔ HÌNH AI (RANDOM FOREST CLASSIFIER)
print("\n--- 3. Đang tiến hành huấn luyện mô hình AI ---")
# Giới hạn max_depth để cây không bị quá khớp (Overfitting)
ai_model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
ai_model.fit(X_train, y_train)
print("--- Huấn luyện hoàn tất ---")

# 5. KIỂM THỬ VÀ ĐÁNH GIÁ CHỈ SỐ TOÁN HỌC MÔ HÌNH
y_pred = ai_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n================== KẾT QUẢ HIỆU NĂNG MÔ HÌNH AI ==================")
print(f"Độ chính xác tổng thể (Accuracy Score): {accuracy * 100:.2f}%")
print("\nBáo cáo phân loại chi tiết (Classification Report):")
print(classification_report(y_test, y_pred, target_names=['0: Tiêu cực', '1: Trung lập', '2: Tích cực']))

# Khởi tạo Ma trận nhầm lẫn (Confusion Matrix) dưới dạng text
print("Ma trận nhầm lẫn (Confusion Matrix Thô):")
print(confusion_matrix(y_test, y_pred))
print("=================================================================\n")

# 6. PHÂN TÍCH ẢNH HƯỞNG TRONG KINH DOANH (FEATURE IMPORTANCE)
importance = ai_model.feature_importances_
feature_importance_df = pd.DataFrame({'Thuộc tính': features_list, 'Mức độ ảnh hưởng (%)': importance * 100})
feature_importance_df = feature_importance_df.sort_values(by='Mức độ ảnh hưởng (%)', ascending=False)

print("--- 4. Độ quan trọng của các khía cạnh đối với tâm lý khách hàng ---")
print(feature_importance_df.head(5).to_string(index=False))
# =================================================================
# 6. ĐỒNG BỘ KỸ THUẬT: ĐÓNG GÓI MÔ HÌNH SANG FILE CỨNG .PKL ĐỂ LÊN GITHUB
# =================================================================
import pickle

print("\n--- 5. Đang tiến hành đóng gói mô hình Random Forest Classifier ---")
# Tên biến bắt buộc phải khớp hoàn toàn với 'ai_model' mà nhóm đang định nghĩa ở mục 4
with open('ai_sentiment_model.pkl', 'wb') as file:
    pickle.dump(ai_model, file)

print("🎉 ĐÃ XUẤT FILE THÀNH CÔNG: Tệp bộ não AI 'ai_sentiment_model.pkl' đã sẵn sàng trong thư mục dự án!")
