from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
import random

# Initialize the application 
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

posts_db = [
    {
        "title": "Oppenheimer's Award Run",
        "content": "Oppenheimer continues winning major awards, dominating the 2024 season.",
        "published": True,
        "id": 54162
    },
    {
        "title": "Mumbai Goes Wild for Guns N' Roses",
        "content": "Thousands gathered in Mumbai as Guns N’ Roses performed live in 2025.",
        "published": True,
        "id": 72543
    },
    {
        "title": "Tame Impala on repeat!",
        "content": "Can't stop listening to the latest album that dropped this week.",
        "published": True,
        "id": 54162
    },
]

# Get root
@app.get("/")
def root():
    return {"message": "Hello World!"}

# Get all posts
@app.get("/posts")
def get_posts():
    return {"posts": posts_db}

# Get post with specific Id
@app.get("/posts/{id}")
def get_post(id: int):
    results = [post for post in posts_db if post["id"] == id]
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with 'id = {id}' was not found."
            )
    return {"post": results[0]}

# Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    id_ = random.randrange(0, 100_000)    # generate random ID
    post_dict["id"] = id_
    posts_db.append(post_dict)     # add post to db
    return { "post": post_dict, "message": "Post created successfully."}


# Delete post
# As per HTTP standards, response with status 204 must not include any content 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = _find_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with 'id = {id}' was not found."
            )
    posts_db.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)   # explicitly tells FastAPI "send exactly this, no body, no serialization"

def _find_index(id):
    for i, post in enumerate(posts_db):
        if post["id"] == id:
            return i
    return None

# Update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = _find_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with 'id = {id}' was not found."
        )
    
    post_dict = post.model_dump()
    post_dict["id"] = id
    posts_db[index] = post_dict
    return {"post": post_dict}