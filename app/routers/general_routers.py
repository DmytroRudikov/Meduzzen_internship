from fastapi import APIRouter
from app.core.db_config import get_redis_db, get_sql_db

router = APIRouter()


@router.on_event("startup")
async def connect_to_db():
    get_redis_db()
    await get_sql_db().connect()


@router.on_event("shutdown")
async def disconnect_from_sql():
    db = get_sql_db()
    await db.disconnect()
