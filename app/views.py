from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, jsonify
from app import app
from app.models import User, Feedback
from app.forms import ChooseForm, LoginForm, FeedbackForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime
from app.chatbot import get_bot_response


@app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            next_page = url_for('generate')
        else:
            next_page = url_for('chat')
        return redirect(next_page)
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            if current_user.role == 'Admin':
                next_page = url_for('generate')
            else:
                next_page = url_for('chat')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/chat')
def chat():
    return render_template('chat.html', title='Selly UoB')

@app.route('/get', methods=['POST'])
def get_response():
    user_input = request.form['msg']
    response = get_bot_response(user_input)
    return jsonify({"reply": response})


@app.route('/appointment')
def appointment():
    return render_template('appointment.html', title='Counselling Appointment')


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        fb = Feedback(user_id=current_user.id, content=form.feedback.data, timestamp=datetime.datetime.utcnow())
        db.session.add(fb)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('account'))
    return render_template('feedback.html', title='Feedback', form=form)

@app.route('/generate')
def generate():
    return render_template('generate.html', title='Generate Reports')

# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500