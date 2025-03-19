from pydantic import BaseModel

class Question(BaseModel):
    question: str
    correct_answer: str
    incorrect_answers: list[str]
    category: str 