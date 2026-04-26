from pydantic import BaseModel
from typing import Optional, Any


class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None


class ClusterInfo(BaseModel):
    id: int
    label: str
    count: int
    pct: float
    top_keywords: list[str]
    sentiment_breakdown: dict[str, float]
    summary: Optional[str] = None


class FigureMetadata(BaseModel):
    key: str
    title: str
    subtitle: str
    notebook: str
    methodology_note: str
    url: str