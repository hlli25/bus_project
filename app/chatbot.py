from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask_login import current_user
from flask import url_for
from datetime import datetime

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
        elif current_user.is_authenticated:
            return "Access to the trend report is restricted to administrators only."
        else:
            return "Please log in to check your access to the trend report."
    else:
        response = client.generate_content(
            contents=user_input,
        )
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response to your input."

def get_faq_response(user_input):
    user_message_lower = user_input.lower()

    if "help" in user_message_lower or "faq" in user_message_lower:
        return f"You can find the faq section here: {url_for('faq', _external=True)}"
    elif "support" in user_message_lower:
        return "If you need support, please contact us at support@example.com."
    else:
        response = client.generate_content(
            contents=user_input,
        )
        return response.text.strip() if response.text else "Sorry, I couldn't find an appropriate FAQ response for your input."

def get_greeting_response(user_input):
    user_message_lower = user_input.lower()
    now = datetime.now()
    current_hour = now.hour

    if current_hour < 12:
        time_greeting = "Good morning"
    elif 12 <= current_hour < 18:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(greet in user_message_lower for greet in greetings):
        return f"{time_greeting} {current_user.name}! How can I assist you today?"
    response = client.generate_content(
        contents=user_input,)
    return response.text.strip() if response.text else "Sorry, I couldn't determine an appropriate greeting response."
