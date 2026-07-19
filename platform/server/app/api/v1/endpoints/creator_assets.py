from typing import List, Dict, Any
from fastapi import Depends, status, Query
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_creator_asset_service
)
from app.modules.creator.services.attachment import AssetAttachmentService
from app.modules.creator.models.attachment import AssetAttachmentModel

router = APIRouter()

@router.post("/{draft_id}/assets/attach", status_code=status.HTTP_201_CREATED, tags=["Creator Assets"])
async def attach_asset(
    draft_id: str,
    asset_id: str = Query(...),
    service: AssetAttachmentService = Depends(get_creator_asset_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Attach an upload asset to a workspace draft resource"""
    return await service.attach_asset(draft_id, asset_id, context)

@router.delete("/{draft_id}/assets/detach", status_code=status.HTTP_204_NO_CONTENT, tags=["Creator Assets"])
async def detach_asset(
    draft_id: str,
    asset_id: str = Query(...),
    service: AssetAttachmentService = Depends(get_creator_asset_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Detach an attached asset from a workspace draft resource"""
    await service.detach_asset(draft_id, asset_id, context)

@router.get("/{draft_id}/assets", response_model=List[Dict[str, Any]], tags=["Creator Assets"])
async def get_attachments(
    draft_id: str,
    service: AssetAttachmentService = Depends(get_creator_asset_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve all assets currently attached to a workspace draft resource"""
    links = await service.get_attachments(draft_id, context)
    return [l.model_dump() for l in links]
