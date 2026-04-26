from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ComplaintDocument(BaseModel):
    raw_text: str
    text_clean: str
    text_processed: str
    cluster_id: int
    cluster_label: str
    cluster_keywords: list[str]
    sentiment: str
    sentiment_scores: dict
    sentiment_confidence: float
    product_hint: str
    session_id: Optional[str] = None
    embedding: Optional[list[float]] = None
    word_count: int
    processing_ms: int
    created_at: datetime = Field(default_factory=utc_now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ResponseDocument(BaseModel):
    complaint_id: str
    cluster_id: int
    cluster_label: str
    draft_response: str
    response_tone: str
    suggested_actions: list[str]
    cluster_context: str
    confidence: float
    customer_name: str
    account_ref: Optional[str] = None
    agent_name: str
    status: str = "draft"
    processing_ms: int
    created_at: datetime = Field(default_factory=utc_now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class SessionDocument(BaseModel):
    session_id: str
    complaint_ids: list[str] = []
    response_ids: list[str] = []
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)