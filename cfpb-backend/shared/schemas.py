from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeRequest(BaseModel):
    narrative: str = Field(..., min_length=10, description="Raw complaint narrative text")


class AnalyzeResponse(BaseModel):
    text_clean: str
    text_processed: str
    word_count: int
    redaction_count: int
    compound: float
    sentiment: str
    prob_negative: float
    prob_neutral: float
    prob_positive: float
    severity_score: int


class ClusterRequest(BaseModel):
    narrative: str = Field(..., min_length=10)


class ClusterResponse(BaseModel):
    cluster: int
    cluster_label: str
    top_keywords: list[str]
    umap_x: float
    umap_y: float


class ResolutionRequest(BaseModel):
    narrative: str
    issue: str
    cluster: int
    compound: float
    severity: int = 3
    word_count: int = 100


class ResolutionResponse(BaseModel):
    probabilities: dict[str, float]
    top_prediction: str


class TrendPoint(BaseModel):
    month: str
    cluster: int
    cluster_label: str
    share_pct: float
    total_complaints: int
    is_anomaly: bool
    z_score: float


class TrendsResponse(BaseModel):
    months_analysed: int
    data: list[TrendPoint]
    anomalies: list[TrendPoint]


class QueryFilters(BaseModel):
    cluster: Optional[int] = None
    sentiment: Optional[str] = None
    min_severity: Optional[int] = None
    product: Optional[str] = None


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    top_k: int = Field(default=10, ge=1, le=50)
    filters: Optional[QueryFilters] = None
    synthesize: bool = Field(default=True, description="Call LLM to generate answer")


class RetrievedComplaint(BaseModel):
    rank: int
    similarity: float
    cluster: int
    sentiment: str
    severity_score: int
    product: str
    issue: str
    company_response: str
    narrative_preview: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved: list[RetrievedComplaint]
    total_retrieved: int