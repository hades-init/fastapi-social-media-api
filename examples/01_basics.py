from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

# Initialize the application
app = FastAPI()

## Path operation

# path - "/"
# operation - GET method
@app.get("/")   # Path operation decorator
def root():
    return {"message": "Hello World!"}


fake_items = [{"name": "Foo"}, {"name": "Bar"},]

@app.get("/items")
def get_items():
    return {"items": fake_items}