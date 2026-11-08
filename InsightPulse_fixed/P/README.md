# 📊 InsightPulse — Phân tích cảm xúc review TMĐT (Random Forest + ABSA)

Dashboard Streamlit **20 trang** (đa trang bằng `st.navigation`), dự đoán từ văn bản / video, hiển thị mô hình và số liệu.

## Cấu trúc
```
src/            config.py · pipeline.py · analytics.py · data_loader.py · media.py
dashboard/      dashboard_app.py · engine.py (đăng ký 20 trang) · views/*.py
ai_sentiment_model.pkl · du_lieu_24_cols.csv (tự thêm) · requirements.txt · packages.txt
```

## 20 trang
| Nhóm | Trang |
|---|---|
| Dự đoán AI | văn bản · **video (upload)** · hàng loạt (CSV) · giải thích dự đoán · lịch sử |
| Tổng quan | KPI · phân phối cảm xúc · khám phá dữ liệu · chất lượng dữ liệu |
| ABSA | điểm khía cạnh · heatmap khía cạnh×cảm xúc · so sánh · từ khóa |
| Mô hình | thông tin · độ quan trọng đặc trưng · đánh giá (Acc/P/R/F1, confusion matrix) · What-if |
| Kinh doanh | vấn đề vận hành · đề xuất hành động · báo cáo & xuất file |

## Lưu ý kỹ thuật (đã đối chiếu với `du_lieu_24_cols.csv`)
- Cột `as_*` trong CSV mã hóa **0 = tiêu cực/không nhắc, 1 = trung lập, 2 = tích cực** (không phải -1/0/1 như README cũ). Pipeline cũ đưa giá trị -1 mà mô hình chưa từng thấy.
- `avg_word_length` = tổng độ dài các từ / số từ (pipeline cũ tính cả khoảng trắng); đặc trưng `kw_*` khớp chuỗi con. Nay 15 đặc trưng không-khía-cạnh khớp 100% với CSV.
- `as_*` do LLM gán nên luật từ khóa không tái tạo được. `train_aspect_model.py` huấn luyện bộ nhận diện khía cạnh (TF-IDF + Logistic Regression) -> `aspect_model.pkl`; ước lượng end-to-end bằng cross-validation ≈ 76% (luật từ khóa ≈ 69%; dùng nhãn khía cạnh thật ≈ 92,5%).
- Trang *Vấn đề vận hành* tính tỷ lệ review tiêu cực trong các review nhắc tới từng khía cạnh (theo từ khóa trên nội dung), vì `as_*` không tách được "tiêu cực" khỏi "không nhắc".

## Chạy
```bash
python -m venv venv && venv\Scripts\activate   # Python 3.11 khuyến nghị
pip install -r requirements.txt
streamlit run dashboard/dashboard_app.py
```
Đặt `du_lieu_24_cols.csv` ở thư mục gốc (hoặc tải lên trong ứng dụng). Streamlit Cloud: giữ `packages.txt` (ffmpeg).
