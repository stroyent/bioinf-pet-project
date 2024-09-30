from typing import Union

from fastapi import FastAPI

from random import randint

app = FastAPI()



def load_sandwiches():
    with open("sandwiches.txt", "r", encoding="utf-8") as source_file:
        current_sandwich = ""
        sandwich_list = []

        for line in source_file:
            if line == "\n":
                sandwich_list.append(current_sandwich)
                current_sandwich = ""
                continue
            current_sandwich += line
    return sandwich_list


def random_sandwich(sandwich_list):
    return sandwich_list[randint(0, len(sandwich_list) - 1)]


loaded_sandwiches = load_sandwiches()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/sammiches")
def get_sandwich():
    return {"sandwich": random_sandwich(loaded_sandwiches)}