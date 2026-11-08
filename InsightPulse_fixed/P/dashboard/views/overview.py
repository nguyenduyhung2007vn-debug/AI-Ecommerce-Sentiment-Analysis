import altair as alt
import pandas as pd
import streamlit as st
import src.config as config
from dashboard.views import common as C


# ---------------- Trang 6 ----------------
def page_kpi(ctx):
    st.title("📊 Tổng quan KPI")
    C.require_labels(ctx)
    m = ctx["metrics"]
    st.caption(f"Nguồn dữ liệu: {ctx['source']}")
    a, b, c, d = st.columns(4)
    a.metric("TỔNG PHẢN HỒI", f"{m['total_rows']:,}")
    b.metric("TÍCH CỰC", f"{m['pos_ratio']:.1f}%")
    c.metric("TRUNG LẬP", f"{m['neu_ratio']:.1f}%")
    d.metric("TIÊU CỰC", f"{m['neg_count']:,} ({m['neg_ratio']:.1f}%)")
    st.divider()
    st.altair_chart(C.sentiment_bar(C.dist_frame(m), "Cảm xúc", "Tỷ lệ %"))
    sc = {config.ASPECT_NAMES[k]: v for k, v in m["aspect_scores"].items() if v is not None}
    if sc:
        best, worst = max(sc, key=sc.get), min(sc, key=sc.get)
        st.success(f"Khía cạnh tốt nhất: **{best}** ({sc[best]:.1f}/100)")
        st.error(f"Khía cạnh cần cải thiện nhất: **{worst}** ({sc[worst]:.1f}/100)")


# ---------------- Trang 7 ----------------
def page_distribution(ctx):
    st.title("🥧 Phân phối cảm xúc")
    C.require_labels(ctx)
    m, df, lab = ctx["metrics"], ctx["df"], ctx["label_col"]
    d = C.dist_frame(m)
    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(alt.Chart(d).mark_arc(innerRadius=60).encode(
            theta="Số review:Q", color=alt.Color("Cảm xúc:N", scale=C.COLOR_SCALE),
            tooltip=["Cảm xúc", "Số review", "Tỷ lệ %"]).properties(height=320))
    with c2:
        st.dataframe(d.round(2), hide_index=True)
    st.subheader("Độ dài review trung bình theo cảm xúc")
    if "review_len_word" in df.columns:
        g = df.assign(**{"Cảm xúc": pd.to_numeric(df[lab], errors="coerce").map(config.LABELS)}) \
              .groupby("Cảm xúc")["review_len_word"].mean().reindex(["Tiêu cực", "Trung lập", "Tích cực"]).reset_index()
        g.columns = ["Cảm xúc", "Số từ TB"]
        st.altair_chart(C.sentiment_bar(g, "Cảm xúc", "Số từ TB", height=260))


# ---------------- Trang 8 ----------------
def page_explorer(ctx):
    st.title("🗂️ Khám phá dữ liệu")
    C.require_data(ctx)
    df, lab, txt = ctx["df"], ctx["label_col"], ctx["text_col"]
    f1, f2 = st.columns([1, 2])
    pick = f1.multiselect("Lọc cảm xúc", list(config.LABELS.values()), default=list(config.LABELS.values())) if lab else None
    q = f2.text_input("Tìm trong nội dung") if txt else ""
    view = df
    if lab and pick is not None:
        view = view[pd.to_numeric(view[lab], errors="coerce").map(config.LABELS).isin(pick)]
    if txt and q:
        view = view[view[txt].astype(str).str.contains(q, case=False, na=False, regex=False)]
    st.caption(f"{len(view):,} / {len(df):,} dòng")
    st.dataframe(view, height=480)
    C.download_df(view, "du_lieu_loc.csv")


# ---------------- Trang 9 ----------------
def page_quality(ctx):
    st.title("🧪 Chất lượng dữ liệu")
    C.require_data(ctx)
    df = ctx["df"]
    a, b, c = st.columns(3)
    a.metric("Số dòng", f"{len(df):,}")
    b.metric("Số cột", len(df.columns))
    c.metric("Dòng trùng lặp", f"{int(df.duplicated().sum()):,}")
    miss = df.isna().sum().rename("Thiếu").to_frame()
    miss["Thiếu %"] = (miss["Thiếu"] / len(df) * 100).round(2)
    miss["Kiểu"] = df.dtypes.astype(str)
    st.subheader("Giá trị thiếu theo cột")
    st.dataframe(miss)
    need = [x for x in config.FEATURE_COLUMNS if x not in df.columns]
    if need:
        st.warning("Thiếu cột đặc trưng của mô hình (không đánh giá được mô hình): " + ", ".join(need))
    else:
        st.success("Đủ 21 cột đặc trưng của mô hình.")
    st.success("Có cột nhãn cảm xúc: " + ctx["label_col"]) if ctx["label_col"] else st.warning("Không có cột nhãn cảm xúc.")
    st.info(f"Cột nội dung nhận diện được: {ctx['text_col']}") if ctx["text_col"] else st.info("Không nhận diện được cột nội dung review.")
