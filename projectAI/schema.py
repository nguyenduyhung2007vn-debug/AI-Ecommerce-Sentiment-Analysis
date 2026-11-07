import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập phông chữ để hiển thị tiếng Việt không bị lỗi ô vuông
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("--- ĐANG TIẾN HÀNH TẠO 3 BIỂU ĐỒ CHO SLIDE DỰ ÁN ---")

# =================================================================
# BIỂU ĐỒ 1: MA TRẬN NHẦM LẪN (CONFUSION MATRIX HEATMAP)
# =================================================================
# Dữ liệu ma trận thô từ log chạy Thonny của nhóm
cm_data = np.array([[180,  13,   5],
                    [ 18,  31,  20],
                    [  7,  18, 107]])

classes = ['0: Tiêu cực', '1: Trung lập', '2: Tích cực']
df_cm = pd.DataFrame(cm_data, index=classes, columns=classes)

plt.figure(figsize=(8, 6))
sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            annot_kws={'size': 14, 'weight': 'bold'})

plt.title('Ma Trận Nhầm Lẫn Mô Hình AI (Confusion Matrix)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Mô Hình AI Dự Đoán', fontsize=12, labelpad=10)
plt.ylabel('Sắc Thái Thực Tế', fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig('1_confusion_matrix.png', dpi=300)
plt.close()
print("-> Đã xuất biểu đồ 1: '1_confusion_matrix.png'")

# =================================================================
# BIỂU ĐỒ 2: ĐỘ QUAN TRỌNG CỦA THUỘC TÍNH (FEATURE IMPORTANCE)
# =================================================================
# Dữ liệu độ quan trọng từ thuật toán Random Forest của nhóm
importance_data = {
    'Feature': ['Nội dung (as_content)', 'Hình thức (as_physical)', 'Độ dài ký tự (review_len_char)', 
                'Độ dài từ (review_len_word)', 'Độ dài từ TB (avg_word_length)'],
    'Importance': [24.757159, 15.066722, 11.492080, 10.642574, 8.072639]
}
df_importance = pd.DataFrame(importance_data).sort_values(by='Importance', ascending=True)

plt.figure(figsize=(10, 5))
colors = sns.color_palette('viridis', len(df_importance))
bars = plt.barh(df_importance['Feature'], df_importance['Importance'], color=colors)

# Thêm số phần trăm vào đầu mỗi thanh biểu đồ
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
             va='center', ha='left', fontsize=11, fontweight='bold')

plt.title('Top 5 Thuộc Tính Quyết Định Sắc Thái Khách Hàng', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Mức độ ảnh hưởng (%)', fontsize=12)
plt.xlim(0, 28)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('2_feature_importance.png', dpi=300)
plt.close()
print("-> Đã xuất biểu đồ 2: '2_feature_importance.png'")

# =================================================================
# BIỂU ĐỒ 3: TỔNG QUAN PHÂN PHỐI SẮC THÁI DỮ LIỆU (SENTIMENT DISTRIBUTION)
# =================================================================
# Tính toán tổng mẫu dựa trên tập Train (1594) + Test (399) = 1993 mẫu theo tỷ lệ log
sentiment_counts = {
    'Sắc thái': ['0: Tiêu cực', '2: Tích cực', '1: Trung lập'],
    'Số lượng': [988, 658, 347]  # Phân bổ tỷ lệ mẫu tương ứng dữ liệu của nhóm
}
df_sentiment = pd.DataFrame(sentiment_counts)

plt.figure(figsize=(7, 5))
ax = sns.barplot(x='Sắc thái', y='Số lượng', data=df_sentiment, palette='Set2')

# Ghi số lượng mẫu lên đầu mỗi cột
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())} mẫu', (p.get_x() + p.get_width() / 2., p.get_height() + 15),
                ha='center', va='center', fontsize=11, fontweight='bold', color='black')

plt.title('Phân Phối Sắc Thái Bình Luận Trong Tập Dữ Liệu', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Nhóm sắc thái cảm xúc', fontsize=12)
plt.ylabel('Số lượng bình luận', fontsize=12)
plt.ylim(0, 1100)
plt.tight_layout()
plt.savefig('3_sentiment_distribution.png', dpi=300)
plt.close()
print("-> Đã xuất biểu đồ 3: '3_sentiment_distribution.png'")
print("\n--- HOÀN TẤT TẠO ẢNH! NHÓM CÓ THỂ LẤY 3 FILE ẢNH TRONG THƯ MỤC ĐỂ CHÈN VÀO SLIDE ---")
