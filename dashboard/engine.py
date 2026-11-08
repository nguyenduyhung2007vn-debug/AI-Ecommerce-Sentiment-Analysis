# ============================================================
# dashboard/engine.py - Đăng ký 20 trang và điều hướng
# ============================================================
import streamlit as st
from dashboard.views import predict, overview, absa, model_pages, business

# (nhóm, [(tiêu đề, icon, url_path, hàm render)])
PAGES = [
    ("🤖 Dự đoán AI", [
        ("Dự đoán từ văn bản", "💬", "predict-text", predict.page_text),
        ("Dự đoán từ video", "🎬", "predict-video", predict.page_video),
        ("Dự đoán hàng loạt", "📑", "predict-batch", predict.page_batch),
        ("Giải thích dự đoán", "🔍", "explain", predict.page_explain),
        ("Lịch sử dự đoán", "🕘", "history", predict.page_history)]),
    ("📊 Tổng quan dữ liệu", [
        ("Tổng quan KPI", "📊", "kpi", overview.page_kpi),
        ("Phân phối cảm xúc", "🥧", "distribution", overview.page_distribution),
        ("Khám phá dữ liệu", "🗂️", "explorer", overview.page_explorer),
        ("Chất lượng dữ liệu", "🧪", "quality", overview.page_quality)]),
    ("🎯 Phân tích khía cạnh", [
        ("Điểm khía cạnh", "🎯", "aspect-scores", absa.page_scores),
        ("Khía cạnh × Cảm xúc", "🔥", "aspect-heatmap", absa.page_heatmap),
        ("So sánh khía cạnh", "⚖️", "aspect-compare", absa.page_compare),
        ("Từ khóa ngữ nghĩa", "🔤", "keywords", absa.page_keywords)]),
    ("🧠 Mô hình", [
        ("Thông tin mô hình", "🤖", "model-info", model_pages.page_info),
        ("Độ quan trọng đặc trưng", "📌", "feature-importance", model_pages.page_importance),
        ("Đánh giá mô hình", "🧮", "evaluation", model_pages.page_eval),
        ("Mô phỏng What-if", "🎛️", "what-if", model_pages.page_whatif)]),
    ("💡 Kinh doanh", [
        ("Vấn đề vận hành", "🚨", "issues", business.page_issues),
        ("Đề xuất hành động", "🛠️", "actions", business.page_actions),
        ("Báo cáo & xuất dữ liệu", "📥", "report", business.page_report)]),
]


def _bind(fn, ctx):
    def _page():
        fn(ctx)
    return _page


def build_navigation(ctx):
    nav = {g: [st.Page(_bind(fn, ctx), title=t, icon=i, url_path=u, default=(u == "predict-text"))
               for t, i, u, fn in items] for g, items in PAGES}
    assert sum(len(v) for v in nav.values()) == 20
    return st.navigation(nav)
