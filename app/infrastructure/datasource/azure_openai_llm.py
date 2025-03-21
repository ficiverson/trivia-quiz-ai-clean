import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

class LlmProvider:
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

        

            print("Successfully initialized Azure OpenAI")
            
        except Exception as e:
            print(f"Error initializing Azure OpenAI: {str(e)}")
            raise

    def get_llm(self) -> AzureChatOpenAI:
        return self.llm