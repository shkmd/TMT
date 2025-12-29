"""Signal schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from api.models import SignalStatus, OrderType, OrderAction


class SignalCreate(BaseModel):
    """Schema for creating a signal (usually from Telegram)"""
    telegram_channel_id: int
    raw_message: str
    message_id: Optional[str] = None


class ParsedSignalData(BaseModel):
    """Schema for parsed signal data"""
    symbol: Optional[str] = None
    order_type: Optional[OrderType] = None
    action: Optional[OrderAction] = None
    quantity: Optional[int] = None
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    stoploss_price: Optional[float] = None


class SignalResponse(BaseModel):
    """Schema for signal response"""
    id: int
    telegram_channel_id: int
    raw_message: str
    message_id: Optional[str]
    symbol: Optional[str]
    order_type: Optional[OrderType]
    action: Optional[OrderAction]
    quantity: Optional[int]
    entry_price: Optional[float]
    target_price: Optional[float]
    stoploss_price: Optional[float]
    parsed_data: Optional[Dict[str, Any]]
    status: SignalStatus
    error_message: Optional[str]
    signal_time: Optional[datetime]
    received_at: datetime
    parsed_at: Optional[datetime]

    class Config:
        from_attributes = True


class SignalExecutionResponse(BaseModel):
    """Schema for signal execution response"""
    id: int
    signal_id: int
    broker_id: int
    order_id: Optional[str]
    status: str
    executed_price: Optional[float]
    executed_quantity: Optional[int]
    broker_response: Optional[Dict[str, Any]]
    error_message: Optional[str]
    executed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class SignalWithExecutions(SignalResponse):
    """Schema for signal with execution details"""
    executions: List[SignalExecutionResponse] = []

    class Config:
        from_attributes = True
