import logging
from app.domain.entities.question import Question
from app.domain.interfaces.question_generator import QuestionGenerator

logger = logging.getLogger(__name__)

class GenerateQuestionUseCase:
    def __init__(self, question_generator: QuestionGenerator):
        self.question_generator = question_generator

    async def execute(self, category: str) -> Question:
        try:
            # Generate initial question
            logger.info(f"Generating initial question for category: {category}")
            question = await self.question_generator.generate_question(category)
            
            # Validate and potentially regenerate the question
            max_attempts = 3
            current_attempt = 1
            
            while current_attempt <= max_attempts:
                logger.info(f"Validating question (attempt {current_attempt}/{max_attempts})")
                needs_regeneration, updated_question, reason = await self.question_generator.validate_question(question)
                
                if not needs_regeneration:
                    logger.info("Question validation successful")
                    break
                    
                logger.info(f"Regenerating question because: {reason}")
                question = updated_question
                current_attempt += 1
            
            return question
            
        except Exception as e:
            logger.error(f"Error in GenerateQuestionUseCase: {str(e)}")
            raise 