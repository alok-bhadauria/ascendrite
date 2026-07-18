from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.config import settings
from core.database import get_database
from models.user import UserModel
from repositories.user import MongoUserRepository, UserRepository
from repositories.progress import MongoProgressRepository, ProgressRepository
from repositories.quiz_submission import MongoQuizSubmissionRepository, QuizSubmissionRepository

async def get_user_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return MongoUserRepository(db)

async def get_progress_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ProgressRepository:
    return MongoProgressRepository(db)

async def get_quiz_submission_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> QuizSubmissionRepository:
    return MongoQuizSubmissionRepository(db)

async def get_current_user(
    request: Request,
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserModel:
    """Resolve active user session from HttpOnly cookies or Bearer Authorization headers"""
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not found in request headers/cookies."
        )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token context."
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired or is invalid."
        )

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account associated with this token was not found."
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )
    return user
