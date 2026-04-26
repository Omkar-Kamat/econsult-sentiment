from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from schemas.complaint import RespondRequest, RespondResponse
from services.response_bot import generate_response
from core.database import get_db
from datetime import datetime, timezone
import logging

router = APIRouter(prefix="/api/v1", tags=["Response Bot"])
logger = logging.getLogger(__name__)


@router.post("/respond", response_model=RespondResponse, summary="Generate a complaint response")
async def respond_to_complaint(
    payload: RespondRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        complaint_doc = await db.complaints.find_one({"_id": ObjectId(payload.complaint_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid complaint_id format")

    if not complaint_doc:
        raise HTTPException(
            status_code=404,
            detail=f"Complaint {payload.complaint_id} not found"
        )

    try:
        response_data = generate_response(
            complaint_document=complaint_doc,
            customer_name=payload.customer_name,
            account_ref=payload.account_ref,
            agent_name=payload.agent_name,
        )
    except Exception as e:
        logger.error(f"Response generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")

    response_doc = {
        **response_data,
        "complaint_id": payload.complaint_id,
        "status": "draft",
        "created_at": datetime.now(timezone.utc),
    }

    insert_result = await db.responses.insert_one(response_doc)
    response_id = str(insert_result.inserted_id)

    logger.info(
        f"Response generated | response_id={response_id} | "
        f"complaint_id={payload.complaint_id} | cluster={response_data['cluster_id']} | "
        f"ms={response_data['processing_ms']}"
    )

    return RespondResponse(
        response_id=response_id,
        draft_response=response_data["draft_response"],
        response_tone=response_data["response_tone"],
        suggested_actions=response_data["suggested_actions"],
        cluster_context=response_data["cluster_context"],
        confidence=response_data["confidence"],
        processing_ms=response_data["processing_ms"],
    )