import altair as alt
import pandas as pd
import streamlit as st
import src.config as config
from src.data_loader import read_csv_any

LABEL_ICON = {0: "🚨", 1: "😐", 2: "🎉"}
COLOR_SCALE = alt.Scale(domain=list(config.LABEL_COLORS), range=list(config.LABEL_COLORS.values()))


def require_data(ctx):
    """Chặn trang cần dữ liệu CSV nếu chưa có; cho phép tải CSV lên ngay tại chỗ."""
    if ctx["df"] is not None:
        return
    st.warning(f"Chưa tìm thấy `{config.DATA_FILE.name}`. Hãy đặt file vào thư mục gốc dự án hoặc tải lên bên dưới.")
    up = st.file_uploader("Tải file dữ liệu CSV", type=["csv"], key=f"gate_{st.session_state.get('_g', 0)}")
    if up is not None:
        st.session_state["uploaded_df"] = read_csv_any(up)
        st.rerun()
    st.stop()


def require_labels(ctx):
    require_data(ctx)
    if not ctx["label_col"]:
        st.error("CSV không có cột nhãn cảm xúc (`sentiment_llm`).")
        st.stop()


def show_result(res):
    p = res["pred"]
    label = config.LABELS.get(p, str(p))
    box = {0: st.error, 1: st.warning, 2: st.success}.get(p, st.info)
    box(f"{LABEL_ICON.get(p, '')} SẮC THÁI {label.upper()}  —  độ tin cậy {res['proba'][p] * 100:.1f}%")
    cols = st.columns(3)
    for c, k in zip(cols, (0, 1, 2)):
        c.metric(config.LABELS[k], f"{res['proba'].get(k, 0) * 100:.1f}%")


def aspect_frame(res):
    code = {0.0: "⚪ Không nhắc / tiêu cực", 1.0: "🟡 Trung lập", 2.0: "🟢 Tích cực"}
    rule = {-1.0: "🔴 Tiêu cực", 0.0: "—", 1.0: "🟢 Tích cực"}
    X, asp = res["X"].iloc[0], res["aspects"]
    return pd.DataFrame([{"Khía cạnh": config.ASPECT_NAMES[k], "Mã đưa vào mô hình": code[float(X[k])],
                          "Luật từ khóa": rule[asp[k]]} for k in config.ASPECT_NAMES])


def log_history(res, source):
    h = st.session_state.setdefault("history", [])
    h.append({"Nguồn": source, "Nội dung": res["text"][:300], "Dự đoán": config.LABELS[res["pred"]],
              "Tin cậy %": round(res["proba"][res["pred"]] * 100, 1)})


def sentiment_bar(df, x, y, color="Cảm xúc", height=300):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X(x, sort=None), y=y, color=alt.Color(color, scale=COLOR_SCALE, legend=None),
        tooltip=list(df.columns)).properties(height=height)


def dist_frame(m):
    return pd.DataFrame({"Cảm xúc": ["Tiêu cực", "Trung lập", "Tích cực"],
                         "Số review": [m["neg_count"], m["neu_count"], m["pos_count"]],
                         "Tỷ lệ %": [m["neg_ratio"], m["neu_ratio"], m["pos_ratio"]]})


def download_df(df, name, label="⬇️ Tải CSV"):
    st.download_button(label, df.to_csv(index=False).encode("utf-8-sig"), file_name=name, mime="text/csv")
