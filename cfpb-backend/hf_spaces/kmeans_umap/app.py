import gradio as gr
import numpy as np
import joblib

CLUSTER_LABELS = {
    0: "Credit Report Disputes",
    1: "Debt Collection & Recovery",
    2: "Card Payments & Account Calls",
}

kmeans = joblib.load("kmeans_k3.pkl")
umap   = joblib.load("umap_reducer.pkl")

print("KMeans + UMAP loaded")


def predict(embedding: list[float]) -> dict:
    vec  = np.array(embedding, dtype="float32").reshape(1, -1)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    cluster_id  = int(kmeans.predict(vec)[0])
    umap_coords = umap.transform(vec)[0]

    return {
        "cluster":       cluster_id,
        "cluster_label": CLUSTER_LABELS.get(cluster_id, f"Cluster {cluster_id}"),
        "umap_x":        round(float(umap_coords[0]), 4),
        "umap_y":        round(float(umap_coords[1]), 4),
    }


demo = gr.Interface(
    fn=predict,
    inputs=gr.JSON(label="384-dim embedding (list of floats)"),
    outputs=gr.JSON(label="Cluster + UMAP result"),
    title="KMeans + UMAP — CFPB",
)

if __name__ == "__main__":
    demo.launch()