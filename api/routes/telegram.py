"""
Telegram channel management routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import User, TelegramChannel
from api.schemas.telegram import TelegramChannelCreate, TelegramChannelResponse, TelegramChannelUpdate
from api.services.auth_service import AuthService

router = APIRouter(prefix="/channels", tags=["Telegram Channels"])


@router.post("/", response_model=TelegramChannelResponse, status_code=status.HTTP_201_CREATED)
def create_telegram_channel(
    channel_data: TelegramChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Add a new Telegram channel to monitor

    Args:
        channel_data: Channel configuration
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created channel data
    """
    # Check if channel already exists for this user
    existing_channel = db.query(TelegramChannel).filter(
        TelegramChannel.user_id == current_user.id,
        TelegramChannel.channel_name == channel_data.channel_name
    ).first()

    if existing_channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Channel already exists"
        )

    # Create new channel
    new_channel = TelegramChannel(
        user_id=current_user.id,
        channel_name=channel_data.channel_name,
        channel_id=channel_data.channel_id,
        description=channel_data.description,
        is_active=channel_data.is_active
    )

    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)

    return new_channel


@router.get("/", response_model=List[TelegramChannelResponse])
def list_telegram_channels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    List all Telegram channels for current user

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of telegram channels
    """
    channels = db.query(TelegramChannel).filter(
        TelegramChannel.user_id == current_user.id
    ).offset(skip).limit(limit).all()

    return channels


@router.get("/{channel_id}", response_model=TelegramChannelResponse)
def get_telegram_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Get a specific Telegram channel by ID

    Args:
        channel_id: Channel ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Channel data
    """
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )

    return channel


@router.put("/{channel_id}", response_model=TelegramChannelResponse)
def update_telegram_channel(
    channel_id: int,
    channel_data: TelegramChannelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Update a Telegram channel

    Args:
        channel_id: Channel ID
        channel_data: Updated channel data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated channel data
    """
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )

    # Update fields if provided
    if channel_data.channel_name is not None:
        channel.channel_name = channel_data.channel_name
    if channel_data.description is not None:
        channel.description = channel_data.description
    if channel_data.is_active is not None:
        channel.is_active = channel_data.is_active

    db.commit()
    db.refresh(channel)

    return channel


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_telegram_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Delete a Telegram channel

    Args:
        channel_id: Channel ID
        db: Database session
        current_user: Current authenticated user
    """
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )

    db.delete(channel)
    db.commit()
