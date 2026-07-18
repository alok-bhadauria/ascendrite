import logging
from typing import Optional
from app.modules.users.models.user import UserModel
from app.modules.users.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password, get_password_hash
from app.modules.users.repositories.user import UserRepository

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> Optional[UserModel]:
        """Register a new student user after verifying username uniqueness"""
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            logger.warning(f"Registration aborted: Email '{user_data.email}' already exists.")
            return None
        
        # Hash password and create database model
        pwd_hash = get_password_hash(user_data.password)
        new_user = UserModel(
            email=user_data.email.lower(),
            password_hash=pwd_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role="Student"
        )
        
        created = await self.user_repo.create(new_user)
        logger.info(f"Successfully registered user ID: {created.id}")
        return created

    async def authenticate_user(self, login_data: UserLogin) -> Optional[UserModel]:
        """Authenticate user credentials using bcrypt password checks"""
        user = await self.user_repo.get_by_email(login_data.email)
        if not user or not user.password_hash:
            logger.warning(f"Authentication failed: User profile not found for '{login_data.email}'")
            return None
        
        if verify_password(login_data.password, user.password_hash):
            return user
            
        logger.warning(f"Authentication failed: Invalid credentials entered for '{login_data.email}'")
        return None
