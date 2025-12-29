"""
Telegram Service - Monitor multiple Telegram channels for trading signals
"""
import asyncio
from typing import List, Optional, Callable
from telethon import TelegramClient, events
from telethon.tl.types import Channel
from sqlalchemy.orm import Session
from loguru import logger

from config.settings import settings
from api.models import TelegramChannel as TelegramChannelModel, Signal, SignalStatus
from api.services.signal_parser import SignalParser


class TelegramService:
    """
    Service for monitoring Telegram channels and receiving trading signals.
    Supports multiple channels simultaneously.
    """

    def __init__(self, api_id: int, api_hash: str, session_name: str = "auto_trade_bot"):
        """
        Initialize Telegram service

        Args:
            api_id: Telegram API ID
            api_hash: Telegram API Hash
            session_name: Session name for Telethon client
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client: Optional[TelegramClient] = None
        self.monitored_channels: List[str] = []
        self.signal_callback: Optional[Callable] = None

    async def start(self):
        """Start the Telegram client"""
        if not self.api_id or not self.api_hash:
            raise ValueError("Telegram API credentials not configured")

        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        await self.client.start()
        logger.info("Telegram client started successfully")

    async def stop(self):
        """Stop the Telegram client"""
        if self.client:
            await self.client.disconnect()
            logger.info("Telegram client stopped")

    def set_signal_callback(self, callback: Callable):
        """
        Set callback function to be called when a new signal is received

        Args:
            callback: Async function to call with (channel_id, message_text, message_id)
        """
        self.signal_callback = callback

    async def add_channel(self, channel_username_or_id: str):
        """
        Add a channel to monitor

        Args:
            channel_username_or_id: Channel username (@channel) or ID
        """
        try:
            # Get channel entity
            entity = await self.client.get_entity(channel_username_or_id)

            if isinstance(entity, Channel):
                channel_id = str(entity.id)
                if channel_id not in self.monitored_channels:
                    self.monitored_channels.append(channel_id)
                    logger.info(f"Added channel {entity.title} (ID: {channel_id}) to monitoring")
                    return channel_id
                else:
                    logger.warning(f"Channel {channel_id} already being monitored")
                    return channel_id
            else:
                logger.error(f"Entity {channel_username_or_id} is not a channel")
                return None

        except Exception as e:
            logger.error(f"Error adding channel {channel_username_or_id}: {str(e)}")
            raise

    async def remove_channel(self, channel_id: str):
        """
        Remove a channel from monitoring

        Args:
            channel_id: Channel ID to remove
        """
        if channel_id in self.monitored_channels:
            self.monitored_channels.remove(channel_id)
            logger.info(f"Removed channel {channel_id} from monitoring")

    async def start_monitoring(self, db: Session):
        """
        Start monitoring all configured channels for new messages

        Args:
            db: Database session for storing signals
        """
        if not self.client:
            raise RuntimeError("Telegram client not started. Call start() first.")

        @self.client.on(events.NewMessage)
        async def handle_new_message(event):
            """Handle new messages from monitored channels"""
            try:
                # Get channel ID
                if event.is_channel:
                    channel_id = str(event.chat_id)

                    # Check if this channel is being monitored
                    if channel_id in self.monitored_channels:
                        message_text = event.message.message
                        message_id = str(event.message.id)

                        logger.info(f"New message from channel {channel_id}: {message_text[:100]}")

                        # Find the channel in database
                        telegram_channel = db.query(TelegramChannelModel).filter(
                            TelegramChannelModel.channel_id == channel_id,
                            TelegramChannelModel.is_active == True
                        ).first()

                        if telegram_channel:
                            # Parse the signal
                            parsed_data = SignalParser.parse(message_text)

                            # Create signal record
                            signal = Signal(
                                telegram_channel_id=telegram_channel.id,
                                raw_message=message_text,
                                message_id=message_id,
                                symbol=parsed_data.get('symbol'),
                                order_type=parsed_data.get('order_type'),
                                action=parsed_data.get('action'),
                                quantity=parsed_data.get('quantity'),
                                entry_price=parsed_data.get('entry_price'),
                                target_price=parsed_data.get('target_price'),
                                stoploss_price=parsed_data.get('stoploss_price'),
                                parsed_data=parsed_data.get('parsed_data'),
                                status=parsed_data.get('status', SignalStatus.RECEIVED),
                                error_message=parsed_data.get('error_message')
                            )

                            db.add(signal)
                            db.commit()
                            db.refresh(signal)

                            logger.info(f"Signal saved to database: ID {signal.id}")

                            # Call callback if set
                            if self.signal_callback:
                                await self.signal_callback(signal, db)

            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                db.rollback()

        logger.info(f"Monitoring {len(self.monitored_channels)} channels for trading signals")
        await self.client.run_until_disconnected()

    async def get_channel_info(self, channel_username_or_id: str) -> dict:
        """
        Get information about a Telegram channel

        Args:
            channel_username_or_id: Channel username or ID

        Returns:
            Dictionary with channel information
        """
        try:
            entity = await self.client.get_entity(channel_username_or_id)

            if isinstance(entity, Channel):
                return {
                    'id': str(entity.id),
                    'title': entity.title,
                    'username': entity.username,
                    'participants_count': getattr(entity, 'participants_count', None),
                    'verified': getattr(entity, 'verified', False),
                }
            else:
                raise ValueError("Not a channel")

        except Exception as e:
            logger.error(f"Error getting channel info: {str(e)}")
            raise

    async def test_channel_access(self, channel_username_or_id: str) -> bool:
        """
        Test if we can access a channel

        Args:
            channel_username_or_id: Channel username or ID

        Returns:
            True if accessible, False otherwise
        """
        try:
            await self.client.get_entity(channel_username_or_id)
            return True
        except Exception as e:
            logger.error(f"Cannot access channel {channel_username_or_id}: {str(e)}")
            return False


# Global Telegram service instance
telegram_service: Optional[TelegramService] = None


async def get_telegram_service() -> TelegramService:
    """Get or create global Telegram service instance"""
    global telegram_service

    if telegram_service is None:
        if not settings.TELEGRAM_API_ID or not settings.TELEGRAM_API_HASH:
            raise ValueError("Telegram API credentials not configured in settings")

        telegram_service = TelegramService(
            api_id=settings.TELEGRAM_API_ID,
            api_hash=settings.TELEGRAM_API_HASH,
            session_name=settings.TELEGRAM_SESSION_NAME
        )
        await telegram_service.start()

    return telegram_service
