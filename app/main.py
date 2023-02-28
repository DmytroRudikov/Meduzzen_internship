from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
import json
from db.db_config import get_redis_db, get_sql_db

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



if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("APP_PORT")), reload=True)
