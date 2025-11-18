"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.auth import service, schemas
from backend.utils.logger import logger

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    try:
        user = await service.create_user(db, user_data)
        token_response = await service.generate_token_for_user(user)
        return token_response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    login_data: schemas.UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user and return access token"""
    user = await service.authenticate_user(db, login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_response = await service.generate_token_for_user(user)
    logger.info(f"User logged in: {user.email}")
    return token_response
