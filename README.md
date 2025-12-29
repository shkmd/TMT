# Auto Trade Sync App

Automatically receive trading signals from Telegram channels and execute them on multiple Indian broker platforms (Angel One, Zerodha, Dhan, Upstox).

## Features

- **Multi-Channel Support**: Monitor multiple Telegram channels simultaneously
- **Intelligent Signal Parser**: Parse trading signals in various formats
- **Multi-Broker Integration**: Send signals to multiple brokers
- **User Authentication**: Secure JWT-based authentication
- **Signal History**: Track all received signals and their execution status
- **RESTful API**: Full-featured API for management and monitoring
- **Extensible Architecture**: Easy to add new brokers and signal formats

## Supported Brokers

- ✅ Angel One (Angel Broking)
- ✅ Zerodha Kite Connect
- ✅ Dhan HQ
- ✅ Upstox

## Project Structure

```
TMT/
├── api/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py       # Database connection
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── telegram.py       # Telegram channel management
│   │   ├── broker.py         # Broker management
│   │   └── signal.py         # Signal monitoring
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py   # JWT authentication
│   │   ├── telegram_service.py  # Telegram integration
│   │   ├── signal_parser.py  # Signal parsing logic
│   │   └── broker_service.py # Broker integrations
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── telegram.py
│   │   ├── broker.py
│   │   ├── signal.py
│   │   └── mapping.py
│   └── models.py             # Database models
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration
├── logs/                     # Application logs
├── main.py                   # Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Telegram API credentials (get from https://my.telegram.org/apps)

### Setup

1. **Clone the repository**
   ```bash
   cd TMT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb auto_trade_sync
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run database migrations** (optional - tables auto-create on startup)
   ```bash
   python main.py
   ```

## Configuration

Edit `.env` file with your credentials:

### Required Settings

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/auto_trade_sync"

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY="your-super-secret-key-change-this"

# Telegram API (from https://my.telegram.org/apps)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH="your_telegram_api_hash"
```

### Broker API Credentials

Add credentials for brokers you want to use (stored per-user in database):

- **Angel One**: Get from https://smartapi.angelbroking.com/
- **Zerodha**: Get from https://kite.trade/
- **Dhan**: Get from https://dhanhq.co/
- **Upstox**: Get from https://upstox.com/developer/

## Running the Application

### Development Mode

```bash
python main.py
```

The application will start on `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Guide

### 1. Register and Login

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader1",
    "email": "trader1@example.com",
    "password": "securepassword123"
  }'

# Login to get access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=trader1&password=securepassword123"
```

### 2. Add Telegram Channels

```bash
# Add a channel to monitor
curl -X POST "http://localhost:8000/api/v1/channels/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "@trading_signals",
    "description": "Main trading signals channel",
    "is_active": true
  }'
```

### 3. Configure Brokers

```bash
# Add Angel One broker
curl -X POST "http://localhost:8000/api/v1/brokers/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "broker_type": "angel_one",
    "broker_name": "My Angel One Account",
    "api_key": "your_api_key",
    "client_id": "your_client_id",
    "is_active": true
  }'
```

### 4. Create Channel-Broker Mapping

```bash
# Map channel to broker (signals from channel will go to broker)
curl -X POST "http://localhost:8000/api/v1/brokers/mappings" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_channel_id": 1,
    "broker_id": 1,
    "is_active": true
  }'
```

### 5. Monitor Signals

```bash
# Get latest signals
curl -X GET "http://localhost:8000/api/v1/signals/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get signal statistics
curl -X GET "http://localhost:8000/api/v1/signals/stats/summary?days=7" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Signal Parsing

The app automatically parses various trading signal formats:

### Supported Formats

**Example 1: Standard Format**
```
BUY RELIANCE
ENTRY: 2450
TARGET: 2500
STOPLOSS: 2420
QTY: 100
```

**Example 2: Compact Format**
```
#INFY LONG @ 1520
TGT 1550
SL 1500
```

**Example 3: Detailed Format**
```
STOCK: TCS
ACTION: BUY
CMP: 3420
TARGET 1: 3480
STOP LOSS: 3380
QUANTITY: 50
```

The parser automatically extracts:
- Symbol (stock name)
- Order Type (BUY/SELL)
- Action (ENTRY/EXIT/STOPLOSS/TARGET)
- Prices (entry, target, stoploss)
- Quantity

## Database Schema

### Main Tables

- **users**: User accounts
- **telegram_channels**: Configured Telegram channels
- **brokers**: Broker configurations and credentials
- **signals**: Parsed trading signals
- **signal_executions**: Signal execution history
- **channel_broker_mappings**: Channel-to-broker mappings

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

### Linting

```bash
flake8
```

## Extending the App

### Adding a New Broker

1. Create a new broker class in `api/services/broker_service.py`:

```python
class NewBroker(BaseBroker):
    async def authenticate(self) -> bool:
        # Implement authentication
        pass

    async def place_order(self, symbol, order_type, quantity, price, **kwargs):
        # Implement order placement
        pass
```

2. Register in `BrokerFactory`:

```python
_broker_classes = {
    ...
    BrokerType.NEW_BROKER: NewBroker,
}
```

3. Add to `BrokerType` enum in `api/models.py`

### Customizing Signal Parser

Edit `api/services/signal_parser.py` to add new parsing patterns.

## Security Considerations

⚠️ **Important Security Notes**:

1. **Change SECRET_KEY**: Use a strong, unique secret key in production
2. **Encrypt Broker Credentials**: Consider encrypting broker API keys in database
3. **Use HTTPS**: Always use HTTPS in production
4. **Limit CORS**: Configure specific allowed origins instead of "*"
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Input Validation**: All inputs are validated via Pydantic schemas

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
DATABASE_URL="postgresql://user:password@localhost:5432/auto_trade_sync"
```

### Telegram Connection Error

- Verify TELEGRAM_API_ID and TELEGRAM_API_HASH
- Check you have access to the channels
- Ensure you've authenticated with Telegram (first run creates session)

### Broker API Errors

- Verify broker credentials are correct
- Check if broker API is active
- Review broker-specific documentation

## Production Deployment

### Using Docker

```dockerfile
# Dockerfile (create this file)
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t auto-trade-sync .
docker run -p 8000:8000 --env-file .env auto-trade-sync
```

### Using Systemd

Create `/etc/systemd/system/auto-trade-sync.service`:

```ini
[Unit]
Description=Auto Trade Sync App
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/TMT
Environment="PATH=/path/to/TMT/venv/bin"
ExecStart=/path/to/TMT/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## License

MIT License

## Disclaimer

⚠️ **Trading involves risk**. This software is for educational purposes. The developers are not responsible for any financial losses incurred through the use of this software. Always test thoroughly in a paper trading environment before using with real money.

## Support

For issues and feature requests, please create an issue on GitHub.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Roadmap

- [ ] Add more Indian brokers (Groww, 5Paisa, etc.)
- [ ] Implement webhook support for signals
- [ ] Add strategy backtesting
- [ ] Mobile app for monitoring
- [ ] Advanced risk management features
- [ ] Multi-language support for signals
- [ ] WhatsApp integration
- [ ] Discord integration

## Version History

- **v1.0.0** (2025-01-01): Initial release
  - Multi-channel Telegram monitoring
  - Support for 4 Indian brokers
  - Intelligent signal parsing
  - RESTful API
  - JWT authentication
