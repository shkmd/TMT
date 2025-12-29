"""
Signal monitoring and management routes
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from api.database import get_db
from api.models import User, Signal, TelegramChannel, SignalStatus
from api.schemas.signal import SignalResponse, SignalWithExecutions
from api.services.auth_service import AuthService

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/", response_model=List[SignalResponse])
def list_signals(
    channel_id: Optional[int] = Query(None, description="Filter by telegram channel ID"),
    status: Optional[SignalStatus] = Query(None, description="Filter by signal status"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    List trading signals for current user

    Args:
        channel_id: Optional filter by telegram channel ID
        status: Optional filter by signal status
        symbol: Optional filter by symbol
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of signals
    """
    # Build query to get signals from user's channels only
    query = db.query(Signal).join(TelegramChannel).filter(
        TelegramChannel.user_id == current_user.id
    )

    # Apply filters
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
        query = query.filter(Signal.telegram_channel_id == channel_id)

    if status:
        query = query.filter(Signal.status == status)

    if symbol:
        query = query.filter(Signal.symbol.ilike(f"%{symbol}%"))

    # Order by most recent first
    query = query.order_by(Signal.received_at.desc())

    signals = query.offset(skip).limit(limit).all()
    return signals


@router.get("/{signal_id}", response_model=SignalWithExecutions)
def get_signal(
    signal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Get a specific signal with execution details

    Args:
        signal_id: Signal ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Signal with execution details
    """
    signal = db.query(Signal).join(TelegramChannel).filter(
        Signal.id == signal_id,
        TelegramChannel.user_id == current_user.id
    ).first()

    if not signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signal not found"
        )

    return signal


@router.get("/stats/summary")
def get_signal_stats(
    days: int = Query(7, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Get signal statistics for current user

    Args:
        days: Number of days to analyze
        db: Database session
        current_user: Current authenticated user

    Returns:
        Signal statistics
    """
    # Calculate date range
    start_date = datetime.utcnow() - timedelta(days=days)

    # Get all signals for user's channels in date range
    signals = db.query(Signal).join(TelegramChannel).filter(
        TelegramChannel.user_id == current_user.id,
        Signal.received_at >= start_date
    ).all()

    # Calculate statistics
    total_signals = len(signals)
    parsed_signals = len([s for s in signals if s.status == SignalStatus.PARSED])
    executed_signals = len([s for s in signals if s.status == SignalStatus.EXECUTED])
    failed_signals = len([s for s in signals if s.status == SignalStatus.FAILED])

    # Group by symbol
    symbol_counts = {}
    for signal in signals:
        if signal.symbol:
            symbol_counts[signal.symbol] = symbol_counts.get(signal.symbol, 0) + 1

    # Group by channel
    channel_counts = {}
    for signal in signals:
        channel_id = signal.telegram_channel_id
        channel_counts[channel_id] = channel_counts.get(channel_id, 0) + 1

    return {
        "period_days": days,
        "start_date": start_date.isoformat(),
        "total_signals": total_signals,
        "parsed_signals": parsed_signals,
        "executed_signals": executed_signals,
        "failed_signals": failed_signals,
        "success_rate": round((parsed_signals / total_signals * 100), 2) if total_signals > 0 else 0,
        "execution_rate": round((executed_signals / total_signals * 100), 2) if total_signals > 0 else 0,
        "top_symbols": sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        "signals_by_channel": channel_counts
    }


@router.get("/recent/latest")
def get_latest_signals(
    limit: int = Query(10, ge=1, le=50, description="Number of latest signals to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Get latest signals received (for dashboard/monitoring)

    Args:
        limit: Number of signals to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        Latest signals
    """
    signals = db.query(Signal).join(TelegramChannel).filter(
        TelegramChannel.user_id == current_user.id
    ).order_by(Signal.received_at.desc()).limit(limit).all()

    return [
        {
            "id": signal.id,
            "symbol": signal.symbol,
            "order_type": signal.order_type.value if signal.order_type else None,
            "action": signal.action.value if signal.action else None,
            "status": signal.status.value,
            "received_at": signal.received_at.isoformat(),
            "channel_id": signal.telegram_channel_id,
        }
        for signal in signals
    ]
