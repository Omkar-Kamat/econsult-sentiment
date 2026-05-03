from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.loader import load_all
from gateway.routers import analyze, cluster, resolution, trends, query


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all artifacts before accepting requests."""
    print("Starting up — loading artifacts...")
    load_all()
    print("Ready.")
    yield
    print("Shutting down.")


app = FastAPI(
    title="CFPB Complaint Analysis API",
    version="1.0.0",
    description=(
        "Microservice backend for CFPB complaint analysis. "
        "Provides preprocessing, clustering, severity scoring, "
        "resolution prediction, trend detection, and RAG Q&A."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router,    prefix="/analyze",    tags=["analyze"])
app.include_router(cluster.router,    prefix="/cluster",    tags=["cluster"])
app.include_router(resolution.router, prefix="/resolution", tags=["resolution"])
app.include_router(trends.router,     prefix="/trends",     tags=["trends"])
app.include_router(query.router,      prefix="/query",      tags=["query"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "service": "CFPB Complaint Analysis API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/cluster", "/resolution", "/trends", "/query"],
    }