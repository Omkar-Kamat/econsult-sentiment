import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.database import connect_to_mongo, close_mongo_connection
from services.ml_pipeline import ml_pipeline
from routers import classify, respond, clusters, analytics, figures, history

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== ComplaintIQ API Starting ===")
    await connect_to_mongo()
    ml_pipeline.load()
    logger.info("=== ComplaintIQ API Ready ===")
    yield
    logger.info("=== ComplaintIQ API Shutting Down ===")
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "ComplaintIQ API — AI-powered financial complaint triage and response generation. "
        "Built on CFPB complaint data with BERT sentiment classification, "
        "K-Means topic clustering, and T5 abstractive summarisation."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(classify.router)
app.include_router(respond.router)
app.include_router(clusters.router)
app.include_router(analytics.router)
app.include_router(figures.router)
app.include_router(history.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An internal server error occurred.",
            "detail": str(exc) if settings.debug else "Contact support.",
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": f"Route {request.url.path} not found.",
        },
    )

@app.get("/", tags=["Health"])
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "ml_pipeline_loaded": ml_pipeline._loaded,
        "models": {
            "bert": ml_pipeline.bert_model is not None,
            "t5": ml_pipeline.t5_model is not None,
            "kmeans": ml_pipeline.kmeans is not None,
            "encoder": ml_pipeline.encoder is not None,
        }
    }