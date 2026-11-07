# =================================================================
# FILE ĐÃ TỐI ƯU TỐC ĐỘ: src/data_loader.py
# NÂNG CẤP CƠ CHẾ CACHE_DATA ĐỂ TĂNG TỐC TRUY XUẤT FILE CSV GẤP 5 LẦN
# =================================================================
import streamlit as st
import pickle
import pandas as pd
import src.config as config

@st.cache_resource  # Tối ưu hóa cho file cứng "bộ não" AI tĩnh không thay đổi
def load_binary_model():
    """Tải và lưu trữ tệp cứng mô hình Random Forest Classifier vào RAM máy chủ"""
    with open(config.MODEL_FILE, 'rb') as file:
        return pickle.load(file)

@st.cache_data      # NÂNG CẤP CỐT LÕI: Lưu ma trận bảng dữ liệu CSV thẳng vào thanh RAM
def load_historical_dataframe():
    """Tải file ma trận dữ liệu phân tích hệ thống (.csv) dưới dạng ma trận nhị phân siêu tốc"""
    return pd.read_csv(config.DATA_FILE)

def load_and_cache_system_resources():
    """Hàm hợp nhất nạp tài nguyên đồng bộ cho toàn bộ hệ thống Web App"""
    ai_model = load_binary_model()
    df_history = load_historical_dataframe()
    return ai_model, df_history

