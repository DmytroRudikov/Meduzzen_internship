import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import json
from routers import user_routers, general_routers, token_routers

load_dotenv()

app = FastAPI()
app.include_router(general_routers.router)
app.include_router(user_routers.router)
app.include_router(token_routers.router)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("APP_PORT")), reload=True)
