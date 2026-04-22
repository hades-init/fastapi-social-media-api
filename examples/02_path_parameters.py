from fastapi import FastAPI
from enum import Enum

# Initialize the application
app = FastAPI()

## Path parameters

# using standard Python type declarations
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}


## Path operations are evaluated in order

@app.get("/users/me")
def get_user_me():
    return {"message": "myprofile"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"message": f"user{user_id} profile"}


## Pre-defined values for path parameters

# `ModelName` class inherits from `str` and `Enum`
class ModelName(str, Enum):
    openai = "openai"
    claude = "claude"
    gemini = "gemini"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.openai:
        return {"model_name": model_name, "message": "Ask ChatGPT !"}
    
    if model_name.value == "claude":
        return {"model_name": model_name, "message": "Chat with Claude ..."}
    
    return {"model_name": model_name, "message": "Ask Gemini !"}


## Path parameters containing path

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    # read file
    return {"file_path": file_path}
