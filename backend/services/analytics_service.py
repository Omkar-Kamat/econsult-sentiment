import logging
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.ml_pipeline import CLUSTER_METADATA

logger = logging.getLogger(__name__)

MODEL_METRICS = {
    "bert_test_accuracy": 0.8742,
    "bert_test_f1_macro": 0.8615,
    "bert_test_f1_negative": 0.9021,
    "bert_test_f1_neutral": 0.7843,
    "bert_test_f1_positive": 0.7982,
    "training_epochs": 3,
    "training_samples": 14000,
    "val_samples": 3000,
    "test_samples": 3000,
    "max_len": 128,
    "batch_size": 32,
    "learning_rate": 2e-5,
}

DATASET_STATS = {
    "total_source_complaints": 14_700_000,
    "working_sample_size": 20_000,
    "avg_word_count": 98.4,
    "median_word_count": 91.0,
    "p95_word_count": 247.0,
    "redaction_rate_pct": 71.2,
    "product_categories": 5,
    "num_clusters": 3,
}


async def get_live_analytics(db: AsyncIOMotorDatabase) -> dict:
    total_complaints = await db.complaints.count_documents({})
    total_responses = await db.responses.count_documents({})

    sentiment_pipeline = [
        {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    sentiment_cursor = db.complaints.aggregate(sentiment_pipeline)
    sentiment_raw = await sentiment_cursor.to_list(length=10)
    sentiment_distribution = {
        item["_id"]: item["count"] for item in sentiment_raw
    }

    cluster_pipeline = [
        {"$group": {"_id": "$cluster_id", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    cluster_cursor = db.complaints.aggregate(cluster_pipeline)
    cluster_raw = await cluster_cursor.to_list(length=10)
    cluster_distribution = {
        item["_id"]: item["count"] for item in cluster_raw
    }

    return {
        "live": {
            "total_complaints_processed": total_complaints,
            "total_responses_generated": total_responses,
            "sentiment_distribution": sentiment_distribution,
            "cluster_distribution": cluster_distribution,
        },
        "model_metrics": MODEL_METRICS,
        "dataset_stats": DATASET_STATS,
    }


async def get_cluster_stats(db: AsyncIOMotorDatabase) -> list:
    results = []
    total = await db.complaints.count_documents({}) or 1

    for cluster_id, meta in CLUSTER_METADATA.items():
        count = await db.complaints.count_documents({"cluster_id": cluster_id})

        sent_pipeline = [
            {"$match": {"cluster_id": cluster_id}},
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}},
        ]
        sent_cursor = db.complaints.aggregate(sent_pipeline)
        sent_raw = await sent_cursor.to_list(length=5)
        cluster_total = count or 1
        sentiment_breakdown = {
            item["_id"]: round(item["count"] / cluster_total * 100, 1)
            for item in sent_raw
        }

        results.append({
            "id": cluster_id,
            "label": meta["label"],
            "count": count,
            "pct": round(count / total * 100, 1),
            "top_keywords": meta["keywords"],
            "product_hint": meta["product_hint"],
            "context": meta["context"],
            "sentiment_breakdown": sentiment_breakdown,
        })

    return results