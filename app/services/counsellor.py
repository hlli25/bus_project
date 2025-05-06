from app.models import db, CounsellingSession, Ticket
from app.entities import Resource, Report, Ticket

def manage_counselling_session(self, session_id):
    session = db.session.get(CounsellingSession, session_id)
    if not session:
        return False
    # Simple rule: toggle between "scheduled" → "completed"
    new_status = "completed" if session.status != "completed" else "scheduled"
    session.status = new_status
    db.session.commit()
    return True

def respond_to_ticket(self, ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return None
    ticket.messages.append("Response from counsellor")
    db.session.commit()
    return ticket