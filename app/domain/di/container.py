from typing import Optional
import logging
from fastapi import HTTPException

from app.domain.use_cases.generate_question_use_case import GenerateQuestionUseCase
from app.infrastructure.repositories.langgraph_question_generator import LangGraphQuestionGenerator
from app.infrastructure.datasource.azure_openai_llm import LlmProvider
from app.infrastructure.tools.generation_tools import GenerationTool
from app.infrastructure.tools.reflection_tools import ReflectionTool
logger = logging.getLogger(__name__)

class Container:
    _instance: Optional['Container'] = None
    _initialized: bool = False

    def __init__(self):
        if Container._initialized:
            return
        
        try:
            # Initialize llm provider
            self.llm_provider = LlmProvider()
            # Initialize generation tool
            self.generation_tool = GenerationTool(self.llm_provider)
            self.reflection_tool = ReflectionTool(self.llm_provider)
            self.question_generator = LangGraphQuestionGenerator(self.generation_tool, self.reflection_tool)
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