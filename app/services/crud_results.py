from schemas import results_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, func
from typing import List, Dict
from services.crud_quiz import QuizCrud


class ResultsCrud:
    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def correct_rounding(num: str) -> float:
        split_num = num.split(".")
        first_part = split_num[0]
        second_part = split_num[1]
        if len(second_part) == 2:
            if int(second_part[1]) >= 5:
                if int(second_part[0]) != 9:
                    second_part = int(second_part[0]) + 1
                else:
                    second_part = 0
                    first_part = int(first_part) + 1
            else:
                second_part = int(second_part[0])
        result = float(str(first_part) + "." + str(second_part))
        return result

    async def answers_len_check(self, answers: results_schemas.AnswerQuiz, quiz_record_id: int):
        questions = await self.db.fetch_all(select(models.Question).filter_by(quiz_record_id=quiz_record_id))
        for answer in answers.answers:
            if answers.answers[answer] == "" or answers.answers[answer] is None:
                raise HTTPException(status_code=403, detail="Not all questions were answered")
        if len(answers.answers) < len(questions):
            raise HTTPException(status_code=403, detail="Not all questions were answered")

    async def results_to_record(self, answers: results_schemas.AnswerQuiz, user_id: int, company_id: int, quiz_record_id: int) -> results_schemas.Results:
        questions = await self.db.fetch_all(select(models.Question).filter_by(quiz_record_id=quiz_record_id))
        result_count = 0
        for q_num, answer in answers.answers.items():
            for question in questions:
                if question.question_id_in_quiz == int(q_num):
                    correct_answer = question.correct_answer
                    if correct_answer == answer:
                        result_count += 1

        highest_num_of_quest_record = await self.db.fetch_one(select(models.QuizResults).filter_by(user_id=user_id, company_id=company_id, quiz_record_id=quiz_record_id).order_by(models.QuizResults.number_of_questions.desc()))
        if highest_num_of_quest_record:
            number_of_questions = highest_num_of_quest_record.number_of_questions + len(questions)
            correct_answers = highest_num_of_quest_record.correct_answers + result_count
            average_result = round(correct_answers / number_of_questions * len(questions), 2)
            correct_average_result = self.correct_rounding(str(average_result))
        else:
            correct_average_result = result_count
            correct_answers = result_count
            number_of_questions = len(questions)

        values = {
            "pass_date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "user_id": user_id,
            "company_id": company_id,
            "quiz_record_id": quiz_record_id,
            "average_result": correct_average_result,
            "correct_answers": correct_answers,
            "number_of_questions": number_of_questions
        }
        return values

    async def record_results(self, answers: results_schemas.AnswerQuiz, company_id: int, quiz_id_in_company: int, user_id: int) -> status.HTTP_200_OK:
        crud_quiz = QuizCrud(db=self.db)
        quiz_record = await crud_quiz.get_quiz(company_id=company_id, quiz_id_in_company=quiz_id_in_company)
        await self.answers_len_check(answers=answers, quiz_record_id=quiz_record.quiz_record_id)
        values = await self.results_to_record(answers=answers, user_id=user_id, company_id=company_id, quiz_record_id=quiz_record.quiz_record_id)
        await self.db.execute(insert(models.QuizResults), values=values)
        return HTTPException(status_code=200, detail="success")

    async def get_all_user_results(self, user_id: int) -> List[results_schemas.Results]:
        results = await self.db.fetch_all(select(models.QuizResults).filter_by(user_id=user_id))
        return results

    async def get_all_company_member_results(self, user_id: int, company_id: int) -> List[results_schemas.Results]:
        results = await self.db.fetch_all(select(models.QuizResults).filter_by(user_id=user_id, company_id=company_id))
        return results

    async def get_company_member_results_by_quiz(self, user_id: int, company_id: int, quiz_id_in_company: int) -> List[results_schemas.Results]:
        crud_quiz = QuizCrud(db=self.db)
        quiz_record = await crud_quiz.get_quiz(company_id=company_id, quiz_id_in_company=quiz_id_in_company)
        results = await self.db.fetch_all(select(models.QuizResults).filter_by(user_id=user_id, company_id=company_id, quiz_record_id=quiz_record.quiz_record_id))
        return results

    async def get_all_results_by_company(self, company_id: int) -> List[results_schemas.Results]:
        results = await self.db.fetch_all(select(models.QuizResults).filter_by(company_id=company_id))
        return results

    async def get_all_results_by_company_for_quiz_specified(self, company_id: int, quiz_id_in_company: int) -> List[results_schemas.Results]:
        crud_quiz = QuizCrud(db=self.db)
        quiz_record = await crud_quiz.get_quiz(company_id=company_id, quiz_id_in_company=quiz_id_in_company)
        results = await self.db.fetch_all(select(models.QuizResults).filter_by(company_id=company_id, quiz_record_id=quiz_record.quiz_record_id))
        return results

    async def average_result_for_company_member(self, user_id: int, company_id: int) -> float:
        average_result = round(await self.db.execute(select([func.avg(models.QuizResults.average_result)]).filter_by(user_id=user_id, company_id=company_id)), 2)
        correct_average_result = self.correct_rounding(str(average_result))
        return correct_average_result

    async def average_result_for_user_in_the_system(self, user_id: int) -> float:
        average_result = round(await self.db.execute(select([func.avg(models.QuizResults.average_result)]).filter_by(user_id=user_id)), 2)
        correct_average_result = self.correct_rounding(str(average_result))
        return correct_average_result
