from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from schemas.complaint import ClassifyRequest, ClassifyResponse
from services.ml_pipeline import ml_pipeline
from core.database import get_db
from datetime import datetime, timezone
import logging

router = APIRouter(prefix="/api/v1", tags=["Classification"])
logger = logging.getLogger(__name__)


@router.post("/classify", response_model=ClassifyResponse, summary="Classify a complaint")
async def classify_complaint(
    payload: ClassifyRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        result = ml_pipeline.classify(payload.complaint_text)
    except Exception as e:
        logger.error(f"ML Pipeline error: {e}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

    doc = {
        "raw_text": payload.complaint_text,
        "text_clean": result["text_clean"],
        "text_processed": result["text_processed"],
        "cluster_id": result["cluster_id"],
        "cluster_label": result["cluster_label"],
        "cluster_keywords": result["cluster_keywords"],
        "sentiment": result["sentiment"],
        "sentiment_scores": result["sentiment_scores"],
        "sentiment_confidence": result["sentiment_confidence"],
        "product_hint": result["product_hint"],
        "embedding": result["embedding"],
        "word_count": result["word_count"],
        "processing_ms": result["processing_ms"],
        "session_id": payload.session_id,
        "created_at": datetime.now(timezone.utc),
    }

    insert_result = await db.complaints.insert_one(doc)
    complaint_id = str(insert_result.inserted_id)

    logger.info(
        f"Complaint classified | id={complaint_id} | "
        f"cluster={result['cluster_id']} | sentiment={result['sentiment']} | "
        f"ms={result['processing_ms']}"
    )

    return ClassifyResponse(
        complaint_id=complaint_id,
        cluster_id=result["cluster_id"],
        cluster_label=result["cluster_label"],
        cluster_keywords=result["cluster_keywords"],
        sentiment=result["sentiment"],
        sentiment_scores=result["sentiment_scores"],
        product_hint=result["product_hint"],
        processing_ms=result["processing_ms"],
    )