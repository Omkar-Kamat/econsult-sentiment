from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.analytics_service import get_cluster_stats
from core.database import get_db

router = APIRouter(prefix="/api/v1", tags=["Clusters"])


@router.get("/clusters", summary="Get cluster metadata and live complaint counts")
async def get_clusters(db: AsyncIOMotorDatabase = Depends(get_db)):
    clusters = await get_cluster_stats(db)
    return {
        "success": True,
        "data": {
            "clusters": clusters,
            "total_clusters": len(clusters),
        }
    }