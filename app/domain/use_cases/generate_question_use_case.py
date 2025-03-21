import logging
from app.domain.entities.question import Question
from app.infrastructure.repositories.langgraph_question_generator import LangGraphQuestionGenerator
logger = logging.getLogger(__name__)

class GenerateQuestionUseCase:
    def __init__(self, langgraph_question_generator: LangGraphQuestionGenerator):
        self.langgraph_question_generator = langgraph_question_generator

    async def execute(self, category: str) -> Question:
        try:
            # Generate initial question
            logger.info(f"Generating initial question for category: {category}")
            result = self.langgraph_question_generator.generate_question(category)
            return result
            
        except Exception as e:
            logger.error(f"Error in GenerateQuestionUseCase: {str(e)}")
            raise 