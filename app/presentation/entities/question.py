from pydantic import BaseModel

class QuestionRequest(BaseModel):
    category: str

class QuestionResponse(BaseModel):
    question: str
    correct_answer: str
    incorrect_answers: list[str] 