# ============================================================
# src/pipeline.py - Văn bản -> vector 21 đặc trưng (đồng bộ với CSV huấn luyện)
#   * as_*  : mã 0 = tiêu cực/không nhắc, 1 = trung lập, 2 = tích cực
#   * avg_word_length = tổng độ dài các từ / số từ (không tính khoảng trắng)
#   * kw_*  : khớp chuỗi con (đúng cách tạo dữ liệu huấn luyện)
# ============================================================
import pickle
import re
import pandas as pd
import src.config as config

_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
_NEG = r"(?:không|chẳng|chả|chưa|ko|hổng)"
_SPLIT = re.compile(r"[.!?;,\n]|\bnhưng\b|\bmà\b|\btuy\b|\bsong\b")

POS_ALL = config.KW_TICH_CUC_MANH + config.KW_TICH_CUC_NHE + config.KW_SHIP_NHANH + config.EXTRA_POSITIVE
NEG_ALL = (config.KW_TIEU_CUC_MANH + config.KW_TIEU_CUC_NHE + config.KW_SHIP_CHAM
           + config.KW_LOI_SAN_PHAM + config.KW_LOI_DINH_KEM + config.EXTRA_NEGATIVE)

_AM = {"loaded": False, "obj": None}


def get_aspect_model():
    """Bộ nhận diện khía cạnh huấn luyện từ CSV (aspect_model.pkl); None nếu chưa có."""
    if not _AM["loaded"]:
        _AM["loaded"] = True
        p = config.ASPECT_MODEL_FILE
        if p.exists():
            try:
                with open(p, "rb") as f:
                    _AM["obj"] = pickle.load(f)
            except Exception:
                _AM["obj"] = None
    return _AM["obj"]


def _has(text, kw, strict=None):
    if strict is None:
        strict = len(kw) <= 2          # từ rất ngắn ('ok', 'xu') phải khớp nguyên từ
    if strict:
        return re.search(rf"(?<!\w){re.escape(kw)}(?!\w)", text) is not None
    return kw in text


def _any(text, kws, strict=None):
    return any(_has(text, k, strict) for k in kws)


def _negated(clause, kw):
    return re.search(rf"(?<!\w){_NEG}\s+(?:\w+\s+){{0,2}}{re.escape(kw)}", clause) is not None


def _clause_polarity(clause):
    if any(_has(clause, k) and not _negated(clause, k) for k in NEG_ALL) or \
       any(_has(clause, k) and _negated(clause, k) for k in POS_ALL):
        return -1.0
    if any(_has(clause, k) and not _negated(clause, k) for k in POS_ALL) or \
       any(_has(clause, k) and _negated(clause, k) for k in NEG_ALL):
        return 1.0
    return 0.0


def extract_aspect_sentiment_logic(text_lower, aspect_keywords):
    """Luật từ khóa theo mệnh đề: -1 tiêu cực / 0 trung lập hoặc không nhắc / 1 tích cực."""
    scores = [_clause_polarity(c) for c in _SPLIT.split(text_lower) if c.strip() and _any(c, aspect_keywords)]
    if not scores:
        return 0.0
    if min(scores) < 0:
        return -1.0
    return 1.0 if max(scores) > 0 else 0.0


def aspects_of(raw_text):
    """Luật từ khóa (-1/0/1) — dùng để HIỂN THỊ chi tiết, kể cả tiêu cực."""
    t = str(raw_text).lower().strip()
    return {k: extract_aspect_sentiment_logic(t, kws) for k, kws in config.ASPECT_KEYWORDS.items()}


def aspect_codes_many(texts):
    """Mã khía cạnh (0/1/2) đưa vào mô hình RF cho nhiều văn bản."""
    am = get_aspect_model()
    low = [str(t).lower().strip() for t in texts]
    if am:
        return pd.DataFrame({a: am["models"][a].predict(low).astype(float) for a in config.ASPECT_KEYWORDS})
    rule = pd.DataFrame([aspects_of(t) for t in texts])
    return rule.replace({-1.0: 0.0, 1.0: 2.0}).astype(float)


def _base_features(raw_text):
    raw_text = str(raw_text)
    t = raw_text.lower().strip()
    words = raw_text.split()
    kw = lambda lst: 1 if _any(t, lst, strict=False) else 0
    return [
        len(raw_text), len(words), (sum(len(w) for w in words) / len(words)) if words else 0.0,
        raw_text.count("!"), raw_text.count("?"),
        1 if ("emoji_" in t or _EMOJI_RE.search(raw_text)) else 0,
        1 if re.search(r"(\d\s*sao|\d\*|1star|5star)", t) else 0,
        kw(config.KW_TIEU_CUC_MANH), kw(config.KW_TIEU_CUC_NHE), kw(config.KW_TICH_CUC_MANH),
        kw(config.KW_TICH_CUC_NHE), kw(config.KW_SHIP_NHANH), kw(config.KW_SHIP_CHAM),
        kw(config.KW_LOI_SAN_PHAM), kw(config.KW_LOI_DINH_KEM),
    ]


def build_feature_frame(texts):
    """DataFrame 21 cột đúng tên & thứ tự của mô hình."""
    texts = [str(t) for t in texts]
    asp = aspect_codes_many(texts)
    base = pd.DataFrame([_base_features(t) for t in texts], columns=config.FEATURE_COLUMNS[6:])
    return pd.concat([asp[list(config.ASPECT_KEYWORDS)], base], axis=1)[config.FEATURE_COLUMNS]


def convert_text_to_feature_matrix(raw_text):
    return build_feature_frame([raw_text]).iloc[0].tolist()
