import requests
import json

def test_generate_question():
    url = "http://localhost:8000/generate-question"
    payload = {"category": "cine y tv"}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if not result["success"]:
            print(f"\nError: {result['error']}")
            return False
            
        question_data = result["data"]
        print("\nAPI Response:")
        print(f"Question: {question_data['question']}")
        print(f"Correct Answer: {question_data['correct_answer']}")
        print(f"Incorrect Answers: {', '.join(question_data['incorrect_answers'])}")
        
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def test_health_check():
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        print("\nHealth Check Response:")
        if result["success"]:
            print(f"Status: {result['data']}")
            return True
        else:
            print(f"Error: {result['error']}")
            return False
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing the Question Generator API...")
    
    print("\nTesting health check endpoint...")
    test_health_check()
    
    print("\nTesting question generation...")
    test_generate_question() 