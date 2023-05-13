import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import uvicorn
from dotenv import load_dotenv
import json
from routers import user_routers, general_routers, auth_routers, company_routers, member_routers, request_routers, invite_routers, quiz_routers, results_routers, export_redis_data_routers, analytics_routers

load_dotenv()

app = FastAPI()
app.include_router(general_routers.router)
app.include_router(user_routers.router)
app.include_router(auth_routers.router)
app.include_router(company_routers.router)
app.include_router(member_routers.router)
app.include_router(request_routers.router)
app.include_router(invite_routers.router)
app.include_router(quiz_routers.router)
app.include_router(results_routers.router)
app.include_router(export_redis_data_routers.router)
app.include_router(analytics_routers.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=json.loads(os.getenv("ORIGINS")) if os.getenv("ORIGINS") is not None else "*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_pagination(app)


@app.get("/")
async def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("APP_PORT")), reload=True)
