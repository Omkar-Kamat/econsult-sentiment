from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from services.figure_service import get_figure_path, get_all_figure_metadata, FIGURE_CATALOG

router = APIRouter(prefix="/api/v1", tags=["Figures"])


@router.get("/figures", summary="List all available notebook figures")
async def list_figures(request: Request):
    base_url = str(request.base_url).rstrip("/")
    figures = get_all_figure_metadata(base_url)
    return {"success": True, "data": {"figures": figures, "count": len(figures)}}


@router.get("/figures/{figure_key}", summary="Serve a notebook figure PNG")
async def get_figure(figure_key: str):
    if figure_key not in FIGURE_CATALOG:
        raise HTTPException(
            status_code=404,
            detail=f"Figure '{figure_key}' not found. Valid keys: {list(FIGURE_CATALOG.keys())}"
        )

    path = get_figure_path(figure_key)
    if path is None:
        raise HTTPException(
            status_code=404,
            detail=f"Figure file for '{figure_key}' not found on disk. "
                   f"Ensure the PNG is in static/figures/{figure_key}.png"
        )

    return FileResponse(
        path=str(path),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400"},
    )