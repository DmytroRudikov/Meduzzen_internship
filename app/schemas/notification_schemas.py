from pydantic import BaseModel


class Notification(BaseModel):
    notification_id: int
    status: str
    date_time: str
    text: str
    company_id: int
    user_id: int
    quiz_record_id: int
