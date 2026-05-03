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
    """Predict the most likely company resolution for a complaint."""
    prep = preprocess(body.narrative)

    result = predict_resolution(
        text_processed = prep["text_processed"],
        issue          = body.issue,
        cluster        = body.cluster,
        compound       = body.compound,
        severity       = body.severity,
        word_count     = prep["word_count"],
    )

    return ResolutionResponse(**result)