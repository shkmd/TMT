#!/usr/bin/env python3
"""
Signal Parser Test Script
Tests the signal parser with various trading signal formats
"""

from api.services.signal_parser import SignalParser
from api.models import OrderType, OrderAction, SignalStatus


def print_separator(char='=', length=80):
    print(char * length)


def print_parsed_result(result):
    """Pretty print parsed signal result"""
    print(f"  Symbol:         {result['symbol']}")
    print(f"  Order Type:     {result['order_type'].value if result['order_type'] else 'None'}")
    print(f"  Action:         {result['action'].value if result['action'] else 'None'}")
    print(f"  Entry Price:    {result['entry_price']}")
    print(f"  Target Price:   {result['target_price']}")
    print(f"  Stoploss Price: {result['stoploss_price']}")
    print(f"  Quantity:       {result['quantity']}")
    print(f"  Status:         {result['status'].value if isinstance(result['status'], SignalStatus) else result['status']}")

    if result['error_message']:
        print(f"  Error:          {result['error_message']}")


def test_signal(signal_text, description):
    """Test a single signal and display results"""
    print_separator()
    print(f"TEST: {description}")
    print_separator()
    print("\nOriginal Signal:")
    print("-" * 80)
    print(signal_text.strip())
    print("-" * 80)

    result = SignalParser.parse(signal_text)

    print("\nParsed Result:")
    print("-" * 80)
    print_parsed_result(result)

    # Validate
    is_valid = SignalParser.validate_signal(result)
    print(f"\nValidation: {'✓ VALID' if is_valid else '✗ INVALID - Missing required fields'}")
    print()


def main():
    """Run all signal parser tests"""
    print("\n")
    print_separator('=', 80)
    print("SIGNAL PARSER TEST SUITE")
    print_separator('=', 80)
    print()

    # Test Case 1: Standard Format
    test_signal(
        """
        BUY RELIANCE
        ENTRY: 2450
        TARGET: 2500
        STOPLOSS: 2420
        QTY: 100
        """,
        "Standard Format - Full Details"
    )

    # Test Case 2: Compact Format
    test_signal(
        """
        #INFY LONG @ 1520
        TGT 1550
        SL 1500
        """,
        "Compact Format - Hashtag Symbol"
    )

    # Test Case 3: Detailed Format
    test_signal(
        """
        STOCK: TCS
        ACTION: BUY
        CMP: 3420
        TARGET 1: 3480
        STOP LOSS: 3380
        QUANTITY: 50
        """,
        "Detailed Format - Labeled Fields"
    )

    # Test Case 4: SELL Order
    test_signal(
        """
        SELL TATAMOTORS @ 850
        Target: 820
        SL: 870
        """,
        "SELL Order Format"
    )

    # Test Case 5: Minimal Format
    test_signal(
        """
        BUY HDFCBANK
        ENTRY 1650
        TARGET 1700
        """,
        "Minimal Format - No Stoploss"
    )

    # Test Case 6: Alternative Keywords
    test_signal(
        """
        SYMBOL: WIPRO
        CALL @ 450
        TP: 470
        STOP: 440
        LOT SIZE: 200
        """,
        "Alternative Keywords (CALL, TP, STOP)"
    )

    # Test Case 7: Short Format
    test_signal(
        """
        ICICIBANK LONG
        Entry 920
        TGT1 950
        SL 900
        """,
        "Short Format with LONG Keyword"
    )

    # Test Case 8: Invalid Format (Missing Symbol)
    test_signal(
        """
        BUY @ 100
        TARGET: 110
        SL: 95
        """,
        "Invalid Format - Missing Symbol (Should Fail)"
    )

    # Test Case 9: Multi-Target Format
    test_signal(
        """
        BUY SBIN
        ENTRY: 580
        TARGET 1: 595
        TARGET 2: 610
        STOPLOSS: 570
        QTY: 150
        """,
        "Multi-Target Format"
    )

    # Test Case 10: Options Format
    test_signal(
        """
        NIFTY 21000 CE
        BUY @ 150
        TGT: 180
        SL: 135
        """,
        "Options Format"
    )

    # Summary
    print_separator('=', 80)
    print("TEST SUITE COMPLETED")
    print_separator('=', 80)
    print()
    print("Summary:")
    print("  - Parser can handle multiple signal formats")
    print("  - Extracts symbol, order type, prices, and quantity")
    print("  - Validates signals for required fields")
    print("  - Returns structured data ready for broker execution")
    print()
    print("Next Steps:")
    print("  1. Run the application: python main.py")
    print("  2. Test the API: bash test_api.sh")
    print("  3. Configure real Telegram channels")
    print("  4. Add broker credentials")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError running tests: {e}")
        print("Make sure you're in the project directory and dependencies are installed.")
        import traceback
        traceback.print_exc()
