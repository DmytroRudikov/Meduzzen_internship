import pytest
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


@app.get("/")
async def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)
