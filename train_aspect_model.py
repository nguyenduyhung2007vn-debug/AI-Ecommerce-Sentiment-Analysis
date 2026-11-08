"""Huấn luyện bộ nhận diện khía cạnh (as_*) từ nội dung review trong CSV -> aspect_model.pkl
Chạy:  python train_aspect_model.py
Lý do: mô hình RF được huấn luyện với as_* do LLM gán; luật từ khóa không tái tạo được chúng (độ chính xác end-to-end ~69%).
"""
import pickle
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import src.config as config                      # noqa: E402
from src import pipeline as P                    # noqa: E402

df = pd.read_csv(config.DATA_FILE, encoding="utf-8-sig")
text = df["content"].astype(str).str.lower().str.strip()
make = lambda: make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2),
                             LogisticRegression(C=30, max_iter=3000, class_weight="balanced"))
models, cv_pred = {}, {}
for a in config.ASPECT_KEYWORDS:
    y = df[a].astype(int)
    cv_pred[a] = cross_val_predict(make(), text, y, cv=StratifiedKFold(5, shuffle=True, random_state=0))
    models[a] = make().fit(text, y)

rf = pickle.load(open(config.MODEL_FILE, "rb"))
X = P.build_feature_frame(list(df["content"]))
for a in config.ASPECT_KEYWORDS:
    X[a] = cv_pred[a].astype(float)               # khía cạnh dự đoán chéo -> ước lượng trung thực
acc = float((rf.predict(X[config.FEATURE_COLUMNS]) == df["sentiment_llm"]).mean())
meta = {"n_train": len(df), "cv_end_to_end_accuracy": acc,
        "cv_aspect_accuracy": {a: float((cv_pred[a] == df[a]).mean()) for a in cv_pred}}
pickle.dump({"models": models, "meta": meta}, open(ROOT / "aspect_model.pkl", "wb"))
print("Đã lưu aspect_model.pkl | end-to-end accuracy (cross-validation): %.3f" % acc)
