"""
AI Copilot API routes
"""
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.ai_copilot import service
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from typing import List, Dict

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/copilot")
async def chat_copilot(
    messages: List[Dict] = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chat with AI Copilot"""
    response = await service.chat_with_copilot(messages, str(current_user.id), db)
    return response
