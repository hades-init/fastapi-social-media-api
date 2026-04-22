from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from app.schemas import TokenPayload
from app.models import User
from app.core.database import get_db
from app.core.config import settings


# OAuth2 flow for authentication using a bearer token obtained with a password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create access token
def create_access_token(data: dict):
    payload = data.copy()

    # Add token expiration 
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)    # Note: PyJWT compares the `exp` against UTC time, you must always pass `timezone.utc`
    # expire = datetime.now(timezone.utc) + timedelta(seconds=30)
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

# Verify access token
def verify_access_token(access_token: str):
    try:
        payload = jwt.decode(access_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Access token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return TokenPayload(**payload)

# Get current logged in user 
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)],
    ) -> User:
    # Verify access token
    payload = verify_access_token(token)
    # Get User from database
    user = db.get(User, payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found.",
            )
    return user