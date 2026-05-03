import os
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print(f"Loading {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)
print(f"MiniLM loaded: {MODEL_NAME}")

app = FastAPI(title="CFPB MiniLM Embed")


class PredictRequest(BaseModel):
    data: list[str]


class PredictResponse(BaseModel):
    data: list[list[float]]


@app.get("/")
def root():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "dim": 384,
        "endpoint": "POST /run/predict with {\"data\": [\"text\"]}",
    }


@app.post("/run/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    Gateway-compatible endpoint.
    Input:  {"data": ["text to embed"]}
    Output: {"data": [[384 floats]]}
    """
    if not req.data:
        return {"data": [[0.0] * 384]}

    text = req.data[0]
    if not isinstance(text, str) or not text.strip():
        return {"data": [[0.0] * 384]}

    vec = model.encode([text], normalize_embeddings=True)[0]
    return {"data": [[round(float(v), 6) for v in vec]]}