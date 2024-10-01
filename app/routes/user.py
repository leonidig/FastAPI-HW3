from aiohttp import ClientSession
from sqlalchemy import select
from fastapi import HTTPException
from .. import app
from ..db import User, Session
from ..schemas import UserData


@app.get("/mock_data")
async def get_mock_users():
    async with ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/users") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise HTTPException(500, "Could not get users!")
            
@app.get("/users")
async def get_all_users():
    async with Session.begin() as session:
        users = await session.scalars(select(User))
        users = [UserData.model_validate(user) for user in users]
        return users
    
@app.post("/create_user", status_code=201)
async def create_user(data: UserData):
    try: 
        async with Session.begin() as session:
            user = User(**data.model_dump())
            session.add(user)
    except:
        raise HTTPException(409, detail="User exists!")
    
@app.delete("/users/{username}")
async def delete_user(name: str):
    async with Session.begin() as session:
            user = await session.scalar(select(User).where(User.name == name))
            if user:
                await session.delete(user)
            else:
                raise HTTPException(404, detail="User not found!")