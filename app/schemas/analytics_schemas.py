from pydantic import BaseModel


class Basic(BaseModel):
    quiz_id_in_company: int


class QuizzesList(Basic):
    company_id: int
    pass_date: str


class MyResults(QuizzesList):
    average_result: float


class MemberResults(Basic):
    user_id: int
    average_result: float
    pass_date: str


class MembersPassed(Basic):
    company_member_id: int
