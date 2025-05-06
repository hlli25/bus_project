from app import db
from app.models import User, Review, Admin, Student, Counsellor
import datetime

# use this reset function in a flask shell via the terminal to reset the SQL database with the following dummy data
def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'cls': Admin,      'username': 'admin1',      'email': 'admin1@uniss.com',   'role': 'Admin',      'pw': 'admin1.pw', 'admin_level': 1},
        {'cls': Admin,      'username': 'admin2',      'email': 'admin2@uniss.com',   'role': 'Admin',      'pw': 'admin2.pw', 'admin_level': 2},
        {'cls': Student,    'username': 'student1',    'email': 'student1@uniss.com', 'role': 'Student',    'pw': 'student1.pw'},
        {'cls': Student,    'username': 'student2',    'email': 'student2@uniss.com', 'role': 'Student',    'pw': 'student2.pw'},
        {'cls': Counsellor, 'username': 'counsellor1', 'email': 'counsel1@uniss.com', 'role': 'Counsellor', 'pw': 'counsel1.pw', 'specialisation': 'General'},
        {'cls': Counsellor, 'username': 'counsellor2', 'email': 'counsel2@uniss.com', 'role': 'Counsellor', 'pw': 'counsel2.pw', 'specialisation': 'Academic'},
    ]

    for u in users:
        pw = u.pop('pw')
        model_cls = u.pop('cls')

        user = model_cls(**u)
        user.set_password(pw)

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

if __name__ == '__main__':
    from app import app
    with app.app_context():
        reset_db()