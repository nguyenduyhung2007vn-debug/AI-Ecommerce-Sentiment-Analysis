# =================================================================
# KHỐI CODE 3: TẦNG ĐỌC FILE MÔ HÌNH VÀ FILE CSV QUẢN TRỊ QUA CACHE
# Đường dẫn lưu trữ trên GitHub: src/data_loader.py
# =================================================================
import streamlit as st
import pickle
import pandas as pd
import src.config as config

@st.cache_resource
def load_system_assets():
    """Tải bộ não AI (.pkl) và file ma trận dữ liệu phân tích hệ thống (.csv) vào bộ nhớ cache"""
    with open(config.MODEL_FILE, 'rb') as file:
        model = pickle.load(file)
    df = pd.read_csv(config.DATA_FILE)
    return model, df
