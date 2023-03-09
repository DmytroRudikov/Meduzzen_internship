from fastapi import APIRouter, Depends
from app.core.db_config import get_redis_db, get_sql_db
from databases import Database

router = APIRouter()


@router.on_event("startup")
async def connect_to_db(database: Database = Depends(get_sql_db)):
    get_redis_db()
    await database.connect()
    yield database


# @router.on_event("startup")
# async def connect_to_engine():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@router.on_event("shutdown")
async def disconnect_from_sql():
    db = get_sql_db()
    await db.disconnect()
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
