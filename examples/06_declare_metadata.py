from typing import Annotated
from fastapi import FastAPI, Query, Path

app = FastAPI()

## Declare metadata

# Declaring metadata for query parameter

@app.get("/items/")
def get_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",     # alias parameter
            title="Query string",
            description="Query string for the items to search in the database",
            min_length=3,
            max_length=25,
            deprecated=True,        # deprecating parameter
            # include_in_schema=False,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Declaring metadata for path parameter

@app.get("/items/{item_id}")
def read_item(
    item_id: Annotated[
        int, 
        Path(
            alias="item-id",
            title="Item ID",
            description="ID of the item to get",
        ),
    ],
):
    return {"item_id": item_id, "item_name": "Foobar"}