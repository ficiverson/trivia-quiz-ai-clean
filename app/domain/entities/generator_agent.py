from pydantic import BaseModel, Field

class GenerateQuestion(BaseModel):
    """You are a trivia expert generating questions for a trivia game. Generate a structured response based on the given category. 
    The category is coming in Spanish. 
    The output field should contain a new version of the JSON with the correct answer fixed. 
    Keep Spanish as the output language.
    When the category is "cine y tv", the question should be about a movie or a tv show.
    When the category is "geografía", the question should be about a country, a city or a landmark.
    When the category is "historia", the question should be about a historical event, a person or a place.
    When the category is "deportes", the question should be about a sport, a player or a team.
    When the category is "corazón", the question should be about a romantic relationship, a break-up or a love story of famous people.
    When the category is "videojuegos", the question should be about a video game, a character or a game console.
    When the category is "tongurso", one of the incorrect answers should be a typo of the correct answer and you can pick a random category.
    JSON Schema:
    {
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
        "required": [
            "question",
            "correctAnswer",
            "incorrectAnswers"
        ]
    }
    """
    
    output : str = Field(description="The json of the response withut special characters")