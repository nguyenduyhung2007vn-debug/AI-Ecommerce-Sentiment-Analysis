# 📊 InsightPulse - Đồ Án Cuối Kỳ Trí Tuệ Nhân Tạo Trong Kinh Doanh

**Khoa Thương mại Điện tử - Trường Đại học Kinh tế - Đại học Đà Nẵng (DUE)**

---

## 📝 1. Tổng Quan Dự Án & Mục Tiêu Kinh Doanh

Dự án tập trung xây dựng một hệ thống Data Pipeline (End-to-End AI Pipeline) ứng dụng các thuật toán học máy để tự động hóa quy trình phân tích sắc thái phản hồi (Sentiment Analysis) của khách hàng trên sàn thương mại điện tử.

Tri thức khai phá từ mô hình hỗ trợ doanh nghiệp định lượng trải nghiệm người dùng theo từng khía cạnh thông qua phương pháp Aspect-Based Sentiment Analysis (ABSA), từ đó nhận diện các vấn đề vận hành như giao hàng trễ, sản phẩm bị lỗi vật lý, sách rách gáy hoặc đóng gói chưa cẩn thận. Những thông tin này là cơ sở hỗ trợ doanh nghiệp cải thiện chất lượng dịch vụ và hạn chế nguy cơ khách hàng rời bỏ nền tảng (Customer Churn).

**Thông tin mô hình AI:**
- **Thuật toán lõi:** Random Forest Classifier.
- **Quy mô mô hình:** 100 cây quyết định (Decision Trees) theo cấu hình của mô hình đã lưu.
- **Số lượng đặc trưng đầu vào:** 21 Features.
- **Các lớp dự đoán:** Tiêu cực (Negative), Trung lập (Neutral), Tích cực (Positive).
- **Mục tiêu:** Phân loại cảm xúc phản hồi khách hàng và hỗ trợ phân tích các vấn đề kinh doanh.

*Lưu ý: Các chỉ số Accuracy, Precision, Recall và F1-Score cần được cập nhật từ kết quả đánh giá thực nghiệm trên tập kiểm thử của dự án.*

## 📁 2. Cấu Trúc Thư Mục Dự Án Trên GitHub

Mã nguồn được tổ chức theo kiến trúc mô-đun hóa, phân tách giữa tầng xử lý thuật toán (src/) và tầng giao diện hiển thị (dashboard/), giúp quản lý và phát triển hệ thống thuận tiện hơn.

```text
AI-Ecommerce-Sentiment-Analysis/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   └── pipeline.py
│
├── dashboard/
│   ├── __init__.py
│   ├── dashboard_app.py
│   ├── engine.py
│   └── pages/
│       ├── __init__.py
│       ├── aspects_features.py
│       ├── business_insights.py
│       └── prediction.py
│
├── ai_sentiment_model.pkl
├── du_lieu_24_cols.csv
├── requirements.txt
└── README.md
```

**Chức năng các thành phần:**

- `src/config.py`: Cấu hình đường dẫn dữ liệu, danh sách đặc trưng và từ khóa phục vụ phân tích.
- `src/data_loader.py`: Tải mô hình AI, đọc dữ liệu CSV và tính toán các chỉ số thống kê.
- `src/pipeline.py`: Chuyển đổi nội dung đánh giá thành vector đặc trưng đầu vào cho mô hình.
- `dashboard/dashboard_app.py`: File khởi chạy giao diện chính của hệ thống.
- `dashboard/engine.py`: Bộ điều phối và kết xuất các phân hệ chức năng.
- `dashboard/pages/prediction.py`: Giao diện dự đoán cảm xúc từ văn bản và hỗ trợ nhận diện lời thoại video khi các thư viện cần thiết khả dụng.
- `dashboard/pages/business_insights.py`: Phân hệ phân tích tổng quan kinh doanh.
- `dashboard/pages/aspects_features.py`: Phân hệ phân tích các khía cạnh và đặc trưng đánh giá.

**Các tệp tài nguyên chính:**

- `ai_sentiment_model.pkl`: Mô hình Random Forest Classifier đã huấn luyện và lưu trữ.
- `du_lieu_24_cols.csv`: Tập dữ liệu phục vụ phân tích và thống kê.
- `requirements.txt`: Danh sách thư viện Python cần thiết để triển khai hệ thống.

## 📊 3. Ma Trận 21 Thuộc Tính Toán Học Đầu Vào (Feature Columns)

Để đảm bảo vector đầu vào tương thích với mô hình Random Forest, hệ thống sử dụng 21 đặc trưng được tổ chức theo đúng tên và thứ tự đã xác định trong quá trình huấn luyện.

Các đặc trưng được chia thành những nhóm sau:

**Nhóm 1: Đặc trưng khía cạnh (Aspect Features) – 6 thuộc tính**

1. `as_content`: Chất lượng nội dung sản phẩm.
2. `as_physical`: Tình trạng vật lý sản phẩm.
3. `as_price`: Giá cả sản phẩm.
4. `as_packaging`: Chất lượng đóng gói.
5. `as_delivery`: Chất lượng giao hàng.
6. `as_service`: Chất lượng dịch vụ.

Các đặc trưng này được biểu diễn theo quy ước:
- `-1`: Tiêu cực.
- `0`: Trung lập hoặc không phát hiện đề cập.
- `1`: Tích cực.

**Nhóm 2: Đặc trưng độ dài văn bản – 3 thuộc tính**

7. `review_len_char`: Số lượng ký tự trong đánh giá.
8. `review_len_word`: Số lượng từ trong đánh giá.
9. `avg_word_length`: Độ dài trung bình của từ.

**Nhóm 3: Đặc trưng cú pháp và biểu cảm – 4 thuộc tính**

10. `exclamation_count`: Số lượng dấu chấm than.
11. `question_count`: Số lượng dấu hỏi.
12. `contains_emoji_text`: Trạng thái xuất hiện biểu tượng cảm xúc.
13. `mention_star_rating`: Trạng thái đề cập đến số sao đánh giá.

**Nhóm 4: Đặc trưng từ khóa ngữ nghĩa – 8 thuộc tính**

14. `kw_tieu_cuc_manh`: Từ khóa tiêu cực mạnh.
15. `kw_tieu_cuc_nhe`: Từ khóa tiêu cực nhẹ.
16. `kw_tich_cuc_manh`: Từ khóa tích cực mạnh.
17. `kw_tich_cuc_nhe`: Từ khóa tích cực nhẹ.
18. `kw_ship_nhanh`: Từ khóa liên quan đến giao hàng nhanh.
19. `kw_ship_cham`: Từ khóa liên quan đến giao hàng chậm.
20. `kw_loi_san_pham`: Từ khóa liên quan đến lỗi sản phẩm.
21. `kw_loi_dinh_kem`: Từ khóa liên quan đến lỗi hoặc vấn đề đi kèm.

**Nguyên tắc đồng bộ:** Vector đặc trưng đầu vào phải bảo đảm đủ 21 thuộc tính, đúng tên, đúng thứ tự và đúng kiểu dữ liệu tương thích với mô hình đã huấn luyện.

## 💻 4. Hướng Dẫn Cài Đặt Và Chạy Cục Bộ (Local Deployment)

**Bước 1: Clone kho lưu trữ về máy tính**

Mở Terminal hoặc Command Prompt:

```bash
git clone <GITHUB_REPOSITORY_URL>
cd AI-Ecommerce-Sentiment-Analysis
```

Thay `<GITHUB_REPOSITORY_URL>` bằng địa chỉ repository GitHub thực tế.

**Bước 2: Tạo môi trường Python và cài đặt thư viện**

Khuyến nghị sử dụng Python 3.11 và môi trường ảo để hạn chế xung đột thư viện.

```bash
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

Cài đặt các thư viện:

```bash
pip install -r requirements.txt
```

**Bước 3: Khởi chạy Dashboard**

Tại thư mục gốc dự án, thực hiện:

```bash
streamlit run dashboard/dashboard_app.py
```

Sau khi khởi chạy thành công, Streamlit sẽ cung cấp địa chỉ truy cập ứng dụng trên trình duyệt, thông thường là:

```text
http://localhost:8501
```

**Lưu ý:** Cần bảo đảm các tệp `ai_sentiment_model.pkl` và `du_lieu_24_cols.csv` nằm đúng vị trí theo cấu hình trong `src/config.py`.

## 🌐 5. Thông Tin Bản Phát Hành Trực Tuyến Công Khai

**Nền tảng triển khai:** Streamlit Community Cloud.

**Đường dẫn ứng dụng Demo:** Cập nhật URL Streamlit Cloud thực tế sau khi triển khai thành công.

**Quy mô hệ thống:**
- Tích hợp 4 phân hệ chức năng theo bộ điều phối Engine.
- Sử dụng mô hình Random Forest để dự đoán sắc thái đánh giá.
- Hỗ trợ phân tích dữ liệu đánh giá khách hàng từ tập dữ liệu CSV.
- Sử dụng cơ chế caching của Streamlit để tối ưu việc tải mô hình và dữ liệu.
- Cung cấp giao diện trực quan hỗ trợ theo dõi kết quả phân tích và thông tin kinh doanh.

**Các cải tiến kỹ thuật:**

- Chuẩn hóa đường dẫn tài nguyên bằng `pathlib` để hỗ trợ triển khai trên nhiều môi trường.
- Sử dụng `st.cache_resource` để lưu mô hình AI đã tải trong bộ nhớ.
- Sử dụng `st.cache_data` để hạn chế việc đọc và tính toán lại dữ liệu CSV không cần thiết.
- Chuẩn hóa kết quả dự đoán bằng cách ép kiểu về số nguyên:

```python
pred_class = int(ai_model_object.predict(df_predict)[0])
```

Cách xử lý này giúp tránh lỗi so sánh trực tiếp mảng NumPy với giá trị vô hướng trong câu lệnh điều kiện.

---

**InsightPulse – AI-Powered E-commerce Customer Review Intelligence**

*Ứng dụng trí tuệ nhân tạo trong phân tích cảm xúc khách hàng và hỗ trợ ra quyết định kinh doanh.*