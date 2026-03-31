from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
import os
import traceback
from fastapi.responses import PlainTextResponse

app = FastAPI()

# When set to true, return full Python tracebacks in HTTP 500 responses.
DEBUG_TRACEBACK = os.getenv("DEBUG_TRACEBACK", "false").lower() in ("1", "true", "yes")


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print("Unhandled exception:", exc)
    print(tb)
    # Allow on-demand tracebacks via env var, query param, or request header.
    want_trace = DEBUG_TRACEBACK or request.query_params.get("debug") == "1" or request.headers.get("x-debug-trace", "").lower() in ("1", "true", "yes")
    if want_trace:
        return PlainTextResponse(tb, status_code=500)
    return PlainTextResponse("Internal Server Error", status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection helper: accept either MONGODB_URL or MONGO_URI environment variable
DEFAULT_URI = os.getenv("MONGODB_URL") or os.getenv("MONGO_URI") or "mongodb+srv://kannanvathi:Athira123@cluster1.qobvrwa.mongodb.net/expenses_db?retryWrites=true&w=majority"

client = MongoClient(DEFAULT_URI, serverSelectionTimeoutMS=5000)
atlas_connect_error = None
try:
    client.server_info()  # trigger connect
    print("Connected to Atlas MongoDB")
except Exception as e:
    atlas_connect_error = e
    print("Atlas connection failed (stored error). Falling back to local MongoDB:", e)
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)

db = client.expenses_db

# Routes
@app.post("/users")
def create_user(user: dict):
    result = db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        uid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user = db.users.find_one({"_id": uid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

@app.post("/categories")
def create_category(category: dict):
    result = db.categories.insert_one(category)
    category["_id"] = str(result.inserted_id)
    return category

@app.get("/categories/{user_id}")
def get_categories(user_id: str):
    categories = list(db.categories.find({"user_id": user_id}).limit(100))
    for cat in categories:
        cat["_id"] = str(cat["_id"])
    return categories

@app.post("/expenses")
def create_expense(expense: dict):
    if "date" in expense and isinstance(expense["date"], str):
        expense["date"] = datetime.fromisoformat(expense["date"])
    result = db.expenses.insert_one(expense)
    expense["_id"] = str(result.inserted_id)
    expense["date"] = expense["date"].isoformat() if isinstance(expense["date"], datetime) else expense["date"]
    return expense

@app.get("/expenses/{user_id}")
def get_expenses(user_id: str, category_id: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None):
    if atlas_connect_error:
        raise atlas_connect_error
    query = {"user_id": user_id}
    if category_id:
        query["category_id"] = category_id
    date_query = {}
    if date_from:
        date_query["$gte"] = datetime.fromisoformat(date_from)
    if date_to:
        date_query["$lte"] = datetime.fromisoformat(date_to)
    if date_query:
        query["date"] = date_query
    expenses = list(db.expenses.find(query).limit(1000))
    for exp in expenses:
        exp["_id"] = str(exp["_id"])
        if isinstance(exp.get("date"), datetime):
            exp["date"] = exp["date"].isoformat()
    return expenses

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: str, expense: dict):
    try:
        exp_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense_id")
    if "date" in expense and isinstance(expense["date"], str):
        expense["date"] = datetime.fromisoformat(expense["date"])
    result = db.expenses.update_one({"_id": exp_id}, {"$set": expense})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense["_id"] = expense_id
    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    try:
        exp_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense_id")
    result = db.expenses.delete_one({"_id": exp_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)