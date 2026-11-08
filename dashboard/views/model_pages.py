import altair as alt
import pandas as pd
import streamlit as st
import sklearn
import src.config as config
from src import analytics as A
from src.data_loader import read_csv_any
from dashboard.views import common as C


# ---------------- Trang 14 ----------------
def page_info(ctx):
    st.title("🤖 Thông tin mô hình")
    m = ctx["model"]
    a, b, c, d = st.columns(4)
    a.metric("Thuật toán", type(m).__name__.replace("Classifier", ""))
    b.metric("Số cây", getattr(m, "n_estimators", "?"))
    c.metric("Số đặc trưng", getattr(m, "n_features_in_", "?"))
    d.metric("Số lớp", len(m.classes_))
    st.write(f"Lớp: {[config.LABELS.get(int(k), k) for k in m.classes_]} | scikit-learn đang chạy: `{sklearn.__version__}`")
    if hasattr(m, "get_params"):
        st.subheader("Siêu tham số")
        st.dataframe(pd.DataFrame({"Tham số": list(m.get_params()), "Giá trị": [str(v) for v in m.get_params().values()]}),
                     hide_index=True)
    depths = [e.get_depth() for e in m.estimators_]
    leaves = [e.get_n_leaves() for e in m.estimators_]
    st.write(f"Độ sâu cây: TB {sum(depths) / len(depths):.1f}, tối đa {max(depths)} | "
             f"Số lá TB: {sum(leaves) / len(leaves):.0f}")
    am = __import__("src.pipeline", fromlist=["x"]).get_aspect_model()
    if am:
        st.success(f"Bộ nhận diện khía cạnh (aspect_model.pkl) đang hoạt động — huấn luyện trên {am['meta']['n_train']:,} review; "
                   f"ước lượng end-to-end bằng cross-validation: {am['meta']['cv_end_to_end_accuracy'] * 100:.1f}% accuracy.")
    else:
        st.warning("Chưa có aspect_model.pkl: khía cạnh được nhận diện bằng luật từ khóa (kém chính xác hơn). Chạy `python train_aspect_model.py`.")
    st.info("Mô hình được pin `scikit-learn==1.9.1` trong requirements.txt để tương thích file .pkl.")


# ---------------- Trang 15 ----------------
def page_importance(ctx):
    st.title("📌 Độ quan trọng đặc trưng")
    m = ctx["model"]
    imp = pd.DataFrame({"feature": config.FEATURE_COLUMNS, "mô tả": [config.FEATURE_DESC[f] for f in config.FEATURE_COLUMNS],
                        "importance %": (m.feature_importances_ * 100).round(2)}).sort_values("importance %", ascending=False)
    st.altair_chart(alt.Chart(imp).mark_bar(color="#4F46E5").encode(
        x="importance %:Q", y=alt.Y("feature:N", sort=None), tooltip=["mô tả", "importance %"]).properties(height=520),
        )
    groups = {"Khía cạnh": config.FEATURE_COLUMNS[:6], "Độ dài": config.FEATURE_COLUMNS[6:9],
              "Cú pháp": config.FEATURE_COLUMNS[9:13], "Từ khóa": config.FEATURE_COLUMNS[13:]}
    g = pd.DataFrame({"Nhóm": list(groups), "importance %": [imp[imp.feature.isin(v)]["importance %"].sum().round(2) for v in groups.values()]})
    st.subheader("Theo nhóm đặc trưng")
    st.bar_chart(g.set_index("Nhóm"))
    st.dataframe(imp, hide_index=True)


# ---------------- Trang 16 ----------------
def page_eval(ctx):
    st.title("🧮 Đánh giá mô hình")
    st.warning("Nếu tập dữ liệu đã dùng để huấn luyện, kết quả sẽ cao hơn thực tế. Chỉ số báo cáo chính thức nên lấy trên "
               "tập kiểm thử độc lập — bạn có thể tải riêng bên dưới.")
    src = st.radio("Tập đánh giá", ["Dữ liệu đang nạp (21 đặc trưng có sẵn)", "Toàn quy trình từ nội dung văn bản", "Tải tập kiểm thử riêng"], horizontal=True)
    df, lab = ctx["df"], ctx["label_col"]
    if src.startswith("Tải"):
        up = st.file_uploader("CSV kiểm thử (đủ 21 cột đặc trưng + sentiment_llm)", type=["csv"], key="eval_up")
        if up is None:
            return
        df = read_csv_any(up)
        lab, _ = A.detect_columns(df)
    else:
        C.require_labels(ctx)
    if not lab:
        st.error("Không tìm thấy cột nhãn.")
        return
    try:
        if src.startswith("Toàn"):
            if not ctx["text_col"]:
                st.error("Không có cột nội dung review.")
                return
            st.info("Chạy lại pipeline trên nội dung gốc (khía cạnh do aspect_model dự đoán). Vì aspect_model được huấn luyện từ chính CSV này nên kết quả hơi lạc quan; "
                    "ước lượng cross-validation xem ở trang Thông tin mô hình.")
            ev = A.evaluate_end_to_end(ctx["model"], df, ctx["text_col"], lab)
        else:
            ev = A.evaluate_model(ctx["model"], df, lab)
    except Exception as e:
        st.error(f"Không đánh giá được: {e}")
        return
    a, b, c, d = st.columns(4)
    a.metric("Số mẫu", f"{ev['n']:,}")
    b.metric("Accuracy", f"{ev['accuracy'] * 100:.2f}%")
    c.metric("Macro F1", f"{ev['macro_f1'] * 100:.2f}%")
    d.metric("Weighted F1", f"{ev['weighted_f1'] * 100:.2f}%")
    st.subheader("Precision / Recall / F1 theo lớp")
    st.dataframe(ev["report"].round(3))
    st.subheader("Ma trận nhầm lẫn")
    cm = ev["cm"].reset_index().melt(id_vars="index", var_name="Dự đoán", value_name="Số mẫu").rename(columns={"index": "Thực tế"})
    base = alt.Chart(cm).encode(x=alt.X("Dự đoán:N", sort=None), y=alt.Y("Thực tế:N", sort=None))
    st.altair_chart(base.mark_rect().encode(color=alt.Color("Số mẫu:Q", scale=alt.Scale(scheme="blues"))).properties(height=300)
                    + base.mark_text(color="white").encode(text="Số mẫu:Q"))


# ---------------- Trang 17 ----------------
def page_whatif(ctx):
    st.title("🎛️ Mô phỏng What-if")
    st.write("Điều chỉnh trực tiếp 21 đặc trưng để xem mô hình phản ứng thế nào.")
    cols = st.columns(3)
    vals = {}
    for i, f in enumerate(config.FEATURE_COLUMNS):
        with cols[i % 3]:
            if f.startswith("as_"):
                vals[f] = st.select_slider(config.FEATURE_DESC[f].replace(" (-1/0/1)", ""), [0, 1, 2], value=0, key=f"wi_{f}",
                                           format_func=lambda v: {0: "0 · Tiêu cực/không nhắc", 1: "1 · Trung lập", 2: "2 · Tích cực"}[v])
            elif f.startswith("kw_") or f in ("contains_emoji_text", "mention_star_rating"):
                vals[f] = int(st.checkbox(config.FEATURE_DESC[f], key=f"wi_{f}"))
            elif f == "avg_word_length":
                vals[f] = st.slider(config.FEATURE_DESC[f], 1.0, 12.0, 4.5, 0.1, key=f"wi_{f}")
            elif f in ("exclamation_count", "question_count"):
                vals[f] = st.slider(config.FEATURE_DESC[f], 0, 10, 0, key=f"wi_{f}")
            else:
                vals[f] = st.slider(config.FEATURE_DESC[f], 0, 1000 if f == "review_len_char" else 200,
                                    120 if f == "review_len_char" else 25, key=f"wi_{f}")
    X = pd.DataFrame([vals], columns=config.FEATURE_COLUMNS)
    pred = int(ctx["model"].predict(X)[0])
    proba = dict(zip((int(c) for c in ctx["model"].classes_), ctx["model"].predict_proba(X)[0]))
    st.divider()
    C.show_result({"pred": pred, "proba": proba})
