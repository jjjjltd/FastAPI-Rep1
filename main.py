from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Validators(Enum):
    FRUITORVEG = ["Apple", "Banana", "Cherry"]
    SIZE = [1, 2, 3, 4, 5]
    JUICINESS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Fruit(BaseModel):
    id: int
    name: str
    size: int
    juiciness: int
    description: str
    


fruits = {
    0: Fruit(name="Apple", size=3, juiciness=2, description="", id=0),
    1: Fruit(name="Banana", size=3, juiciness=1, description="", id=1),
    2: Fruit(name="Cherry", size=1, juiciness=1, description="", id=2),
    3: Fruit(name="Roses", size=3, juiciness=3, description="bollocks", id=3),
}

@app.get("/")
def index() -> dict[str, dict[int, Fruit]]:
    return {"fruits": fruits}

@app.get("/{id}")
def query_fruit_by_id(id: int) -> Fruit:

    if id < 0 or id > len(fruits)-1:
        print("I am here")
        raise HTTPException(
            status=404, detail=("Integer value out of range.")
        )
    print("After range check.")
    if id not in fruits:
        raise HTTPException(
           status_code=404, detail=(f"Fruit with id {id} does not exist.")
        )
        print("no clue!!")
    return fruits[id]

Selection=dict[
    str, str | int | int | str | int | None
]

@app.get("/fruits/")
def query_fruits_by_parameters(
    name: str | None=None,
    size: int | None=None,
    juiciness: int | None=None,
    description: str | None=None,
    id: int | None=None,
) -> dict[str, Selection | list[Fruit]]:
    def check_fruit(fruit: Fruit):
        return all(
            {
            name is None or fruit.name == name,
            size is None or fruit.size == size,
            juiciness is None or fruit.juiciness == juiciness,
            description is None or fruit.description == description,
            id is None or fruit.id == id,
            }
        )

    selection=[fruit for fruit in fruits.values() if check_fruit(fruit)]
    return {
        "query": {"name": name, "size": size, "juiciness": juiciness, "description": description, "id": id},
        "selection": selection

    }

@app.post("/")
def add_fruit(fruit: Fruit) -> dict[str, Fruit]:
    if fruit.id in fruits:
        raise HTTPException(
            status_code=404, detail=f"Fruit with{fruit.id} already exists")

    fruits[fruit.id]=fruit
    return {"added": fruit}

@app.put("/update/{user}")
def update(
    id: int,
    name: str | None=None,
    size: int | None=None,
    juiciness: int | None=None,
    description: str | None=None,

) -> dict[str, Fruit]:

    if id not in fruits:
        raise HTTPException(
            status_code=404, detail=f"Fruit with {id} not avaialble for update")
    if all(info is None for info in (name, size, juiciness, description)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update.")

    fruit=fruit[id]
    if name is not None:
        fruit.name=name
    if size is not None:
        fruit.size=size
    if juiciness is not None:
        fruit.juiciness=juiciness
    if description is not None:
        fruit.description=description

    return {"updated": fruit}

@ app.delete("/delete/{id}")
def delete_fuirt(id: int) -> dict[str, Fruit]:

    if id not in fruits:
        raise HTTPException(
            status_code=404, details=f"Fruit with {id} does not exist")

    fruits=fruits.pop(id)
    return {"Deleted": id}
