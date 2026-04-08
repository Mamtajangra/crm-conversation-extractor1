from openai import OpenAI  
import os
import dotenv  

#  Load environment variables from .env file
dotenv.load_dotenv()

#  Fetch Groq API key from environment variables
groq_key = os.getenv("GROQ_API_KEY")

#  Initialize OpenAI client with Groq API endpoint
# This client will be used to send requests to Groq LLM (Llama 3.1)
client = OpenAI(api_key=groq_key,base_url="https://api.groq.com/openai/v1")