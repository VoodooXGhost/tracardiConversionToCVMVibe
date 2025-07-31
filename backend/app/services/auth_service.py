from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import Optional
import uuid
from datetime import datetime

from ..models import User
from ..schemas import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        return UserResponse.model_validate(user)

    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        
        # Get the actual user record to check password
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if not db_user or not self.verify_password(password, db_user.password_hash):
            return None
        
        return user

    async def create_user(self, user_data: UserCreate, hashed_password: str) -> UserResponse:
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            password_hash=hashed_password
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return UserResponse.model_validate(user)

    async def update_last_login(self, user_id: uuid.UUID):
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if user:
            user.last_login = datetime.utcnow()
            await self.db.commit()