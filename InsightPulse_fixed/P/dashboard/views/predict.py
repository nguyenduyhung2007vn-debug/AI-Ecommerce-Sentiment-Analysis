import os
import tempfile
import pandas as pd
import streamlit as st
import src.config as config
from src import analytics as A
from src import media
from src.data_loader import read_csv_any
from dashboard.views import common as C

EXAMPLES = {
    "— Chọn ví dụ —": "",
    "Tích cực": "Sách rất đẹp, đóng gói cẩn thận, giao hàng nhanh. Rất hài lòng!",
    "Tiêu cực": "Sách bị rách gáy, đóng gói cẩu thả, giao trễ quá, thất vọng.",
    "Hỗn hợp": "Giao hàng ok, nhưng sách bị móp bìa và thiếu trang.",
}


# ---------------- Trang 1 ----------------
def page_text(ctx):
    st.title("💬 Dự đoán từ văn bản")
    ex = st.selectbox("Ví dụ nhanh", list(EXAMPLES))
    text = st.text_area("Nhập review khách hàng:", value=EXAMPLES[ex], height=140,
                        placeholder="Ví dụ: Sách rất đẹp, đóng gói cẩn thận, giao hàng nhanh...")
    if st.button("KÍCH HOẠT DỰ BÁO AI", type="primary"):
        if not text.strip():
            st.warning("Vui lòng nhập nội dung đánh giá.")
            return
        res = A.predict_one(ctx["model"], text)
        st.session_state["last_text"] = text
        C.log_history(res, "Văn bản")
        C.show_result(res)
        st.subheader("Phân tích theo khía cạnh")
        st.dataframe(C.aspect_frame(res), hide_index=True)


# ---------------- Trang 2 ----------------
def page_video(ctx):
    st.title("🎬 Dự đoán từ video / âm thanh")
    ok, msg = media.media_ready()
    if not ok:
        st.error(msg)
        st.stop()
    c1, c2 = st.columns([3, 1])
    f = c1.file_uploader("Tải video review", type=["mp4", "mov", "mkv", "avi", "webm", "m4a", "mp3", "wav"])
    lang = c2.selectbox("Ngôn ngữ", ["vi-VN", "en-US"])
    st.caption("Nhận diện giọng nói dùng Google Web Speech nên cần Internet. Video dài được cắt thành đoạn 25 giây.")
    if f is None:
        return
    if f.type and f.type.startswith("video"):
        st.video(f)
    else:
        st.audio(f)
    if st.button("🎙️ Trích xuất lời thoại", type="primary"):
        suffix = os.path.splitext(f.name)[1] or ".mp4"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            tmp.write(f.getbuffer())
            tmp.close()
            bar = st.progress(0.0, text="AI đang trích xuất lời thoại...")
            text, dur = media.transcribe_file(tmp.name, lang, progress=lambda p: bar.progress(p))
            bar.empty()
            st.session_state["video_text"] = text
            st.session_state["video_dur"] = dur
            if not text:
                st.warning("Không nhận diện được lời thoại. Bạn có thể tự nhập vào ô bên dưới.")
        except Exception as e:
            st.error(f"Không thể trích xuất lời thoại: {e}")
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
    if "video_dur" in st.session_state:
        st.caption(f"Thời lượng: {st.session_state['video_dur']:.0f} giây")
    text = st.text_area("Lời thoại (có thể chỉnh sửa trước khi dự đoán):", key="video_text", height=160)
    if st.button("KÍCH HOẠT DỰ BÁO AI", type="primary", key="video_predict"):
        if not text.strip():
            st.warning("Chưa có lời thoại để phân tích.")
            return
        res = A.predict_one(ctx["model"], text)
        C.log_history(res, f"Video: {f.name}")
        C.show_result(res)
        st.dataframe(C.aspect_frame(res), hide_index=True)


# ---------------- Trang 3 ----------------
def page_batch(ctx):
    st.title("📑 Dự đoán hàng loạt")
    mode = st.radio("Nguồn dữ liệu", ["Tải file CSV", "Dán nhiều review (mỗi dòng một review)"], horizontal=True)
    texts = None
    if mode.startswith("Tải"):
        up = st.file_uploader("CSV có cột nội dung review", type=["csv"])
        if up:
            df = read_csv_any(up)
            _, guess = A.detect_columns(df)
            cols = list(df.columns)
            col = st.selectbox("Cột nội dung", cols, index=cols.index(guess) if guess in cols else 0)
            texts = df[col].dropna().astype(str).tolist()
    else:
        raw = st.text_area("Danh sách review", height=200)
        texts = [t.strip() for t in raw.splitlines() if t.strip()] or None
    if not texts:
        return
    st.caption(f"{len(texts):,} review")
    if st.button("🚀 Dự đoán tất cả", type="primary"):
        with st.spinner("Đang dự đoán..."):
            out, _ = A.predict_texts(ctx["model"], texts)
        st.session_state["batch_out"] = out
    out = st.session_state.get("batch_out")
    if out is not None:
        vc = out["sentiment"].value_counts().reindex(["Tiêu cực", "Trung lập", "Tích cực"]).fillna(0).reset_index()
        vc.columns = ["Cảm xúc", "Số review"]
        st.altair_chart(C.sentiment_bar(vc, "Cảm xúc", "Số review"))
        st.dataframe(out, hide_index=True)
        C.download_df(out, "ket_qua_du_doan.csv")


# ---------------- Trang 4 ----------------
def page_explain(ctx):
    st.title("🔍 Giải thích dự đoán")
    st.write("Với mỗi đặc trưng, hệ thống đưa nó về giá trị nền rồi đo xác suất của lớp dự đoán thay đổi bao nhiêu "
             "(dương = đặc trưng đó đang **đẩy** mô hình về lớp được dự đoán).")
    text = st.text_area("Review cần giải thích:", value=st.session_state.get("last_text", ""), height=120)
    if not text.strip():
        return
    res = A.predict_one(ctx["model"], text)
    C.show_result(res)
    base = A.length_baseline(ctx["df"])
    cls, p, imp = A.occlusion_importance(ctx["model"], res["X"], base)
    import altair as alt
    top = imp.head(10)
    st.altair_chart(alt.Chart(top).mark_bar().encode(
        x="Đóng góp:Q", y=alt.Y("feature:N", sort=None),
        color=alt.condition(alt.datum["Đóng góp"] > 0, alt.value("#10B981"), alt.value("#EF4444")),
        tooltip=["mô tả", "giá trị", "Đóng góp"]).properties(height=320))
    st.subheader("Vector 21 đặc trưng")
    st.dataframe(imp, hide_index=True)


# ---------------- Trang 5 ----------------
def page_history(ctx):
    st.title("🕘 Lịch sử dự đoán (phiên hiện tại)")
    h = st.session_state.get("history", [])
    if not h:
        st.info("Chưa có dự đoán nào trong phiên này.")
        return
    df = pd.DataFrame(h)
    st.dataframe(df, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        C.download_df(df, "lich_su_du_doan.csv")
    if c2.button("🗑️ Xóa lịch sử"):
        st.session_state["history"] = []
        st.rerun()
