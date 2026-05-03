from __future__ import annotations
import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from gateway.auth import require_api_key
from shared.schemas import ClusterRequest, ClusterResponse
from shared.hf_client import call_space
from services.preprocessor import preprocess
from services.cluster_service import predict_cluster

router = APIRouter()


@router.post("", response_model=ClusterResponse)
async def cluster(
    body: ClusterRequest,
    _key: str = Depends(require_api_key),
):
    """Cluster a complaint narrative."""
    prep = preprocess(body.narrative)

    try:
        embed_result = await call_space("embed", prep["text_clean"])
        embedding = np.array(embed_result, dtype="float32")
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
    except Exception as e:
        print(f"[cluster] MiniLM Space call failed: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=503,
            detail="Embedding service temporarily unavailable. Please retry."
            # ← Don't leak the Space URL in the error message
        )

    result = predict_cluster(embedding)

    return ClusterResponse(**result)