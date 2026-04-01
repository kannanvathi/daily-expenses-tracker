from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from datetime import datetime
import os
import traceback
from fastapi.responses import PlainTextResponse
from bson import json_util

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

# --- Authentication / Authorization (JWT) ---
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(username: str):
    u = db.users.find_one({"username": username})
    if not u:
        return None
    u["_id"] = str(u["_id"])
    return u

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.get("hashed_password", "")):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.users.find_one({"_id": ObjectId(sub)})
    if not user:
        raise credentials_exception
    user["_id"] = str(user["_id"])
    return user


# Routes
@app.post("/users")
def create_user(user: dict):
    # legacy create user route (keeps backward compatibility)
    result = db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return user


@app.post("/auth/register")
async def register(request: Request):
    """Register a new user. Expects JSON with `username` and `password`."""
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    if db.users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="username already registered")
    hashed = get_password_hash(password)
    res = db.users.insert_one({"username": username, "hashed_password": hashed})
    return {"_id": str(res.inserted_id), "username": username}

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


@app.post("/auth/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["_id"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/categories")
def create_category(category: dict):
    result = db.categories.insert_one(category)
    category["_id"] = str(result.inserted_id)
    return category

@app.get("/categories/{user_id}")
def get_categories(user_id: str, current_user: dict = Depends(get_current_user)):
    # Only allow users to fetch their own categories
    if user_id != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    categories = list(db.categories.find({"user_id": user_id}).limit(100))
    for cat in categories:
        cat["_id"] = str(cat["_id"])
    return categories

@app.post("/expenses")
def create_expense(expense: dict, current_user: dict = Depends(get_current_user)):
    # Ensure expense is created for the authenticated user only
    expense_user_id = expense.get("user_id")
    if expense_user_id and expense_user_id != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Cannot create expense for other user")
    expense["user_id"] = current_user["_id"]
    if "date" in expense and isinstance(expense["date"], str):
        expense["date"] = datetime.fromisoformat(expense["date"])
    result = db.expenses.insert_one(expense)
    expense["_id"] = str(result.inserted_id)
    expense["date"] = expense["date"].isoformat() if isinstance(expense["date"], datetime) else expense["date"]
    return expense

@app.get("/expenses/{user_id}")
def get_expenses(user_id: str, category_id: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    if atlas_connect_error:
        raise atlas_connect_error
    # Only allow fetching your own expenses
    if user_id != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
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
def update_expense(expense_id: str, expense: dict, current_user: dict = Depends(get_current_user)):
    try:
        exp_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense_id")
    if "date" in expense and isinstance(expense["date"], str):
        expense["date"] = datetime.fromisoformat(expense["date"])
    # Verify ownership
    existing = db.expenses.find_one({"_id": exp_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")
    if str(existing.get("user_id")) != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Cannot modify another user's expense")
    result = db.expenses.update_one({"_id": exp_id}, {"$set": expense})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense["_id"] = expense_id
    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, current_user: dict = Depends(get_current_user)):
    try:
        exp_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense_id")
    existing = db.expenses.find_one({"_id": exp_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")
    if str(existing.get("user_id")) != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Cannot delete another user's expense")
    result = db.expenses.delete_one({"_id": exp_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}


# debug db dump endpoint removed


@app.get("/settings/{user_id}")
def get_settings(user_id: str, current_user: dict = Depends(get_current_user)):
    if user_id != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    settings = db.settings.find_one({"user_id": user_id}) or {}
    settings["_id"] = str(settings.get("_id")) if settings.get("_id") else None
    return settings


@app.post("/settings/{user_id}")
def save_settings(user_id: str, settings: dict, current_user: dict = Depends(get_current_user)):
    if user_id != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    settings["user_id"] = user_id
    db.settings.update_one({"user_id": user_id}, {"$set": settings}, upsert=True)
    res = db.settings.find_one({"user_id": user_id})
    res["_id"] = str(res["_id"])
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)