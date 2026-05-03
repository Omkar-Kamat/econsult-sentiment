from __future__ import annotations
import numpy as np
from scipy.sparse import hstack, csr_matrix
from shared.loader import ARTIFACTS


def predict_resolution(
    text_processed: str,
    issue: str,
    cluster: int,
    compound: float,
    severity: int = 3,
    word_count: int = 100,
) -> dict:
    """Predict company resolution probabilities for a complaint."""
    clf       = ARTIFACTS["resolution_clf"]
    tfidf_n   = ARTIFACTS["resolution_tfidf_narrative"]
    tfidf_i   = ARTIFACTS["resolution_tfidf_issue"]
    le        = ARTIFACTS["label_encoder"]

    sentiment_val = (
        -1 if compound <= -0.05
        else 1 if compound >= 0.05
        else 0
    )

    x_narr  = tfidf_n.transform([text_processed])
    x_issue = tfidf_i.transform([issue])
    x_dense = csr_matrix([[
        float(cluster), compound, float(severity),
        float(word_count), float(sentiment_val)
    ]])

    x = hstack([x_narr, x_issue, x_dense])

    probs  = clf.predict_proba(x)[0]
    result = {
        le.classes_[i]: round(float(p), 4)
        for i, p in enumerate(probs)
    }
    result = dict(sorted(result.items(), key=lambda kv: kv[1], reverse=True))
    top    = next(iter(result))

    return {"probabilities": result, "top_prediction": top}