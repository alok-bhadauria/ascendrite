from fastapi import APIRouter, HTTPException, status
from app.modules.knowledge.services.curriculum import curriculum_service

router = APIRouter()

@router.get("/subjects", tags=["Curriculum"])
async def list_subjects():
    """List all subjects cached from the decentralized JSON database"""
    return curriculum_service.get_subjects_index()

@router.get("/subject/{subject_id}", tags=["Curriculum"])
async def get_subject(subject_id: str):
    """Retrieve full syllabus metadata and structural modules for a specific subject"""
    sub = curriculum_service.get_subject(subject_id)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with ID '{subject_id}' not found."
        )
    return sub

@router.get("/subject/{subject_id}/{asset_type}/{topic_id}", tags=["Curriculum"])
async def get_topic_asset(subject_id: str, asset_type: str, topic_id: str):
    """Retrieve parsed JSON contents for specific topic assets (notes, revision, quiz, etc.)"""
    allowed_assets = ["notes", "revision", "interview", "diagrams", "examples", "practice", "quiz"]
    if asset_type not in allowed_assets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid asset type. Must be one of: {', '.join(allowed_assets)}"
        )
    
    asset = curriculum_service.get_topic_asset(subject_id, asset_type, topic_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset of type '{asset_type}' not found for topic '{topic_id}' in subject '{subject_id}'."
        )
    return asset
