from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.database import get_db
from app.core.security import get_current_user


# APIRouter class, used to group path operations
router = APIRouter(prefix="/posts", tags=["Posts"])


# Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Create new `Post` object
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # Add the object to session
    db.add(new_post)
    # Commit changes to database
    db.commit()
    # Fetch the newly inserted object from database (refresh the attributes on the given object)
    db.refresh(new_post)

    return new_post


# Get all posts
@router.get("/", response_model=List[schemas.PostPublic])
def get_posts(
    filter: Annotated[schemas.FilterParam, Query()],     # query params
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Select statement

    # chain with `.where(models.Post.owner_id == current_user.id)` to get only posts of current user
    # 
    # stmt = select(models.Post).where(models.Post.title.icontains(q)).limit(limit).offset(skip)
    # posts = db.scalars(stmt).all()

    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote)
        .where(models.Post.title.icontains(filter.q))
        .group_by(models.Post.id)
        .limit(filter.limit).offset(filter.skip)
    )

    # Execute statement and retrieve results
    results = db.execute(stmt).all()
    
    posts = [
        schemas.PostPublic(**post.__dict__, owner=post.owner, votes=votes)
        for post, votes in results
    ]
    
    return posts


# Get post by Id
@router.get("/{id}", response_model=schemas.PostPublic)
def get_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Fetch post by primary key (PK)
    # post = db.get(models.Post, id)

    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote).where(models.Post.id == id)
        .group_by(models.Post.id)
    )
    
    result = db.execute(stmt).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} does not exist.",
        )
    
    post, votes = result
    return schemas.PostPublic(**post.__dict__, owner=post.owner, votes=votes)


# Update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Fetch post from database
    db_post = db.get(models.Post, id)

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} does not exist."
        )
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action."
        )

    # Extract updated attributes from request body
    post_data = post.model_dump(exclude_unset=True)

    # Update attributes of `db_post` using `setattr()` method
    for key, value in post_data.items():
        setattr(db_post, key, value)
    
    # Add changes to session
    db.add(db_post)
    # Commit changes to database
    db.commit()
    # Refresh attributes on given object
    db.refresh(db_post)

    return db_post


# Delete post
# As per HTTP standards, response with status code 204 must not include any content 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Fetch post from database
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id = {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
        )

    # Delete post from session
    db.delete(post)
    # Commit changes to database
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)   # explicitly tells FastAPI "send exactly this, no body, no serialization"
