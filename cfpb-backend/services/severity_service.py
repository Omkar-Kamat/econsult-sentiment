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
    """Predict severity score (1–5) using the NB07 GradientBoosting model."""
    clf = ARTIFACTS["severity"]

    length_pct = 0.5

    features = np.array([[
        prob_negative, prob_neutral, prob_positive,
        compound,
        float(cluster),
        float(word_count), length_pct,
        float(redaction_count), redaction_density,
    ]])

    return int(clf.predict(features)[0])