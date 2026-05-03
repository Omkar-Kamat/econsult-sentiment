from __future__ import annotations
import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
_API_KEY       = os.getenv("API_KEY", "")


def require_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Dependency — validates the X-API-Key header."""
    if not _API_KEY:
        return "dev"
    if api_key != _API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key