import json
import pandas as pd
import streamlit as st
import src.config as config
from src import analytics as A
from dashboard.views import common as C


# ---------------- Trang 18 ----------------
def page_issues(ctx):
    st.title("🚨 Vấn đề vận hành")
    C.require_data(ctx)
    it = A.issue_table(ctx["df"])
    st.subheader("Tỷ lệ tiêu cực theo khía cạnh (trên số lượt nhắc)")
    if it.empty:
        st.info("CSV không có các cột khía cạnh.")
    else:
        st.bar_chart(it.set_index("Khía cạnh")["Tỷ lệ tiêu cực %"])
        st.dataframe(it.drop(columns="aspect"), hide_index=True)
    fr = A.flag_rates(ctx["df"])
    if not fr.empty:
        st.subheader("Chỉ báo sự cố")
        st.dataframe(fr.drop(columns="feature"), hide_index=True)


# ---------------- Trang 19 ----------------
def page_actions(ctx):
    st.title("🛠️ Đề xuất hành động")
    C.require_data(ctx)
    it = A.issue_table(ctx["df"])
    it = it[it["Lượt nhắc"] > 0]
    if it.empty:
        st.info("Chưa đủ dữ liệu khía cạnh để đề xuất.")
        return
    st.caption("Xếp theo tỷ lệ tiêu cực; mức ưu tiên: ≥40% Cao, ≥20% Trung bình, còn lại Theo dõi. Đề xuất mang tính tham khảo.")
    for i, r in it.iterrows():
        lvl = "🔴 Cao" if r["Tỷ lệ tiêu cực %"] >= 40 else "🟠 Trung bình" if r["Tỷ lệ tiêu cực %"] >= 20 else "🟢 Theo dõi"
        with st.expander(f"#{i + 1} {r['Khía cạnh']} — {r['Tỷ lệ tiêu cực %']}% tiêu cực — {lvl}", expanded=i < 2):
            st.write(f"{r['Tiêu cực']:,}/{r['Lượt nhắc']:,} lượt nhắc tiêu cực.")
            st.info(A.ACTIONS[r["aspect"]])


# ---------------- Trang 20 ----------------
def page_report(ctx):
    st.title("📥 Báo cáo & xuất dữ liệu")
    C.require_data(ctx)
    m = ctx["metrics"]
    it = A.issue_table(ctx["df"])
    lines = [f"# Báo cáo InsightPulse", f"- Nguồn dữ liệu: {ctx['source']}", f"- Tổng phản hồi: {m['total_rows']:,}",
             f"- Tích cực: {m['pos_ratio']:.1f}% | Trung lập: {m['neu_ratio']:.1f}% | Tiêu cực: {m['neg_ratio']:.1f}%", "",
             "## Tỷ lệ tiêu cực theo khía cạnh"]
    lines += [f"- {r['Khía cạnh']}: {r['Tỷ lệ tiêu cực %']}% ({r['Tiêu cực']}/{r['Lượt nhắc']})" for _, r in it.iterrows()]
    md = "\n".join(lines)
    st.markdown(md)
    c1, c2, c3 = st.columns(3)
    c1.download_button("⬇️ Báo cáo (.md)", md.encode("utf-8"), "bao_cao_insightpulse.md")
    c2.download_button("⬇️ KPI (.json)", json.dumps({k: v for k, v in m.items() if k != "aspect_counts"},
                       ensure_ascii=False, indent=2, default=float).encode("utf-8"), "kpi.json")
    c3.download_button("⬇️ Bảng khía cạnh (.csv)", it.to_csv(index=False).encode("utf-8-sig"), "khia_canh.csv")
