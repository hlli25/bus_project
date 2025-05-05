from app import db
from app.models import User, Review
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'username': 'admin1',      'email': 'admin1@uniss.com',   'role': 'Admin',      'pw': 'admin1.pw'},
        {'username': 'admin2',      'email': 'admin2@uniss.com',   'role': 'Admin',      'pw': 'admin2.pw'},
        {'username': 'student1',    'email': 'student1@uniss.com', 'role': 'Student',    'pw': 'student1.pw'},
        {'username': 'student2',    'email': 'student2@uniss.com', 'role': 'Student',    'pw': 'student2.pw'},
        {'username': 'counsellor1', 'email': 'counsel1@uniss.com', 'role': 'Counsellor', 'pw': 'counsel1.pw'},
        {'username': 'counsellor2', 'email': 'counsel2@uniss.com', 'role': 'Counsellor', 'pw': 'counsel2.pw'}
    ]

    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = User(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)


    reviews = [
        Review(feature="Account Management",
               text="Editing my account is straightforward, but it could have more functionality.",
               stars=3,
               user_id=3),
        Review(feature="Reporting Module",
               text="Generating reports is slow and occasionally throws errors.",
               stars=2,
               user_id=5),
        Review(feature="Chatbot",
               text="The chatbot layout is clean and gives me all the insights I need at a glance.",
               stars=4,
               user_id=4),
        Review(feature="Mobile Responsiveness",
               text="On mobile devices the UI adapts perfectly—great job!",
               stars=5,
               user_id=4),
    ]

    db.session.add_all(reviews)


    db.session.commit()

# if __name__ == '__main__':
#     from app import app
#     with app.app_context():
#         reset_db()