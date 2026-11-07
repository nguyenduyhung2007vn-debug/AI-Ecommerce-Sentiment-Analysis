
📊 InsightPulse - Đồ Án Cuối Kỳ Trí Tuệ Nhân Tạo Trong Kinh Doanh


Khoa Thương mại Điện tử - Trường Đại học Kinh tế - Đại học Đà Nẵng (DUE)


📝 1. Tổng Quan Dự Án & Mục Tiêu Kinh Doanh

Dự án tập trung xây dựng một hệ thống Data Pipeline khép kín (End-to-End AI Pipeline) ứng dụng thuật toán học máy nâng cao để tự động hóa quy trình phân tích sắc thái phản hồi (Sentiment Analysis) của khách hàng trên sàn TMĐT.
Tri thức khai phá từ mô hình giúp doanh nghiệp định lượng chính xác trải nghiệm người dùng theo từng phòng ban/khía cạnh dựa trên bộ luật ngữ nghĩa thực tế (Aspect-Based Sentiment Analysis - ABSA), phát hiện sớm rủi ro vận hành (Giao hàng trễ, lỗi vật lý sách rách gáy, đóng gói cẩu thả) nhằm giảm thiểu tỷ lệ rời bỏ sàn (Churn Rate) của người mua.
• Thuật toán lõi: Random Forest Classifier (200 cây quyết định ngẫu nhiên).
• Độ chính xác mô hình (Accuracy): Đạt 79.70% trên tập dữ liệu kiểm thử thực tế bám sát phân phối nhãn.
• Hiệu năng lớp Tiêu cực (Lọc lỗi vận hành): Đạt F1-Score vượt trội 0.89.

📁 2. Cấu Trúc Thư Mục Dự Án Trên GitHub

Mã nguồn dự án được tổ chức mô-đun hóa cấu trúc, phân tách độc lập giữa tầng xử lý thuật toán ngầm (src/) và tầng giao diện hiển thị (dashboard/) để tối ưu hóa hiệu năng:
text
AI-Ecommerce-Sentiment-Analysis [Public]
├── src
│   ├── config.py                      # Cấu hình danh mục 4 trang và từ khóa ABSA
│   ├── data_loader.py                 # Bộ nạp dữ liệu và tiền tính toán lưu trực tiếp trên RAM
│   └── pipeline.py                    # Pipeline bóc tách tự động 21 cột thuộc tính toán học
├── dashboard
│   ├── dashboard_app.py               # File khởi chạy giao diện chính Tech Style nền tối
│   ├── engine.py                      # Bộ điều phối luồng kết xuất nội dung động
│   └── pages
│       ├── aspects_features.py        # TRANG 3 & 4: Lượng hóa khía cạnh ABSA & BI Insights
│       ├── business_insights.py       # TRANG 2: Analytics Dashboard số liệu thật 100%
│       └── prediction.py              # TRANG 1: Nhận diện Đa phương thức (Chữ + Video API)
├── ai_sentiment_model.pkl             # File cứng "bộ não" AI Random Forest (scikit-learn 1.5.2)
├── du_lieu_24_cols.csv                # Tập dữ liệu ma trận phân tích gốc (Tiki Book Reviews)
├── requirements.txt                   # Danh sách thư viện Python cần cài (Tối ưu hóa hình thức)
└── README.md                          # Hướng dẫn End-to-End AI Pipeline dự án
Hãy thận trọng khi sử dụng mã.

📊 3. Ma Trận 21 Thuộc Tính Toán Học Đầu Vào (Feature Columns)

Để đảm bảo thuật toán Random Forest đối chiếu ma trận không bị lỗi lệch pha (Feature Mismatch), vector trích xuất tự động thời gian thực từ văn bản và lời thoại video được đồng bộ nghiêm ngặt theo đúng cấu trúc nhị phân của bộ não AI bao gồm:
1. as_content, as_physical, as_price, as_packaging, as_delivery, as_service: Lượng hóa phân cực khía cạnh thực tế (-1: Chê, 0: Trung lập, 1: Khen) thay vì gán cứng 0.0.
2. review_len_char & review_len_word: Chỉ số thuộc tính đo độ dài câu.
3. avg_word_length: Độ dài ký tự trung bình của từ.
4. exclamation_count & question_count: Chỉ số cú pháp biểu cảm mạnh (!, ?).
5. contains_emoji_text & mention_star_rating: Trạng thái chuỗi văn bản đặc biệt.
6. kw_tieu_cuc_manh đến kw_loi_dinh_kem: 8 trường lọc trạng thái nhị phân từ khóa kinh doanh.

💻 4. Hướng Dẫn Cài Đặt Và Chạy Cục Bộ (Local Deployment)


Bước 1: Clone kho lưu trữ về máy tính

bash
git clone https://github.com
cd AI-Ecommerce-Sentiment-Analysis
Hãy thận trọng khi sử dụng mã.

Bước 2: Cài đặt các thư viện phụ trợ bắt buộc

Cài đặt môi trường ảo thông qua trình quản lý gói (Khuyến khích dùng môi trường ổn định Python 3.11):
bash
pip install -r requirements.txt
Hãy thận trọng khi sử dụng mã.

Bước 3: Khởi chạy trang Web Dashboard dự báo trên máy tính

bash
streamlit run dashboard/dashboard_app.py
Hãy thận trọng khi sử dụng mã.

🌐 5. Thông Tin Bản Phát Hành Trực Tuyến Công Khai

• Đường link sản phẩm Web App Demo (Streamlit Cloud): https://streamlit.app
• Quy mô hệ thống: Tích hợp trọn vẹn 4 Phân hệ trang hiển thị chuyên sâu bám sát số liệu thật. Tốc độ phản hồi và chuyển đổi menu đạt mức tối ưu dưới 0.1 giây nhờ cơ chế Global Pre-computation nạp dữ liệu trực tiếp trên thanh RAM máy chủ đám mây.
• Fix lỗi logic: Ép kiểu mảng dữ liệu dự đoán int() chống lỗi Truth value of an array is ambiguous của mảng NumPy.