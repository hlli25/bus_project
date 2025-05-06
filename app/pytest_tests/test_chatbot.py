import pytest
from app.chatbot import get_bot_response, FAQ_RESPONSES, client

class DummyResponse:
    def __init__(self, text):
        self.text = text


# Positive test case
def test_get_bot_response_known_faq():
    user_input = "how can i clear all conversation history?"
    expected = FAQ_RESPONSES[user_input.lower()]
    assert get_bot_response(user_input) == expected

# Positive test case
def test_get_bot_response_external(monkeypatch):
    user_input = "Tell me a joke"
    def dummy_generate_content(model, contents):
        return DummyResponse("This is a joke")
    # Monkeypatch the Gemini API call
    monkeypatch.setattr(client.models, "generate_content", dummy_generate_content)
    response = get_bot_response(user_input)
    # Assert that the stubbed API returns the dummy joke
    assert response == "This is a joke"

# Negative test case: simulate an API failure and ensure the exception is propagated
def test_get_bot_response_external_api_error(monkeypatch):
    user_input = "Tell me a joke"
    def dummy_generate_content_error(model, contents):
        raise RuntimeError("API failure")
    # Monkeypatch the Gemini API call to raise an error
    monkeypatch.setattr(client.models, "generate_content", dummy_generate_content_error)
    with pytest.raises(RuntimeError) as excinfo:
        get_bot_response(user_input)
    assert "API failure" in str(excinfo.value)