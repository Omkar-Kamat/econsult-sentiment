from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClassifyRequest(BaseModel):
    complaint_text: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="Raw complaint narrative text",
        example="My credit report shows an account I never opened. "
                "I have disputed this three times with the bureau and nothing has changed."
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID to group multiple complaints together"
    )


class SentimentScores(BaseModel):
    negative: float
    neutral: float
    positive: float


class ClassifyResponse(BaseModel):
    complaint_id: str = Field(..., description="MongoDB document ID of saved complaint")
    cluster_id: int = Field(..., description="0, 1, or 2")
    cluster_label: str = Field(..., description="Human-readable cluster name")
    cluster_keywords: list[str] = Field(..., description="Top 10 TF-IDF keywords for this cluster")
    sentiment: str = Field(..., description="negative | neutral | positive")
    sentiment_scores: SentimentScores
    product_hint: str = Field(..., description="Most likely product category")
    processing_ms: int = Field(..., description="Total inference time in milliseconds")


class RespondRequest(BaseModel):
    complaint_id: str = Field(..., description="ID returned by /classify")
    customer_name: Optional[str] = Field("Valued Customer", description="Customer name for letter salutation")
    account_ref: Optional[str] = Field(None, description="Account or case reference number")
    agent_name: Optional[str] = Field("Customer Relations Team", description="Responding agent name")


class RespondResponse(BaseModel):
    response_id: str = Field(..., description="MongoDB document ID of saved response")
    draft_response: str = Field(..., description="Full AI-generated response letter")
    response_tone: str = Field(..., description="formal-apologetic | formal-informational | formal-resolving")
    suggested_actions: list[str] = Field(..., description="Cluster-specific recommended next steps")
    cluster_context: str = Field(..., description="Brief description of the matched cluster type")
    confidence: float = Field(..., description="Model confidence 0.0–1.0")
    processing_ms: int