from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, AfterValidator
from datetime import datetime


# --- Users ---

# Base class for User schemas
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API for create User
class UserCreate(UserBase):
    password: str

# Properties to return via API for create/update User
class User(UserBase):
    id: int
    created_at: datetime

# Properties to return via API for get User
class UserPublic(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)     # Allows reading from SQLAlchemy objects

# Properties to receive via API for User login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Posts ---

# Base class for Post schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Properties to receive via API for create/update Post
class PostCreate(PostBase):
    pass

# Properties to return via API for create/update Post
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int


# Properties to return via API for get Post
class PostPublic(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserPublic
    votes: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")     # Allows reading from SQLAlchemy objects




# Vote
class Vote(BaseModel):
    post_id: int
    like: bool 


# --- Token ---

# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Token payload (encoded data)
class TokenPayload(BaseModel):
    sub: str | None = None


# --- Query parameters ---

# Filter parameters
class FilterParam(BaseModel):
    q: Annotated[str | None, AfterValidator(lambda q : q.strip())] = ""
    limit: Annotated[int, Field(gt=0, le=100)] = 10
    skip: Annotated[int, Field(ge=0)] = 0