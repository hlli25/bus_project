from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user

# decorator design pattern to check a user is logged in before accessing a webpage
# redirects to login if not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# decorator design pattern to check a user is an admin before accessing a webpage
# throws error 403 if not an admin, showing warning page that user does not have access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# decorator design pattern to check a user is a student before accessing a webpage
# throws error 403 if not a student, showing warning page that user does not have access
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Student':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function