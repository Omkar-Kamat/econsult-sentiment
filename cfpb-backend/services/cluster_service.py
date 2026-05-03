from __future__ import annotations
import numpy as np
from shared.loader import ARTIFACTS, CLUSTER_LABELS, FEATURE_COLS


def predict_cluster(embedding: np.ndarray) -> dict:
    km    = ARTIFACTS["kmeans"]
    umap  = ARTIFACTS["umap"]

    cluster_id  = int(km.predict(embedding.reshape(1, -1))[0])
    umap_coords = umap.transform(embedding.reshape(1, -1))[0]

    # O(1) lookup — computed once at startup
    top_keywords = ARTIFACTS["cluster_keywords"].get(cluster_id, [])

    return {
        "cluster":       cluster_id,
        "cluster_label": CLUSTER_LABELS.get(cluster_id, f"Cluster {cluster_id}"),
        "top_keywords":  top_keywords,
        "umap_x":        float(umap_coords[0]),
        "umap_y":        float(umap_coords[1]),
    }