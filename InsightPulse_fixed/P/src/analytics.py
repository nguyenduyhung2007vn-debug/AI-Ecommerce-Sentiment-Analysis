# ============================================================
# src/analytics.py - Logic phân tích thuần (không phụ thuộc Streamlit)
# ============================================================
import numpy as np
import pandas as pd
import src.config as config
from src.pipeline import build_feature_frame, aspects_of, get_aspect_model, _any

ASPECTS = list(config.ASPECT_NAMES)


# ---------- Nhận diện cột ----------
def detect_columns(df):
    label_col = next((c for c in ("sentiment_llm", "sentiment", "label") if c in df.columns), None)
    text_col = None
    best = 0
    for c in df.columns:
        if df[c].dtype == object or str(df[c].dtype).startswith("str"):
            avg = df[c].astype(str).str.len().mean()
            if avg > best:
                best, text_col = avg, c
    if best < 15:       # cột chữ quá ngắn -> không phải nội dung review
        text_col = None
    return label_col, text_col


# ---------- Dự đoán ----------
def predict_one(model, text):
    X = build_feature_frame([text])
    vec = X.iloc[0].tolist()
    proba = dict(zip((int(c) for c in model.classes_), model.predict_proba(X)[0]))
    return {"text": text, "vector": vec, "X": X, "pred": int(model.predict(X)[0]),
            "proba": proba, "aspects": aspects_of(text)}


def predict_texts(model, texts):
    X = build_feature_frame(list(texts))
    out = pd.DataFrame({"review": list(texts)})
    out["pred"] = model.predict(X).astype(int)
    out["sentiment"] = out["pred"].map(config.LABELS)
    proba = model.predict_proba(X)
    for i, c in enumerate(model.classes_):
        out[f"p_{config.LABELS[int(c)]}"] = (proba[:, i] * 100).round(1)
    out["confidence_%"] = (proba.max(axis=1) * 100).round(1)
    return out, X


def occlusion_importance(model, X_row, baseline):
    """Độ giảm xác suất lớp dự đoán khi đưa từng đặc trưng về giá trị nền."""
    cls = int(model.predict(X_row)[0])
    idx = list(model.classes_).index(cls)
    base_p = model.predict_proba(X_row)[0][idx]
    rows = []
    for f in config.FEATURE_COLUMNS:
        alt = X_row.copy()
        alt[f] = baseline.get(f, 0.0)
        rows.append({"feature": f, "mô tả": config.FEATURE_DESC[f], "giá trị": float(X_row[f].iloc[0]),
                     "Đóng góp": round((base_p - model.predict_proba(alt)[0][idx]) * 100, 2)})
    return cls, base_p, pd.DataFrame(rows).sort_values("Đóng góp", key=abs, ascending=False)


def length_baseline(df=None):
    b = {}
    for f in ("review_len_char", "review_len_word", "avg_word_length"):
        b[f] = float(df[f].median()) if df is not None and f in df.columns else 0.0
    return b


# ---------- Thống kê tập dữ liệu ----------
def compute_metrics(df):
    label_col, text_col = detect_columns(df)
    total = len(df)
    if label_col:
        s = pd.to_numeric(df[label_col], errors="coerce")
        cnt = {k: int((s == k).sum()) for k in (0, 1, 2)}
    else:
        cnt = {0: 0, 1: 0, 2: 0}
    asp_scores, asp_counts = {}, []
    for a in ASPECTS:
        if a in df.columns:
            v = pd.to_numeric(df[a], errors="coerce").dropna()
            # Mã thực tế trong CSV: 0 = tiêu cực/không nhắc, 1 = trung lập, 2 = tích cực
            c0, c1, c2 = int((v == 0).sum()), int((v == 1).sum()), int((v == 2).sum())
            m = c1 + c2
            asp_scores[a] = c2 / m * 100 if m else None      # % tích cực trong các lượt nhắc có sắc thái
            asp_counts.append({"aspect": a, "Tiêu cực/Không nhắc": c0, "Trung lập": c1, "Tích cực": c2})
        else:
            asp_scores[a] = None
    return {
        "total_rows": total, "label_col": label_col, "text_col": text_col,
        "neg_count": cnt[0], "neu_count": cnt[1], "pos_count": cnt[2],
        "neg_ratio": cnt[0] / total * 100 if total else 0, "neu_ratio": cnt[1] / total * 100 if total else 0,
        "pos_ratio": cnt[2] / total * 100 if total else 0,
        "aspect_scores": asp_scores, "aspect_counts": pd.DataFrame(asp_counts),
    }


def aspect_sentiment_long(df, label_col):
    """Mỗi dòng: khía cạnh x cảm xúc tổng thể x số lượt nhắc (chỉ đếm khi khía cạnh được nhắc)."""
    rows = []
    s = pd.to_numeric(df[label_col], errors="coerce") if label_col else None
    for a in ASPECTS:
        if a not in df.columns:
            continue
        v = pd.to_numeric(df[a], errors="coerce")
        mentioned = v != 0
        for k, name in config.LABELS.items():
            n = int(((s == k) & mentioned).sum()) if s is not None else 0
            rows.append({"Khía cạnh": config.ASPECT_NAMES[a], "Cảm xúc": name, "Số review": n})
    return pd.DataFrame(rows)


def issue_table(df):
    """Tỷ lệ review tiêu cực trong các review có NHẮC tới khía cạnh (nhận diện bằng từ khóa trên nội dung),
    vì cột as_* trong CSV không phân biệt được 'tiêu cực' với 'không nhắc'."""
    label_col, text_col = detect_columns(df)
    if not (label_col and text_col):
        return pd.DataFrame(columns=["aspect", "Khía cạnh", "Lượt nhắc", "Tiêu cực", "Tỷ lệ tiêu cực %"])
    s = pd.to_numeric(df[label_col], errors="coerce")
    low = df[text_col].astype(str).str.lower()
    rows = []
    for a, kws in config.ASPECT_KEYWORDS.items():
        mentioned = low.map(lambda t: _any(t, kws))
        m = int(mentioned.sum())
        neg = int(((s == 0) & mentioned).sum())
        rows.append({"aspect": a, "Khía cạnh": config.ASPECT_NAMES[a], "Lượt nhắc": m, "Tiêu cực": neg,
                     "Tỷ lệ tiêu cực %": round(neg / m * 100, 1) if m else 0.0})
    return pd.DataFrame(rows).sort_values("Tỷ lệ tiêu cực %", ascending=False).reset_index(drop=True)


def flag_rates(df):
    out = []
    for f in ("kw_ship_cham", "kw_loi_san_pham", "kw_loi_dinh_kem", "kw_tieu_cuc_manh"):
        if f in df.columns:
            out.append({"feature": f, "Chỉ báo": config.FEATURE_DESC[f],
                        "Số review": int(pd.to_numeric(df[f], errors="coerce").fillna(0).gt(0).sum()),
                        "Tỷ lệ %": round(pd.to_numeric(df[f], errors="coerce").fillna(0).gt(0).mean() * 100, 2)})
    return pd.DataFrame(out)


ACTIONS = {
    "as_packaging": "Bọc màng co + chống sốc, dùng thùng carton đúng cỡ, kiểm tra ảnh đóng gói trước khi bàn giao.",
    "as_delivery": "Làm việc với đơn vị vận chuyển về SLA, cảnh báo đơn quá hạn, bổ sung ĐVVC dự phòng mùa cao điểm.",
    "as_physical": "Kiểm tra chất lượng (QC) tại kho: bìa, gáy sách, mực in; loại bỏ lô hàng lỗi vật lý.",
    "as_content": "Rà soát chất lượng bản dịch/biên tập, làm việc với nhà xuất bản về lỗi in thiếu/lặp trang.",
    "as_price": "Xem lại chính sách giá, voucher và so sánh giá đối thủ; truyền thông rõ giá trị nhận được.",
    "as_service": "Chuẩn hóa kịch bản CSKH, rút ngắn thời gian phản hồi, đơn giản hóa đổi trả.",
}


# ---------- Đánh giá mô hình ----------
def _metrics(y, pred):
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
    labels = [0, 1, 2]
    rep = pd.DataFrame(classification_report(y, pred, labels=labels, output_dict=True, zero_division=0)).T
    rep.index = [config.LABELS.get(int(i), i) if str(i).isdigit() else i for i in rep.index]
    cm = pd.DataFrame(confusion_matrix(y, pred, labels=labels),
                      index=[f"Thực tế: {config.LABELS[k]}" for k in labels],
                      columns=[f"Dự đoán: {config.LABELS[k]}" for k in labels])
    return {"n": len(y), "accuracy": accuracy_score(y, pred), "macro_f1": f1_score(y, pred, average="macro"),
            "weighted_f1": f1_score(y, pred, average="weighted"), "report": rep, "cm": cm}


def evaluate_model(model, df, label_col):
    """Đánh giá RF trên 21 cột đặc trưng có sẵn trong CSV."""
    missing = [c for c in config.FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Thiếu cột đặc trưng: " + ", ".join(missing))
    d = df[config.FEATURE_COLUMNS + [label_col]].copy()
    d[label_col] = pd.to_numeric(d[label_col], errors="coerce")
    d = d.dropna()
    return _metrics(d[label_col].astype(int), model.predict(d[config.FEATURE_COLUMNS]))


def evaluate_end_to_end(model, df, text_col, label_col):
    """Đánh giá toàn quy trình: nội dung văn bản -> pipeline -> RF (giống lúc người dùng nhập tay)."""
    d = df[[text_col, label_col]].dropna()
    X = build_feature_frame(list(d[text_col]))
    return _metrics(pd.to_numeric(d[label_col]).astype(int), model.predict(X))
