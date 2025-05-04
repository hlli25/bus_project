from app import db
from app.models import User
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'username': 'admin1', 'email': 'admin1@uniss.com', 'role': 'Admin', 'pw': 'admin1.pw'},
        {'username': 'admin2', 'email': 'admin2@uniss.com', 'role': 'Admin', 'pw': 'admin2.pw'},
        {'username': 'user1',  'email': 'user1@uniss.com',                   'pw': 'user1.pw'},
        {'username': 'user2',  'email': 'user2@uniss.com',                   'pw': 'user2.pw'},
        {'username': 'user3',  'email': 'user3@uniss.com',                   'pw': 'user3.pw'}
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
    db.session.commit()

# if __name__ == '__main__':
#     from app import app
#     with app.app_context():
#         reset_db()