from __future__ import annotations
from fastapi import APIRouter, Depends

from gateway.auth import require_api_key
from shared.schemas import ResolutionRequest, ResolutionResponse
from services.preprocessor import preprocess
from services.resolution_service import predict_resolution

router = APIRouter()


@router.post("", response_model=ResolutionResponse)
async def resolution(
    body: ResolutionRequest,
    _key: str = Depends(require_api_key),
):
    """
    Predict the most likely company resolution for a complaint.

    Pass text_processed and word_count from a prior /analyze call to skip re-preprocessing.
    If text_processed is empty, the narrative is re-preprocessed (slower path).
    """
    if body.text_processed:
        # Fast path: caller already has preprocessed text (typical after /analyze)
        text_processed = body.text_processed
        word_count     = body.word_count if body.word_count > 0 else len(body.narrative.split())
    else:
        # Slow path: preprocess from scratch
        prep           = preprocess(body.narrative)
        text_processed = prep["text_processed"]
        word_count     = prep["word_count"]

    result = predict_resolution(
        text_processed = text_processed,
        issue          = body.issue,
        cluster        = body.cluster,
        compound       = body.compound,
        severity       = body.severity,
        word_count     = word_count,
    )

    return ResolutionResponse(**result)