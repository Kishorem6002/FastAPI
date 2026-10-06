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

#defining the user model for creating a new user
class Usercreate(BaseModel):
    name: str
    email: str
    age: int

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
        "email":user.email,
        "age":user.age
         }
    users.append(new_user)
    with open("data/users.json","w")as file:
        json.dump(users,file,indent=4)
    return new_user
class UserUpdate(BaseModel):
    name:str
    email:str
    age:int
#defining the endpoint for updating a user
@app.put("/users/{user_id}")
def update_user(user_id:int,user:UserUpdate):
    with open("data/users.json","r")as file:
        users=json.load(file)
    for user_data in users:
        if user_data["id"]==user_id:
            user_data["name"]=user.name
            user_data["email"]=user.email
            user_data["age"]=user.age
            with open("data/users.json","w")as file:
                json.dump(users,file,indent=4)
            return user_data
    raise HTTPException(status_code=404,detail="User not found")

@app.delete("/users/{user_id}")

def delete_user(user_id:int):
    with open("data/users.json","r")as file:
        users=json.load(file)
    for user_data in users:
        if user_data["id"]==user_id:
            users.remove(user_data)
            with open("data/users.json","w")as file:
                json.dump(users,file,indent=4)
            return {"message":"user is deleted successfully"}
    raise HTTPException(status_code=404,detail="User not found")






