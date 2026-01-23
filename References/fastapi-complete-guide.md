# FastAPI Complete Guide

## Table of Contents
1. [Introduction to FastAPI](#introduction-to-fastapi)
2. [Installation & Setup](#installation--setup)
3. [Basic Concepts](#basic-concepts)
4. [Path Operations](#path-operations)
5. [Pydantic Models](#pydantic-models)
6. [Request Parameters](#request-parameters)
7. [Request Body](#request-body)
8. [Response Models](#response-models)
9. [Form Data & File Uploads](#form-data--file-uploads)
10. [Dependencies](#dependencies)
11. [Authentication & Security](#authentication--security)
12. [Database Integration](#database-integration)
13. [CRUD Operations](#crud-operations)
14. [Async/Await](#asyncawait)
15. [Background Tasks](#background-tasks)
16. [Middleware](#middleware)
17. [CORS](#cors)
18. [Error Handling](#error-handling)
19. [Testing](#testing)
20. [WebSockets](#websockets)
21. [Deployment](#deployment)
22. [Best Practices](#best-practices)
23. [Interview Questions (3 YOE)](#interview-questions-3-years-experience)

---

## Introduction to FastAPI

### What is FastAPI?
- **Modern, fast (high-performance)** Python web framework
- Built on **Starlette** (web) and **Pydantic** (data validation)
- **Automatic API documentation** (Swagger UI, ReDoc)
- **Type hints** everywhere for better IDE support
- **Async support** out of the box
- Created by Sebastián Ramírez in 2018

### Key Features
- **Fast Performance** - One of the fastest Python frameworks (comparable to NodeJS and Go)
- **Fast to Code** - 2-3x faster development speed
- **Fewer Bugs** - Reduces human errors by ~40%
- **Intuitive** - Great editor support with autocomplete
- **Easy** - Designed to be easy to learn and use
- **Short** - Minimize code duplication
- **Robust** - Production-ready code with automatic interactive documentation
- **Standards-based** - Based on OpenAPI and JSON Schema
- **Type Safety** - Full type hints support
- **Async Native** - Built-in async/await support

### Why Use FastAPI?
- **Performance:** As fast as NodeJS and Go
- **Developer Experience:** Excellent autocomplete and type checking
- **Automatic Docs:** Interactive API documentation (Swagger/ReDoc)
- **Data Validation:** Automatic request/response validation with Pydantic
- **Modern Python:** Uses latest Python features (3.7+)
- **Production Ready:** Used by Microsoft, Uber, Netflix, etc.
- **Easy Testing:** Built-in test client
- **Standards Compliance:** Full OpenAPI and JSON Schema support

### FastAPI vs Flask vs Django
| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Performance | Very High | Medium | Medium |
| Async Support | Native | Via extensions | Limited (3.1+) |
| Type Hints | Required | Optional | Optional |
| Data Validation | Automatic (Pydantic) | Manual | Django Forms |
| API Docs | Automatic | Manual (Swagger) | DRF (manual) |
| Learning Curve | Low-Medium | Low | High |
| Batteries Included | No (microframework) | No | Yes |
| Best For | APIs, Microservices | Small apps, APIs | Full-stack web apps |

---

## Installation & Setup

### Prerequisites
```bash
# Python 3.7+ required
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

### Install FastAPI
```bash
# Install FastAPI and Uvicorn (ASGI server)
pip install fastapi uvicorn[standard]

# Install additional dependencies (recommended)
pip install python-multipart      # For form data and file uploads
pip install python-jose[cryptography]  # For JWT tokens
pip install passlib[bcrypt]       # For password hashing
pip install sqlalchemy            # For database ORM
pip install alembic               # For database migrations
pip install aiofiles              # For async file operations
pip install pytest                # For testing
pip install httpx                 # For testing async endpoints
pip install pydantic[email]       # For email validation
```

### First FastAPI Application
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Run the Application
```bash
# Development server with auto-reload
uvicorn main:app --reload

# Specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production mode (no reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access Interactive Docs
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

### Project Structure
```
fastapi-project/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── dependencies.py      # Shared dependencies
│   │
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── posts.py
│   │   │   │   └── auth.py
│   │   │   └── api.py       # API router
│   │
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Security utilities
│   │   └── database.py      # Database connection
│   │
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── crud/                # CRUD operations
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   └── tests/               # Tests
│       ├── __init__.py
│       ├── test_users.py
│       └── test_posts.py
│
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
│
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## Basic Concepts

### Path Operations
```python
from fastapi import FastAPI

app = FastAPI()

# GET request
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# POST request
@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

# PUT request
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

# DELETE request
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}

# PATCH request
@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, price: float = None):
    return {"item_id": item_id, "price": price}
```

### Type Hints & Validation
```python
from typing import Optional, List
from datetime import datetime

@app.get("/items/{item_id}")
def read_item(
    item_id: int,              # Path parameter (required, must be int)
    q: Optional[str] = None,   # Query parameter (optional)
    limit: int = 10,           # Query parameter with default
    skip: int = 0
):
    return {
        "item_id": item_id,
        "q": q,
        "limit": limit,
        "skip": skip
    }

# FastAPI automatically:
# - Converts types (string "123" to int 123)
# - Validates types (returns 422 if type mismatch)
# - Generates OpenAPI schema
# - Provides interactive docs
```

### Response Types
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

# Default: JSON response
@app.get("/json")
def get_json():
    return {"message": "JSON response"}

# HTML response
@app.get("/html", response_class=HTMLResponse)
def get_html():
    return "<html><body><h1>Hello HTML</h1></body></html>"

# Plain text response
@app.get("/text", response_class=PlainTextResponse)
def get_text():
    return "Plain text response"

# Redirect response
@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/json")

# Custom status code
@app.get("/custom")
def custom_response():
    return JSONResponse(
        content={"message": "Custom response"},
        status_code=201
    )
```

---

## Path Operations

### Path Parameters
```python
from fastapi import FastAPI, Path

app = FastAPI()

# Basic path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}

# Path parameter with validation
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="Item ID", ge=1, le=1000)
):
    return {"item_id": item_id}

# Path with Enum (predefined values)
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "message": "Have some residuals"}

# Path containing forward slash (must be last)
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
# URL: /files/home/user/myfile.txt
```

### Query Parameters
```python
from typing import Optional, List
from fastapi import Query

# Optional query parameter
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
# URL: /items/?skip=0&limit=10

# Required query parameter (no default)
@app.get("/items/")
def read_items(q: str):
    return {"q": q}

# Query parameter with validation
@app.get("/items/")
def read_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9]+$",
        title="Query string",
        description="Search query parameter"
    )
):
    return {"q": q}

# Multiple values for same parameter
@app.get("/items/")
def read_items(q: Optional[List[str]] = Query(None)):
    return {"q": q}
# URL: /items/?q=foo&q=bar

# Required query parameter with validation
@app.get("/items/")
def read_items(q: str = Query(..., min_length=3)):
    return {"q": q}

# Query parameter with alias
@app.get("/items/")
def read_items(item_query: str = Query(..., alias="item-query")):
    return {"item_query": item_query}
# URL: /items/?item-query=test

# Deprecated parameter
@app.get("/items/")
def read_items(
    old_param: Optional[str] = Query(None, deprecated=True),
    new_param: Optional[str] = Query(None)
):
    return {"old_param": old_param, "new_param": new_param}
```

### Headers & Cookies
```python
from fastapi import Header, Cookie

# Request headers
@app.get("/items/")
def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

# Multiple header values
@app.get("/items/")
def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}

# Cookies
@app.get("/items/")
def read_items(session_id: Optional[str] = Cookie(None)):
    return {"session_id": session_id}
```

---

## Pydantic Models

### Basic Models
```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    """User model"""
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime

class Post(BaseModel):
    """Post model"""
    id: int
    title: str
    content: str
    author_id: int
    published: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Sample Post",
                "content": "This is a sample post",
                "author_id": 1,
                "published": False
            }
        }
```

### Field Validation
```python
from pydantic import BaseModel, Field, validator, constr, conint

class UserCreate(BaseModel):
    """User creation schema"""
    username: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    age: conint(ge=18, le=120)
    
    # Or using Field
    # username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$")
    # age: int = Field(..., ge=18, le=120)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """Validate username is alphanumeric"""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123",
                "age": 25
            }
        }
```

### Nested Models
```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class UserProfile(BaseModel):
    username: str
    email: EmailStr
    address: Address
    tags: List[str] = []

# Usage
@app.post("/users/")
def create_user(user: UserProfile):
    return user

# Request body:
# {
#     "username": "johndoe",
#     "email": "john@example.com",
#     "address": {
#         "street": "123 Main St",
#         "city": "New York",
#         "country": "USA",
#         "postal_code": "10001"
#     },
#     "tags": ["python", "fastapi"]
# }
```

### Model Inheritance
```python
class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Schema for creating user"""
    password: str

class UserUpdate(UserBase):
    """Schema for updating user"""
    password: Optional[str] = None

class UserInDB(UserBase):
    """User in database (includes hashed password)"""
    id: int
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    
    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy

class User(UserBase):
    """User response (without sensitive data)"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True
```

---

## Request Parameters

### Combined Parameters
```python
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.put("/items/{item_id}")
def update_item(
    *,  # Force keyword-only arguments
    item_id: int = Path(..., ge=1),
    q: Optional[str] = Query(None, max_length=50),
    item: Item = Body(...),
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

### Multiple Body Parameters
```python
class User(BaseModel):
    username: str
    email: EmailStr

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(...)  # Single value in body
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }

# Request body:
# {
#     "item": {"name": "Foo", "price": 45.2},
#     "user": {"username": "john", "email": "john@example.com"},
#     "importance": 5
# }

# Embed single body parameter
@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item = Body(..., embed=True)
):
    return {"item_id": item_id, "item": item}

# Request body:
# {
#     "item": {"name": "Foo", "price": 45.2}
# }
```

---

## Request Body

### Basic Request Body
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body:
# {
#     "name": "Laptop",
#     "description": "A powerful laptop",
#     "price": 999.99,
#     "tax": 99.99
# }
```

### Request Body with Extra Data
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., example="Laptop")
    description: Optional[str] = Field(None, example="A powerful laptop")
    price: float = Field(..., gt=0, example=999.99)
    tax: Optional[float] = Field(None, ge=0, example=99.99)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": 999.99,
                "tax": 99.99
            }
        }

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### List of Models
```python
@app.post("/items/")
async def create_items(items: List[Item]):
    return items

# Request body:
# [
#     {"name": "Item 1", "price": 10.0},
#     {"name": "Item 2", "price": 20.0}
# ]
```

### Arbitrary Dict
```python
@app.post("/items/")
async def create_item(item: Dict[str, Any]):
    return item

# Accepts any JSON object
```

---

## Response Models

### Basic Response Model
```python
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    # Password is not returned (not in UserOut)
    return user

# Request: {"username": "john", "password": "secret", "email": "john@example.com"}
# Response: {"username": "john", "email": "john@example.com"}
```

### Response Model with Status Code
```python
from fastapi import status

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# Returns 201 Created status code
```

### Multiple Response Models
```python
from typing import Union

class BaseItem(BaseModel):
    name: str
    price: float

class CarItem(BaseItem):
    type: str = "car"
    doors: int

class PlaneItem(BaseItem):
    type: str = "plane"
    seats: int

@app.get("/items/{item_id}", response_model=Union[CarItem, PlaneItem])
async def get_item(item_id: int):
    if item_id == 1:
        return CarItem(name="Tesla", price=50000, doors=4)
    return PlaneItem(name="Boeing 747", price=1000000, seats=400)
```

### Response with Additional Models
```python
from typing import List

@app.get("/items/", response_model=List[Item])
async def get_items():
    return [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0}
    ]

# Response model dict
@app.get("/items/{item_id}", response_model=Dict[str, Any])
async def get_item(item_id: int):
    return {"item_id": item_id, "name": "Item"}
```

### Exclude Fields from Response
```python
class User(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.get("/users/{user_id}", response_model=User, response_model_exclude={"password"})
async def get_user(user_id: int):
    return {
        "username": "john",
        "email": "john@example.com",
        "password": "secret"
    }
# Password is excluded from response

# Or include specific fields
@app.get("/users/{user_id}", response_model=User, response_model_include={"username", "email"})
async def get_user(user_id: int):
    return user
```

### Response with None Values
```python
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item(item_id: int):
    return {"name": "Item", "price": 10.0}
# description is not included in response (not set)

# Other options:
# response_model_exclude_defaults=True  # Exclude fields with default values
# response_model_exclude_none=True      # Exclude fields with None values
```

---

## Form Data & File Uploads

### Form Data
```python
from fastapi import Form

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

# Content-Type: application/x-www-form-urlencoded
```

### File Upload
```python
from fastapi import File, UploadFile
from typing import List

# Single file upload (bytes)
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# Single file upload (UploadFile - recommended)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# Multiple file uploads
@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return [
        {
            "filename": file.filename,
            "content_type": file.content_type
        }
        for file in files
    ]

# File with additional form data
@app.post("/files/")
async def create_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...)
):
    return {
        "filename": file.filename,
        "title": title,
        "description": description
    }
```

### Save Uploaded File
```python
import aiofiles
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {
        "filename": file.filename,
        "location": str(file_path)
    }
```

---

## Dependencies

### Basic Dependency
```python
from fastapi import Depends

def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-based Dependency
```python
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

### Dependency with Database Session
```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Sub-dependencies
```python
def query_extractor(q: Optional[str] = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```

### Global Dependencies
```python
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")

app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# All routes now require these headers
```

---

## Authentication & Security

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### OAuth2 with Password Flow
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuration
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Get current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Login endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### API Key Authentication
```python
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = "your-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.get("/protected")
async def protected_route(api_key: str = Depends(get_api_key)):
    return {"message": "Access granted"}
```

### Role-Based Access Control
```python
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(BaseModel):
    username: str
    role: Role

def require_role(required_role: Role):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

@app.get("/admin")
async def admin_route(user: User = Depends(require_role(Role.ADMIN))):
    return {"message": "Admin access granted"}
```

---

## Database Integration

### SQLAlchemy Setup
```python
# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# Or PostgreSQL: "postgresql://user:password@localhost/dbname"
# Or MySQL: "mysql://user:password@localhost/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Database Models
```python
# models/user.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    posts = relationship("Post", back_populates="author")

# models/post.py
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="posts")
```

### Pydantic Schemas
```python
# schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserWithPosts(User):
    posts: List["Post"] = []
    
    class Config:
        orm_mode = True

# schemas/post.py
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostWithAuthor(Post):
    author: User
    
    class Config:
        orm_mode = True
```

---

## CRUD Operations

### CRUD Functions
```python
# crud/user.py
from sqlalchemy.orm import Session
from typing import Optional, List
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# crud/post.py
from models.post import Post
from schemas.post import PostCreate, PostUpdate

def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Get post by ID"""
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    """Get all posts with pagination"""
    return db.query(Post).offset(skip).limit(limit).all()

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
    """Get posts by user"""
    return db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """Create new post"""
    db_post = Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: PostUpdate) -> Optional[Post]:
    """Update post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    """Delete post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return False
    
    db.delete(db_post)
    db.commit()
    return True
```

### API Endpoints
```python
# api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.user import User, UserCreate, UserUpdate
from crud import user as crud_user

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return crud_user.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user"""
    db_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    success = crud_user.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# api/v1/endpoints/posts.py
router = APIRouter()

@router.get("/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all posts"""
    posts = crud_post.get_posts(db, skip=skip, limit=limit)
    return posts

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new post"""
    return crud_post.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/{post_id}", response_model=PostWithAuthor)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """Get post by ID"""
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update post"""
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud_post.update_post(db, post_id=post_id, post_update=post_update)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete post"""
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud_post.delete_post(db, post_id=post_id)
    return None
```

---

## Async/Await

### Async Path Operations
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Async with I/O operations
import httpx

@app.get("/external")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### Async Database Operations
```python
# Using databases library
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/")
async def read_users():
    query = "SELECT * FROM users"
    return await database.fetch_all(query)

# Using SQLAlchemy with async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### When to Use Async
**Use async when:**
- Making HTTP requests to external APIs
- Database I/O operations
- File I/O operations
- Network operations

**Don't use async for:**
- CPU-intensive operations
- Synchronous libraries (use regular def)
- Simple operations without I/O

---

## Background Tasks

### Basic Background Task
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message + "\n")

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in the background"}
```

### Background Task with Parameters
```python
def send_email(email: str, subject: str, body: str):
    # Send email logic
    print(f"Sending email to {email}: {subject}")
    time.sleep(5)  # Simulate email sending
    print(f"Email sent to {email}")

@app.post("/send-email/")
async def send_email_endpoint(
    email: str,
    subject: str,
    body: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, subject, body)
    return {"message": "Email will be sent in the background"}
```

### Multiple Background Tasks
```python
@app.post("/process/")
async def process_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(task1, arg1, arg2)
    background_tasks.add_task(task2, arg3, arg4)
    background_tasks.add_task(task3, arg5)
    return {"message": "Processing in the background"}
```

### For Heavy Tasks: Use Celery
```python
# For production, use Celery for complex background tasks
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def heavy_processing_task(data):
    # Heavy processing
    return result

@app.post("/heavy-task/")
async def trigger_heavy_task(data: dict):
    task = heavy_processing_task.delay(data)
    return {"task_id": task.id}
```

---

## Middleware

### Built-in Middleware
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# HTTPS redirect (production)
app.add_middleware(HTTPSRedirectMiddleware)

# Trusted host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

### Custom Middleware
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)

# Or using decorator
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Logging Middleware
```python
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status code: {response.status_code}")
    return response
```

---

## CORS

### Basic CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (development only!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Production CORS (specific origins)
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://example.com",
    "https://www.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## Error Handling

### Custom Exception Handlers
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Usage
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

### HTTP Exceptions
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            headers={"X-Error": "Custom header"},
        )
    return items[item_id]
```

---

## Testing

### Basic Testing
```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": None}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.0}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
```

### Testing with Database
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user(test_db):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
```

### Testing Async Endpoints
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

### Pytest Fixtures
```python
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    return response.json()

def test_with_fixture(client, test_user):
    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
```

---

## WebSockets

### Basic WebSocket
```python
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### WebSocket Chat
```python
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```

---

## Deployment

### Production Settings
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = False
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()

# .env file
# DATABASE_URL=postgresql://user:password@localhost/dbname
# SECRET_KEY=your-secret-key
# DEBUG=False
```

### Running with Gunicorn + Uvicorn
```bash
# Install
pip install gunicorn uvicorn[standard]

# Run
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Best Practices

### 1. Project Structure
- Separate routers by domain (users, posts, etc.)
- Keep business logic in CRUD functions
- Use Pydantic schemas for validation
- Environment-based configuration
- Use dependency injection

### 2. Type Hints
- Always use type hints
- Helps with IDE autocomplete
- Automatic validation
- Better documentation

### 3. Async Best Practices
- Use async for I/O operations
- Don't block the event loop
- Use async database drivers
- For CPU-intensive tasks, use background workers

### 4. Security
- Never store passwords in plain text
- Use JWT for authentication
- Implement rate limiting
- Validate all inputs
- Use HTTPS in production
- Keep dependencies updated

### 5. Error Handling
- Use HTTP exceptions
- Implement custom exception handlers
- Provide meaningful error messages
- Log errors properly

### 6. Testing
- Write tests for all endpoints
- Test with database
- Test authentication
- Test edge cases
- Use pytest fixtures

### 7. Documentation
- Use docstrings
- Add examples to Pydantic models
- Customize OpenAPI schema
- Keep README updated

---

## Interview Questions (3 Years Experience)

### Q1: What is FastAPI and what are its main advantages?
**Answer:** FastAPI is a modern, high-performance Python web framework for building APIs.

**Main Advantages:**
- **Performance:** One of the fastest Python frameworks (comparable to NodeJS and Go)
- **Type Safety:** Built-in type hints with automatic validation
- **Automatic Documentation:** Interactive API docs (Swagger UI, ReDoc)
- **Async Support:** Native async/await support
- **Developer Experience:** Excellent IDE support with autocomplete
- **Less Code:** Reduces code duplication and bugs
- **Standards-Based:** OpenAPI and JSON Schema compliant

**Comparison:**
- **vs Flask:** Faster, automatic validation, async support
- **vs Django:** Lighter, faster, better for APIs
- **vs DRF:** Better performance, simpler syntax, automatic docs

### Q2: Explain Pydantic models and their role in FastAPI.
**Answer:** Pydantic models are Python classes that define data schemas with type hints.

**Role in FastAPI:**
```python
from pydantic import BaseModel, EmailStr, validator

class User(BaseModel):
    username: str
    email: EmailStr
    age: int
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

**Benefits:**
- **Automatic Validation:** Validates request data automatically
- **Type Conversion:** Converts types automatically
- **Clear Errors:** Provides detailed validation errors
- **Documentation:** Generates API documentation
- **IDE Support:** Autocomplete and type checking
- **Serialization:** Converts between Python objects and JSON

**Use Cases:**
- Request body validation
- Response models
- Configuration settings
- Database schemas (with orm_mode)

### Q3: What is dependency injection in FastAPI?
**Answer:** Dependency injection is a design pattern where dependencies are provided to functions rather than created inside them.

```python
from fastapi import Depends
from sqlalchemy.orm import Session

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use dependency
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

**Benefits:**
- **Code Reusability:** Share common logic across endpoints
- **Testing:** Easy to mock dependencies
- **Separation of Concerns:** Clean architecture
- **Flexibility:** Easy to change implementations

**Common Use Cases:**
- Database sessions
- Authentication/authorization
- Configuration
- External services
- Common parameters

**Sub-dependencies:**
```python
def get_token(x_token: str = Header(...)):
    return x_token

def get_user(token: str = Depends(get_token)):
    return validate_token(token)

@app.get("/items/")
def read_items(user: User = Depends(get_user)):
    return items
```

### Q4: How do you handle authentication in FastAPI?
**Answer:**

**OAuth2 with JWT (Recommended):**
```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return get_user(username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

**API Key:**
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

### Q5: Explain async/await in FastAPI. When should you use it?
**Answer:**

**Async allows concurrent I/O operations:**
```python
# Async endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Async with I/O
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fetch_user_from_db(user_id)
    return user
```

**When to Use Async:**
- External API calls
- Database I/O operations
- File I/O operations
- Network operations
- Any waiting/blocking operations

**When NOT to Use Async:**
- CPU-intensive operations
- Synchronous libraries (use regular def)
- Simple operations without I/O

**Performance:**
```python
# Async allows handling multiple requests concurrently
async def call_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()

# While waiting for API response, FastAPI can handle other requests
```

**Async vs Sync:**
- **Async:** Non-blocking, concurrent I/O
- **Sync:** Blocking, one at a time
- FastAPI handles both automatically

### Q6: How do you implement CRUD operations in FastAPI?
**Answer:**

**1. Database Models (SQLAlchemy):**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
```

**2. Pydantic Schemas:**
```python
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class User(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        orm_mode = True
```

**3. CRUD Functions:**
```python
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**4. API Endpoints:**
```python
@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

### Q7: How do you handle file uploads in FastAPI?
**Answer:**

```python
from fastapi import File, UploadFile
import aiofiles

# Single file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# Save file
@app.post("/save-file/")
async def save_file(file: UploadFile = File(...)):
    async with aiofiles.open(f"uploads/{file.filename}", 'wb') as f:
        content = await file.read()
        await f.write(content)
    return {"filename": file.filename}

# Multiple files
@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return [{"filename": file.filename} for file in files]

# File with form data
@app.post("/upload-with-data/")
async def upload_with_data(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...)
):
    return {
        "filename": file.filename,
        "title": title,
        "description": description
    }
```

**Validation:**
```python
def validate_file(file: UploadFile):
    # Check file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large")
    
    # Check file extension
    allowed_extensions = ['.jpg', '.png', '.pdf']
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")
```

### Q8: What are background tasks in FastAPI?
**Answer:** Background tasks allow you to run functions after returning a response.

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Email sending logic
    time.sleep(5)
    print(f"Email sent to {email}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification will be sent"}
```

**Use Cases:**
- Send emails
- Write logs
- Process uploaded files
- Update database records
- Call external APIs

**Multiple Tasks:**
```python
@app.post("/process/")
async def process(background_tasks: BackgroundTasks):
    background_tasks.add_task(task1, arg1)
    background_tasks.add_task(task2, arg2)
    background_tasks.add_task(task3, arg3)
    return {"message": "Processing"}
```

**For Heavy Tasks:**
Use Celery for production:
```python
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def heavy_task(data):
    # Process data
    return result

@app.post("/heavy-process/")
async def trigger_task(data: dict):
    task = heavy_task.delay(data)
    return {"task_id": task.id}
```

### Q9: How do you implement pagination in FastAPI?
**Answer:**

**Simple Pagination:**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
```

**With Count:**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(Item).count()
    items = db.query(Item).offset(skip).limit(limit).all()
    return {
        "total": total,
        "items": items,
        "skip": skip,
        "limit": limit
    }
```

**Custom Pagination:**
```python
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[Item]

@app.get("/items/", response_model=PaginatedResponse)
def read_items(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    total = db.query(Item).count()
    items = db.query(Item).offset(skip).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": items
    }
```

### Q10: How do you handle errors and exceptions in FastAPI?
**Answer:**

**HTTP Exceptions:**
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Custom header"}
        )
    return items[item_id]
```

**Custom Exception Handlers:**
```python
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=418,
        content={"message": f"Error: {exc.name}"}
    )

# Validation Error Handler
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

**Global Exception Handler:**
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
```

### Q11: How do you test FastAPI applications?
**Answer:**

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test", "price": 10.0}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
```

**Testing with Database:**
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

**Testing Async:**
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

### Q12: What is middleware in FastAPI and how do you use it?
**Answer:** Middleware is code that runs before/after each request.

```python
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)

# Or using decorator
@app.middleware("http")
async def add_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Custom-Header"] = "Value"
    return response
```

**Built-in Middleware:**
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Q13: How do you optimize FastAPI performance?
**Answer:**

**1. Use Async for I/O:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fetch_user_async(user_id)
    return user
```

**2. Database Query Optimization:**
```python
# Use select_related/joinedload
users = db.query(User).options(joinedload(User.posts)).all()

# Add database indexes
class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
```

**3. Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_settings():
    return Settings()
```

**4. Response Model Optimization:**
```python
# Only return necessary fields
class UserMinimal(BaseModel):
    id: int
    username: str

@app.get("/users/", response_model=List[UserMinimal])
def get_users():
    return users
```

**5. Background Tasks:**
```python
# Move heavy tasks to background
background_tasks.add_task(process_data, data)
```

**6. Gzip Compression:**
```python
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**7. Connection Pooling:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0
)
```

### Q14: How do you implement WebSockets in FastAPI?
**Answer:**

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

**Chat Application:**
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Q15: How do you deploy FastAPI applications?
**Answer:**

**1. Using Uvicorn:**
```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**2. Using Gunicorn + Uvicorn:**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**3. Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**4. With Docker Compose:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
  db:
    image: postgres:14
```

**5. Environment Variables:**
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Production Best Practices:**
- Use HTTPS
- Set up proper logging
- Use environment variables for secrets
- Implement health checks
- Use reverse proxy (Nginx)
- Monitor performance
- Set up CI/CD
- Use database connection pooling

---

**This comprehensive guide covers all essential FastAPI concepts for 3 years of experience. Practice building APIs, understand async programming, and be prepared to discuss your real-world experience with FastAPI projects.**
