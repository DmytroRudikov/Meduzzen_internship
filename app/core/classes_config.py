from utils.crud_user import UserCrud
from core.db_config import get_sql_db

crud_user = UserCrud(get_sql_db())
