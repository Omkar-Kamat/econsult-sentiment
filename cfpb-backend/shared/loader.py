from __future__ import annotations
import joblib
import faiss
import numpy as np
import pandas as pd
from pathlib import Path

ARTIFACTS: dict = {}

CLUSTER_LABELS = {
    0: "Credit Report Disputes",
    1: "Debt Collection & Recovery",
    2: "Card Payments & Account Calls",
}

FEATURE_COLS = [
    "prob_negative", "prob_neutral", "prob_positive",
    "compound",
    "cluster_int",
    "word_count", "length_pct",
    "redaction_count", "redaction_density",
]


def load_all(base: str = "artifacts") -> None:
    """Load all artifacts from disk into the ARTIFACTS dict."""
    p = Path(base)

    print("Loading TF-IDF vectorizer...")
    ARTIFACTS["tfidf"] = joblib.load(p / "tfidf_vectorizer.pkl")

    print("Loading KMeans model...")
    ARTIFACTS["kmeans"] = joblib.load(p / "kmeans_k3.pkl")

    print("Loading UMAP reducer...")
    ARTIFACTS["umap"] = joblib.load(p / "umap_reducer.pkl")

    print("Loading severity model...")
    ARTIFACTS["severity"] = joblib.load(p / "severity_model.pkl")

    print("Loading resolution classifier bundle...")
    bundle = joblib.load(p / "resolution_classifier.pkl")
    ARTIFACTS["resolution_clf"]             = bundle["clf"]
    ARTIFACTS["resolution_tfidf_narrative"] = bundle["tfidf_narrative"]
    ARTIFACTS["resolution_tfidf_issue"]     = bundle["tfidf_issue"]

    print("Loading label encoder...")
    ARTIFACTS["label_encoder"] = joblib.load(p / "resolution_label_encoder.pkl")

    print("Loading FAISS index...")
    ARTIFACTS["faiss_index"] = faiss.read_index(str(p / "faiss_index.bin"))

    print("Loading embeddings...")
    embeddings = np.load(p / "embeddings.npy").astype("float32")
    faiss.normalize_L2(embeddings)
    ARTIFACTS["embeddings"] = embeddings

    print("Loading severity_data.csv...")
    ARTIFACTS["df"] = pd.read_csv(p / "severity_data.csv")

    print("Loading TF-IDF feature names...")
    ARTIFACTS["tfidf_features"] = np.array(
        ARTIFACTS["tfidf"].get_feature_names_out()
    )

    print(f"✓ All artifacts loaded | df={len(ARTIFACTS['df']):,} rows | "
          f"index={ARTIFACTS['faiss_index'].ntotal:,} vectors")