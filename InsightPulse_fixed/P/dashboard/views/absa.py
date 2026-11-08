import altair as alt
import pandas as pd
import streamlit as st
import src.config as config
from src import analytics as A
from dashboard.views import common as C


# ---------------- Trang 10 ----------------
def page_scores(ctx):
    st.title("🎯 Điểm theo khía cạnh (ABSA)")
    C.require_data(ctx)
    st.write("Cột `as_*` trong dữ liệu mã hóa: 0 = tiêu cực/không nhắc, 1 = trung lập, 2 = tích cực. Điểm = % tích cực (mã 2) trong các lượt nhắc có sắc thái (mã 1 và 2), thang 100.")
    rows = []
    for a, v in ctx["metrics"]["aspect_scores"].items():
        name = config.ASPECT_NAMES[a]
        if v is None:
            st.markdown(f"**{name}** (`{a}`): chưa đủ dữ liệu")
            continue
        st.markdown(f"**{name}** (`{a}`): {v:.1f} / 100")
        st.progress(min(max(v / 100, 0.0), 1.0))
        rows.append({"Khía cạnh": name, "Điểm": round(v, 1)})
    if rows:
        st.bar_chart(pd.DataFrame(rows).set_index("Khía cạnh"))


# ---------------- Trang 11 ----------------
def page_heatmap(ctx):
    st.title("🔥 Khía cạnh × Cảm xúc tổng thể")
    C.require_labels(ctx)
    long = A.aspect_sentiment_long(ctx["df"], ctx["label_col"])
    if long.empty:
        st.info("CSV không có các cột khía cạnh.")
        return
    base = alt.Chart(long).encode(x=alt.X("Cảm xúc:N", sort=["Tiêu cực", "Trung lập", "Tích cực"]), y="Khía cạnh:N")
    st.altair_chart(base.mark_rect().encode(color=alt.Color("Số review:Q", scale=alt.Scale(scheme="viridis")),
                                            tooltip=["Khía cạnh", "Cảm xúc", "Số review"]).properties(height=320)
                    + base.mark_text(color="white").encode(text="Số review:Q"))
    st.caption("Chỉ đếm các review có nhắc tới khía cạnh đó (giá trị ≠ 0).")


# ---------------- Trang 12 ----------------
def page_compare(ctx):
    st.title("⚖️ So sánh khía cạnh")
    C.require_data(ctx)
    ac = ctx["metrics"]["aspect_counts"]
    if ac.empty:
        st.info("CSV không có các cột khía cạnh.")
        return
    ac = ac.assign(**{"Khía cạnh": ac["aspect"].map(config.ASPECT_NAMES)})
    long = ac.melt(id_vars="Khía cạnh", value_vars=["Tiêu cực/Không nhắc", "Trung lập", "Tích cực"],
                   var_name="Phân cực", value_name="Số review")
    norm = st.toggle("Chuẩn hóa theo % (100%)", value=False)
    st.altair_chart(alt.Chart(long).mark_bar().encode(
        x=alt.X("Khía cạnh:N", sort=None), y=alt.Y("Số review:Q", stack="normalize" if norm else "zero"),
        color=alt.Color("Phân cực:N", scale=alt.Scale(domain=["Tiêu cực/Không nhắc", "Trung lập", "Tích cực"],
                                                      range=["#64748B", "#F59E0B", "#10B981"])),
        tooltip=["Khía cạnh", "Phân cực", "Số review"]).properties(height=360))
    st.dataframe(ac.drop(columns="aspect"), hide_index=True)


# ---------------- Trang 13 ----------------
def page_keywords(ctx):
    st.title("🔤 Từ khóa & chỉ báo ngữ nghĩa")
    C.require_data(ctx)
    df, txt = ctx["df"], ctx["text_col"]
    kw_cols = [c for c in config.KEYWORD_GROUPS if c in df.columns]
    if kw_cols:
        r = pd.DataFrame({"Nhóm": [config.FEATURE_DESC[c] for c in kw_cols],
                          "Tỷ lệ review %": [round(pd.to_numeric(df[c], errors="coerce").fillna(0).gt(0).mean() * 100, 2)
                                             for c in kw_cols]})
        st.altair_chart(alt.Chart(r).mark_bar().encode(x=alt.X("Nhóm:N", sort=None), y="Tỷ lệ review %:Q",
                        tooltip=list(r.columns)).properties(height=300))
    if txt:
        st.subheader("Từ khóa xuất hiện nhiều nhất trong nội dung")
        group = st.selectbox("Nhóm từ khóa", list(config.KEYWORD_GROUPS), format_func=lambda k: config.FEATURE_DESC[k])
        s = df[txt].astype(str).str.lower()
        cnt = pd.DataFrame({"Từ khóa": config.KEYWORD_GROUPS[group],
                            "Số review": [int(s.str.contains(k, regex=False).sum()) for k in config.KEYWORD_GROUPS[group]]})
        st.bar_chart(cnt.sort_values("Số review", ascending=False).set_index("Từ khóa"))
    else:
        st.info("Không có cột nội dung review để đếm từ khóa.")
