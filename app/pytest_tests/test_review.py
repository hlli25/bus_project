import pytest
from app import app as flask_app
from app.forms import ReviewForm

# Disable CSRF protection for testing and set valid choices for the 'feature' field
flask_app.config['WTF_CSRF_ENABLED'] = False
ReviewForm.feature.choices = [('Chatbot','Chatbot'),('Trend Report','Trend Report'),
                              ('Review System','Review System'),('General','General')]

# Positive test case
def test_review_form_valid():
    with flask_app.test_request_context():
        form = ReviewForm(data={"feature": "Review System", "stars": 4})
        assert form.validate() is True

# Negative test case
def test_review_form_invalid():
    with flask_app.test_request_context():
        form = ReviewForm(data={"feature": "invalid_choice", "stars": 6})
        assert form.validate() is False
        assert "feature" in form.errors
        assert "stars" in form.errors
