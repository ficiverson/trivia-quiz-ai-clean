from typing import Optional
import logging
from fastapi import HTTPException

from app.domain.use_cases.generate_question_use_case import GenerateQuestionUseCase
from app.infrastructure.repositories.azure_question_generator import AzureQuestionGenerator

logger = logging.getLogger(__name__)

class Container:
    _instance: Optional['Container'] = None
    _initialized: bool = False

    def __init__(self):
        if Container._initialized:
            return
        
        try:
            # Initialize repositories
            self.question_generator = AzureQuestionGenerator()
            logger.info("Successfully initialized repositories")

            # Initialize use cases
            self.generate_question_use_case = GenerateQuestionUseCase(self.question_generator)
            logger.info("Successfully initialized use cases")

            Container._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize dependencies: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize dependencies: {str(e)}")

    @classmethod
    def get_instance(cls) -> 'Container':
        if not cls._instance:
            cls._instance = Container()
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None
        cls._initialized = False 