from typing import List
from pydantic import BaseModel


class CreateQuiz(BaseModel):
    quiz_name: str
    description: str
    questions: dict
    answer_options: list
    correct_answer: list


class UpdateQuiz(BaseModel):
    quiz_name: str | None = None
    description: str | None = None


class DeleteQuestions(BaseModel):
    questions: list


class UpdateQuestions(BaseModel):
    questions: dict
    answer_options: list | None = None
    correct_answer: list | None = None


class Quiz(BaseModel):
    quiz_record_id: int
    company_id: int
    quiz_id_in_company: int
    quiz_name: str
    description: str
    times_quiz_passed_per_day: int | None = None


class Questions(BaseModel):
    question_record_id: int
    quiz_record_id: int
    question_id_in_quiz: int
    question: str
    answer_options: List[str]
