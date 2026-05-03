from __future__ import annotations
import os
import httpx
from typing import Any

HF_SPACES: dict[str, str] = {
    "sentiment": os.getenv("HF_BERT_URL", ""),
    "embed":     os.getenv("HF_MINILM_URL", ""),
    "summarize": os.getenv("HF_T5_URL", ""),
    "cluster":   os.getenv("HF_KMEANS_URL", ""),
}

TIMEOUT = 60.0


async def call_space(space: str, payload: Any) -> Any:
    """Call a HuggingFace Gradio Space."""
    url = HF_SPACES.get(space, "")
    if not url:
        raise ValueError(f"HF Space URL not configured for: '{space}'. "
                         f"Set the HF_{space.upper()}_URL environment variable.")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(
            f"{url.rstrip('/')}/run/predict",
            json={"data": [payload]},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()["data"][0]


async def call_space_batch(space: str, payloads: list[Any]) -> list[Any]:
    """Call a Space for a list of payloads concurrently."""
    import asyncio
    tasks = [call_space(space, p) for p in payloads]
    return await asyncio.gather(*tasks)