from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask_login import current_user
from flask import url_for

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]
client = genai.GenerativeModel(model_name="gemini-2.0-flash")

def get_bot_response(user_input):
    user_message_lower = user_input.lower()

    if "review" in user_message_lower:
        return f"You can leave a review here: {url_for('review', _external=True)}"
    elif "report" in user_message_lower:
        if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role == 'admin':
            return f"You can access the trend report here: {url_for('trend_report', _external=True)}"
        else:
            return "Only administrators can access the trend report."
    else:
        response = client.generate_content(
            contents=user_input,
        )
        return response.text