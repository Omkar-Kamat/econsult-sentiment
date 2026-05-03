import gradio as gr
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model      = SentenceTransformer(MODEL_NAME)

print(f"MiniLM loaded: {MODEL_NAME}")


def embed(text: str) -> list[float]:
    vec  = model.encode([text], normalize_embeddings=True)[0]
    return [round(float(v), 6) for v in vec]


demo = gr.Interface(
    fn=embed,
    inputs=gr.Textbox(label="Text to embed"),
    outputs=gr.JSON(label="Embedding (384-dim, L2-normalised)"),
    title="MiniLM Embeddings — CFPB",
    description="Returns a 384-dimensional L2-normalised sentence embedding.",
)

if __name__ == "__main__":
    demo.launch()