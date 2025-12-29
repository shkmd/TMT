# Full Stack Setup Guide - Auto Trade Sync App

Complete guide to run the entire application (Backend + Frontend) locally.

## 📋 Overview

This application consists of:
- **Backend**: Python FastAPI REST API (Port 8000)
- **Frontend**: React + TypeScript SPA (Port 3000)

## 🚀 Quick Start (10 Minutes)

### Prerequisites

✅ Python 3.9+
✅ Node.js 16+
✅ PostgreSQL 12+
✅ Git

---

## Part 1: Backend Setup (5 minutes)

### 1. Set Up PostgreSQL

```bash
# Start PostgreSQL (if not running)
sudo systemctl start postgresql

# Create database
sudo -u postgres psql
```

In PostgreSQL:
```sql
CREATE DATABASE auto_trade_sync;
CREATE USER trade_user WITH PASSWORD 'trade_password_123';
GRANT ALL PRIVILEGES ON DATABASE auto_trade_sync TO trade_user;
\q
```

### 2. Configure Backend

```bash
# Navigate to project root
cd /home/user/TMT

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Update these values in `.env`:
```env
DATABASE_URL="postgresql://trade_user:trade_password_123@localhost:5432/auto_trade_sync"
SECRET_KEY="your-super-secret-key-$(openssl rand -hex 32)"
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH="your_api_hash"
```

### 3. Install Backend Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Backend Server

```bash
# Make sure venv is activated
source venv/bin/activate

# Run the application
python main.py
```

Expected output:
```
Starting Auto Trade Sync App v1.0.0
Database tables created successfully
Application started on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is running on **http://localhost:8000**

Test it:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","app":"Auto Trade Sync App","version":"1.0.0"}
```

---

## Part 2: Frontend Setup (5 minutes)

### 1. Navigate to Frontend

**Open a NEW terminal** (keep backend running in first terminal):

```bash
cd /home/user/TMT/frontend
```

### 2. Install Frontend Dependencies

```bash
npm install
```

This will install ~200MB of node_modules (takes 2-3 minutes).

### 3. Configure Frontend

```bash
# Copy environment template
cp .env.example .env
```

Default `.env` is already configured for local development:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1
```

### 4. Start Frontend Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

✅ Frontend is running on **http://localhost:3000**

---

## 🎉 Test the Application

### 1. Open in Browser

Go to: **http://localhost:3000**

You should see the login page!

### 2. Create an Account

1. Click "Sign up"
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123!`
3. Click "Sign Up"

You'll be automatically logged in and redirected to the dashboard!

### 3. Explore the Dashboard

Navigate through:
- **Dashboard**: Overview and statistics
- **Channels**: Add Telegram channels
- **Brokers**: Add broker accounts
- **Signals**: View trading signals
- **Mappings**: Route channels to brokers

---

## 📊 Project Structure

```
TMT/
├── backend/
│   ├── api/                   # Backend API code
│   ├── config/                # Configuration
│   ├── main.py                # Backend entry point
│   └── requirements.txt       # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── api/               # API services
    │   ├── components/        # React components
    │   ├── pages/             # Page components
    │   ├── store/             # State management
    │   └── App.tsx            # Frontend entry point
    ├── package.json           # Node dependencies
    └── README.md              # Frontend docs
```

---

## 🔄 Daily Development Workflow

### Starting the Application

**Terminal 1 (Backend)**:
```bash
cd /home/user/TMT
source venv/bin/activate
python main.py
```

**Terminal 2 (Frontend)**:
```bash
cd /home/user/TMT/frontend
npm run dev
```

### Stopping the Application

Press `Ctrl+C` in each terminal.

---

## 🛠️ Common Tasks

### Add a Telegram Channel

1. Go to **Channels** page
2. Click "Add Channel"
3. Enter `@your_channel_name`
4. Click "Add Channel"

### Add a Broker

1. Go to **Brokers** page
2. Click "Add Broker"
3. Select broker type (Angel One, Zerodha, etc.)
4. Enter credentials
5. Click "Add Broker"

### Create a Mapping

1. Go to **Mappings** page
2. Click "Add Mapping"
3. Select channel and broker
4. Click "Create Mapping"

Signals from that channel will now route to that broker!

### View Signals

Go to **Signals** page to see all received signals.

---

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `Database connection failed`

**Solution**:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# If not, start it
sudo systemctl start postgresql

# Test connection
psql -U trade_user -d auto_trade_sync -h localhost
```

---

**Issue**: `Port 8000 already in use`

**Solution**:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

---

**Issue**: `Module not found`

**Solution**:
```bash
# Activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Frontend Issues

**Issue**: `Cannot connect to API`

**Solution**:
```bash
# Check backend is running
curl http://localhost:8000/health

# Check .env file
cat frontend/.env

# Restart frontend
cd frontend
npm run dev
```

---

**Issue**: `Port 3000 already in use`

**Solution**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or run on different port
npm run dev -- --port 3001
```

---

**Issue**: `npm install fails`

**Solution**:
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force

# Reinstall
npm install
```

---

## 📚 API Documentation

While the app is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Interactive API documentation with "Try it out" functionality.

---

## 🧪 Testing

### Test Backend

```bash
# In backend directory
source venv/bin/activate
./test_api.sh
```

### Test Frontend

```bash
# In frontend directory
npm run build
```

If build succeeds, frontend is working correctly!

---

## 🎯 Next Steps

### 1. Get Telegram API Credentials

1. Visit: https://my.telegram.org/apps
2. Login with your phone
3. Create an application
4. Copy API ID and API Hash
5. Add to backend `.env`

### 2. Add Real Telegram Channels

1. Join trading signal channels on Telegram
2. Add them in the "Channels" page
3. Signals will be automatically monitored

### 3. Add Broker Credentials

Get API credentials from:
- **Angel One**: https://smartapi.angelbroking.com/
- **Zerodha**: https://kite.trade/
- **Dhan**: https://dhanhq.co/
- **Upstox**: https://upstox.com/developer/

Add them in the "Brokers" page.

### 4. Create Mappings

Map your channels to brokers to start automated trading!

---

## 📦 Production Deployment

### Backend Deployment

```bash
# Build
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or use Docker
docker build -t auto-trade-sync-backend .
docker run -p 8000:8000 auto-trade-sync-backend
```

### Frontend Deployment

```bash
cd frontend

# Build
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - S3 + CloudFront
# - Any static hosting
```

---

## 🔐 Security Checklist

Before production:
- [ ] Change SECRET_KEY in backend .env
- [ ] Use strong PostgreSQL password
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Encrypt broker credentials
- [ ] Enable firewall
- [ ] Regular backups

---

## 📊 Monitoring

### Check Backend Health

```bash
curl http://localhost:8000/health
```

### Check Frontend

Browser: http://localhost:3000

### View Logs

**Backend**:
```bash
tail -f logs/auto_trade_sync.log
```

**Frontend**:
Check browser console (F12)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs**:
   - Backend: `tail -f logs/auto_trade_sync.log`
   - Frontend: Browser console (F12)

2. **Check processes**:
   ```bash
   # Backend
   curl http://localhost:8000/health

   # Frontend
   curl http://localhost:3000
   ```

3. **Restart everything**:
   ```bash
   # Stop all (Ctrl+C in each terminal)
   # Then start again from scratch
   ```

4. **Check documentation**:
   - Backend: `README.md`
   - Frontend: `frontend/README.md`
   - Setup: `SETUP_GUIDE.md`

---

## ✅ Success Checklist

- [ ] PostgreSQL running and database created
- [ ] Backend starts without errors (port 8000)
- [ ] Can access http://localhost:8000/docs
- [ ] Health check returns OK
- [ ] Frontend starts without errors (port 3000)
- [ ] Can access http://localhost:3000
- [ ] Can register a new user
- [ ] Can login
- [ ] Can navigate to all pages
- [ ] Dashboard shows statistics
- [ ] Can add channels and brokers

**All checked?** 🎉 You're ready to trade!

---

## 📈 Performance Tips

### Backend

- Use connection pooling (already configured)
- Enable caching for frequently accessed data
- Use background tasks for heavy operations

### Frontend

- Code splitting for large pages
- Image optimization
- Lazy loading components
- Service worker for offline support

---

## 🚀 Advanced Features

### WebSocket for Real-Time Updates

Add WebSocket support for live signal updates without polling.

### Signal Parser Customization

Edit `api/services/signal_parser.py` to add custom parsing patterns.

### Add More Brokers

1. Create broker class in `api/services/broker_service.py`
2. Add to `BrokerType` enum
3. Register in `BrokerFactory`
4. Frontend will automatically support it!

---

## 📝 Summary

**You now have**:
- ✅ Full-stack trading automation platform
- ✅ Modern React dashboard
- ✅ RESTful API backend
- ✅ Multi-broker support
- ✅ Real-time signal monitoring
- ✅ User authentication
- ✅ Complete documentation

**Happy Trading!** 🚀📈

---

## Quick Reference

| Component | URL | Port |
|-----------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |
| PostgreSQL | localhost | 5432 |

| Command | Description |
|---------|-------------|
| `python main.py` | Start backend |
| `npm run dev` | Start frontend |
| `curl http://localhost:8000/health` | Check backend |
| `curl http://localhost:3000` | Check frontend |
