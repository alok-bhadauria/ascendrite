import asyncio
import pytest
from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import LocalEventDispatcher
from app.core.runtime.audit.service import MongoAuditService
from app.core.runtime.activity.service import MongoActivityService
from app.core.runtime.notification.dispatcher import NotificationDispatcher
from app.core.runtime.notification.channels import InAppChannel, MockEmailChannel, MockSMSChannel, MockPushChannel
from app.core.runtime.tasks.providers import AsyncioBackgroundTaskProvider, FastAPIBackgroundTaskProvider
from app.core.runtime.tasks.scheduler import BackgroundTaskScheduler

@pytest.mark.anyio
async def test_event_dispatcher():
    dispatcher = LocalEventDispatcher()
    event_received = asyncio.Event()
    received_payload = {}

    async def test_handler(event: Event):
        nonlocal received_payload
        received_payload = event.payload
        event_received.set()

    dispatcher.register("UserRegistered", test_handler)

    ctx = RuntimeContext(correlation_id="test-corr-id-1")
    evt = Event(name="UserRegistered", payload={"email": "test@example.com"}, context=ctx)
    
    await dispatcher.dispatch(evt)
    await asyncio.wait_for(event_received.wait(), timeout=1.0)
    
    assert received_payload == {"email": "test@example.com"}

@pytest.mark.anyio
async def test_audit_service(client):
    # We retrieve the database using clear_db sync MongoClient implicitly or using direct motor connection
    from app.infrastructure.database.mongodb import db_manager
    assert db_manager.db is not None
    db: AsyncIOMotorDatabase = db_manager.db

    audit_service = MongoAuditService(db)
    
    principal = AuthenticatedPrincipal(
        id="user-actor-123",
        identity_type="user",
        role="Student",
        capabilities=["knowledge:read"]
    )
    ctx = RuntimeContext(
        correlation_id="corr-audit-123",
        principal=principal,
        ip_address="127.0.0.1",
        user_agent="Pytest Client"
    )

    await audit_service.log(
        action="user.login",
        resource="identity:user-actor-123",
        status="success",
        context=ctx,
        metadata={"auth_method": "password"}
    )

    from pymongo import MongoClient
    sync_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    sync_db = sync_client["ascendrite"]
    record = sync_db["audit_logs"].find_one({"correlation_id": "corr-audit-123"})
    sync_client.close()

    assert record is not None
    assert record["actor_id"] == "user-actor-123"
    assert record["actor_type"] == "user"
    assert record["action"] == "user.login"
    assert record["status"] == "success"
    assert record["metadata"]["ip_address"] == "127.0.0.1"

@pytest.mark.anyio
async def test_activity_service(client):
    from app.infrastructure.database.mongodb import db_manager
    db: AsyncIOMotorDatabase = db_manager.db

    activity_service = MongoActivityService(db)
    principal = AuthenticatedPrincipal(
        id="student-456",
        identity_type="user",
        role="Student",
        capabilities=[]
    )
    ctx = RuntimeContext(correlation_id="corr-act-456", principal=principal)

    await activity_service.log(
        type="module_completed",
        title="TypeScript Fundamentals",
        description="Completed the first modular curriculum track successfully.",
        context=ctx,
        metadata={"score": 100}
    )

    from pymongo import MongoClient
    sync_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    sync_db = sync_client["ascendrite"]
    record = sync_db["activity_logs"].find_one({"correlation_id": "corr-act-456"})
    sync_client.close()

    assert record is not None
    assert record["user_id"] == "student-456"
    assert record["type"] == "module_completed"
    assert record["title"] == "TypeScript Fundamentals"
    assert record["metadata"]["score"] == 100

@pytest.mark.anyio
async def test_notification_channels(client):
    from app.infrastructure.database.mongodb import db_manager
    db: AsyncIOMotorDatabase = db_manager.db

    in_app = InAppChannel(db)
    email = MockEmailChannel()
    sms = MockSMSChannel()
    push = MockPushChannel()

    dispatcher = NotificationDispatcher([in_app, email, sms, push])

    await dispatcher.send(
        recipient_id="recipient-111",
        channels=["in_app", "email", "sms", "push"],
        title="Notification test",
        body="Testing pluggable dispatch routes",
        metadata={"payload_ref": "test"}
    )

    # Verify In-App persistence via sync client
    from pymongo import MongoClient
    sync_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    sync_db = sync_client["ascendrite"]
    record = sync_db["in_app_notifications"].find_one({"recipient_id": "recipient-111"})
    sync_client.close()

    assert record is not None
    assert record["title"] == "Notification test"
    assert record["body"] == "Testing pluggable dispatch routes"

@pytest.mark.anyio
async def test_background_task_providers():
    task_executed = asyncio.Event()
    
    async def dummy_task(arg1, arg2):
        assert arg1 == "hello"
        assert arg2 == "world"
        task_executed.set()

    # 1. Test Asyncio Provider
    async_provider = AsyncioBackgroundTaskProvider()
    scheduler = BackgroundTaskScheduler(async_provider)
    await scheduler.run_in_background(dummy_task, "hello", "world")
    
    await asyncio.wait_for(task_executed.wait(), timeout=1.0)
    assert task_executed.is_set()

    # 2. Test FastAPI Provider
    task_executed_fastapi = False
    def dummy_sync_task(arg):
        nonlocal task_executed_fastapi
        assert arg == "fastapi"
        task_executed_fastapi = True

    fastapi_tasks = BackgroundTasks()
    fastapi_provider = FastAPIBackgroundTaskProvider(fastapi_tasks)
    scheduler_fastapi = BackgroundTaskScheduler(fastapi_provider)
    
    await scheduler_fastapi.run_in_background(dummy_sync_task, "fastapi")
    
    # Execute queued background tasks manually to simulate FastAPI response lifecycle
    await fastapi_tasks()
    assert task_executed_fastapi is True
