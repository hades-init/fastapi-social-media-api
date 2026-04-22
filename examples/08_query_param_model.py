from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

## Query parameters with Pydantic model

# Declare query parameters using a Pydantic model
# You can use `Field` function to provide additional metadata or complex validations 
class FilterParams(BaseModel):
    limit: Annotated[int, Field(gt=0, le=100)] = 100
    offset: Annotated[int, Field(ge=0)] = 0
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

# Declare parameter as `Query` to indicate FastAPI that this is a query parameter
@app.get("/items/")
def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query