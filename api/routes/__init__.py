"""API routes module"""
from .auth import router as auth_router
from .telegram import router as telegram_router
from .broker import router as broker_router
from .signal import router as signal_router

__all__ = ["auth_router", "telegram_router", "broker_router", "signal_router"]
