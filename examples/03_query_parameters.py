from fastapi import FastAPI
from typing import Optional
from enum import Enum

# Initialize the application
app = FastAPI()

## Query Parameters

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Quux"}]

# filter by `skip` and `limit` - used in pagination of results
@app.get("/items/")
def fetch_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


## Query parameters type conversion

# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes

# or any other case variations of these, 
# the function will see the parameter `desc` with a bool value of `True`

@app.get("/items/{item_name}")
async def read_items(item_name: str, desc: bool = False):
    item = {"item_name": item_name}
    if desc:
        item.update(
            {"description": "This is an item that has a long description"}
        )
    return item


## Optional query parameters

fake_orders_db = [{"id": 42, "status": "completed"}, {"id": 37, "status": "pending"}, {"id": 11, "status": "shipped"}]

class Status(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    SHIPPED = "shipped"

@app.get("/orders/")
async def get_orders(status: Status | None = None):
    if status:
        return [order for order in fake_orders_db if order["status"] == status.value]
    return fake_orders_db


## Multiple path and query parameters

@app.get("/users/{user_id}/orders/{order_id}")
def get_user_orders(
    user_id: int, 
    order_id: int, 
    status: Optional[str] = None,
    desc: bool = False,    # if True return a long description
):
    order = {"order_id": order_id, "user_id": user_id}
    if status:
        order.update({"status": status})
    if desc:
        order.update(
            {"description": "This is an order that has a long description."}
        )
    return order

