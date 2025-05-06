from datetime import datetime
from typing import List, Any
from app.chatbot import chat_and_log
from app import db
from app.models import CounsellingSession


class Resource:
    def __init__(self, resource_id: int, title: str, description: str, last_updated: datetime):
        self.resource_id = resource_id
        self.title = title
        self.description = description
        self.last_updated = last_updated

    def get_resource_details(self) -> str:
        return (
            f"Resource ID: {self.resource_id}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Last Updated: {self.last_updated.isoformat()}"
        )

    def update_resource(self, title: str, description: str):
        self.title = title
        self.description = description
        self.last_updated = datetime.now()
        return self

    query = None


class CounsellingSession:
    def __init__(self, session_id: int, date_time: datetime, status: str) -> None:
        self.session_id = session_id
        self.date_time = date_time
        self.status = status

    @staticmethod
    def schedule_session(student, counsellor):
        new_session = CounsellingSession(
            student_id=student.id,
            counsellor_id=counsellor.id,
            status="scheduled",
        )
        db.session.add(new_session)
        db.session.commit()
        return new_session

    def update_session_status(self, new_status: str):
        self.status = new_status
        return self


class Notification:
    def __init__(self, notification_id: int, message: str, date_sent: datetime):
        self.notification_id = notification_id
        self.message = message
        self.date_sent = date_sent

    def send_to_user(self, user: Any):
        # Send this notification to a User.
        """ Placeholder implementation: actual send logic (e.g., email, push) """
        return True


class Ticket:
    query = None

    def __init__(self, ticket_id: int, status: str, messages: list[str] = None):
        self.ticket_id = ticket_id
        self.status = status
        self.messages = messages or []

    def add_message(self, message):
        self.messages.append(message)
        return self

    def close_ticket(self):
        if self.status.lower() == 'closed':
            return False
        self.status = 'closed'
        return True


class PDFDocument:
    """ Placeholder implementation; integrate with a PDF library."""

    def __init__(self, pdf_bytes):
        self._bytes = pdf_bytes

    @staticmethod
    def from_text(text) -> "PDFDocument":
        """Placeholder implementation; convert plain text to fake‑PDF bytes (UTF‑8)."""
        return PDFDocument(text.encode("utf-8"))

    def save(self, file_path):
        with open(file_path, "wb") as fp:
            fp.write(self._bytes)


class Report:
    def __init__(self, report_id, report_type, content: list[str], generated_on: datetime,):
        self.report_id = report_id
        self.report_type = report_type
        self.content = content
        self.generated_on = generated_on

    @staticmethod
    def generate(student, trend_summary):
        header = (
            f"Report for {getattr(student, 'username', student)} "
            f"generated on {datetime().isoformat()}"
        )
        combined = header + "" + trend_summary

        # Create placeholder PDF and save to /tmp
        pdf = PDFDocument.from_text(combined)
        filename = (
            f"report_{getattr(student, 'id', 'unknown')}_{datetime().date()}.pdf"
        )
        pdf.save(f"/tmp/{filename}")

        return trend_summary


class TrendAnalyser:
    def __init__(self, trend_summary: str = ""):
        self.trend_summary = trend_summary

    def track_trends(self):
        # Collect data and update the trend summary.
        """ Placeholder implementation: actual trend tracking """
        self.trend_summary = "Trends updated at " + datetime.now().isoformat()

    def produce_summary(self):
        return self.trend_summary


class AIChatbot:
    def __init__(self):
        self.internal_state = ""  # for remembering sth about conversation as it progresses

    def chat(self, user_input):
        bot_reply = chat_and_log(user_input)
        self.internal_state = bot_reply
        return bot_reply

    @staticmethod
    def generate_recommendations(self, student: Any) -> List[Resource]:
        return []

    @staticmethod
    def create_ticket(self, student: Any):
        new_ticket = Ticket(ticket_id=0, status="open")
        return new_ticket

    def receive_feedback(self, student: Any, feedback: Any):
        # Done in review() in views.py
        pass