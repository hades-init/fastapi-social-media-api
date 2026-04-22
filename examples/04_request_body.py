from fastapi import FastAPI
from pydantic import BaseModel

# Declare your data model
# Your data model class must inherit from Pydantic `BaseModel` class
class Item(BaseModel):
    name: str
    description: str | None = None    # Optional attribute  
    price: float
    tax: float | None = None      # Optional attribute 

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()   # return a dictionary representation of model
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


## Request body + path parameters + query parameters

# `item_id` - path parameter
# `item` - request body (Pydantic model)
# `q` - query parameter
@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result