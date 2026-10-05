from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json 
app = FastAPI()

@app.get("/users")
def getuser():
    with open("data/users.json","r")as file:
        user=json.load(file)
    return user


@app.get("/users/{user_id}")
def getusers(user_id:int):
    with open ("data/users.json","r") as file:
        users=json.load(file)

    for user in users:
        if user["id"]==user_id:
            return user
    raise HTTPException(status_code=404,detail="user not found")


class Usercreate(BaseModel):
    name: str
    email: str

@app.post("/users",status_code=201)
def create_user(user: Usercreate):
    with open("data/users.json","r")as file:
        users=json.load(file)
    if users:
        new_id=max(user["id"] for user in users)+1
    else:
        new_id=1

    new_user={
        "id":new_id,
        "name":user.name,
        "email":user.email
         }
    users.append(new_user)
    with open("data/users.json","w")as file:
        json.dump(users,file,indent=4)
    return new_user