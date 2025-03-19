from abc import ABC, abstractmethod
from typing import Tuple
from app.domain.entities.question import Question

class QuestionGenerator(ABC):
    @abstractmethod
    async def generate_question(self, category: str) -> Question:
        pass

    @abstractmethod
    async def validate_question(self, question: Question) -> Tuple[bool, Question, str]:
        pass 