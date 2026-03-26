#!/bin/bash

# Daily Expenses Tracker - Quick Start Script
# This script sets up and runs both frontend and backend

set -e

echo "=================================================="
echo "Daily Expenses Tracker - Quick Start"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo -e "${YELLOW}Error: Please run this script from the daily-expenses-tracker root directory${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up Backend${NC}"
echo "================================"

if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    cd ..
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
    cd backend
    source venv/bin/activate
    cd ..
fi

echo ""
echo -e "${BLUE}Step 2: Setting up Frontend${NC}"
echo "================================"

if [ ! -d "frontend/node_modules" ]; then
    echo "Installing npm dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo -e "${GREEN}✓ Node modules already exist${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Starting Services${NC}"
echo "================================"
echo ""
echo -e "${YELLOW}IMPORTANT: You'll need two terminal windows/tabs${NC}"
echo ""

echo -e "${GREEN}Backend Setup:${NC}"
echo "1. Open a new terminal/tab"
echo "2. Navigate to the backend directory: cd backend"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Start the server: uvicorn main:app --reload"
echo "   Backend will run at: http://localhost:8000"
echo "   API docs at: http://localhost:8000/docs"
echo ""

echo -e "${GREEN}Frontend Setup:${NC}"
echo "1. Open another terminal/tab"
echo "2. Navigate to the frontend directory: cd frontend"
echo "3. Start the dev server: npm run dev"
echo "   Frontend will run at: http://localhost:5173"
echo ""

echo -e "${YELLOW}Database Setup:${NC}"
echo "Make sure MongoDB is running (Atlas or local):"
echo "- Atlas: Connection string in backend/main.py"
echo "- Local: brew services start mongodb-community (macOS)"
echo "         sudo systemctl start mongodb (Linux)"
echo ""

echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Quick Links:${NC}"
echo "- Application: http://localhost:5173"
echo "- API Docs: http://localhost:8000/docs"
echo "- Design System: See DESIGN_SYSTEM.md"
echo "- README: See README.md"
echo ""
echo "=================================================="
