import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import user_schemas, notification_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from app.services.crud_notification import NotificationCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user

router = APIRouter()


@router.get("/my_notifications", response_model=Page[notification_schemas.Notification])
async def get_my_notifications(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[notification_schemas.Notification]:
    crud_notification = NotificationCrud(db=db)
    notifications = await crud_notification.get_all_unread_notifications(user_id=user.id)
    return paginate(notifications)


@router.put("/my_notifications/{notification_id}/read", status_code=200)
async def read_notification(notification_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_notification = NotificationCrud(db=db)
    user_notifications = await crud_notification.get_all_unread_notifications(user_id=user.id)
    notification_ids = [n.notification_id for n in user_notifications]
    if notification_id not in notification_ids:
        raise HTTPException(status_code=403, detail="You are allowed to change status of only unread notifications that belong to you")
    return await crud_notification.update_notification(notification_id=notification_id)