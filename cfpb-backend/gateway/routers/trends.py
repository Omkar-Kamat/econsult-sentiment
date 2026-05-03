from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, Query

from gateway.auth import require_api_key
from shared.schemas import TrendsResponse
from services.trend_service import get_trends

router = APIRouter()


@router.get("", response_model=TrendsResponse)
async def trends(
    months:  Optional[int] = Query(default=None, ge=1, le=120,
                                    description="Number of recent months to return"),
    cluster: Optional[int] = Query(default=None, ge=0,
                                    description="Filter to a specific cluster id"),
    _key: str = Depends(require_api_key),
):
    """Return monthly cluster share time-series with anomaly flags."""
    result = get_trends(months=months, cluster=cluster)
    return TrendsResponse(**result)