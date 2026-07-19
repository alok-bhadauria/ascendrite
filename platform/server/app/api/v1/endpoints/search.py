from typing import List, Optional
from fastapi import Depends, Query
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import get_runtime_context, get_search_service
from app.core.search.service import SearchService
from app.core.search.base import SearchDocument

router = APIRouter()

@router.get("", response_model=List[SearchDocument], tags=["Search"])
async def platform_search(
    q: str = Query(..., min_length=1),
    doc_type: Optional[str] = Query(None, description="subject | content"),
    service: SearchService = Depends(get_search_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.search(query=q, doc_type=doc_type, context=context)
