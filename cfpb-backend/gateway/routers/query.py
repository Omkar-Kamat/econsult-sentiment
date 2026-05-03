from __future__ import annotations
import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from gateway.auth import require_api_key
from shared.schemas import QueryRequest, QueryResponse
from shared.hf_client import call_space
from services.rag_service import retrieve, format_results, synthesize_answer

router = APIRouter()


@router.post("", response_model=QueryResponse)
async def query(
    body: QueryRequest,
    _key: str = Depends(require_api_key),
):
    """RAG Q&A over CFPB complaints."""
    try:
        embed_result = await call_space("embed", body.question)
        q_embedding  = np.array(embed_result, dtype="float32")
        norm = np.linalg.norm(q_embedding)
        if norm > 0:
            q_embedding = q_embedding / norm
    except Exception as e:
        print(f"[query] MiniLM Space call failed: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=503,
            detail="Embedding service temporarily unavailable. Please retry."
        )

    filters  = body.filters or {}
    filter_kwargs = {}
    if hasattr(filters, "cluster")      and filters.cluster      is not None:
        filter_kwargs["cluster"]      = filters.cluster
    if hasattr(filters, "sentiment")    and filters.sentiment    is not None:
        filter_kwargs["sentiment"]    = filters.sentiment
    if hasattr(filters, "min_severity") and filters.min_severity is not None:
        filter_kwargs["min_severity"] = filters.min_severity
    if hasattr(filters, "product")      and filters.product      is not None:
        filter_kwargs["product"]      = filters.product

    retrieved = retrieve(q_embedding, top_k=body.top_k, **filter_kwargs)

    if retrieved.empty:
        return QueryResponse(
            question        = body.question,
            answer          = "No complaints matched the specified filters.",
            retrieved       = [],
            total_retrieved = 0,
        )

    answer = (
        await synthesize_answer(body.question, retrieved)
        if body.synthesize
        else f"Retrieved {len(retrieved)} complaints."
    )

    return QueryResponse(
        question        = body.question,
        answer          = answer,
        retrieved       = format_results(retrieved),
        total_retrieved = len(retrieved),
    )