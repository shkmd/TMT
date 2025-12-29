"""Telegram channel schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TelegramChannelCreate(BaseModel):
    """Schema for creating a new telegram channel"""
    channel_name: str = Field(..., description="Channel username (@channel) or title")
    channel_id: Optional[str] = Field(None, description="Telegram channel ID (auto-detected if not provided)")
    description: Optional[str] = None
    is_active: bool = True


class TelegramChannelUpdate(BaseModel):
    """Schema for updating a telegram channel"""
    channel_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TelegramChannelResponse(BaseModel):
    """Schema for telegram channel response"""
    id: int
    user_id: int
    channel_name: str
    channel_id: Optional[str]
    is_active: bool
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
