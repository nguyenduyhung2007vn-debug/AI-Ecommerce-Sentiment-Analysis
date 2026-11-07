import json
import pandas as pd

# 1. Trỏ trực tiếp tới đường dẫn trên ổ D của bạn
file_path = r"D:\projectAI\test_clean.JSON"

# 2. Đọc file JSON và chuyển sang DataFrame
with open(file_path, "r", encoding="utf-8") as f:
  data = json.load(f)

df = pd.DataFrame(data)

# 3. Xuất ra file CSV ngay tại thư mục projectAI
output_path = r"D:\projectAI\tiki_reviews_clean.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Đã chuyển đổi thành công! File CSV được lưu tại: {output_path}")
print("Kích thước dữ liệu:", df.shape)