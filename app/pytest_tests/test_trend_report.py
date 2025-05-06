import pytest
from flask.signals import template_rendered
from app import app as flask_app
from app.models import Review
from app.views import chatbot_queries

# Disable authentication requirement for testing
flask_app.config['LOGIN_DISABLED'] = True


# Positive test case
def test_trend_report_view_with_data(monkeypatch):
    with flask_app.app_context():
        # Prepare dummy reviews with known stars values (2 and 4)
        class DummyReviewObj:
            def __init__(self, stars):
                self.stars = stars
        dummy_reviews = [DummyReviewObj(2), DummyReviewObj(4)]

        # Define named function for classmethod
        def dummy_all_reviews(cls):
            return dummy_reviews

        # Monkeypatch Review.query.all() to return dummy reviews
        QueryStub = type('Q', (), {'all': classmethod(dummy_all_reviews)})
        monkeypatch.setattr(Review, 'query', QueryStub)

        # Populate chatbot_queries list with sample query strings to simulate recorded chatbot interactions
        chatbot_queries.clear()
        chatbot_queries.extend(['x', 'x', 'y'])

        # Capture the template context passed to the trend_report.html template
        recorded = []
        def record(sender, template, context, **extra):
            recorded.append(context)
        template_rendered.connect(record, flask_app)

        # Issue a GET request on /trend_report using flask_app.test_client(), and asserts a 200 OK response
        client = flask_app.test_client()
        response = client.get('/trend_report')
        assert response.status_code == 200

        # Disconnect the signal listener to avoid side effects on other tests
        template_rendered.disconnect(record, flask_app)

        # Inspect the captured context dict, asserting that:
        # - avg_score is (2+4)/2 = 3.0
        # - total_ratings is 2
        # - common_queries lists the most-frequent chatbot queries in descending order: x twice then y once
        context = recorded[0]
        assert context['avg_score'] == pytest.approx(3.0)
        assert context['total_ratings'] == 2
        assert context['common_queries'] == [
            {'text': 'x', 'count': 2},
            {'text': 'y', 'count': 1}
        ]


# Negative test case
def test_trend_report_view_without_data(monkeypatch):
    with flask_app.app_context():
        # Define named function for no reviews
        def no_reviews(cls):
            return []
        # Monkeypatch no reviews
        QueryStub = type('Q', (), {'all': classmethod(no_reviews)})
        monkeypatch.setattr(Review, 'query', QueryStub)

        # Clear the chatbot_queries list to simulate zero recorded interactions
        chatbot_queries.clear()

        # Capture template context
        recorded = []
        def record(sender, template, context, **extra):
            recorded.append(context)
        template_rendered.connect(record, flask_app)

        # GETs /trend_report via the test client and asserts 200 OK
        client = flask_app.test_client()
        response = client.get('/trend_report')
        assert response.status_code == 200

        # Disconnect signal listener
        template_rendered.disconnect(record, flask_app)

        # Asserts in the captured context that:
        # - avg_score is 0 (no reviews)
        # - total_ratings is 0
        # - common_queries is an empty list (no queries)
        context = recorded[0]
        assert context['avg_score'] == 0
        assert context['total_ratings'] == 0
        assert context['common_queries'] == []