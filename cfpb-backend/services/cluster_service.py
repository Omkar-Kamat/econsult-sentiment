from __future__ import annotations
import numpy as np
from shared.loader import ARTIFACTS, CLUSTER_LABELS, FEATURE_COLS


def predict_cluster(embedding: np.ndarray) -> dict:
    """Given a 384-dim MiniLM embedding, return cluster id, label, top-10 keywords, and 2D UMAP coords."""
    km    = ARTIFACTS["kmeans"]
    umap  = ARTIFACTS["umap"]
    tfidf = ARTIFACTS["tfidf"]
    feats = ARTIFACTS["tfidf_features"]
    df    = ARTIFACTS["df"]

    cluster_id = int(km.predict(embedding.reshape(1, -1))[0])

    umap_coords = umap.transform(embedding.reshape(1, -1))[0]

    cluster_mask = df["cluster"].values == cluster_id
    cluster_texts = df.loc[cluster_mask, "text_processed"].fillna("").tolist()

    if cluster_texts:
        tfidf_matrix  = tfidf.transform(cluster_texts)
        cluster_mean  = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        top_idx       = cluster_mean.argsort()[::-1][:10]
        top_keywords  = feats[top_idx].tolist()
    else:
        top_keywords = []

    return {
        "cluster":       cluster_id,
        "cluster_label": CLUSTER_LABELS.get(cluster_id, f"Cluster {cluster_id}"),
        "top_keywords":  top_keywords,
        "umap_x":        float(umap_coords[0]),
        "umap_y":        float(umap_coords[1]),
    }