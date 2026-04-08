# Import Groq client from configuration file
from source.Api_config import client
import json

'''this is dictionary just like json we want to extract useful data from its parameters like name,email,phone,age etc'''
# Define schema (structure) for extracting user information
# This schema tells the LLM what fields to extract and in what format
schema = {
    "name": "extract_user_info",
    "description": "Extracts personal info from chat",       ##determine the purpose of schema
    "parameters": {                                            ## it shows which data should extract and in which format
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "location": {"type": "string"},
            "age": {"type": "string"}
        },
        "required": ["name", "email", "phone", "location", "age"]
    }
}
''' same use llama 3 model so output follows the JSON schema'''
def extract_info(chat_text):
    """
    🔹 Extract structured user information from unstructured chat text
    
    Steps:
    1. Send chat text to LLM
    2. LLM extracts data based on schema
    3. Convert output to JSON
    4. Clean and normalize data
    """
    try: 
        # Send request to Groq LLM for information extraction   
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   
            messages=[                              ## system = instruct to model that only extract the user info in json schema, user = jahan se info nikalna hai
                {"role": "system", "content": "Extract user info in JSON schema."},
                {"role": "user", "content": chat_text}
            ],
            # Provide schema as a tool (function calling)
            tools=[{"type": "function", "function": schema}],
            #  Force model to use this schema
            tool_choice={"type": "function", "function": {"name": "extract_user_info"}}
        )
        # Extract arguments (JSON string) returned by LLM
        args = response.choices[0].message.tool_calls[0].function.arguments
        # Convert JSON string into Python dictionary
        result = json.loads(args)
    #  Handle missing values
        for key, value in result.items():
            if value == "":
                # Replace empty strings with "Not Found"
                result[key] = "Not Found"

#  Convert age to integer
#  Convert age from string → integer (if possible)
        if "age" in result:
            try:
                result["age"] = int(result["age"])
            except:
                # If conversion fails, set age as None
                result["age"] = None
# Return cleaned structured data
        return result 
# Handle any errors (API issues, parsing issues, etc.)
    except Exception as e:
        return {"error": str(e)}