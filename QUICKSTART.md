# Quick Start Guide - 5 Minutes to Running App

Follow these steps to get the Auto Trade Sync App running in under 5 minutes!

## Prerequisites Check

```bash
# Check if you have everything
python3 --version    # Should be 3.9+
psql --version       # Should be PostgreSQL 12+
```

Don't have these? See [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation instructions.

## Step 1: Run Automated Setup (2 minutes)

```bash
cd /home/user/TMT
./quick_setup.sh
```

This script will:
- Create virtual environment
- Install all dependencies
- Generate secure SECRET_KEY
- Create `.env` file
- Set up logs directory

## Step 2: Set Up Database (1 minute)

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Run these commands in PostgreSQL:
CREATE DATABASE auto_trade_sync;
CREATE USER trade_user WITH PASSWORD 'trade_password_123';
GRANT ALL PRIVILEGES ON DATABASE auto_trade_sync TO trade_user;
\q
```

## Step 3: Configure Environment (1 minute)

Edit `.env` file:

```bash
nano .env
# or: vim .env
# or: code .env
```

**Update these 3 essential settings:**

```env
# 1. Database (use the credentials from Step 2)
DATABASE_URL="postgresql://trade_user:trade_password_123@localhost:5432/auto_trade_sync"

# 2. Telegram API (get from https://my.telegram.org/apps)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH="your_api_hash_here"

# 3. SECRET_KEY is already generated, keep it as is
```

**Getting Telegram Credentials (30 seconds):**
1. Go to https://my.telegram.org/auth
2. Login with your phone
3. Click "API Development Tools"
4. Create app (any name works)
5. Copy `api_id` and `api_hash`

## Step 4: Start the Application (30 seconds)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python main.py
```

You should see:
```
Starting Auto Trade Sync App v1.0.0
Database tables created successfully
Application started on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**🎉 Your app is now running!**

## Step 5: Test the Application (30 seconds)

### Option A: Web Browser (Easiest)

Open: http://localhost:8000/docs

You'll see interactive API documentation where you can test all endpoints!

### Option B: Automated Test Script

Open a **new terminal** (keep the app running):

```bash
cd /home/user/TMT
source venv/bin/activate
./test_api.sh
```

This will:
- Test all API endpoints
- Create a test user
- Add sample channels and brokers
- Show you how everything works

### Option C: Test Signal Parser

```bash
cd /home/user/TMT
source venv/bin/activate
python test_signal_parser.py
```

This demonstrates how signals are parsed.

## What's Next?

### 1. Explore the API (Interactive)

Go to http://localhost:8000/docs and try:

1. **Register** a user (POST `/api/v1/auth/register`)
2. **Login** to get your token (POST `/api/v1/auth/login`)
3. Click "Authorize" button (top right)
4. Paste your token
5. Now test any endpoint!

### 2. Add Your First Channel

```bash
# Use the token from login
export TOKEN="your_token_here"

# Add a Telegram channel
curl -X POST "http://localhost:8000/api/v1/channels/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "@your_signal_channel",
    "description": "My trading signals",
    "is_active": true
  }'
```

### 3. Add Your First Broker

```bash
curl -X POST "http://localhost:8000/api/v1/brokers/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "broker_type": "angel_one",
    "broker_name": "My Angel One Account",
    "api_key": "your_api_key",
    "client_id": "your_client_id",
    "is_active": true
  }'
```

### 4. Connect Channel to Broker

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

Now signals from your channel will automatically route to your broker!

## Troubleshooting

### App won't start?

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# If not running:
sudo systemctl start postgresql
```

### Can't connect to database?

```bash
# Test connection
psql -U trade_user -d auto_trade_sync -h localhost

# If it fails, recreate the database (Step 2)
```

### Module not found errors?

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port 8000 already in use?

```bash
# Find what's using it
lsof -i :8000

# Kill it
kill -9 <PID>

# Or run on different port
uvicorn main:app --port 8001
```

## Useful Commands

```bash
# Start app
python main.py

# Start with auto-reload (development)
uvicorn main:app --reload

# View logs
tail -f logs/auto_trade_sync.log

# Check database
psql -U trade_user -d auto_trade_sync -h localhost

# Test API
./test_api.sh

# Test parser
python test_signal_parser.py
```

## File Overview

- `main.py` - Application entry point
- `quick_setup.sh` - Automated setup script
- `test_api.sh` - API testing script
- `test_signal_parser.py` - Signal parser demo
- `SETUP_GUIDE.md` - Detailed setup instructions
- `README.md` - Full documentation
- `.env` - Configuration (don't commit this!)
- `requirements.txt` - Python dependencies

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |
| `/api/v1/auth/register` | POST | Register user |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/channels/` | GET/POST | Manage channels |
| `/api/v1/brokers/` | GET/POST | Manage brokers |
| `/api/v1/brokers/mappings` | GET/POST | Manage mappings |
| `/api/v1/signals/` | GET | View signals |
| `/api/v1/signals/stats/summary` | GET | Signal statistics |

## Success Checklist

- [x] PostgreSQL installed and running
- [x] Virtual environment created
- [x] Dependencies installed
- [x] Database created
- [x] `.env` configured
- [x] App starts successfully
- [x] Can access http://localhost:8000/docs
- [x] API tests pass

## Next Steps

1. ✅ **You've completed the quick start!**

2. **For production use:**
   - See [SETUP_GUIDE.md](SETUP_GUIDE.md) for deployment
   - Get real broker API credentials
   - Configure actual Telegram channels
   - Implement broker API calls

3. **For development:**
   - Read [README.md](README.md) for architecture
   - Explore `api/` directory
   - Customize signal parser
   - Add new brokers

## Getting Help

- **Detailed Setup**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Full Documentation**: See [README.md](README.md)
- **Logs**: Check `logs/auto_trade_sync.log`
- **Database**: Connect with `psql -U trade_user -d auto_trade_sync -h localhost`

## Video Walkthrough (Simulated)

**Terminal 1 (Setup & Run):**
```bash
./quick_setup.sh           # Setup
# Configure .env
source venv/bin/activate   # Activate
python main.py             # Run
```

**Terminal 2 (Test):**
```bash
source venv/bin/activate   # Activate
./test_api.sh              # Test everything
```

**Browser:**
```
http://localhost:8000/docs # Interactive API
```

That's it! You're ready to trade! 🚀

---

**Need more detail?** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
**Want full docs?** → [README.md](README.md)
