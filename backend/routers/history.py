from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from core.database import get_db
from datetime import datetime, timezone
import logging

router = APIRouter(prefix="/api/v1", tags=["History"])
logger = logging.getLogger(__name__)


def serialize_doc(doc: dict) -> dict:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


@router.get("/history", summary="Get complaint processing history")
async def get_history(
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    cluster_id: int = Query(None, description="Filter by cluster (0, 1, or 2)"),
    sentiment: str = Query(None, description="Filter by sentiment (negative/neutral/positive)"),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    query = {}
    if cluster_id is not None:
        query["cluster_id"] = cluster_id
    if sentiment:
        query["sentiment"] = sentiment

    cursor = (
        db.complaints.find(query, {"embedding": 0})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    docs = await cursor.to_list(length=limit)
    total = await db.complaints.count_documents(query)

    return {
        "success": True,
        "data": {
            "complaints": [serialize_doc(doc) for doc in docs],
            "total": total,
            "limit": limit,
            "skip": skip,
        },
    }


@router.get("/history/{complaint_id}", summary="Get a single complaint with its response")
async def get_complaint_detail(
    complaint_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        complaint = await db.complaints.find_one(
            {"_id": ObjectId(complaint_id)}, {"embedding": 0}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid complaint_id format")

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    response = await db.responses.find_one({"complaint_id": complaint_id})

    return {
        "success": True,
        "data": {
            "complaint": serialize_doc(complaint),
            "response": serialize_doc(response) if response else None,
        },
    }


@router.patch("/history/{response_id}/status", summary="Update response status")
async def update_response_status(
    response_id: str,
    status: str = Query(..., description="New status: draft | sent | archived"),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    if status not in ("draft", "sent", "archived"):
        raise HTTPException(status_code=400, detail="Status must be: draft, sent, or archived")

    result = await db.responses.update_one(
        {"_id": ObjectId(response_id)},
        {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Response not found")

    return {"success": True, "message": f"Response status updated to '{status}'"}