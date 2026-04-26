from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.analytics_service import get_live_analytics
from core.database import get_db

router = APIRouter(prefix="/api/v1", tags=["Analytics"])


@router.get("/analytics", summary="Get dashboard analytics")
async def get_analytics(db: AsyncIOMotorDatabase = Depends(get_db)):
    analytics = await get_live_analytics(db)
    return {"success": True, "data": analytics}