from typing import List
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import get_runtime_context, get_knowledge_content_service
from app.modules.knowledge.services.base import KnowledgeContentService
from app.modules.knowledge.schemas.content import (
    KnowledgeContentCreate, KnowledgeContentUpdate, PublicationStateTransition
)
from app.modules.knowledge.models.content import KnowledgeContentModel

router = APIRouter()

@router.post("", response_model=KnowledgeContentModel, status_code=status.HTTP_201_CREATED, tags=["Knowledge Content"])
async def create_content(
    payload: KnowledgeContentCreate,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.create_content(
        topic_id=payload.topic_id,
        category=payload.category,
        title=payload.title,
        body=payload.body,
        assets=payload.assets,
        context=context
    )

@router.get("/{content_id}", response_model=KnowledgeContentModel, tags=["Knowledge Content"])
async def get_content(
    content_id: str,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.get_content(content_id=content_id, context=context)

@router.put("/{content_id}", response_model=KnowledgeContentModel, tags=["Knowledge Content"])
async def update_content(
    content_id: str,
    payload: KnowledgeContentUpdate,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.update_content(
        content_id=content_id,
        title=payload.title,
        body=payload.body,
        assets=payload.assets,
        context=context
    )

@router.get("/topic/{topic_id}", response_model=List[KnowledgeContentModel], tags=["Knowledge Content"])
async def list_content_by_topic(
    topic_id: str,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.list_content_by_topic(topic_id=topic_id, context=context)

@router.delete("/{content_id}", response_model=KnowledgeContentModel, tags=["Knowledge Content"])
async def delete_content(
    content_id: str,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.delete_content(content_id=content_id, context=context)

@router.post("/{content_id}/publish", response_model=KnowledgeContentModel, tags=["Knowledge Content"])
async def transition_publication_state(
    content_id: str,
    payload: PublicationStateTransition,
    service: KnowledgeContentService = Depends(get_knowledge_content_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.transition_publication_state(
        content_id=content_id,
        new_status=payload.status,
        context=context
    )
