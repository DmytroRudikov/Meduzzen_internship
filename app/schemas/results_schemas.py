from pydantic import BaseModel


class AnswerQuiz(BaseModel):
    answers: dict


class Results(BaseModel):
    results_id: int
    pass_date: str
    user_id: int
    company_id: int
    quiz_record_id: int
    average_result: float
    number_of_questions: int
    correct_answers: int
