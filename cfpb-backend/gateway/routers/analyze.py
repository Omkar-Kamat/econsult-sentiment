from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException

from gateway.auth import require_api_key
from shared.schemas import AnalyzeRequest, AnalyzeResponse
from shared.hf_client import call_space
from services.preprocessor import preprocess
from services.severity_service import predict_severity

router = APIRouter()


@router.post("", response_model=AnalyzeResponse)
async def analyze(
    body: AnalyzeRequest,
    _key: str = Depends(require_api_key),
):
    """Full analysis pipeline for a single narrative."""
    prep = preprocess(body.narrative)

    try:
        bert_result = await call_space("sentiment", prep["text_clean"])
        raw_probs = bert_result.get("probs")

        # Validate we actually got a usable probs list before trusting it
        if (
            raw_probs is None
            or not isinstance(raw_probs, list)
            or len(raw_probs) != 3
            or any(p is None for p in raw_probs)
        ):
            raise ValueError(f"Unexpected BERT response shape: {bert_result}")

        prob_negative = float(raw_probs[0])
        prob_neutral  = float(raw_probs[1])
        prob_positive = float(raw_probs[2])
        sentiment     = bert_result.get("label", prep["sentiment"])
        compound      = prep["compound"]

    except (ValueError, KeyError, IndexError, TypeError) as e:
        # Malformed response — fall back to VADER, log it
        print(f"[analyze] BERT Space returned unexpected data, falling back to VADER: {e}")
        prob_negative = prep["prob_negative"]
        prob_neutral  = prep["prob_neutral"]
        prob_positive = prep["prob_positive"]
        sentiment     = prep["sentiment"]
        compound      = prep["compound"]

    except Exception as e:
        # Network/timeout failure — fall back to VADER, log it
        print(f"[analyze] BERT Space call failed, falling back to VADER: {e}")
        prob_negative = prep["prob_negative"]
        prob_neutral  = prep["prob_neutral"]
        prob_positive = prep["prob_positive"]
        sentiment     = prep["sentiment"]
        compound      = prep["compound"]

    severity = predict_severity(
        prob_negative  = prob_negative,
        prob_neutral   = prob_neutral,
        prob_positive  = prob_positive,
        compound       = compound,
        cluster        = 0,
        word_count     = prep["word_count"],
        redaction_count = prep["redaction_count"],
        redaction_density = prep["redaction_density"],
    )

    return AnalyzeResponse(
        text_clean      = prep["text_clean"],
        text_processed  = prep["text_processed"],
        word_count      = prep["word_count"],
        redaction_count = prep["redaction_count"],
        compound        = compound,
        sentiment       = sentiment,
        prob_negative   = prob_negative,
        prob_neutral    = prob_neutral,
        prob_positive   = prob_positive,
        severity_score  = severity,
    )