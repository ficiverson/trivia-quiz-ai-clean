import json
from typing import Tuple
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

from app.domain.entities.question import Question
from app.domain.interfaces.question_generator import QuestionGenerator

GENERATE_QUESTION_FUNCTION = {
    "name": "generate_question",
    "description": "Generate a trivia question based on the given category",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The trivia question"
            },
            "correctAnswer": {
                "type": "string",
                "description": "The correct answer"
            },
            "incorrectAnswers": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of incorrect answers"
            }
        },
        "required": ["question", "correctAnswer", "incorrectAnswers"]
    }
}

VALIDATE_QUESTION_FUNCTION = {
    "name": "validate_question",
    "description": "Validate if the question and answers are correct",
    "parameters": {
        "type": "object",
        "properties": {
            "loop_needed": {
                "type": "boolean",
                "description": "True if the question needs to be regenerated"
            },
            "reason": {
                "type": "string",
                "description": "Explanation of why the question needs to be regenerated"
            }
        },
        "required": ["loop_needed", "reason"]
    }
}

class AzureQuestionGenerator(QuestionGenerator):
    def __init__(self):
        load_dotenv()
        
        # Validate environment variables
        required_env_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        
        # Print environment variables for debugging
        print("Azure OpenAI Configuration:")
        for var in required_env_vars:
            print(f"{var}: {os.getenv(var)}")
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        try:
            self.llm = AzureChatOpenAI(
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY")
            )

            print("Successfully initialized Azure OpenAI client")
            
        except Exception as e:
            print(f"Error initializing Azure OpenAI client: {str(e)}")
            raise

    async def generate_question(self, category: str) -> Question:
        try:
            system_prompt = """You are a trivia expert generating questions for a trivia game. Generate questions based on the given category in Spanish.
            For "cine y tv": questions about movies or TV shows
            For "geografía": questions about countries, cities, or landmarks
            For "historia": questions about historical events, people, or places
            For "deportes": questions about sports, players, or teams
            For "corazón": questions about celebrity relationships or love stories
            For "videojuegos": questions about video games, characters, or consoles
            For "tongurso": include a typo in one incorrect answer, random category"""
            
            response = await self.llm.ainvoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a question for category: {category}"}
                ],
                functions=[GENERATE_QUESTION_FUNCTION],
                function_call={"name": "generate_question"}
            )
            
            function_call = response.additional_kwargs['function_call']
            question_data = json.loads(function_call['arguments'])
            
            return Question(
                question=question_data["question"],
                correct_answer=question_data["correctAnswer"],
                incorrect_answers=question_data["incorrectAnswers"],
                category=category
            )
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            raise

    async def validate_question(self, question: Question) -> Tuple[bool, Question, str]:
        try:
            response = await self.llm.ainvoke(
                [
                    {"role": "system", "content": "You are a trivia expert validating questions and answers in Spanish."},
                    {"role": "user", "content": question.model_dump_json()}
                ],
                functions=[VALIDATE_QUESTION_FUNCTION],
                function_call={"name": "validate_question"}
            )
            
            function_call = response.additional_kwargs['function_call']
            result = json.loads(function_call['arguments'])
            
            return result["loop_needed"], question, result["reason"]
        except Exception as e:
            print(f"Error validating question: {str(e)}")
            raise 