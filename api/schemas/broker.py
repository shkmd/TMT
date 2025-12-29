"""Broker schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from api.models import BrokerType


class BrokerCreate(BaseModel):
    """Schema for creating a new broker"""
    broker_type: BrokerType
    broker_name: str = Field(..., description="User-friendly name for the broker")
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    client_id: Optional[str] = None
    access_token: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: bool = True


class BrokerUpdate(BaseModel):
    """Schema for updating a broker"""
    broker_name: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    client_id: Optional[str] = None
    access_token: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class BrokerResponse(BaseModel):
    """Schema for broker response (credentials are masked)"""
    id: int
    user_id: int
    broker_type: BrokerType
    broker_name: str
    is_active: bool
    has_api_key: bool = Field(default=False, description="Whether API key is configured")
    has_api_secret: bool = Field(default=False, description="Whether API secret is configured")
    has_client_id: bool = Field(default=False, description="Whether client ID is configured")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_masking(cls, broker):
        """Create response with masked credentials"""
        return cls(
            id=broker.id,
            user_id=broker.user_id,
            broker_type=broker.broker_type,
            broker_name=broker.broker_name,
            is_active=broker.is_active,
            has_api_key=bool(broker.api_key),
            has_api_secret=bool(broker.api_secret),
            has_client_id=bool(broker.client_id),
            created_at=broker.created_at,
            updated_at=broker.updated_at
        )
