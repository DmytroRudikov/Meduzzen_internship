from app.schemas import notification_schemas
from app.db import models
from databases import Database
from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from typing import List
from app.services.crud_member import MemberCrud
import datetime


class NotificationCrud:

    def __init__(self, db: Database):
        self.db = db
        self.date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.text = "Please take the quiz at any time convenient for you"
        self.status = "unread"

    async def create_notification(self, company_id: int, quiz_record_id: int):
        notification_values = []
        crud_member = MemberCrud(db=self.db)
        company_members = await crud_member.get_all_members(company_id=company_id)
        for member in company_members:
            values = {
                "quiz_record_id": quiz_record_id,
                "status": self.status,
                "date_time": self.date_time,
                "text": self.text,
                "company_id": company_id,
                "user_id": member.user_id,
            }
            notification_values.append(values)
        await self.db.execute_many(insert(models.Notification), values=notification_values)

    async def get_all_unread_notifications(self, user_id: int) -> List[notification_schemas.Notification]:
        notifications = await self.db.fetch_all(select(models.Notification).filter_by(user_id=user_id, status="unread"))
        return notifications

    async def update_notification(self, notification_id: int) -> status.HTTP_200_OK:
        values = {"status": "read"}
        await self.db.execute(update(models.Notification).filter_by(notification_id=notification_id).values(**values))
        return HTTPException(status_code=200, detail="success")
