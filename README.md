# Trivia Question Generator API

A FastAPI-based API that generates trivia questions using Azure OpenAI. Built with Clean Architecture principles.

## Features

- Generate trivia questions in Spanish for various categories
- Validates questions for quality and accuracy
- Clean Architecture implementation
- Dependency Injection pattern
- Async/await support
- Error handling and logging

## Langgraph agents

![Screenshot 2025-03-19 at 09 50 14](https://github.com/user-attachments/assets/ba7c0e04-4f33-4077-b28e-6f327fadd10a)


## Project Structure

```
app/
├── domain/
│   ├── di/           # Dependency injection
│   ├── entities/     # Domain entities
│   ├── interfaces/   # Abstract interfaces
│   └── use_cases/    # Business logic
├── infrastructure/
│   └── repositories/ # Implementation of interfaces
└── presentation/
    ├── api/         # FastAPI routes
    └── entities/    # API request/response models
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   ```

## Running the Application

```bash
python -m uvicorn app.presentation.api.routes:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check endpoint
- `POST /generate-question` - Generate a trivia question
  - Request body:
    ```json
    {
      "category": "string"
    }
    ```
  - Available categories:
    - "cine y tv"
    - "geografía"
    - "historia"
    - "deportes"
    - "corazón"
    - "videojuegos"
    - "tongurso"

## License

MIT 
