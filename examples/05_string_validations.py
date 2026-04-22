from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import AfterValidator
import random

app = FastAPI()

## String validations

# Use `Annotated` in the type for query parameter
# Add `Query` inside `Annotated` to set additional validations (like `max_length`)

@app.get("/items/")
def read_items(q: Annotated[str | None, Query(min_length=10, max_length=25)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Checking parameter against regular expression `pattern`
@app.get("/info/")
def read_info(
    name: str,
    phone: Annotated[str | None, Query(pattern="^[0-9]{10}$")]
):
    result = {"name": name, "phone": phone}
    return result


## Query parameter list / multiple values

movies_db = [{"movie": "Intersteller", "tags": ["sci-fi", "adventure"]}, 
             {"movie": "Knight and Day", "tags": ["action", "romance"]}, 
             {"movie": "Get Out", "tags": ["thriller", "mystery"]}]

@app.get("/movies/")
def read_movies(tags: Annotated[list[str], Query()] = ["foo", "bar"]):
    # lambda function to check if a movie has any of given tags
    has_tag = lambda movie: any(tag in movie["tags"] for tag in tags)
    results = [movie for movie in movies_db if has_tag(movie)]
    return results if results else movies_db    # if results in None, return all movies


## Custom validations

books_db = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "isbn-978-1400079278": "Kafka On The Shore",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

# custom validator function
def check_valid_id(id_: str):
    if not id_.startswith("isbn"):
        raise ValueError("Invalid ID format, it must start with 'isbn-'")
    # return the value unchanged after performing validation check
    return id_

@app.get("/books/")
def read_books(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item_name = books_db.get(id)
    else:
        id, item_name = random.choice(list(books_db.items()))
    
    return {"id": id, "name": item_name}
