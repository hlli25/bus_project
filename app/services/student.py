from app.models import Student, db
from app.entities import Resource, Report, Ticket, TrendAnalyser
from flask import abort
from datetime import datetime

def request_resource(student, resource_id):
    # e.g. check enrollment, lookup Resource, create & return it
    resource = Resource.query.get_or_404(resource_id)
    if resource.course_id not in student.course_enrollments:
        abort(403, "Not enrolled in that course.")
    return resource

def view_well_being_progress(student):
    analyser = TrendAnalyser()
    analyser.track_trends()
    trend_summary = analyser.produce_summary()
    return trend_summary

def respond_to_ticket(student, ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.responded_by = student.id
    db.session.commit()
    return ticket