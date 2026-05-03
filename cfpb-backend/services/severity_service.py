from __future__ import annotations
import numpy as np
from shared.loader import ARTIFACTS, FEATURE_COLS


def predict_severity(
    prob_negative: float,
    prob_neutral: float,
    prob_positive: float,
    compound: float,
    cluster: int,
    word_count: int,
    redaction_count: int,
    redaction_density: float,
) -> int:
    clf      = ARTIFACTS["severity"]
    wc_sorted = ARTIFACTS.get("wc_sorted")

    # Compute real percentile rank if CDF is available, else fall back to 0.5
    if wc_sorted is not None and len(wc_sorted) > 0:
        length_pct = float(np.searchsorted(wc_sorted, word_count, side="right")) / len(wc_sorted)
    else:
        length_pct = 0.5

    features = np.array([[
        prob_negative, prob_neutral, prob_positive,
        compound,
        float(cluster),
        float(word_count), length_pct,
        float(redaction_count), redaction_density,
    ]])

    return int(clf.predict(features)[0])