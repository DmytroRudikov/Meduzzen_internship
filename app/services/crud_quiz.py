from schemas import quiz_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update, case
from typing import List, Dict
from app.services.crud_notification import NotificationCrud


class QuizCrud:
    def __init__(self, db: Database):
        self.db = db

    async def quiz_exists(self, quiz_id_in_company: int, company_id: int) -> quiz_schemas.Quiz:
        quiz_exists = await self.db.fetch_one(select(models.Quiz).filter_by(company_id=company_id, quiz_id_in_company=quiz_id_in_company))
        if not quiz_exists:
            raise HTTPException(status_code=404, detail=f"Quiz not found")
        return quiz_exists

    async def check_the_last_quiz_id_in_company(self, company_id: int) -> int:
        last_quiz_in_company = await self.db.fetch_one(select(models.Quiz).filter_by(company_id=company_id).order_by(models.Quiz.quiz_id_in_company.desc()))
        if last_quiz_in_company:
            last_quiz_id_in_company = last_quiz_in_company.quiz_id_in_company
        else:
            last_quiz_id_in_company = 0
        return last_quiz_id_in_company

    @staticmethod
    async def create_questions(quiz_record_id: int, create_quiz_form: quiz_schemas.CreateQuiz) -> List[dict]:
        question_values = []
        for i in range(len(create_quiz_form.questions)):
            values = {
                "quiz_record_id": quiz_record_id,
                "question_id_in_quiz": int(list(create_quiz_form.questions.keys())[i]),
                "question": create_quiz_form.questions[list(create_quiz_form.questions.keys())[i]],
                "answer_options": create_quiz_form.answer_options[i],
                "correct_answer": create_quiz_form.correct_answer[i],
            }
            question_values.append(values)
        return question_values

    async def values_for_add_questions(self, company_id, quiz_id_in_company: int, new_questions: quiz_schemas.UpdateQuestions) -> List[dict]:
        quiz_record = await self.db.fetch_one(select(models.Quiz).filter_by(company_id=company_id, quiz_id_in_company=quiz_id_in_company))
        question_values = []
        for i in range(len(new_questions.questions)):
            values = {
                "quiz_record_id": quiz_record.quiz_record_id,
                "question_id_in_quiz": int(list(new_questions.questions.keys())[i]),
                "question": new_questions.questions[list(new_questions.questions.keys())[i]],
                "answer_options": new_questions.answer_options[i],
                "correct_answer": new_questions.correct_answer[i],
            }
            question_values.append(values)
        return question_values

    async def create_quiz_with_questions(self, company_id: int, create_quiz_form: quiz_schemas.CreateQuiz) -> status.HTTP_200_OK:
        last_quiz_id_in_company = await self.check_the_last_quiz_id_in_company(company_id=company_id)
        last_quiz_id_in_company += 1
        quiz_values = {
            "quiz_name": create_quiz_form.quiz_name,
            "company_id": company_id,
            "description": create_quiz_form.description,
            "quiz_id_in_company": last_quiz_id_in_company,
            "quiz_to_be_passed_in_hours": create_quiz_form.quiz_to_be_passed_in_hours
        }
        await self.db.execute(insert(models.Quiz), values=quiz_values)
        quiz_record = await self.db.fetch_one(select(models.Quiz).filter_by(company_id=company_id, quiz_id_in_company=last_quiz_id_in_company))
        question_values = await self.create_questions(quiz_record_id=quiz_record.quiz_record_id, create_quiz_form=create_quiz_form)
        await self.db.execute_many(query=insert(models.Question), values=question_values)
        crud_notification = NotificationCrud(db=self.db)
        await crud_notification.create_notification(company_id=company_id, quiz_record_id=quiz_record.quiz_record_id)
        return HTTPException(status_code=200, detail="success")

    async def get_quiz(self, company_id: int, quiz_id_in_company: int) -> quiz_schemas.Quiz:
        quiz = await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        return quiz

    async def get_all_quizzes(self, company_id: int) -> List[quiz_schemas.Quiz]:
        result = await self.db.fetch_all(select(models.Quiz).filter_by(company_id=company_id))
        return result

    async def get_all_questions_for_the_quiz(self, company_id: int, quiz_id_in_company: int) -> List[quiz_schemas.Questions]:
        await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        result = await self.db.fetch_all(select(models.Question).join(models.Quiz).filter_by(company_id=company_id, quiz_id_in_company=quiz_id_in_company))
        return result

    @staticmethod
    async def update_question_details(update_questions_form: quiz_schemas.UpdateQuestions, question_model: quiz_schemas.Questions) -> List[dict]:
        question_values = []
        q_values = []
        ao_values = []
        ca_values = []
        for key in question_model._mapping.keys():
            if key == "question":
                for i in range(len(update_questions_form.questions)):
                    q_dict = {
                        "question_id_in_quiz": int(list(update_questions_form.questions.keys())[i]),
                        "question": update_questions_form.questions[list(update_questions_form.questions.keys())[i]]
                    }
                    q_values.append(q_dict)
            elif key not in update_questions_form.dict() or update_questions_form.dict()[key] is None:
                continue
            else:
                for i in range(len(update_questions_form.questions)):
                    values_dict = {key: update_questions_form.dict()[key][i]}
                    if key == "answer_options":
                        ao_values.append(values_dict)
                    elif key == "correct_answer":
                        ca_values.append(values_dict)

        for i in range(len(q_values)):
            if len(ao_values) == 0 and len(ca_values) != 0:
                values = {
                    "question_id_in_quiz": q_values[i]["question_id_in_quiz"],
                    "question": q_values[i]["question"],
                    "correct_answer": ca_values[i]["correct_answer"],
                }
            elif len(ao_values) == 0 and len(ca_values) == 0:
                values = {
                    "question_id_in_quiz": q_values[i]["question_id_in_quiz"],
                    "question": q_values[i]["question"],
                }
            elif len(ao_values) != 0 and len(ca_values) == 0:
                values = {
                    "question_id_in_quiz": q_values[i]["question_id_in_quiz"],
                    "question": q_values[i]["question"],
                    "answer_options": ao_values[i]["answer_options"],
                }
            else:
                values = {
                    "question_id_in_quiz": q_values[i]["question_id_in_quiz"],
                    "question": q_values[i]["question"],
                    "answer_options": ao_values[i]["answer_options"],
                    "correct_answer": ca_values[i]["correct_answer"],
                }
            question_values.append(values)
        return question_values

    @staticmethod
    async def update_quiz_details(update_quiz_form: quiz_schemas.UpdateQuiz, quiz: quiz_schemas.Quiz) -> dict:
        quiz_values = {}
        for key in quiz._mapping.keys():
            if key not in update_quiz_form.dict() or update_quiz_form.dict()[key] is None:
                continue
            else:
                quiz_values[key] = update_quiz_form.dict()[key]
        return quiz_values

    async def update_quiz(self, company_id: int, quiz_id_in_company: int, update_quiz_form: quiz_schemas.UpdateQuiz) -> status.HTTP_200_OK:
        quiz = await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        quiz_values = await self.update_quiz_details(update_quiz_form=update_quiz_form, quiz=quiz)
        await self.db.execute(update(models.Quiz).filter_by(quiz_id_in_company=quiz_id_in_company, company_id=company_id).values(**quiz_values))
        return HTTPException(status_code=200, detail="success")

    async def update_questions(self, company_id: int, quiz_id_in_company: int, update_questions_form: quiz_schemas.UpdateQuestions) -> status.HTTP_200_OK:
        all_questions = await self.get_all_questions_for_the_quiz(company_id=company_id, quiz_id_in_company=quiz_id_in_company)
        question_values = await self.update_question_details(update_questions_form=update_questions_form, question_model=all_questions[0])
        for i in range(len(question_values)):
            await self.db.execute(update(models.Question).filter_by(quiz_record_id=all_questions[0].quiz_record_id, question_id_in_quiz=question_values[i]["question_id_in_quiz"]).values(**question_values[i]))
        return HTTPException(status_code=200, detail="success")

    async def delete_quiz(self, company_id: int, quiz_id_in_company: int) -> status.HTTP_200_OK:
        await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        await self.db.execute(delete(models.Quiz).filter_by(company_id=company_id, quiz_id_in_company=quiz_id_in_company))
        return HTTPException(status_code=200, detail="success")

    async def delete_questions(self, company_id: int, quiz_id_in_company: int, questions: quiz_schemas.DeleteQuestions) -> status.HTTP_200_OK:
        await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        questions_in_quiz = await self.get_all_questions_for_the_quiz(company_id=company_id, quiz_id_in_company=quiz_id_in_company)
        if len(questions_in_quiz) - len(questions.questions) < 2:
            raise HTTPException(status_code=403, detail="Quiz must include at least 2 questions")
        await self.db.execute(delete(models.Question).filter_by(quiz_record_id=questions_in_quiz[0].quiz_record_id).where(models.Question.question_id_in_quiz.in_(questions.questions)))
        return HTTPException(status_code=200, detail="success")

    async def add_questions(self, company_id: int, quiz_id_in_company: int, new_questions: quiz_schemas.UpdateQuestions) -> status.HTTP_200_OK:
        await self.quiz_exists(quiz_id_in_company=quiz_id_in_company, company_id=company_id)
        questions = await self.values_for_add_questions(company_id=company_id, quiz_id_in_company=quiz_id_in_company, new_questions=new_questions)
        await self.db.execute_many(query=insert(models.Question), values=questions)
        return HTTPException(status_code=200, detail="success")
