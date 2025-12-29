# Local Setup and Testing Guide

This guide will help you set up and test the Auto Trade Sync App on your local machine.

## Prerequisites

Before starting, ensure you have:

- **Python 3.9 or higher** installed
- **PostgreSQL 12+** installed and running
- **Git** installed
- A **Telegram account** (for API credentials)

## Step 1: Check Prerequisites

```bash
# Check Python version (should be 3.9+)
python --version
# or
python3 --version

# Check PostgreSQL installation
psql --version

# Check if PostgreSQL is running
# On Linux:
sudo systemctl status postgresql

# On macOS:
brew services list | grep postgresql

# On Windows:
# Check Services app for PostgreSQL service
```

## Step 2: Install PostgreSQL (if not installed)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Windows
Download and install from: https://www.postgresql.org/download/windows/

## Step 3: Set Up PostgreSQL Database

```bash
# Switch to postgres user (Linux)
sudo -u postgres psql

# Or connect directly (macOS/Windows)
psql postgres

# Inside PostgreSQL shell, run:
CREATE DATABASE auto_trade_sync;
CREATE USER trade_user WITH PASSWORD 'trade_password_123';
GRANT ALL PRIVILEGES ON DATABASE auto_trade_sync TO trade_user;
\q
```

Test the connection:
```bash
psql -U trade_user -d auto_trade_sync -h localhost
# Enter password: trade_password_123
# If successful, type \q to quit
```

## Step 4: Clone and Navigate to Project

```bash
cd /home/user/TMT
# or wherever your project is located
```

## Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your prompt should now show (venv)
```

## Step 6: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will take a few minutes...
```

## Step 7: Get Telegram API Credentials

1. Go to https://my.telegram.org/auth
2. Log in with your phone number
3. Click on "API Development Tools"
4. Fill in the form:
   - App title: "Auto Trade Sync App"
   - Short name: "trade_sync"
   - Platform: Desktop
   - Description: "Auto trading signal sync"
5. Click "Create application"
6. **Copy your `api_id` and `api_hash`** - you'll need these!

## Step 8: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file
nano .env
# or use your preferred editor: vim .env, code .env, etc.
```

**Update these values in `.env`:**

```env
# Database - Use the credentials from Step 3
DATABASE_URL="postgresql://trade_user:trade_password_123@localhost:5432/auto_trade_sync"

# Security - Generate a strong secret key
SECRET_KEY="your-super-secret-key-$(openssl rand -hex 32)"

# Telegram - Use your credentials from Step 7
TELEGRAM_API_ID=12345678  # Your actual API ID
TELEGRAM_API_HASH="abcdef1234567890abcdef1234567890"  # Your actual API hash

# Keep other settings as default for now
DEBUG=true
LOG_LEVEL="INFO"
```

**Quick secret key generator:**
```bash
# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the output to SECRET_KEY in .env
```

## Step 9: Create Logs Directory

```bash
mkdir -p logs
```

## Step 10: Run the Application

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Run the app
python main.py
```

You should see output like:
```
2025-01-01 10:00:00 | INFO     | Starting Auto Trade Sync App v1.0.0
2025-01-01 10:00:00 | INFO     | Database tables created successfully
2025-01-01 10:00:00 | INFO     | Application started on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**🎉 Your app is now running!**

## Step 11: Test the API

### Option 1: Using Web Browser

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints interactively from Swagger UI!

### Option 2: Using curl (Command Line)

Open a **new terminal** (keep the app running in the first terminal):

#### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Auto Trade Sync App",
  "version": "1.0.0"
}
```

#### Test 2: Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Expected response:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-01-01T10:00:00"
}
```

#### Test 3: Login and Get Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=SecurePass123!"
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Copy the `access_token` - you'll need it for the next requests!**

Set it as a variable for easier testing:
```bash
export TOKEN="your_access_token_here"
# Replace with your actual token from the login response
```

#### Test 4: Add a Telegram Channel
```bash
curl -X POST "http://localhost:8000/api/v1/channels/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "@test_trading_signals",
    "channel_id": "1234567890",
    "description": "Test trading channel",
    "is_active": true
  }'
```

#### Test 5: List Your Channels
```bash
curl -X GET "http://localhost:8000/api/v1/channels/" \
  -H "Authorization: Bearer $TOKEN"
```

#### Test 6: Add a Broker
```bash
curl -X POST "http://localhost:8000/api/v1/brokers/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "broker_type": "angel_one",
    "broker_name": "My Angel One Account",
    "api_key": "test_api_key",
    "client_id": "test_client_id",
    "is_active": true
  }'
```

#### Test 7: List Your Brokers
```bash
curl -X GET "http://localhost:8000/api/v1/brokers/" \
  -H "Authorization: Bearer $TOKEN"
```

#### Test 8: Create Channel-Broker Mapping
```bash
curl -X POST "http://localhost:8000/api/v1/brokers/mappings" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_channel_id": 1,
    "broker_id": 1,
    "is_active": true
  }'
```

#### Test 9: View Signals (will be empty initially)
```bash
curl -X GET "http://localhost:8000/api/v1/signals/" \
  -H "Authorization: Bearer $TOKEN"
```

### Option 3: Using Postman or Insomnia

1. Import the OpenAPI spec from: http://localhost:8000/openapi.json
2. Create a new environment with variable `base_url` = `http://localhost:8000`
3. Test all endpoints visually

## Step 12: Test Signal Parser

Create a test script to test the signal parser:

```bash
# Create test file
cat > test_parser.py << 'EOF'
from api.services.signal_parser import SignalParser

# Test different signal formats
signals = [
    """
    BUY RELIANCE
    ENTRY: 2450
    TARGET: 2500
    STOPLOSS: 2420
    QTY: 100
    """,

    """
    #INFY LONG @ 1520
    TGT 1550
    SL 1500
    """,

    """
    STOCK: TCS
    ACTION: BUY
    CMP: 3420
    TARGET 1: 3480
    STOP LOSS: 3380
    QUANTITY: 50
    """,

    """
    SELL TATAMOTORS @ 850
    Target: 820
    SL: 870
    """
]

for i, signal in enumerate(signals, 1):
    print(f"\n{'='*60}")
    print(f"Test Signal {i}:")
    print(f"{'='*60}")
    print(signal.strip())
    print(f"\nParsed Result:")
    print("-" * 60)

    result = SignalParser.parse(signal)

    print(f"Symbol: {result['symbol']}")
    print(f"Order Type: {result['order_type']}")
    print(f"Action: {result['action']}")
    print(f"Entry Price: {result['entry_price']}")
    print(f"Target Price: {result['target_price']}")
    print(f"Stoploss Price: {result['stoploss_price']}")
    print(f"Quantity: {result['quantity']}")
    print(f"Status: {result['status']}")

    if result['error_message']:
        print(f"Error: {result['error_message']}")

print(f"\n{'='*60}\n")
EOF

# Run the test
python test_parser.py
```

You should see parsed results for each signal format!

## Step 13: Check Database

Verify that data is being stored correctly:

```bash
# Connect to database
psql -U trade_user -d auto_trade_sync -h localhost

# View users
SELECT * FROM users;

# View telegram channels
SELECT * FROM telegram_channels;

# View brokers
SELECT * FROM brokers;

# View channel-broker mappings
SELECT * FROM channel_broker_mappings;

# Exit
\q
```

## Step 14: Check Logs

```bash
# View application logs
tail -f logs/auto_trade_sync.log

# Or view all logs
cat logs/auto_trade_sync.log
```

## Troubleshooting

### Issue: Database connection failed

**Error:** `could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start it if not running
sudo systemctl start postgresql

# Verify connection
psql -U trade_user -d auto_trade_sync -h localhost
```

### Issue: Module not found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port already in use

**Error:** `Address already in use: 8000`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or run on different port
uvicorn main:app --port 8001
```

### Issue: Telegram API errors

**Error:** `Telegram API credentials not configured`

**Solution:**
- Verify TELEGRAM_API_ID and TELEGRAM_API_HASH in `.env`
- Make sure they are integers/strings without quotes for ID
- Restart the application after changing .env

### Issue: Permission denied for database

**Error:** `permission denied for database`

**Solution:**
```bash
# Grant permissions again
sudo -u postgres psql

GRANT ALL PRIVILEGES ON DATABASE auto_trade_sync TO trade_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trade_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trade_user;
\q
```

## Next Steps

### 1. Integrate Real Telegram Channels

To actually monitor Telegram channels, you need to:

1. Join the trading signal channels you want to monitor
2. Add them via the API (they'll need actual channel IDs)
3. The app will automatically start monitoring once configured

### 2. Add Real Broker Credentials

Get actual API credentials from:
- **Angel One**: https://smartapi.angelbroking.com/
- **Zerodha**: https://kite.trade/
- **Dhan**: https://dhanhq.co/
- **Upstox**: https://upstox.com/developer/

Add them through the API endpoints.

### 3. Implement Broker API Calls

The broker integrations have placeholder code. You'll need to:
- Install broker SDKs (uncomment in requirements.txt)
- Implement actual API calls in `api/services/broker_service.py`

### 4. Test Signal Flow

1. Send a test message to a Telegram channel you control
2. Watch the app parse it
3. See it get routed to configured brokers
4. Check execution status

## Running in Production

When ready for production:

1. **Update `.env`:**
   ```env
   DEBUG=false
   SECRET_KEY="<strong-random-key>"
   LOG_LEVEL="WARNING"
   ```

2. **Use process manager:**
   ```bash
   # Install gunicorn
   pip install gunicorn

   # Run with workers
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Set up NGINX** as reverse proxy

4. **Use systemd** for auto-start (see README.md)

5. **Enable SSL/HTTPS**

## Useful Commands

```bash
# Start app
python main.py

# Start with auto-reload (development)
uvicorn main:app --reload

# Run on different port
uvicorn main:app --port 8001

# View logs in real-time
tail -f logs/auto_trade_sync.log

# Check database
psql -U trade_user -d auto_trade_sync -h localhost

# Run tests (when you write them)
pytest

# Format code
black .

# Check types
mypy .
```

## API Quick Reference

- **Health**: `GET /health`
- **Docs**: `GET /docs`
- **Register**: `POST /api/v1/auth/register`
- **Login**: `POST /api/v1/auth/login`
- **Channels**: `GET/POST/PUT/DELETE /api/v1/channels/`
- **Brokers**: `GET/POST/PUT/DELETE /api/v1/brokers/`
- **Signals**: `GET /api/v1/signals/`
- **Stats**: `GET /api/v1/signals/stats/summary`

## Success Checklist

- [ ] PostgreSQL installed and running
- [ ] Database created with correct permissions
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] .env file configured correctly
- [ ] App starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Can register a user
- [ ] Can login and get token
- [ ] Can create channels and brokers
- [ ] Signal parser works correctly
- [ ] Database stores data correctly

Once all checkboxes are complete, your app is ready for testing!

## Getting Help

If you encounter issues:
1. Check the logs: `tail -f logs/auto_trade_sync.log`
2. Check this troubleshooting section
3. Verify all prerequisites are installed
4. Ensure .env is configured correctly
5. Check if all services (PostgreSQL) are running

Happy Trading! 🚀📈
