from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
import json
from app.core.db_config import get_redis_db, get_sql_db, get_session
from app.utils import crud_user
from app.schemas import schemas
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=json.loads(os.getenv("ORIGINS")) if os.getenv("ORIGINS") is not None else "*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"}


@app.on_event("startup")
async def connect_to_db():
    db = get_sql_db()
    await db.connect()
    get_redis_db()


@app.on_event("shutdown")
async def disconnect_from_sql():
    db = get_sql_db()
    await db.disconnect()


@app.get("/user")
async def get_user(user_id: int, response: Response, session: AsyncSession = Depends(get_session)):
    return await crud_user.get_user(session=session, user_id=user_id, response=response)


@app.get("/users", response_model=List[schemas.User])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    return await crud_user.get_all_users(session)


@app.post("/user")
async def create_user(signup_form: schemas.SignupRequest, response: Response, session: AsyncSession = Depends(get_session)):
    return await crud_user.create_user(session=session, signup_form=signup_form, response=response)


@app.put("/user")
async def update_user(user_upd: schemas.UserUpdate, user_id: int, response: Response, session: AsyncSession = Depends(get_session)):
    return await crud_user.update_user(session=session, user_id=user_id, user_upd=user_upd, response=response)


@app.delete("/user")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_user.delete_user(session, user_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("APP_PORT")), reload=True)
