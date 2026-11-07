# 📊 InsightPulse - Đồ Án Cuối Kỳ Trí Tuệ Nhân Tạo Trong Kinh Doanh
### Khoa Thương mại Điện tử - Trường Đại học Kinh tế - Đại học Đà Nẵng (DUE)

---

## 📝 1. Tổng Quan Dự Án & Mục Tiêu Kinh Doanh
Dự án tập trung xây dựng một hệ thống **Data Pipeline khép kín (End-to-End AI Pipeline)** ứng dụng thuật toán học máy nâng cao để tự động hóa quy trình phân tích sắc thái phản hồi (Sentiment Analysis) của khách hàng trên sàn TMĐT. 

Tri thức khai phá từ mô hình giúp doanh nghiệp định lượng chính xác trải nghiệm người dùng theo từng phòng ban/khía cạnh khép kín (Aspect-Based Sentiment Analysis), phát hiện sớm rủi ro vận hành (Giao hàng trễ, lỗi vật lý sách rách gáy, in mất trang) nhằm giảm thiểu tỷ lệ rời bỏ sàn (Churn Rate) của người mua.

*   **Thuật toán lõi:** Random Forest Classifier (200 cây quyết định ngẫu nhiên).
*   **Độ chính xác mô hình (Accuracy):** đạt **79.70%** trên tập dữ liệu kiểm thử thực tế.
*   **Hiệu năng lớp Tiêu cực (Lọc lỗi vận hành):** Đạt F1-Score vượt trội **0.89**.

---

## 📁 2. Cấu Trúc Thư Mục Dự Án Trên GitHub
Mã nguồn dự án được tổ chức mô-đun hóa chuyên nghiệp, phân tách độc lập giữa tầng xử lý toán học ngầm (`src/`) và tầng giao diện hiển thị (`dashboard/`):

```text
AI_Ecommerce_Sentiment/
│
├── src/                               # Tầng xử lý logic thuật toán ngầm
│   ├── config.py                      # Định nghĩa từ khóa đặc trưng và cấu trúc 20 trang
│   ├── pipeline.py                    # Pipeline tự động trích xuất ma trận thuộc tính 21 cột
│   └── data_loader.py                 # Tải tài nguyên nhị phân tối ưu hóa qua bộ nhớ đệm Cache
│
├── dashboard/                         # Tầng giao diện người dùng tương tác
│   ├── app.py                         # File khởi chạy giao diện Web nền tối và Sidebar Menu
│   ├── engine.py                      # Bộ điều phối luồng kết xuất nội dung động
│   └── pages/                         # Phân hệ chi tiết cấu trúc các trang hiển thị
│       ├── prediction.py              # TRANG 1: Phân hệ kiểm thử và dự báo thời gian thực
│       ├── business_insights.py       # TRANG 2: Phân hệ Analytics Dashboard thống kê vĩ mô
│       └── aspects_features.py        # TRANG 3->20: Phân hệ lượng hóa chi tiết thuộc tính
│
├── ai_sentiment_model.pkl             # File cứng "bộ não" AI đóng gói dạng nhị phân
├── du_lieu_24_cols.csv                # File tập dữ liệu ma trận phân tích hệ thống gốc
├── requirements.txt                   # File cấu hình môi trường ảo máy chủ đám mây
└── README.md                          # File hướng dẫn và giải trình kỹ thuật hệ thống
```

---

## 📊 3. Ma Trận 21 Thuộc Tính Toán Học Đầu Vào (Feature Columns)
Để đảm bảo thuật toán Random Forest đối chiếu ma trận không bị lỗi lệch pha (`Feature Mismatch`), vector trích xuất tự động thời gian thực từ câu văn bản thô được đồng bộ nghiêm ngặt theo đúng cấu trúc nhị phân của bộ não AI bao gồm:
1.  `as_content` đến `as_service`: 6 cột chỉ số khía cạnh phòng ban hệ thống.
2.  `review_len_char` & `review_len_word`: Chỉ số thuộc tính đo độ dài câu.
3.  `avg_word_length`: Độ dài ký tự trung bình của từ.
4.  `exclamation_count` & `question_count`: Chỉ số cú pháp biểu cảm mạnh (`!`, `?`).
5.  `contains_emoji_text` & `mention_star_rating`: Trạng thái chuỗi văn bản đặc biệt.
6.  `kw_tieu_cuc_manh` đến `kw_loi_dinh_kem`: 8 trường lọc trạng thái nhị phân từ khóa kinh doanh.

---

## 💻 4. Hướng Dẫn Cài Đặt Và Chạy Cục Bộ (Local Deployment)

### Bước 1: Clone kho lưu trữ về máy tính
```bash
git clone https://github.com
cd AI_Ecommerce_Sentiment
```

### Bước 2: Cài đặt các thư viện phụ trợ bắt buộc
Nhóm có thể cài đặt môi trường ảo thông qua file cấu hình phần mềm:
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi chạy trang Web Dashboard dự báo trên máy tính
```bash
streamlit run dashboard/app.py
```

---

## 🌐 5. Thông Tin Bản Phát Hành Trực Tuyến Công Khai
*   **Đường link sản phẩm Web App Demo (Streamlit Cloud):** `https://streamlit.app`
*   **Quy mô hệ thống:** Tích hợp trọn vẹn **20 trang hiển thị biệt lập**, đảm bảo xử lý toàn diện **ít nhất 8 thành phần chức năng (Features)** cho mỗi module trang.

---
*Dự án được xây dựng và nộp đúng hạn định trước 18h00 ngày 16/11/2026 dưới sự hướng dẫn của thầy Trần Văn Lộc - Khoa Thương mại Điện tử DUE.*
