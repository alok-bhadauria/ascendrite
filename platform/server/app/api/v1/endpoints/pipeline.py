from fastapi import Depends, status, Query
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_creator_pipeline_service
)
from app.modules.creator.services.pipeline import PublishingPipelineService
from app.modules.creator.models.workflow import PublishingWorkflowModel

router = APIRouter()

@router.post("/{draft_id}/submit-review", tags=["Creator Publishing"])
async def submit_for_review(
    draft_id: str,
    notes: str = Query(""),
    service: PublishingPipelineService = Depends(get_creator_pipeline_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Submit a validated draft for administrative/collaborator review"""
    wf = await service.submit_for_review(draft_id, notes, context)
    return wf.model_dump()

@router.post("/{draft_id}/approve", tags=["Creator Publishing"])
async def approve_draft(
    draft_id: str,
    notes: str = Query(""),
    service: PublishingPipelineService = Depends(get_creator_pipeline_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Approve a draft resource, moving it to approved state ready for publication"""
    wf = await service.approve_draft(draft_id, notes, context)
    return wf.model_dump()

@router.post("/{draft_id}/reject", tags=["Creator Publishing"])
async def reject_draft(
    draft_id: str,
    notes: str = Query(""),
    service: PublishingPipelineService = Depends(get_creator_pipeline_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Reject a draft resource and return it to creator for revision"""
    wf = await service.reject_draft(draft_id, notes, context)
    return wf.model_dump()

@router.post("/{draft_id}/publish", tags=["Creator Publishing"])
async def publish_draft(
    draft_id: str,
    service: PublishingPipelineService = Depends(get_creator_pipeline_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Finalize and publish the approved draft resource to the active learning system"""
    wf = await service.publish_draft(draft_id, context)
    return wf.model_dump()

@router.get("/{draft_id}/workflow", tags=["Creator Publishing"])
async def get_workflow(
    draft_id: str,
    service: PublishingPipelineService = Depends(get_creator_pipeline_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Retrieve the current publication workflow state and transition history"""
    wf = await service.get_workflow_by_draft(draft_id, context)
    return wf.model_dump()
