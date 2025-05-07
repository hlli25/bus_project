from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

def get_bot_response(user_input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_input,
    )
    return response.text
