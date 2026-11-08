# ============================================================
# src/data_loader.py - Tải mô hình, dữ liệu, KPI (có cache)
# ============================================================
import pickle
import pandas as pd
import streamlit as st
import src.config as config
from src.analytics import compute_metrics, detect_columns


@st.cache_resource(show_spinner=False)
def load_binary_model():
    path = config.MODEL_FILE
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy mô hình AI: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)


def read_csv_any(file_or_path):
    """Đọc CSV, thử nhiều bảng mã thường gặp ở file tiếng Việt."""
    last = None
    for enc in ("utf-8-sig", "utf-8", "cp1258", "latin-1"):
        try:
            if hasattr(file_or_path, "seek"):
                file_or_path.seek(0)
            return pd.read_csv(file_or_path, encoding=enc)
        except UnicodeDecodeError as e:
            last = e
    raise last


@st.cache_data(show_spinner=False)
def load_default_dataframe():
    p = config.DATA_FILE
    if not p.exists():
        return None
    df = read_csv_any(p)
    return None if df.empty else df


@st.cache_data(show_spinner=False)
def cached_metrics(df):
    return compute_metrics(df)


def load_context():
    """Gom mô hình + dữ liệu (ưu tiên CSV người dùng tải lên) + KPI vào một dict."""
    model = load_binary_model()
    df = st.session_state.get("uploaded_df")
    source = "CSV tải lên"
    if df is None:
        df = load_default_dataframe()
        source = config.DATA_FILE.name
    ctx = {"model": model, "df": df, "metrics": None, "label_col": None, "text_col": None,
           "source": source if df is not None else None}
    if df is not None:
        ctx["metrics"] = cached_metrics(df)
        ctx["label_col"], ctx["text_col"] = detect_columns(df)
    return ctx
