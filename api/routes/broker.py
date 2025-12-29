"""
Broker management routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import User, Broker
from api.schemas.broker import BrokerCreate, BrokerResponse, BrokerUpdate
from api.schemas.mapping import ChannelBrokerMappingCreate, ChannelBrokerMappingResponse
from api.models import ChannelBrokerMapping, TelegramChannel
from api.services.auth_service import AuthService

router = APIRouter(prefix="/brokers", tags=["Brokers"])


@router.post("/", response_model=BrokerResponse, status_code=status.HTTP_201_CREATED)
def create_broker(
    broker_data: BrokerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Add a new broker configuration

    Args:
        broker_data: Broker configuration
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created broker data (credentials masked)
    """
    # TODO: Encrypt credentials before storing
    new_broker = Broker(
        user_id=current_user.id,
        broker_type=broker_data.broker_type,
        broker_name=broker_data.broker_name,
        api_key=broker_data.api_key,
        api_secret=broker_data.api_secret,
        client_id=broker_data.client_id,
        access_token=broker_data.access_token,
        config=broker_data.config,
        is_active=broker_data.is_active
    )

    db.add(new_broker)
    db.commit()
    db.refresh(new_broker)

    return BrokerResponse.from_orm_with_masking(new_broker)


@router.get("/", response_model=List[BrokerResponse])
def list_brokers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    List all brokers for current user

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of brokers (credentials masked)
    """
    brokers = db.query(Broker).filter(
        Broker.user_id == current_user.id
    ).offset(skip).limit(limit).all()

    return [BrokerResponse.from_orm_with_masking(broker) for broker in brokers]


@router.get("/{broker_id}", response_model=BrokerResponse)
def get_broker(
    broker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Get a specific broker by ID

    Args:
        broker_id: Broker ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Broker data (credentials masked)
    """
    broker = db.query(Broker).filter(
        Broker.id == broker_id,
        Broker.user_id == current_user.id
    ).first()

    if not broker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broker not found"
        )

    return BrokerResponse.from_orm_with_masking(broker)


@router.put("/{broker_id}", response_model=BrokerResponse)
def update_broker(
    broker_id: int,
    broker_data: BrokerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Update a broker configuration

    Args:
        broker_id: Broker ID
        broker_data: Updated broker data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated broker data (credentials masked)
    """
    broker = db.query(Broker).filter(
        Broker.id == broker_id,
        Broker.user_id == current_user.id
    ).first()

    if not broker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broker not found"
        )

    # Update fields if provided
    if broker_data.broker_name is not None:
        broker.broker_name = broker_data.broker_name
    if broker_data.api_key is not None:
        broker.api_key = broker_data.api_key
    if broker_data.api_secret is not None:
        broker.api_secret = broker_data.api_secret
    if broker_data.client_id is not None:
        broker.client_id = broker_data.client_id
    if broker_data.access_token is not None:
        broker.access_token = broker_data.access_token
    if broker_data.config is not None:
        broker.config = broker_data.config
    if broker_data.is_active is not None:
        broker.is_active = broker_data.is_active

    db.commit()
    db.refresh(broker)

    return BrokerResponse.from_orm_with_masking(broker)


@router.delete("/{broker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broker(
    broker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Delete a broker

    Args:
        broker_id: Broker ID
        db: Database session
        current_user: Current authenticated user
    """
    broker = db.query(Broker).filter(
        Broker.id == broker_id,
        Broker.user_id == current_user.id
    ).first()

    if not broker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broker not found"
        )

    db.delete(broker)
    db.commit()


# Channel-Broker Mapping endpoints
@router.post("/mappings", response_model=ChannelBrokerMappingResponse, status_code=status.HTTP_201_CREATED)
def create_channel_broker_mapping(
    mapping_data: ChannelBrokerMappingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Create a mapping between a Telegram channel and a broker
    Signals from the channel will be automatically sent to the broker

    Args:
        mapping_data: Mapping data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created mapping
    """
    # Verify channel belongs to user
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == mapping_data.telegram_channel_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telegram channel not found"
        )

    # Verify broker belongs to user
    broker = db.query(Broker).filter(
        Broker.id == mapping_data.broker_id,
        Broker.user_id == current_user.id
    ).first()

    if not broker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Broker not found"
        )

    # Check if mapping already exists
    existing_mapping = db.query(ChannelBrokerMapping).filter(
        ChannelBrokerMapping.telegram_channel_id == mapping_data.telegram_channel_id,
        ChannelBrokerMapping.broker_id == mapping_data.broker_id
    ).first()

    if existing_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mapping already exists"
        )

    # Create mapping
    new_mapping = ChannelBrokerMapping(
        telegram_channel_id=mapping_data.telegram_channel_id,
        broker_id=mapping_data.broker_id,
        is_active=mapping_data.is_active
    )

    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)

    return new_mapping


@router.get("/mappings", response_model=List[ChannelBrokerMappingResponse])
def list_channel_broker_mappings(
    channel_id: int = None,
    broker_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    List channel-broker mappings

    Args:
        channel_id: Optional filter by channel ID
        broker_id: Optional filter by broker ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of mappings
    """
    query = db.query(ChannelBrokerMapping)

    if channel_id:
        # Verify channel belongs to user
        channel = db.query(TelegramChannel).filter(
            TelegramChannel.id == channel_id,
            TelegramChannel.user_id == current_user.id
        ).first()
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        query = query.filter(ChannelBrokerMapping.telegram_channel_id == channel_id)

    if broker_id:
        # Verify broker belongs to user
        broker = db.query(Broker).filter(
            Broker.id == broker_id,
            Broker.user_id == current_user.id
        ).first()
        if not broker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Broker not found"
            )
        query = query.filter(ChannelBrokerMapping.broker_id == broker_id)

    mappings = query.all()
    return mappings


@router.delete("/mappings/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel_broker_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Delete a channel-broker mapping

    Args:
        mapping_id: Mapping ID
        db: Database session
        current_user: Current authenticated user
    """
    mapping = db.query(ChannelBrokerMapping).filter(
        ChannelBrokerMapping.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mapping not found"
        )

    # Verify ownership through channel
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == mapping.telegram_channel_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this mapping"
        )

    db.delete(mapping)
    db.commit()
