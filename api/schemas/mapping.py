"""Channel-Broker mapping schemas"""
from pydantic import BaseModel
from datetime import datetime


class ChannelBrokerMappingCreate(BaseModel):
    """Schema for creating a channel-broker mapping"""
    telegram_channel_id: int
    broker_id: int
    is_active: bool = True


class ChannelBrokerMappingResponse(BaseModel):
    """Schema for channel-broker mapping response"""
    id: int
    telegram_channel_id: int
    broker_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
