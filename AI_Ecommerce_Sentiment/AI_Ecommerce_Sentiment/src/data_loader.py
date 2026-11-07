
# ============================================================
# FILE: src/data_loader.py
# Chức năng: Tải mô hình AI, dữ liệu CSV và tính KPI
# ============================================================

import streamlit as st
import pickle
import pandas as pd
from pathlib import Path
import src.config as config


# Thư mục gốc dự án: AI_Ecommerce_Sentiment
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_file_path(file_name):
    """Xác định đường dẫn tuyệt đối của file dữ liệu."""

    path = Path(file_name)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


@st.cache_resource
def load_binary_model():
    """Tải mô hình Random Forest từ file PKL."""

    model_path = get_file_path(config.MODEL_FILE)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy mô hình AI: {model_path}"
        )

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    return model


@st.cache_data
def load_and_preprocess_dataframe():
    """Đọc CSV và tính toán các chỉ số phân tích."""

    data_path = get_file_path(config.DATA_FILE)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu CSV: {data_path}"
        )

    df = pd.read_csv(data_path)

    if df.empty:
        raise ValueError("File CSV không có dữ liệu.")

    # Thống kê cảm xúc
    if "sentiment_llm" in df.columns:
        sentiment = pd.to_numeric(
            df["sentiment_llm"], errors="coerce"
        )

        neg_count = int((sentiment == 0).sum())
        neu_count = int((sentiment == 1).sum())
        pos_count = int((sentiment == 2).sum())
    else:
        neg_count = 0
        neu_count = 0
        pos_count = 0

    total_rows = len(df)

    pos_ratio = pos_count / total_rows * 100
    neg_ratio = neg_count / total_rows * 100
    neu_ratio = neu_count / total_rows * 100

    # Phân tích các khía cạnh ABSA
    aspect_cols = [
        "as_content",
        "as_physical",
        "as_price",
        "as_packaging",
        "as_delivery"
    ]

    aspect_scores = {}

    for col in aspect_cols:

        if col in df.columns:

            values = pd.to_numeric(
                df[col], errors="coerce"
            ).dropna()

            positive_count = int((values == 1).sum())
            mention_count = int((values != 0).sum())

            if mention_count > 0:
                aspect_scores[col] = (
                    positive_count / mention_count * 100
                )
            else:
                aspect_scores[col] = 75.0

        else:
            aspect_scores[col] = 70.0

    metrics = {
        "total_rows": total_rows,
        "neg_count": neg_count,
        "pos_ratio": pos_ratio,
        "neg_ratio": neg_ratio,
        "neu_ratio": neu_ratio,
        "aspect_scores": aspect_scores
    }

    return df, metrics


def load_and_cache_system_resources():
    """
    Hàm tổng hợp được dashboard_app.py gọi.

    Trả về:
        ai_engine: Mô hình AI
        df_matrix: Dữ liệu CSV
        precomputed_metrics: Các chỉ số thống kê
    """

    ai_engine = load_binary_model()

    df_matrix, precomputed_metrics = (
        load_and_preprocess_dataframe()
    )

    return ai_engine, df_matrix, precomputed_metrics
