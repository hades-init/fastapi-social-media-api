from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas, utils
from app.core.database import get_db
from app.core.security import get_current_user


# APIRouter class, used to group path operations
router = APIRouter(prefix="/users", tags=["Users"])


# Create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserPublic)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    stmt = select(models.User).where(models.User.email == user.email)
    db_user = db.scalar(stmt)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists."
        )
    
    # Generate password hash
    user.password = utils.get_password_hash(user.password)
    # Create new user
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# Get current user profile
@router.get("/me", response_model=schemas.UserPublic)
def get_user_me(user: Annotated[models.User, Depends(get_current_user)]):
    return user


# Get user
@router.get("/{id}", response_model=schemas.UserPublic)
def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User(id={id}) does not exist.",
        )
    
    return user