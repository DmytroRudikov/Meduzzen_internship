from sqlalchemy.orm import Session
from app.schemas import models, schemas
from passlib.context import CryptContext
import datetime

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, email: str, password: str, first_name: str, last_name: str):
    hashed_password = context.hash(password)
    created_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    new_user = models.User(first_name=first_name,
                           last_name=last_name,
                           email=email.lower(),
                           password=hashed_password,
                           created_on=created_on,
                           updated_on=updated_on)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, email: str, user_upd: schemas.UserUpdate):
    user = db.query(models.User).filter_by(email=email).first()
    for key in user.__table__.columns.keys():
        if key not in user_upd:
            continue
        else:
            setattr(user, key, user_upd[key])
    db.commit()
    db.refresh(user)
    return user
