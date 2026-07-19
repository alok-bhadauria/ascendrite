from typing import List
from fastapi import Depends, status
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import get_runtime_context, get_academic_structure_service
from app.modules.knowledge.services.base import AcademicStructureService
from app.modules.knowledge.schemas.academic import (
    SubjectCreate, SubjectUpdate, SyllabusCreate, SyllabusUpdate,
    ModuleCreate, ModuleUpdate, TopicCreate, TopicUpdate
)
from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel

router = APIRouter()

# ------------------------------------------------------------------------------
# SUBJECT ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/subjects", response_model=SubjectModel, status_code=status.HTTP_201_CREATED, tags=["Academic"])
async def create_subject(
    payload: SubjectCreate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.create_subject(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        category=payload.category,
        context=context
    )

@router.get("/subjects", response_model=List[SubjectModel], tags=["Academic"])
async def list_subjects(
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.list_subjects(context=context)

@router.get("/subjects/{subject_id}", response_model=SubjectModel, tags=["Academic"])
async def get_subject(
    subject_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.get_subject(subject_id=subject_id, context=context)

@router.put("/subjects/{subject_id}", response_model=SubjectModel, tags=["Academic"])
async def update_subject(
    subject_id: str,
    payload: SubjectUpdate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.update_subject(
        subject_id=subject_id,
        name=payload.name,
        code=payload.code,
        description=payload.description,
        category=payload.category,
        context=context
    )

@router.delete("/subjects/{subject_id}", response_model=SubjectModel, tags=["Academic"])
async def delete_subject(
    subject_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.delete_subject(subject_id=subject_id, context=context)

# ------------------------------------------------------------------------------
# SYLLABUS ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/syllabuses", response_model=SyllabusModel, status_code=status.HTTP_201_CREATED, tags=["Academic"])
async def create_syllabus(
    payload: SyllabusCreate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.create_syllabus(
        subject_id=payload.subject_id,
        name=payload.name,
        version=payload.version,
        description=payload.description,
        context=context
    )

@router.get("/syllabuses/subject/{subject_id}", response_model=List[SyllabusModel], tags=["Academic"])
async def list_syllabuses(
    subject_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.list_syllabuses_by_subject(subject_id=subject_id, context=context)

@router.get("/syllabuses/{syllabus_id}", response_model=SyllabusModel, tags=["Academic"])
async def get_syllabus(
    syllabus_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.get_syllabus(syllabus_id=syllabus_id, context=context)

@router.put("/syllabuses/{syllabus_id}", response_model=SyllabusModel, tags=["Academic"])
async def update_syllabus(
    syllabus_id: str,
    payload: SyllabusUpdate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.update_syllabus(
        syllabus_id=syllabus_id,
        name=payload.name,
        version=payload.version,
        description=payload.description,
        context=context
    )

@router.delete("/syllabuses/{syllabus_id}", response_model=SyllabusModel, tags=["Academic"])
async def delete_syllabus(
    syllabus_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.delete_syllabus(syllabus_id=syllabus_id, context=context)

# ------------------------------------------------------------------------------
# MODULE ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/modules", response_model=ModuleModel, status_code=status.HTTP_201_CREATED, tags=["Academic"])
async def create_module(
    payload: ModuleCreate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.create_module(
        syllabus_id=payload.syllabus_id,
        name=payload.name,
        order=payload.order,
        description=payload.description,
        context=context
    )

@router.get("/modules/syllabus/{syllabus_id}", response_model=List[ModuleModel], tags=["Academic"])
async def list_modules(
    syllabus_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.list_modules_by_syllabus(syllabus_id=syllabus_id, context=context)

@router.get("/modules/{module_id}", response_model=ModuleModel, tags=["Academic"])
async def get_module(
    module_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.get_module(module_id=module_id, context=context)

@router.put("/modules/{module_id}", response_model=ModuleModel, tags=["Academic"])
async def update_module(
    module_id: str,
    payload: ModuleUpdate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.update_module(
        module_id=module_id,
        name=payload.name,
        order=payload.order,
        description=payload.description,
        context=context
    )

@router.delete("/modules/{module_id}", response_model=ModuleModel, tags=["Academic"])
async def delete_module(
    module_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.delete_module(module_id=module_id, context=context)

# ------------------------------------------------------------------------------
# TOPIC ENDPOINTS
# ------------------------------------------------------------------------------

@router.post("/topics", response_model=TopicModel, status_code=status.HTTP_201_CREATED, tags=["Academic"])
async def create_topic(
    payload: TopicCreate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.create_topic(
        module_id=payload.module_id,
        name=payload.name,
        order=payload.order,
        description=payload.description,
        context=context
    )

@router.get("/topics/module/{module_id}", response_model=List[TopicModel], tags=["Academic"])
async def list_topics(
    module_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.list_topics_by_module(module_id=module_id, context=context)

@router.get("/topics/{topic_id}", response_model=TopicModel, tags=["Academic"])
async def get_topic(
    topic_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.get_topic(topic_id=topic_id, context=context)

@router.put("/topics/{topic_id}", response_model=TopicModel, tags=["Academic"])
async def update_topic(
    topic_id: str,
    payload: TopicUpdate,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.update_topic(
        topic_id=topic_id,
        name=payload.name,
        order=payload.order,
        description=payload.description,
        context=context
    )

@router.delete("/topics/{topic_id}", response_model=TopicModel, tags=["Academic"])
async def delete_topic(
    topic_id: str,
    service: AcademicStructureService = Depends(get_academic_structure_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    return await service.delete_topic(topic_id=topic_id, context=context)
