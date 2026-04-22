from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app import utils
from app.core.database import get_db
from app.core import security


router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.email == form_data.username)
    db_user = db.scalar(stmt)

    if not db_user:
        # When the username does not exist in database, we still run verify_password() against a dummy hash.
        # This ensures the endpoint takes roughly the same amount of time to respond whether the username is valid or not, 
        # preventing timing attacks that could be used to enumerate existing usernames.
        utils.verify_password(form_data.password, utils.DUMMY_HASH)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect email or password.",
            )
    
    if not utils.verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect email or password.")
    
    # Payload for JWT
    data = {"sub": str(db_user.id)}
    # Create access token
    access_token = security.create_access_token(data)
    
    return schemas.Token(access_token=access_token)
