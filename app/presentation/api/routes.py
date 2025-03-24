from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.entities.question import QuestionRequest, QuestionResponse
from app.domain.di.container import Container


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Trivia Question Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize container
container = Container.get_instance()

@app.post("/generate-question", response_model=QuestionResponse)
async def generate_question(request: QuestionRequest):
    """API Endpoint to generate trivia questions."""
    try:
        logger.info(f"Generating question for category: {request.category}")
        question = await container.generate_question_use_case.execute(request.category)
        logger.info("Successfully generated question")
        print(question)
        return QuestionResponse(
            question=question["question"],
            correct_answer=question["correctAnswer"],
            incorrect_answers=question["incorrectAnswers"]
        )
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "API is running!"} 