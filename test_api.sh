#!/bin/bash
# API Testing Script for Auto Trade Sync App

BASE_URL="http://localhost:8000"
API_URL="$BASE_URL/api/v1"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "============================================"
echo "Auto Trade Sync App - API Test Script"
echo "============================================"
echo ""
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Health Check
echo -e "${BLUE}Test 1: Health Check${NC}"
echo "GET $BASE_URL/health"
curl -s $BASE_URL/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Root Endpoint
echo -e "${BLUE}Test 2: Root Endpoint${NC}"
echo "GET $BASE_URL/"
curl -s $BASE_URL/ | python3 -m json.tool
echo ""
echo ""

# Test 3: Register User
echo -e "${BLUE}Test 3: Register User${NC}"
echo "POST $API_URL/auth/register"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }')

echo "$REGISTER_RESPONSE" | python3 -m json.tool

# Check if registration was successful or user already exists
if echo "$REGISTER_RESPONSE" | grep -q "already registered"; then
    echo -e "${YELLOW}Note: User already exists, continuing with login...${NC}"
fi
echo ""
echo ""

# Test 4: Login
echo -e "${BLUE}Test 4: Login and Get Token${NC}"
echo "POST $API_URL/auth/login"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=SecurePass123!")

echo "$LOGIN_RESPONSE" | python3 -m json.tool

# Extract token
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Failed to get token! Please check if the app is running.${NC}"
    exit 1
fi

echo -e "${GREEN}Token obtained successfully!${NC}"
echo ""
echo ""

# Test 5: Get Current User
echo -e "${BLUE}Test 5: Get Current User Info${NC}"
echo "GET $API_URL/auth/me"
curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 6: Add Telegram Channel
echo -e "${BLUE}Test 6: Add Telegram Channel${NC}"
echo "POST $API_URL/channels/"
CHANNEL_RESPONSE=$(curl -s -X POST "$API_URL/channels/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "@test_trading_signals",
    "channel_id": "1234567890",
    "description": "Test trading channel for demo",
    "is_active": true
  }')

echo "$CHANNEL_RESPONSE" | python3 -m json.tool

# Extract channel ID
CHANNEL_ID=$(echo "$CHANNEL_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo ""
echo ""

# Test 7: List Channels
echo -e "${BLUE}Test 7: List All Telegram Channels${NC}"
echo "GET $API_URL/channels/"
curl -s -X GET "$API_URL/channels/" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 8: Add Broker
echo -e "${BLUE}Test 8: Add Broker (Angel One)${NC}"
echo "POST $API_URL/brokers/"
BROKER_RESPONSE=$(curl -s -X POST "$API_URL/brokers/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "broker_type": "angel_one",
    "broker_name": "My Angel One Demo Account",
    "api_key": "demo_api_key_12345",
    "client_id": "demo_client_id",
    "is_active": true
  }')

echo "$BROKER_RESPONSE" | python3 -m json.tool

# Extract broker ID
BROKER_ID=$(echo "$BROKER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo ""
echo ""

# Test 9: List Brokers
echo -e "${BLUE}Test 9: List All Brokers${NC}"
echo "GET $API_URL/brokers/"
curl -s -X GET "$API_URL/brokers/" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 10: Create Channel-Broker Mapping
if [ -n "$CHANNEL_ID" ] && [ -n "$BROKER_ID" ]; then
    echo -e "${BLUE}Test 10: Create Channel-Broker Mapping${NC}"
    echo "POST $API_URL/brokers/mappings"
    curl -s -X POST "$API_URL/brokers/mappings" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"telegram_channel_id\": $CHANNEL_ID,
        \"broker_id\": $BROKER_ID,
        \"is_active\": true
      }" | python3 -m json.tool
    echo ""
    echo ""
fi

# Test 11: List Mappings
echo -e "${BLUE}Test 11: List Channel-Broker Mappings${NC}"
echo "GET $API_URL/brokers/mappings"
curl -s -X GET "$API_URL/brokers/mappings" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 12: List Signals
echo -e "${BLUE}Test 12: List Signals (may be empty)${NC}"
echo "GET $API_URL/signals/"
curl -s -X GET "$API_URL/signals/" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 13: Get Signal Statistics
echo -e "${BLUE}Test 13: Get Signal Statistics${NC}"
echo "GET $API_URL/signals/stats/summary?days=7"
curl -s -X GET "$API_URL/signals/stats/summary?days=7" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

# Test 14: Get Latest Signals
echo -e "${BLUE}Test 14: Get Latest Signals${NC}"
echo "GET $API_URL/signals/recent/latest?limit=5"
curl -s -X GET "$API_URL/signals/recent/latest?limit=5" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""
echo ""

echo "============================================"
echo -e "${GREEN}All API Tests Completed!${NC}"
echo "============================================"
echo ""
echo "Your access token (save this for manual testing):"
echo -e "${YELLOW}$TOKEN${NC}"
echo ""
echo "To use this token in curl commands:"
echo "export TOKEN=\"$TOKEN\""
echo ""
echo "Then you can run commands like:"
echo "curl -H \"Authorization: Bearer \$TOKEN\" $API_URL/channels/"
echo ""
