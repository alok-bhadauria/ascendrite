import uuid
from typing import List, Optional
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel, StructuralState
from app.modules.knowledge.repositories.base import SubjectRepository, SyllabusRepository, ModuleRepository, TopicRepository
from app.modules.knowledge.services.base import AcademicStructureService

class MongoAcademicStructureService(AcademicStructureService):
    def __init__(
        self,
        subject_repo: SubjectRepository,
        syllabus_repo: SyllabusRepository,
        module_repo: ModuleRepository,
        topic_repo: TopicRepository,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService,
        db_ref=None,
        search_service=None
    ):
        self.subject_repo = subject_repo
        self.syllabus_repo = syllabus_repo
        self.module_repo = module_repo
        self.topic_repo = topic_repo
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self.activity_service = activity_service
        # Keep collection references for child-existence checks on delete
        self.db = db_ref
        self.search_service = search_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    async def _has_active_children(self, parent_id: str, child_collection: str, parent_key: str) -> bool:
        if self.db is None:
            return False
        col = self.db[child_collection]
        count = await col.count_documents({
            parent_key: parent_id,
            "status": {"$ne": StructuralState.DELETED.value}
        })
        return count > 0

    # --------------------------------------------------------------------------
    # SUBJECT CRUD
    # --------------------------------------------------------------------------

    async def create_subject(self, name: str, code: str, description: str, category: str, context: RuntimeContext) -> SubjectModel:
        self._require_capability(context, "knowledge:write")
        subject = SubjectModel(
            name=name,
            code=code,
            description=description,
            category=category,
            created_by=context.principal.id
        )
        created = await self.subject_repo.create(subject)

        # Sync index subject in search platform
        if self.search_service:
            await self.search_service.index_subject(created)

        # Triggers side effects
        await self.event_dispatcher.dispatch(Event(name="SubjectCreated", payload={"subject_id": created.id}, context=context))
        await self.audit_service.log("academic.subject.create", f"subject:{created.id}", "success", context, metadata={})
        await self.activity_service.log("subject_create", f"Created Subject: {name}", f"Code: {code}", context, metadata={})
        return created

    async def get_subject(self, subject_id: str, context: RuntimeContext) -> SubjectModel:
        self._require_capability(context, "knowledge:read")
        subject = await self.subject_repo.get_by_id(subject_id)
        if not subject or subject.status == StructuralState.DELETED:
            raise AppException(f"Subject '{subject_id}' not found.", code="NOT_FOUND", status_code=404)
        return subject

    async def list_subjects(self, context: RuntimeContext) -> List[SubjectModel]:
        self._require_capability(context, "knowledge:read")
        return await self.subject_repo.list_all()

    async def update_subject(self, subject_id: str, name: str, code: str, description: str, category: str, context: RuntimeContext) -> SubjectModel:
        self._require_capability(context, "knowledge:write")
        subject = await self.get_subject(subject_id, context)
        subject.name = name
        subject.code = code
        subject.description = description
        subject.category = category
        updated = await self.subject_repo.update(subject_id, subject)

        if self.search_service:
            await self.search_service.index_subject(updated)

        await self.audit_service.log("academic.subject.update", f"subject:{subject_id}", "success", context, metadata={})
        return updated

    async def delete_subject(self, subject_id: str, context: RuntimeContext) -> SubjectModel:
        self._require_capability(context, "knowledge:write")
        subject = await self.get_subject(subject_id, context)

        # Integrity Validation: Check for active syllabuses
        if await self._has_active_children(subject_id, "syllabuses", "subject_id"):
            raise AppException(
                "Cannot delete Subject. Active syllabuses reference it.",
                code="INTEGRITY_VIOLATION",
                status_code=400
            )

        subject.status = StructuralState.DELETED
        updated = await self.subject_repo.update(subject_id, subject)

        if self.search_service:
            await self.search_service.remove_subject(subject_id)

        await self.event_dispatcher.dispatch(Event(name="SubjectDeleted", payload={"subject_id": subject_id}, context=context))
        await self.audit_service.log("academic.subject.delete", f"subject:{subject_id}", "success", context, metadata={})
        await self.activity_service.log("subject_delete", f"Deleted Subject: {subject.name}", "", context, metadata={})
        return updated

    # --------------------------------------------------------------------------
    # SYLLABUS CRUD
    # --------------------------------------------------------------------------

    async def create_syllabus(self, subject_id: str, name: str, version: str, description: str, context: RuntimeContext) -> SyllabusModel:
        self._require_capability(context, "knowledge:write")
        # Validate parent exists
        await self.get_subject(subject_id, context)

        syllabus = SyllabusModel(
            subject_id=subject_id,
            name=name,
            version=version,
            description=description,
            created_by=context.principal.id
        )
        created = await self.syllabus_repo.create(syllabus)

        await self.event_dispatcher.dispatch(Event(name="SyllabusCreated", payload={"syllabus_id": created.id}, context=context))
        await self.audit_service.log("academic.syllabus.create", f"syllabus:{created.id}", "success", context, metadata={})
        await self.activity_service.log("syllabus_create", f"Created Syllabus: {name}", f"Version: {version}", context, metadata={})
        return created

    async def get_syllabus(self, syllabus_id: str, context: RuntimeContext) -> SyllabusModel:
        self._require_capability(context, "knowledge:read")
        syllabus = await self.syllabus_repo.get_by_id(syllabus_id)
        if not syllabus or syllabus.status == StructuralState.DELETED:
            raise AppException(f"Syllabus '{syllabus_id}' not found.", code="NOT_FOUND", status_code=404)
        return syllabus

    async def list_syllabuses_by_subject(self, subject_id: str, context: RuntimeContext) -> List[SyllabusModel]:
        self._require_capability(context, "knowledge:read")
        await self.get_subject(subject_id, context)
        return await self.syllabus_repo.list_by_subject(subject_id)

    async def update_syllabus(self, syllabus_id: str, name: str, version: str, description: str, context: RuntimeContext) -> SyllabusModel:
        self._require_capability(context, "knowledge:write")
        syllabus = await self.get_syllabus(syllabus_id, context)
        syllabus.name = name
        syllabus.version = version
        syllabus.description = description
        updated = await self.syllabus_repo.update(syllabus_id, syllabus)

        await self.audit_service.log("academic.syllabus.update", f"syllabus:{syllabus_id}", "success", context, metadata={})
        return updated

    async def delete_syllabus(self, syllabus_id: str, context: RuntimeContext) -> SyllabusModel:
        self._require_capability(context, "knowledge:write")
        syllabus = await self.get_syllabus(syllabus_id, context)

        # Integrity Validation: Check for active modules
        if await self._has_active_children(syllabus_id, "modules", "syllabus_id"):
            raise AppException(
                "Cannot delete Syllabus. Active modules reference it.",
                code="INTEGRITY_VIOLATION",
                status_code=400
            )

        syllabus.status = StructuralState.DELETED
        updated = await self.syllabus_repo.update(syllabus_id, syllabus)

        await self.event_dispatcher.dispatch(Event(name="SyllabusDeleted", payload={"syllabus_id": syllabus_id}, context=context))
        await self.audit_service.log("academic.syllabus.delete", f"syllabus:{syllabus_id}", "success", context, metadata={})
        await self.activity_service.log("syllabus_delete", f"Deleted Syllabus: {syllabus.name}", "", context, metadata={})
        return updated

    # --------------------------------------------------------------------------
    # MODULE CRUD
    # --------------------------------------------------------------------------

    async def create_module(self, syllabus_id: str, name: str, order: int, description: str, context: RuntimeContext) -> ModuleModel:
        self._require_capability(context, "knowledge:write")
        # Validate parent exists
        await self.get_syllabus(syllabus_id, context)

        module = ModuleModel(
            syllabus_id=syllabus_id,
            name=name,
            order=order,
            description=description,
            created_by=context.principal.id
        )
        created = await self.module_repo.create(module)

        await self.event_dispatcher.dispatch(Event(name="ModuleCreated", payload={"module_id": created.id}, context=context))
        await self.audit_service.log("academic.module.create", f"module:{created.id}", "success", context, metadata={})
        await self.activity_service.log("module_create", f"Created Module: {name}", f"Order: {order}", context, metadata={})
        return created

    async def get_module(self, module_id: str, context: RuntimeContext) -> ModuleModel:
        self._require_capability(context, "knowledge:read")
        module = await self.module_repo.get_by_id(module_id)
        if not module or module.status == StructuralState.DELETED:
            raise AppException(f"Module '{module_id}' not found.", code="NOT_FOUND", status_code=404)
        return module

    async def list_modules_by_syllabus(self, syllabus_id: str, context: RuntimeContext) -> List[ModuleModel]:
        self._require_capability(context, "knowledge:read")
        await self.get_syllabus(syllabus_id, context)
        return await self.module_repo.list_by_syllabus(syllabus_id)

    async def update_module(self, module_id: str, name: str, order: int, description: str, context: RuntimeContext) -> ModuleModel:
        self._require_capability(context, "knowledge:write")
        module = await self.get_module(module_id, context)
        module.name = name
        module.order = order
        module.description = description
        updated = await self.module_repo.update(module_id, module)

        await self.audit_service.log("academic.module.update", f"module:{module_id}", "success", context, metadata={})
        return updated

    async def delete_module(self, module_id: str, context: RuntimeContext) -> ModuleModel:
        self._require_capability(context, "knowledge:write")
        module = await self.get_module(module_id, context)

        # Integrity Validation: Check for active topics
        if await self._has_active_children(module_id, "topics", "module_id"):
            raise AppException(
                "Cannot delete Module. Active topics reference it.",
                code="INTEGRITY_VIOLATION",
                status_code=400
            )

        module.status = StructuralState.DELETED
        updated = await self.module_repo.update(module_id, module)

        await self.event_dispatcher.dispatch(Event(name="ModuleDeleted", payload={"module_id": module_id}, context=context))
        await self.audit_service.log("academic.module.delete", f"module:{module_id}", "success", context, metadata={})
        await self.activity_service.log("module_delete", f"Deleted Module: {module.name}", "", context, metadata={})
        return updated

    # --------------------------------------------------------------------------
    # TOPIC CRUD
    # --------------------------------------------------------------------------

    async def create_topic(self, module_id: str, name: str, order: int, description: str, context: RuntimeContext) -> TopicModel:
        self._require_capability(context, "knowledge:write")
        # Validate parent exists
        await self.get_module(module_id, context)

        topic = TopicModel(
            module_id=module_id,
            name=name,
            order=order,
            description=description,
            created_by=context.principal.id
        )
        created = await self.topic_repo.create(topic)

        await self.event_dispatcher.dispatch(Event(name="TopicCreated", payload={"topic_id": created.id}, context=context))
        await self.audit_service.log("academic.topic.create", f"topic:{created.id}", "success", context, metadata={})
        await self.activity_service.log("topic_create", f"Created Topic: {name}", f"Order: {order}", context, metadata={})
        return created

    async def get_topic(self, topic_id: str, context: RuntimeContext) -> TopicModel:
        self._require_capability(context, "knowledge:read")
        topic = await self.topic_repo.get_by_id(topic_id)
        if not topic or topic.status == StructuralState.DELETED:
            raise AppException(f"Topic '{topic_id}' not found.", code="NOT_FOUND", status_code=404)
        return topic

    async def list_topics_by_module(self, module_id: str, context: RuntimeContext) -> List[TopicModel]:
        self._require_capability(context, "knowledge:read")
        await self.get_module(module_id, context)
        return await self.topic_repo.list_by_module(module_id)

    async def update_topic(self, topic_id: str, name: str, order: int, description: str, context: RuntimeContext) -> TopicModel:
        self._require_capability(context, "knowledge:write")
        topic = await self.get_topic(topic_id, context)
        topic.name = name
        topic.order = order
        topic.description = description
        updated = await self.topic_repo.update(topic_id, topic)

        await self.audit_service.log("academic.topic.update", f"topic:{topic_id}", "success", context, metadata={})
        return updated

    async def delete_topic(self, topic_id: str, context: RuntimeContext) -> TopicModel:
        self._require_capability(context, "knowledge:write")
        topic = await self.get_topic(topic_id, context)

        # Integrity Validation: Check for attached active knowledge content
        if await self._has_active_children(topic_id, "knowledge_contents", "topic_id"):
            raise AppException(
                "Cannot delete Topic. Attached knowledge contents reference it.",
                code="INTEGRITY_VIOLATION",
                status_code=400
            )

        topic.status = StructuralState.DELETED
        updated = await self.topic_repo.update(topic_id, topic)

        await self.event_dispatcher.dispatch(Event(name="TopicDeleted", payload={"topic_id": topic_id}, context=context))
        await self.audit_service.log("academic.topic.delete", f"topic:{topic_id}", "success", context, metadata={})
        await self.activity_service.log("topic_delete", f"Deleted Topic: {topic.name}", "", context, metadata={})
        return updated
