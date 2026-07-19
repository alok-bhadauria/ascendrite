import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from app.core.errors import ForbiddenException, AppException
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_event_dispatcher,
    get_audit_service,
    get_activity_service,
    get_asset_service
)
from app.infrastructure.storage.manager import StorageManager
from app.infrastructure.storage.rustfs import get_rustfs
from app.modules.knowledge.repositories.mongo import (
    MongoSubjectRepository,
    MongoSyllabusRepository,
    MongoModuleRepository,
    MongoTopicRepository,
    MongoKnowledgeContentRepository
)
from app.modules.knowledge.models.academic import StructuralState
from app.modules.knowledge.models.content import PublicationState

@pytest.mark.anyio
async def test_academic_hierarchy_and_content_flow(client):
    # Initialize database client local to current event loop
    test_client = AsyncIOMotorClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = test_client["ascendrite"]

    # 1. Initialize Repositories
    subject_repo = MongoSubjectRepository(db)
    syllabus_repo = MongoSyllabusRepository(db)
    module_repo = MongoModuleRepository(db)
    topic_repo = MongoTopicRepository(db)
    content_repo = MongoKnowledgeContentRepository(db)
    from app.modules.assets.repositories.asset import MongoAssetRepository
    asset_repo = MongoAssetRepository(db)

    # 2. Initialize Search & Telemetry
    from app.core.search.mongo import MongoSearchProvider
    from app.core.search.service import SearchService
    search_provider = MongoSearchProvider(db)
    search_serv = SearchService(search_provider)

    event_disp = get_event_dispatcher()
    audit_serv = await get_audit_service(db)
    activity_serv = await get_activity_service(db)

    # 3. Initialize Services
    from app.modules.knowledge.services.academic import MongoAcademicStructureService
    from app.modules.knowledge.services.content import MongoKnowledgeContentService
    from app.modules.assets.services.service import MongoAssetService

    academic_serv = MongoAcademicStructureService(
        subject_repo=subject_repo,
        syllabus_repo=syllabus_repo,
        module_repo=module_repo,
        topic_repo=topic_repo,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv,
        db_ref=db,
        search_service=search_serv
    )

    storage_provider = get_rustfs()
    storage_mgr = StorageManager(storage_provider)
    asset_serv = MongoAssetService(
        repo=asset_repo,
        storage_mgr=storage_mgr,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    content_serv = MongoKnowledgeContentService(
        repo=content_repo,
        academic_service=academic_serv,
        asset_service=asset_serv,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv,
        search_service=search_serv
    )

    # 1. Setup Auth Contexts
    contributor = AuthenticatedPrincipal(
        id="contrib-123",
        identity_type="user",
        role="Contributor",
        capabilities=["knowledge:read", "knowledge:write", "knowledge:publish"]
    )
    ctx_contrib = RuntimeContext(correlation_id="corr-academic-1", principal=contributor)

    student = AuthenticatedPrincipal(
        id="student-999",
        identity_type="user",
        role="Student",
        capabilities=["knowledge:read"]
    )
    ctx_student = RuntimeContext(correlation_id="corr-academic-2", principal=student)

    # --------------------------------------------------------------------------
    # STAGE 3.1: ACADEMIC HIERARCHY TEST
    # --------------------------------------------------------------------------

    # Create Subject
    subject = await academic_serv.create_subject(
        name="Operating Systems",
        code="CS302",
        description="Core OS processes and threads",
        category="core-cs",
        context=ctx_contrib
    )
    assert subject.id is not None
    assert subject.status == StructuralState.ACTIVE

    # Create Syllabus
    syllabus = await academic_serv.create_syllabus(
        subject_id=subject.id,
        name="GLA University B.Tech CSE 2025",
        version="2025.1",
        description="B.Tech curriculum",
        context=ctx_contrib
    )
    assert syllabus.id is not None
    assert syllabus.subject_id == subject.id

    # Try creating syllabus with invalid subject (Validation error)
    with pytest.raises(AppException) as exc:
        await academic_serv.create_syllabus(
            subject_id="invalid-sub-id",
            name="Fail Syllabus",
            version="1.0",
            description="Should fail",
            context=ctx_contrib
        )
    assert exc.value.status_code == 404

    # Create Module
    module = await academic_serv.create_module(
        syllabus_id=syllabus.id,
        name="Process Synchronization",
        order=1,
        description="Semaphores and mutex synchronization rules",
        context=ctx_contrib
    )
    assert module.id is not None

    # Create Topic
    topic = await academic_serv.create_topic(
        module_id=module.id,
        name="Dining Philosophers",
        order=1,
        description="Classical deadlock problem",
        context=ctx_contrib
    )
    assert topic.id is not None

    # Integrity Validation: Try deleting Subject when active Syllabus references it (Fails)
    with pytest.raises(AppException) as exc:
        await academic_serv.delete_subject(subject.id, context=ctx_contrib)
    assert exc.value.status_code == 400
    assert "Active syllabuses reference it" in exc.value.message

    # --------------------------------------------------------------------------
    # STAGE 3.2: KNOWLEDGE CONTENT & ASSET TEST
    # --------------------------------------------------------------------------

    # Create an active Asset to reference (using student upload)
    asset_ctx = RuntimeContext(correlation_id="corr-asset", principal=contributor)
    asset = await asset_serv.upload_asset(
        filename="deadlock_diagram.png",
        content_type="image/png",
        data=b"mock-binary-diagram-stream",
        context=asset_ctx
    )

    # Create Content attached to Topic referencing the Asset (starts as Draft)
    content = await content_serv.create_content(
        topic_id=topic.id,
        category="notes",
        title="Mutex and Deadlock Prevention",
        body="## Mutex Locks\nA lock algorithm preventing race conditions.",
        assets=[asset.id],
        context=ctx_contrib
    )
    assert content.id is not None
    assert content.status == PublicationState.DRAFT
    assert asset.id in content.assets

    # Try creating Content with invalid asset reference (Fails)
    with pytest.raises(AppException) as exc:
        await content_serv.create_content(
            topic_id=topic.id,
            category="revision",
            title="Deadlocks in OS",
            body="Deadlock scenarios",
            assets=["invalid-asset-id"],
            context=ctx_contrib
        )
    assert exc.value.status_code == 400

    # --------------------------------------------------------------------------
    # STAGE 3.3: DISCOVERY & PUBLISHING TEST
    # --------------------------------------------------------------------------

    # Visibility Rule: Student tries to retrieve Draft content (Fails/Forbidden)
    with pytest.raises(ForbiddenException):
        await content_serv.get_content(content.id, context=ctx_student)

    # Contributor retrieves Draft content (Succeeds)
    draft_retrieved = await content_serv.get_content(content.id, context=ctx_contrib)
    assert draft_retrieved.title == "Mutex and Deadlock Prevention"

    # Transition Content status to Published (requires knowledge:publish)
    published_content = await content_serv.transition_publication_state(
        content_id=content.id,
        new_status=PublicationState.PUBLISHED,
        context=ctx_contrib
    )
    assert published_content.status == PublicationState.PUBLISHED

    # Visibility Rule: Student retrieves Published content (Succeeds)
    student_retrieved = await content_serv.get_content(content.id, context=ctx_student)
    assert student_retrieved.status == PublicationState.PUBLISHED

    # Platform Search: Perform regex keyword search
    search_results = await search_serv.search(query="Mutex", doc_type="content", context=ctx_student)
    assert len(search_results) > 0
    assert search_results[0].title == "Mutex and Deadlock Prevention"

    # --------------------------------------------------------------------------
    # RUNTIME TELEMETRY VERIFICATION
    # --------------------------------------------------------------------------
    sync_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    sync_db = sync_client["ascendrite"]

    # Audit check for subject creation and publication transition
    audit_subj = sync_db["audit_logs"].find_one({"action": "academic.subject.create"})
    assert audit_subj is not None
    assert audit_subj["resource"] == f"subject:{subject.id}"

    audit_pub = sync_db["audit_logs"].find_one({"action": "knowledge.content.publish"})
    assert audit_pub is not None
    assert audit_pub["resource"] == f"content:{content.id}"

    # Activity checks
    activity_subj = sync_db["activity_logs"].find_one({"type": "subject_create"})
    assert activity_subj is not None
    assert "Created Subject: Operating Systems" in activity_subj["title"]

    sync_client.close()
    test_client.close()
