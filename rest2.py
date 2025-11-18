from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str


users = []


@app.get("/users")
def get_users():
    return users


@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user
