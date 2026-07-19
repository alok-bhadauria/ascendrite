import logging
from datetime import datetime, timezone
from typing import List, Optional, Any
from bson import ObjectId
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.audit.base import AuditService
from app.modules.collaboration.models.workflow import CollaborationAssignmentModel, CollaborationCommentModel
from app.modules.collaboration.repositories.workflow import CollaborationAssignmentRepository, CollaborationCommentRepository

logger = logging.getLogger(__name__)

class CollaborationWorkflowService:
    def __init__(
        self,
        assignment_repo: CollaborationAssignmentRepository,
        comment_repo: CollaborationCommentRepository,
        audit_service: AuditService
    ):
        self.assignment_repo = assignment_repo
        self.comment_repo = comment_repo
        self.audit_service = audit_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    def _to_db_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def assign_resource(
        self,
        resource_id: str,
        resource_type: str,
        assignee_id: str,
        context: RuntimeContext
    ) -> CollaborationAssignmentModel:
        self._require_capability(context, "collab:write")
        db_assignee_id = self._to_db_id(assignee_id)
        db_actor_id = self._to_db_id(context.principal.id)

        assignment = CollaborationAssignmentModel(
            resource_id=resource_id,
            resource_type=resource_type,
            assignee_id=db_assignee_id,
            assigned_by=db_actor_id,
            status="assigned"
        )
        created = await self.assignment_repo.create(assignment)

        await self.audit_service.log("collab.work.assign", f"resource:{resource_id}", "success", context, {"assignee_id": assignee_id})
        return created

    async def update_assignment_status(
        self,
        assignment_id: str,
        status: str,
        context: RuntimeContext
    ) -> CollaborationAssignmentModel:
        self._require_capability(context, "collab:write")

        assignment = await self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            raise AppException("Assignment not found.", code="NOT_FOUND", status_code=404)

        # Only assignee, assigner, or Admin can update status
        actor_id = str(context.principal.id)
        if actor_id != str(assignment.assignee_id) and actor_id != str(assignment.assigned_by) and context.principal.role != "Admin":
            raise ForbiddenException("Not authorized to update this assignment's status.")

        allowed_statuses = ["assigned", "in_progress", "completed"]
        if status not in allowed_statuses:
            raise AppException(f"Unsupported assignment status: '{status}'.", code="INVALID_STATUS", status_code=400)

        assignment.status = status
        assignment.updated_at = datetime.now(timezone.utc)
        await self.assignment_repo.update(assignment_id, assignment)

        await self.audit_service.log("collab.work.status_update", f"assignment:{assignment_id}", "success", context, {"status": status})
        return assignment

    async def add_comment(
        self,
        resource_id: str,
        content: str,
        context: RuntimeContext
    ) -> CollaborationCommentModel:
        self._require_capability(context, "collab:write")
        author_id = self._to_db_id(context.principal.id)

        comment = CollaborationCommentModel(
            resource_id=resource_id,
            author_id=author_id,
            content=content
        )
        created = await self.comment_repo.create(comment)

        await self.audit_service.log("collab.work.comment", f"resource:{resource_id}", "success", context, {})
        return created

    async def get_comments(self, resource_id: str, context: RuntimeContext) -> List[CollaborationCommentModel]:
        self._require_capability(context, "collab:read")
        return await self.comment_repo.get_by_resource(resource_id)
