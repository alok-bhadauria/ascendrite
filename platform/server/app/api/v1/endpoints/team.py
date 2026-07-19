from fastapi import Depends, status, Query
from app.core.routing import APIRouter
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import (
    get_runtime_context,
    get_collaboration_team_service
)
from app.modules.collaboration.services.team import TeamService
from app.modules.collaboration.models.team import MembershipRole

router = APIRouter()

@router.post("/teams", status_code=status.HTTP_201_CREATED, tags=["Collaboration Teams"])
async def create_team(
    name: str = Query(...),
    description: str = Query(None),
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Create a new collaboration team"""
    team = await service.create_team(name, description, context)
    return team.model_dump()

@router.post("/teams/{team_id}/invite", tags=["Collaboration Teams"])
async def invite_member(
    team_id: str,
    user_id: str = Query(...),
    role: MembershipRole = Query(MembershipRole.COLLABORATOR),
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Invite an existing user to join a collaboration team"""
    membership = await service.invite_member(team_id, user_id, role, context)
    return membership.model_dump()

@router.post("/invitations/{membership_id}/accept", tags=["Collaboration Teams"])
async def accept_invitation(
    membership_id: str,
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Accept a pending team membership invitation"""
    membership = await service.accept_invitation(membership_id, context)
    return membership.model_dump()

@router.delete("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Collaboration Teams"])
async def remove_member(
    team_id: str,
    user_id: str,
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Remove a collaborator from a team"""
    await service.remove_member(team_id, user_id, context)

@router.post("/teams/{team_id}/leave", status_code=status.HTTP_204_NO_CONTENT, tags=["Collaboration Teams"])
async def leave_team(
    team_id: str,
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Leave a collaboration team"""
    await service.leave_team(team_id, context)

@router.post("/teams/{team_id}/transfer", tags=["Collaboration Teams"])
async def transfer_ownership(
    team_id: str,
    new_owner_id: str = Query(...),
    service: TeamService = Depends(get_collaboration_team_service),
    context: RuntimeContext = Depends(get_runtime_context)
):
    """Transfer ownership of a collaboration team to another active member"""
    team = await service.transfer_ownership(team_id, new_owner_id, context)
    return team.model_dump()
