from pydantic import BaseModel, Field

class Reflect(BaseModel):

    """Verify if the correct answer is correct given a json with the question, correct answer and incorrect answers. 
    Keep always Spanish as the input and output language. 
    If it is not, return True. If it is correct, return False in the field loop_needed.
    The output field should contain a new version of the JSON with the correct answer fixed. 
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
    
    loop_needed : bool = Field(description="True if the correct answer is not correct")
    output : str = Field(description="The json with the format")
    reason : str = Field(description="Explain why the answer is correct or not")