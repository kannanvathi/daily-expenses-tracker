# Daily Expenses Tracker

A web application for tracking daily expenses with Vue 3 frontend and Python FastAPI backend using MongoDB.

## Features

- Dashboard with quick add, monthly summary, recent activity, and mini chart
- Add expenses modal with category, date, description, and payment method
- Transactions history with filters and search
- Budgets and reports with pie charts and trends
- Settings for user preferences and category management

## Tech Stack

- **Frontend**: Vue 3, Vue Router, Pinia, Axios, Chart.js
- **Backend**: Python, FastAPI, Motor (MongoDB async driver)
- **Database**: MongoDB

## Setup

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ (for backend)
- MongoDB

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Database

Ensure MongoDB is running on localhost:27017 or set MONGODB_URL environment variable.

## API Endpoints

- POST /users - Create user
- GET /users/{user_id} - Get user
- POST /categories - Create category
- GET /categories/{user_id} - Get user categories
- POST /expenses - Create expense
- GET /expenses/{user_id} - Get user expenses (with optional filters)
- PUT /expenses/{expense_id} - Update expense
- DELETE /expenses/{expense_id} - Delete expense

## MongoDB Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "password_hash": "string",
  "default_currency": "string"
}
```

### Categories Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "name": "string",
  "icon": "string"
}
```

### Expenses Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "category_id": "ObjectId",
  "amount": "number",
  "date": "date",
  "description": "string",
  "payment_method": "string"
}
```