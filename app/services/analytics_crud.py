from app.schemas import analytics_schemas
from app.db import models
from databases import Database
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, func, DateTime, cast, desc
from typing import List
from app.services.crud_results import ResultsCrud


class AnalyticsCrud:
    def __init__(self, db: Database):
        self.db = db

    async def get_my_average_result(self, user_id: int) -> float:
        crud_results = ResultsCrud(db=self.db)
        average_result = await crud_results.average_result_for_user_in_the_system(user_id=user_id)
        return average_result

    async def get_list_my_average_results(self, user_id: int) -> List[analytics_schemas.MyResults]:
        subquery = await self.db.fetch_all(select(models.QuizResults).filter_by(user_id=user_id))
        quiz_ids = [obj.quiz_record_id for obj in subquery]
        results = await self.db.fetch_all(select(
            models.QuizResults.company_id,
            models.Quiz.quiz_id_in_company,
            models.QuizResults.average_result,
            models.QuizResults.pass_date
        ).join(models.Quiz).filter(models.Quiz.quiz_record_id.in_(quiz_ids)).where(models.QuizResults.user_id == user_id))
        return results

    async def get_list_of_quizzes_passed(self, user_id: int) -> List[analytics_schemas.QuizzesList]:
        subquery = await self.db.fetch_all(select(models.QuizResults).filter_by(user_id=user_id))
        quiz_ids = [obj.quiz_record_id for obj in subquery]
        data = await self.db.fetch_all(select([
            models.QuizResults.company_id,
            models.Quiz.quiz_id_in_company,
            models.QuizResults.pass_date,
            func.row_number().over(partition_by=(models.QuizResults.user_id, models.QuizResults.quiz_record_id), order_by=desc(models.QuizResults.pass_date.cast(DateTime))).label("row_num")
        ]).join(models.Quiz).filter(models.Quiz.quiz_record_id.in_(quiz_ids)).where(models.QuizResults.user_id == user_id))
        results = [
            {"company_id": obj.company_id, "quiz_id_in_company": obj.quiz_id_in_company, "pass_date": obj.pass_date}
            for obj in data if obj.row_num == 1]
        return results

    async def get_list_all_members_results(self, company_id: int) -> List[analytics_schemas.MemberResults]:
        subquery = await self.db.fetch_all(select(models.QuizResults).filter_by(company_id=company_id))
        quiz_ids = [obj.quiz_record_id for obj in subquery]
        results = await self.db.fetch_all(select(
            models.Quiz.quiz_id_in_company,
            models.QuizResults.user_id,
            models.QuizResults.average_result,
            models.QuizResults.pass_date
        ).join(models.Quiz).filter(models.Quiz.quiz_record_id.in_(quiz_ids)).where(
            models.QuizResults.company_id == company_id))
        return results

    async def get_all_results_for_specific_member(self, company_id: int, user_id: int) -> List[analytics_schemas.MemberResults]:
        subquery = await self.db.fetch_all(select(models.QuizResults).filter_by(company_id=company_id, user_id=user_id))
        quiz_ids = [obj.quiz_record_id for obj in subquery]
        results = await self.db.fetch_all(select(
            models.Quiz.quiz_id_in_company,
            models.QuizResults.user_id,
            models.QuizResults.average_result,
            models.QuizResults.pass_date
        ).join(models.Quiz).filter(models.Quiz.quiz_record_id.in_(quiz_ids)).where(
            models.QuizResults.user_id == user_id and models.QuizResults.company_id == company_id))
        return results

    async def get_list_of_members_passed(self, company_id: int) -> List[analytics_schemas.MembersPassed]:
        subquery1 = await self.db.fetch_all(select(models.QuizResults.quiz_record_id).filter_by(company_id=company_id))
        quiz_ids = set(obj.quiz_record_id for obj in subquery1)
        subquery2 = await self.db.fetch_all(select(models.QuizResults.user_id).filter_by(company_id=company_id))
        user_ids = set(obj.user_id for obj in subquery2)
        data_1 = await self.db.fetch_all(select(
            models.Quiz.quiz_id_in_company,
            models.QuizResults.user_id,
            func.row_number().over(partition_by=(models.QuizResults.user_id, models.QuizResults.quiz_record_id), order_by=desc(models.QuizResults.pass_date.cast(DateTime))).label("row_num")
        ).join(models.Quiz).filter(models.Quiz.quiz_record_id.in_(quiz_ids)).where(
            models.QuizResults.company_id == company_id))
        data_2 = await self.db.fetch_all(select(
            models.MemberRecord.company_member_id,
            models.MemberRecord.user_id,
        ).filter(models.MemberRecord.user_id.in_(user_ids)).where(models.MemberRecord.company_id == company_id))
        quizzes_by_users = [(e.user_id, e.quiz_id_in_company) for e in data_1 if e.row_num == 1]
        members_by_users = [(e.user_id, e.company_member_id) for e in data_2]
        results = [
            {"company_member_id": [i[1] for i in members_by_users if i[0] == e[0]][0], "quiz_id_in_company": e[1]}
            for e in quizzes_by_users]
        return results
