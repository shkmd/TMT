"""
Signal Parser Service - Parses trading signals from various formats
"""
import re
from typing import Optional, Dict, Any
from datetime import datetime
from api.models import OrderType, OrderAction, SignalStatus
from loguru import logger


class SignalParser:
    """
    Intelligent parser for trading signals from Telegram messages.
    Handles various formats and normalizes them to a standard structure.
    """

    # Common patterns for signal parsing
    SYMBOL_PATTERNS = [
        r'(?:STOCK|SYMBOL|SCRIPT)[:\s]+([A-Z0-9&]+)',
        r'^([A-Z0-9&]+)(?:\s|$)',  # Symbol at start
        r'(?:BUY|SELL)\s+([A-Z0-9&]+)',
        r'#([A-Z0-9&]+)',  # Hashtag symbol
    ]

    ORDER_TYPE_PATTERNS = {
        OrderType.BUY: [r'\bBUY\b', r'\bLONG\b', r'\bBULL\b', r'\bCALL\b'],
        OrderType.SELL: [r'\bSELL\b', r'\bSHORT\b', r'\bBEAR\b', r'\bPUT\b'],
    }

    ACTION_PATTERNS = {
        OrderAction.ENTRY: [r'\bENTRY\b', r'\bENTER\b', r'\bBUY AT\b', r'\bSELL AT\b'],
        OrderAction.EXIT: [r'\bEXIT\b', r'\bCLOSE\b', r'\bBOOK PROFIT\b', r'\bSQUARE OFF\b'],
        OrderAction.STOPLOSS: [r'\bSTOP\s*LOSS\b', r'\bSL\b', r'\bSTOP\b'],
        OrderAction.TARGET: [r'\bTARGET\b', r'\bTP\b', r'\bTAKE PROFIT\b'],
    }

    PRICE_PATTERNS = {
        'entry': [
            r'(?:ENTRY|BUY|SELL)\s*(?:@|AT|PRICE)?[:\s]+(\d+\.?\d*)',
            r'(?:CMP|CURRENT PRICE)[:\s]+(\d+\.?\d*)',
            r'@\s*(\d+\.?\d*)',
        ],
        'target': [
            r'(?:TARGET|TGT|TP)[:\s]+(\d+\.?\d*)',
            r'(?:TARGET|TGT)\s*1?[:\s]+(\d+\.?\d*)',
        ],
        'stoploss': [
            r'(?:STOP\s*LOSS|SL)[:\s]+(\d+\.?\d*)',
            r'(?:STOP|SL)\s*@?\s*(\d+\.?\d*)',
        ],
    }

    QUANTITY_PATTERNS = [
        r'(?:QTY|QUANTITY)[:\s]+(\d+)',
        r'(?:LOT SIZE|LOTS)[:\s]+(\d+)',
        r'(\d+)\s+(?:SHARES|STOCKS)',
    ]

    @staticmethod
    def parse(raw_message: str) -> Dict[str, Any]:
        """
        Parse a raw trading signal message and extract structured data.

        Args:
            raw_message: The raw message text from Telegram

        Returns:
            Dictionary containing parsed signal data
        """
        logger.info(f"Parsing signal: {raw_message[:100]}...")

        parsed_data = {
            'symbol': None,
            'order_type': None,
            'action': None,
            'quantity': None,
            'entry_price': None,
            'target_price': None,
            'stoploss_price': None,
            'status': SignalStatus.RECEIVED,
            'parsed_data': {},
            'error_message': None
        }

        # Normalize message (uppercase for pattern matching)
        normalized_message = raw_message.upper()

        try:
            # 1. Parse Symbol
            parsed_data['symbol'] = SignalParser._parse_symbol(normalized_message)

            # 2. Parse Order Type (BUY/SELL)
            parsed_data['order_type'] = SignalParser._parse_order_type(normalized_message)

            # 3. Parse Action (ENTRY/EXIT/STOPLOSS/TARGET)
            parsed_data['action'] = SignalParser._parse_action(normalized_message)

            # 4. Parse Prices
            prices = SignalParser._parse_prices(normalized_message)
            parsed_data.update(prices)

            # 5. Parse Quantity
            parsed_data['quantity'] = SignalParser._parse_quantity(normalized_message)

            # 6. Additional data extraction
            parsed_data['parsed_data'] = {
                'original_message': raw_message,
                'normalized_message': normalized_message,
                'parsed_at': datetime.utcnow().isoformat(),
            }

            # Determine parsing status
            if parsed_data['symbol'] and parsed_data['order_type']:
                parsed_data['status'] = SignalStatus.PARSED
                logger.info(f"Successfully parsed signal for {parsed_data['symbol']}")
            else:
                parsed_data['status'] = SignalStatus.FAILED
                parsed_data['error_message'] = "Could not extract required fields (symbol or order type)"
                logger.warning(f"Failed to parse signal: {parsed_data['error_message']}")

        except Exception as e:
            parsed_data['status'] = SignalStatus.FAILED
            parsed_data['error_message'] = f"Parsing error: {str(e)}"
            logger.error(f"Error parsing signal: {str(e)}")

        return parsed_data

    @staticmethod
    def _parse_symbol(text: str) -> Optional[str]:
        """Extract stock symbol from text"""
        for pattern in SignalParser.SYMBOL_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                symbol = match.group(1).strip()
                # Basic validation - stock symbols are usually 3-20 chars
                if 2 <= len(symbol) <= 20:
                    return symbol
        return None

    @staticmethod
    def _parse_order_type(text: str) -> Optional[OrderType]:
        """Extract order type (BUY/SELL) from text"""
        for order_type, patterns in SignalParser.ORDER_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return order_type
        return None

    @staticmethod
    def _parse_action(text: str) -> Optional[OrderAction]:
        """Extract action (ENTRY/EXIT/STOPLOSS/TARGET) from text"""
        for action, patterns in SignalParser.ACTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return action
        # Default to ENTRY if BUY/SELL is found
        if SignalParser._parse_order_type(text):
            return OrderAction.ENTRY
        return None

    @staticmethod
    def _parse_prices(text: str) -> Dict[str, Optional[float]]:
        """Extract prices (entry, target, stoploss) from text"""
        prices = {
            'entry_price': None,
            'target_price': None,
            'stoploss_price': None
        }

        for price_type, patterns in SignalParser.PRICE_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        price = float(match.group(1))
                        prices[f'{price_type}_price'] = price
                        break  # Found price for this type, move to next
                    except (ValueError, IndexError):
                        continue

        return prices

    @staticmethod
    def _parse_quantity(text: str) -> Optional[int]:
        """Extract quantity from text"""
        for pattern in SignalParser.QUANTITY_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        return None

    @staticmethod
    def validate_signal(parsed_signal: Dict[str, Any]) -> bool:
        """
        Validate if a parsed signal has minimum required fields

        Args:
            parsed_signal: Parsed signal dictionary

        Returns:
            True if signal is valid, False otherwise
        """
        required_fields = ['symbol', 'order_type']
        return all(parsed_signal.get(field) is not None for field in required_fields)
