"""
Database models for Auto Trade Sync App
"""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON, Float
from sqlalchemy.orm import relationship
from api.database.database import Base


class BrokerType(PyEnum):
    """Supported broker types"""
    ANGEL_ONE = "angel_one"
    ZERODHA = "zerodha"
    DHAN = "dhan"
    UPSTOX = "upstox"


class SignalStatus(PyEnum):
    """Signal processing status"""
    RECEIVED = "received"
    PARSED = "parsed"
    EXECUTING = "executing"
    EXECUTED = "executed"
    FAILED = "failed"
    IGNORED = "ignored"


class OrderType(PyEnum):
    """Order types"""
    BUY = "buy"
    SELL = "sell"


class OrderAction(PyEnum):
    """Order actions"""
    ENTRY = "entry"
    EXIT = "exit"
    STOPLOSS = "stoploss"
    TARGET = "target"


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    telegram_channels = relationship("TelegramChannel", back_populates="user", cascade="all, delete-orphan")
    brokers = relationship("Broker", back_populates="user", cascade="all, delete-orphan")


class TelegramChannel(Base):
    """Telegram channel configuration"""
    __tablename__ = "telegram_channels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_name = Column(String(255), nullable=False)  # @channelname or channel title
    channel_id = Column(String(100), unique=True, index=True)  # Telegram channel ID
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="telegram_channels")
    signals = relationship("Signal", back_populates="telegram_channel", cascade="all, delete-orphan")


class Broker(Base):
    """Broker configuration and credentials"""
    __tablename__ = "brokers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_type = Column(Enum(BrokerType), nullable=False)
    broker_name = Column(String(100), nullable=False)  # User-friendly name
    is_active = Column(Boolean, default=True)

    # Encrypted credentials (will be encrypted before storing)
    api_key = Column(String(500), nullable=True)
    api_secret = Column(String(500), nullable=True)
    client_id = Column(String(255), nullable=True)
    access_token = Column(String(500), nullable=True)
    refresh_token = Column(String(500), nullable=True)

    # Additional broker-specific configuration
    config = Column(JSON, nullable=True)  # Store additional config as JSON

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="brokers")
    signal_executions = relationship("SignalExecution", back_populates="broker", cascade="all, delete-orphan")


class Signal(Base):
    """Parsed trading signals"""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    telegram_channel_id = Column(Integer, ForeignKey("telegram_channels.id"), nullable=False)

    # Original message
    raw_message = Column(Text, nullable=False)
    message_id = Column(String(100), nullable=True)  # Telegram message ID

    # Parsed signal data
    symbol = Column(String(50), nullable=True)  # Stock symbol
    order_type = Column(Enum(OrderType), nullable=True)  # BUY/SELL
    action = Column(Enum(OrderAction), nullable=True)  # ENTRY/EXIT/STOPLOSS/TARGET
    quantity = Column(Integer, nullable=True)
    entry_price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    stoploss_price = Column(Float, nullable=True)

    # Additional parsed data
    parsed_data = Column(JSON, nullable=True)  # Store all parsed fields

    # Status
    status = Column(Enum(SignalStatus), default=SignalStatus.RECEIVED)
    error_message = Column(Text, nullable=True)

    # Timestamps
    signal_time = Column(DateTime, nullable=True)  # Time when signal was generated
    received_at = Column(DateTime, default=datetime.utcnow)
    parsed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    telegram_channel = relationship("TelegramChannel", back_populates="signals")
    executions = relationship("SignalExecution", back_populates="signal", cascade="all, delete-orphan")


class SignalExecution(Base):
    """Track signal execution to brokers"""
    __tablename__ = "signal_executions"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    broker_id = Column(Integer, ForeignKey("brokers.id"), nullable=False)

    # Execution details
    order_id = Column(String(100), nullable=True)  # Order ID from broker
    status = Column(String(50), nullable=False)  # pending, executed, failed, cancelled
    executed_price = Column(Float, nullable=True)
    executed_quantity = Column(Integer, nullable=True)

    # Response from broker
    broker_response = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

    # Timestamps
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    signal = relationship("Signal", back_populates="executions")
    broker = relationship("Broker", back_populates="signal_executions")


class ChannelBrokerMapping(Base):
    """Map which telegram channels send signals to which brokers"""
    __tablename__ = "channel_broker_mappings"

    id = Column(Integer, primary_key=True, index=True)
    telegram_channel_id = Column(Integer, ForeignKey("telegram_channels.id"), nullable=False)
    broker_id = Column(Integer, ForeignKey("brokers.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
