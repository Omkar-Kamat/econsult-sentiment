from __future__ import annotations
import numpy as np
import pandas as pd
import faiss
from shared.loader import ARTIFACTS, CLUSTER_LABELS


def _build_prompt(question: str, retrieved: pd.DataFrame) -> str:
    blocks = []
    for i, row in retrieved.iterrows():
        blocks.append(
            f"[Complaint {i + 1}]\n"
            f"Product: {row['product']} | Issue: {row['issue']}\n"
            f"Sentiment: {row['sentiment']} | Severity: {row['severity_score']}\n"
            f"Resolution: {row['company_response']}\n"
            f"Narrative: {str(row['narrative'])[:400]}\n"
        )
    context = "\n".join(blocks)
    return (
        "You are a CFPB complaint analysis assistant. "
        "Answer the following question using ONLY the provided complaints as evidence. "
        "Be concise and cite specific complaint numbers when relevant.\n\n"
        f"QUESTION: {question}\n\n"
        f"COMPLAINTS:\n{context}\n\n"
        "ANSWER:"
    )


def retrieve(
    query_embedding: np.ndarray,
    top_k: int = 10,
    cluster: int | None = None,
    sentiment: str | None = None,
    min_severity: int | None = None,
    product: str | None = None,
) -> pd.DataFrame:
    """FAISS similarity search with optional pre-filters."""
    df         = ARTIFACTS["df"]
    embeddings = ARTIFACTS["embeddings"]
    index      = ARTIFACTS["faiss_index"]

    mask = pd.Series([True] * len(df), index=df.index)
    if cluster is not None:
        mask &= df["cluster"] == cluster
    if sentiment is not None:
        mask &= df["sentiment"] == sentiment
    if min_severity is not None:
        mask &= df["severity_score"] >= min_severity
    if product is not None:
        mask &= df["product"].str.lower().str.contains(
            product.lower(), na=False
        )

    if mask.all():
        q = query_embedding.reshape(1, -1)
        scores, indices = index.search(q, top_k)
        results = df.iloc[indices[0]].copy()
        results["similarity"] = scores[0]
    else:
        sub_df  = df[mask].reset_index(drop=True)
        sub_emb = embeddings[mask.values].astype("float32").copy()
        faiss.normalize_L2(sub_emb)

        sub_index = faiss.IndexFlatIP(embeddings.shape[1])
        sub_index.add(sub_emb)

        q = query_embedding.reshape(1, -1)
        k = min(top_k, len(sub_df))
        scores, indices = sub_index.search(q, k)

        results = sub_df.iloc[indices[0]].copy()
        results["similarity"] = scores[0]

    return results[[
        "similarity", "cluster", "sentiment", "severity_score",
        "product", "issue", "company_response", "narrative",
    ]].reset_index(drop=True)


def format_results(retrieved: pd.DataFrame) -> list[dict]:
    output = []
    for rank, (_, row) in enumerate(retrieved.iterrows(), start=1):
        output.append({
            "rank":              rank,
            "similarity":        round(float(row["similarity"]), 4),
            "cluster":           int(row["cluster"]),
            "sentiment":         str(row["sentiment"]),
            "severity_score":    int(row["severity_score"]),
            "product":           str(row["product"]),
            "issue":             str(row["issue"]),
            "company_response":  str(row["company_response"]),
            "narrative_preview": str(row["narrative"])[:300],
        })
    return output


async def synthesize_answer(question: str, retrieved: pd.DataFrame) -> str:
    """
    Async synthesis: tries T5 Space first, falls back to structured summary.
    """
    from shared.hf_client import call_space

    # Concatenate top-5 narratives as T5 input
    top5 = retrieved.head(5)
    combined = " ".join(str(r["narrative"])[:200] for _, r in top5.iterrows())

    try:
        summary = await call_space("summarize", combined)
        return f"[T5 Summary of top {len(top5)} complaints]: {summary}"
    except Exception as e:
        print(f"[rag] T5 Space call failed, using structured fallback: {e}")

    # Structured fallback
    lines = [f"Retrieved {len(retrieved)} complaints for: '{question}'\n"]
    for i, row in retrieved.iterrows():
        lines.append(
            f"  [{i + 1}] sim={row['similarity']:.3f}  "
            f"cluster={row['cluster']}  sentiment={row['sentiment']}\n"
            f"       {str(row['narrative'])[:200]}"
        )
    return "\n".join(lines)