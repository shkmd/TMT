#!/bin/bash
# Quick Setup Script for Auto Trade Sync App

set -e  # Exit on error

echo "============================================"
echo "Auto Trade Sync App - Quick Setup"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if PostgreSQL is installed
echo -e "\n${YELLOW}Checking PostgreSQL...${NC}"
if command -v psql &> /dev/null; then
    POSTGRES_VERSION=$(psql --version | awk '{print $3}')
    echo -e "${GREEN}PostgreSQL is installed: $POSTGRES_VERSION${NC}"
else
    echo -e "${RED}PostgreSQL is not installed!${NC}"
    echo "Please install PostgreSQL first:"
    echo "  Ubuntu/Debian: sudo apt install postgresql"
    echo "  macOS: brew install postgresql"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}Dependencies installed successfully${NC}"

# Create logs directory
echo -e "\n${YELLOW}Creating logs directory...${NC}"
mkdir -p logs
echo -e "${GREEN}Logs directory created${NC}"

# Setup .env file
echo -e "\n${YELLOW}Setting up environment file...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env

    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

    # Update .env with generated secret
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-super-secret-key-change-this-immediately/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-super-secret-key-change-this-immediately/$SECRET_KEY/" .env
    fi

    echo -e "${GREEN}.env file created with generated SECRET_KEY${NC}"
    echo -e "${YELLOW}⚠️  Please update these values in .env:${NC}"
    echo "  - DATABASE_URL (PostgreSQL connection string)"
    echo "  - TELEGRAM_API_ID (from https://my.telegram.org/apps)"
    echo "  - TELEGRAM_API_HASH (from https://my.telegram.org/apps)"
else
    echo ".env file already exists"
fi

# Database setup instructions
echo -e "\n${YELLOW}============================================${NC}"
echo -e "${YELLOW}Database Setup Instructions:${NC}"
echo -e "${YELLOW}============================================${NC}"
echo ""
echo "Run these commands to set up the database:"
echo ""
echo -e "${GREEN}sudo -u postgres psql${NC}"
echo "Then in PostgreSQL shell:"
echo -e "${GREEN}CREATE DATABASE auto_trade_sync;${NC}"
echo -e "${GREEN}CREATE USER trade_user WITH PASSWORD 'trade_password_123';${NC}"
echo -e "${GREEN}GRANT ALL PRIVILEGES ON DATABASE auto_trade_sync TO trade_user;${NC}"
echo -e "${GREEN}\\q${NC}"
echo ""
echo "Update DATABASE_URL in .env:"
echo -e "${GREEN}DATABASE_URL=\"postgresql://trade_user:trade_password_123@localhost:5432/auto_trade_sync\"${NC}"
echo ""

# Next steps
echo -e "\n${YELLOW}============================================${NC}"
echo -e "${YELLOW}Setup Complete! Next Steps:${NC}"
echo -e "${YELLOW}============================================${NC}"
echo ""
echo "1. Set up PostgreSQL database (see instructions above)"
echo "2. Update .env file with your configuration"
echo "3. Get Telegram API credentials from: https://my.telegram.org/apps"
echo "4. Run the application:"
echo -e "   ${GREEN}source venv/bin/activate${NC}"
echo -e "   ${GREEN}python main.py${NC}"
echo ""
echo "5. Open your browser to: http://localhost:8000/docs"
echo ""
echo -e "${GREEN}For detailed instructions, see: SETUP_GUIDE.md${NC}"
echo ""
