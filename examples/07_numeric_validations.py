from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

## Numeric validations

@app.get("/items/{item_id}")
def read_item(
    *,
    item_id: Annotated[int, Path(title="Item ID", ge=0, lt=1000)],
    q: str | None = None,
    count: Annotated[int, Query(gt=0, le=5)] = 1,
    size: Annotated[float, Query(gt=0, lt=10.5, multiple_of=0.5)],
):
    results = {"item_id": item_id, "item_name": "Foobar", "count": count}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results