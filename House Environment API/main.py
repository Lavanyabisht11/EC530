#this is my actual REST API

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# In-memory "database"
users = {}
houses = {}
floors = {}
rooms = {}
devices = {}

# ---------- Models ----------
class User(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None

class House(BaseModel):
    house_id: str
    address: str
    gps_location: str
    size: float
    floors: List[str] = []

class Floor(BaseModel):
    floor_id: str
    house_id: str
    rooms: List[str] = []

class Room(BaseModel):
    room_id: str
    name: str
    floor_id: str
    devices: List[str] = []

class Device(BaseModel):
    device_id: str
    type: str
    room_id: str

# ---------- User APIs ----------
@app.post("/users/")
def create_user(user: User):
    users[user.user_id] = user
    return {"message": "User created", "user": user}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    users[user_id] = user
    return {"message": "User updated", "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    users.pop(user_id, None)
    return {"message": "User deleted"}

# ---------- House APIs ----------
@app.post("/houses/")
def create_house(house: House):
    houses[house.house_id] = house
    return {"message": "House created", "house": house}

@app.get("/houses/{house_id}")
def read_house(house_id: str):
    house = houses.get(house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@app.put("/houses/{house_id}")
def update_house(house_id: str, house: House):
    houses[house_id] = house
    return {"message": "House updated", "house": house}

@app.delete("/houses/{house_id}")
def delete_house(house_id: str):
    houses.pop(house_id, None)
    return {"message": "House deleted"}

# ---------- Device, Room, Floor endpoints can be similarly added (you’ve already written the logic) ----------
