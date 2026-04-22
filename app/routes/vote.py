from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas, utils
from app.core.database import get_db
from app.core.security import get_current_user


router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: schemas.Vote,
    current_user: Annotated[models.User, Depends(get_current_user)], 
    db: Annotated[Session, Depends(get_db)]
):
    # Check if post exists
    db_post = db.get(models.Post, vote.post_id)
    if not db_post:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post(id={vote.post_id}) does not exist.",
        )
    
    # Check if vote exists
    db_vote = db.get(models.Vote, (vote.post_id, current_user.id))
    
    # upvote/like
    if vote.like:
        # if already liked the post, raise exception
        if db_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User(id={current_user.id}) has already voted on the Post(id={vote.post_id})."
            )
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)
    
    # remove like
    else:
        # if vote does not exist, raise exception
        if not db_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist.",
            )
        
        db.delete(db_vote)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

