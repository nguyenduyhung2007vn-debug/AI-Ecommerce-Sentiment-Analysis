import streamlit as st
import pickle
import pandas as pd
import src.config as config

@st.cache_resource
def load_binary_model():
    """Nạp bộ não AI tĩnh vào bộ nhớ hệ thống"""
    with open(config.MODEL_FILE, 'rb') as file:
        return pickle.load(file)

@st.cache_data
def load_and_preprocess_dataframe():
    """NẠP FILE CSV THẲNG VÀO RAM VÀ TÍNH TOÁN SẴN TOÀN BỘ SỐ LIỆU ĐỂ TĂNG TỐC GẤP 10 LẦN"""
    df = pd.read_csv(config.DATA_FILE)
    
    # Tiền tính toán sẵn các chỉ số thống kê vĩ mô (Lazy Loading)
    metrics = {
        'total_rows': len(df),
        'mean_len_char': df['review_len_char'].mean() if 'review_len_char' in df.columns else 0,
        'mean_len_word': df['review_len_word'].mean() if 'review_len_word' in df.columns else 0,
        'neg_count': len(df[df['sentiment_llm'] == 0]) if 'sentiment_llm' in df.columns else 0,
        'pos_ratio': (len(df[df['sentiment_llm'] == 2]) / len(df)) * 100 if 'sentiment_llm' in df.columns and len(df) > 0 else 0.0
    }
    
    # Tính toán sẵn điểm số khía cạnh phòng ban (ABSA) thang điểm 100
    aspect_cols = ['as_content', 'as_physical', 'as_price', 'as_packaging', 'as_delivery']
    metrics['aspect_means'] = df[aspect_cols].mean() * 50 if all(c in df.columns for c in aspect_cols) else pd.Series(0, index=aspect_cols)
    metrics['raw_aspect_means'] = df[aspect_cols].mean() if all(c in df.columns for c in aspect_cols) else pd.Series(0, index=aspect_cols)
    
    return df, metrics

def load_and_cache_system_resources():
    """Hàm hợp nhất tài nguyên trả về DataFrame và Bộ số liệu đã tính toán sẵn"""
    ai_model = load_binary_model()
    df_history, precomputed_metrics = load_and_preprocess_dataframe()
    return ai_model, df_history, precomputed_metrics

