"""
Authentication service - user creation and authentication
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.models import User, UserRole
from backend.auth.utils import hash_password, verify_password, create_access_token
from backend.auth.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from backend.utils.logger import logger
from typing import Optional

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    logger.info(f"Created new user: {user_data.email}")
    return new_user

async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> Optional[User]:
    """Authenticate user and return user if valid"""
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    if not verify_password(login_data.password, user.password_hash):
        return None
    
    return user

async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """Get user by ID"""
    from uuid import UUID
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    return result.scalar_one_or_none()

async def generate_token_for_user(user: User) -> TokenResponse:
    """Generate access token for user"""
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=str(user.id),
        email=user.email,
        role=user.role.value
    )
