import logging
from datetime import datetime, timezone
from typing import List, Optional, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.audit.base import AuditService
from app.modules.collaboration.models.team import TeamModel, TeamMembershipModel, MembershipRole, MembershipStatus
from app.modules.collaboration.repositories.team import TeamRepository, TeamMembershipRepository

logger = logging.getLogger(__name__)

class TeamService:
    def __init__(
        self,
        repo: TeamRepository,
        membership_repo: TeamMembershipRepository,
        db: AsyncIOMotorDatabase,
        audit_service: AuditService
    ):
        self.repo = repo
        self.membership_repo = membership_repo
        self.db = db
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

    async def create_team(self, name: str, description: Optional[str], context: RuntimeContext) -> TeamModel:
        self._require_capability(context, "collab:write")
        owner_id = self._to_db_id(context.principal.id)

        # 1. Create team
        team = TeamModel(name=name, description=description, owner_id=owner_id)
        created = await self.repo.create(team)

        # 2. Add owner membership
        membership = TeamMembershipModel(
            team_id=created.id,
            user_id=owner_id,
            role=MembershipRole.OWNER,
            status=MembershipStatus.ACTIVE,
            invited_by=owner_id
        )
        await self.membership_repo.create(membership)

        await self.audit_service.log("collab.team.create", f"team:{created.id}", "success", context, {})
        return created

    async def invite_member(
        self,
        team_id: str,
        user_id: str,
        role: MembershipRole,
        context: RuntimeContext
    ) -> TeamMembershipModel:
        self._require_capability(context, "collab:write")
        db_team_id = self._to_db_id(team_id)
        db_user_id = self._to_db_id(user_id)

        # 1. Verify team exists and actor is owner
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise AppException(f"Team '{team_id}' not found.", code="NOT_FOUND", status_code=404)
        if str(team.owner_id) != str(context.principal.id) and context.principal.role != "Admin":
            raise ForbiddenException("Only the team owner can invite members.")

        # 2. Verify target user exists in database
        target_user = await self.db["users"].find_one({"_id": db_user_id})
        if not target_user:
            raise AppException(f"Target user '{user_id}' not found.", code="NOT_FOUND", status_code=404)

        # 3. Check existing membership
        existing = await self.membership_repo.get_membership(db_team_id, db_user_id)
        if existing:
            return existing

        # 4. Create membership invitation
        membership = TeamMembershipModel(
            team_id=db_team_id,
            user_id=db_user_id,
            role=role,
            status=MembershipStatus.INVITED,
            invited_by=self._to_db_id(context.principal.id)
        )
        created = await self.membership_repo.create(membership)

        await self.audit_service.log("collab.team.invite", f"team:{team_id}", "success", context, {"invited_user": user_id})
        return created

    async def accept_invitation(self, membership_id: str, context: RuntimeContext) -> TeamMembershipModel:
        self._require_capability(context, "collab:write")
        db_mem_id = self._to_db_id(membership_id)

        membership = await self.membership_repo.get_by_id(membership_id)
        if not membership:
            raise AppException("Invitation not found.", code="NOT_FOUND", status_code=404)
        if str(membership.user_id) != str(context.principal.id):
            raise ForbiddenException("You cannot accept an invitation meant for another user.")

        membership.status = MembershipStatus.ACTIVE
        membership.updated_at = datetime.now(timezone.utc)
        await self.membership_repo.update(membership_id, membership)

        await self.audit_service.log("collab.team.accept", f"membership:{membership_id}", "success", context, {})
        return membership

    async def remove_member(self, team_id: str, user_id: str, context: RuntimeContext) -> bool:
        self._require_capability(context, "collab:write")
        db_team_id = self._to_db_id(team_id)
        db_user_id = self._to_db_id(user_id)

        # 1. Verify team ownership
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise AppException(f"Team '{team_id}' not found.", code="NOT_FOUND", status_code=404)
        if str(team.owner_id) != str(context.principal.id) and context.principal.role != "Admin":
            raise ForbiddenException("Only the team owner can remove members.")

        # 2. Get and delete membership
        membership = await self.membership_repo.get_membership(db_team_id, db_user_id)
        if not membership:
            return False

        if membership.role == MembershipRole.OWNER:
            raise AppException("The owner cannot be removed from the team. Transfer ownership first.", code="OWNER_REMOVAL", status_code=400)

        deleted = await self.membership_repo.delete(str(membership.id))
        if deleted:
            await self.audit_service.log("collab.team.remove_member", f"team:{team_id}", "success", context, {"user_id": user_id})
        return deleted

    async def leave_team(self, team_id: str, context: RuntimeContext) -> bool:
        self._require_capability(context, "collab:write")
        db_team_id = self._to_db_id(team_id)
        db_user_id = self._to_db_id(context.principal.id)

        membership = await self.membership_repo.get_membership(db_team_id, db_user_id)
        if not membership:
            raise AppException("You are not a member of this team.", code="NOT_FOUND", status_code=404)

        if membership.role == MembershipRole.OWNER:
            raise AppException("The owner cannot leave the team. Transfer ownership first.", code="OWNER_LEAVE", status_code=400)

        deleted = await self.membership_repo.delete(str(membership.id))
        if deleted:
            await self.audit_service.log("collab.team.leave", f"team:{team_id}", "success", context, {})
        return deleted

    async def transfer_ownership(self, team_id: str, new_owner_id: str, context: RuntimeContext) -> TeamModel:
        self._require_capability(context, "collab:write")
        db_team_id = self._to_db_id(team_id)
        db_new_owner_id = self._to_db_id(new_owner_id)

        # 1. Verify team ownership
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise AppException(f"Team '{team_id}' not found.", code="NOT_FOUND", status_code=404)
        if str(team.owner_id) != str(context.principal.id) and context.principal.role != "Admin":
            raise ForbiddenException("Only the team owner can transfer ownership.")

        # 2. Verify new owner is active member
        new_mem = await self.membership_repo.get_membership(db_team_id, db_new_owner_id)
        if not new_mem or new_mem.status != MembershipStatus.ACTIVE:
            raise AppException("New owner must be an active member of the team.", code="INVALID_MEMBER", status_code=400)

        # 3. Update roles
        old_mem = await self.membership_repo.get_membership(db_team_id, self._to_db_id(context.principal.id))
        if old_mem:
            old_mem.role = MembershipRole.COLLABORATOR
            await self.membership_repo.update(str(old_mem.id), old_mem)

        new_mem.role = MembershipRole.OWNER
        await self.membership_repo.update(str(new_mem.id), new_mem)

        # 4. Update team owner
        team.owner_id = db_new_owner_id
        team.updated_at = datetime.now(timezone.utc)
        await self.repo.update(team_id, team)

        await self.audit_service.log("collab.team.transfer", f"team:{team_id}", "success", context, {"new_owner": new_owner_id})
        return team
